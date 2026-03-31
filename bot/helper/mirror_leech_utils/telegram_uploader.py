from PIL import Image
from aioshutil import rmtree
from asyncio import sleep, gather, Semaphore
from logging import getLogger
from natsort import natsorted
from os import walk, path as ospath
from time import time
from re import match as re_match, sub as re_sub
from aiofiles.os import (
    remove,
    path as aiopath,
    rename,
)
from pytdbot.types import (
    ChatTypePrivate,
    InputMessageVideo,
    InputMessageAudio,
    InputMessageDocument,
    InputMessagePhoto,
    InputFileRemote,
    InputFileLocal,
    InputThumbnail,
    MessageTopicForum,
)

from ...core.config_manager import Config
from ...core.telegram_client import TgManager
from ..ext_utils.bot_utils import sync_to_async
from ..ext_utils.files_utils import is_archive, get_base_name
from ..telegram_helper.progress import tracker
from ..ext_utils.exceptions import TgUploadException
from ..ext_utils.media_utils import (
    get_media_info,
    get_document_type,
    get_video_thumbnail,
    get_audio_thumbnail,
    get_multiple_frames_thumbnail,
    optimize_thumbnail,
)
from ..telegram_helper.message_utils import (
    delete_message,
    send_album,
    send_message_with_content,
)

LOGGER = getLogger(__name__)


class TelegramUploader:
    def __init__(self, listener, path):
        self._last_uploaded = {}
        self._processed_bytes = 0
        self._listener = listener
        self._path = path
        self._start_time = time()
        self._total_files = 0
        self._thumb = self._listener.thumb or f"thumbnails/{listener.user_id}.jpg"
        self._msgs_dict = {}
        self._corrupted = 0
        self._media_dict = {"videos": {}, "documents": {}}
        self._last_msg_in_group = False
        self._lprefix = ""
        self._media_group = False
        self._is_private = False
        self._sent_msg = None
        self._user_session = self._listener.user_transmission
        self._lock = Semaphore(1)

    async def _upload_progress(self, key, progress_dict, _):
        if self._listener.is_cancelled:
            await tracker.cancel_progress(key)

        async with self._lock:
            last_uploaded = self._last_uploaded.get(key, 0)
            chunk_size = progress_dict["transferred"] - last_uploaded
            self._last_uploaded[key] = progress_dict["transferred"]
            self._processed_bytes += chunk_size

    async def _user_settings(self):
        self._media_group = self._listener.user_dict.get("MEDIA_GROUP") or (
            Config.MEDIA_GROUP
            if "MEDIA_GROUP" not in self._listener.user_dict
            else False
        )
        self._lprefix = self._listener.user_dict.get("LEECH_FILENAME_PREFIX") or (
            Config.LEECH_FILENAME_PREFIX
            if "LEECH_FILENAME_PREFIX" not in self._listener.user_dict
            else ""
        )
        if self._thumb != "none" and not await aiopath.exists(self._thumb):
            self._thumb = None

    async def _msg_to_reply(self):
        if self._listener.up_dest:
            msg = (
                self._listener.message_link
                if self._listener.is_super_chat
                else self._listener.message.text.lstrip("/")
            )
            if self._user_session:
                self._sent_msg = await TgManager.user.sendTextMessage(
                    chat_id=self._listener.up_dest,
                    text=msg,
                    disable_web_page_preview=True,
                    topic_id=MessageTopicForum(self._listener.chat_thread_id),
                    disable_notification=True,
                )
            else:
                self._sent_msg = await self._listener.client.sendTextMessage(
                    chat_id=self._listener.up_dest,
                    text=msg,
                    disable_web_page_preview=True,
                    topic_id=MessageTopicForum(self._listener.chat_thread_id),
                    disable_notification=True,
                )
                if not self._sent_msg.is_error:
                    dest_chat = await self._sent_msg.getChat()
                    self._is_private = isinstance(dest_chat.type, ChatTypePrivate)
            if self._sent_msg.is_error:
                await self._listener.on_upload_error(self._sent_msg["message"])
                return False
        elif self._user_session:
            self._sent_msg = await TgManager.user.getMessage(
                chat_id=self._listener.message.chat_id, message_id=self._listener.mid
            )
            if self._sent_msg.is_error:
                self._sent_msg = await TgManager.user.sendTextMessage(
                    chat_id=self._listener.message.chat_id,
                    text="Deleted Cmd Message! Don't delete the cmd message again!",
                    disable_web_page_preview=True,
                    disable_notification=True,
                )
        else:
            self._sent_msg = self._listener.message
        return True

    async def _prepare_file(self, file_, dirpath, up_path):
        lprefix = self._lprefix
        if lprefix:
            cap_mono = f"{lprefix} <code>{file_}</code>"
            lprefix = re_sub("<.*?>", "", lprefix)
            file_ = f"{lprefix} {file_}"
            new_path = ospath.join(dirpath, file_)
            await rename(up_path, new_path)
            up_path = new_path
        else:
            cap_mono = f"<code>{file_}</code>"
        if len(file_) > 60:
            if is_archive(file_):
                name = get_base_name(file_)
                ext = file_.split(name, 1)[1]
            elif match := re_match(r".+(?=\..+\.0*\d+$)|.+(?=\.part\d+\..+$)", file_):
                name = match.group(0)
                ext = file_.split(name, 1)[1]
            elif len(fsplit := ospath.splitext(file_)) > 1:
                name = fsplit[0]
                ext = fsplit[1]
            else:
                name = file_
                ext = ""
            extn = len(ext)
            remain = 60 - extn
            name = name[:remain]
            file_ = f"{name}{ext}"
            new_path = ospath.join(dirpath, file_)
            await rename(up_path, new_path)
            up_path = new_path
        return cap_mono, up_path, file_

    def _get_input_media(self, subkey, key):
        rlist = []
        for msg in self._media_dict[key][subkey]:
            if key == "videos":
                input_media = InputMessageVideo(
                    video=InputFileRemote(id=msg.remote_file_id),
                    supports_streaming=True,
                    caption=msg.caption,
                )
            else:
                input_media = InputMessageDocument(
                    document=InputFileRemote(id=msg.remote_file_id),
                    caption=msg.caption,
                )
            rlist.append(input_media)
        return rlist

    async def _send_screenshots(self, dirpath, outputs):
        inputs = [
            InputMessagePhoto(
                photo=InputFileLocal(path=ospath.join(dirpath, p)),
                caption=p.rsplit("/", 1)[-1],
            )
            for p in outputs
        ]
        for i in range(0, len(inputs), 10):
            batch = inputs[i : i + 10]
            self._sent_msg = (await send_album(self._sent_msg, batch)).messages[-1]

    async def _send_media_group(self, subkey, key, msgs, client):
        for index, msg in enumerate(msgs):
            msgs[index] = await client.getMessage(
                chat_id=msg[0], message_id=msg[1]
            )

        replied_to = await msgs[0].getRepliedMessage()
        msgs_list = (
            await send_album(replied_to, self._get_input_media(subkey, key), client=client)
        ).messages

        for msg in msgs:
            msg_link = await msg.getMessageLink()
            link = msg_link.link
            async with self._lock:
                self._msgs_dict.pop(link, None)
            await delete_message(msg)

        async with self._lock:
            self._media_dict[key].pop(subkey, None)
            if self._listener.is_super_chat or self._listener.up_dest:
                for m in msgs_list:
                    msg_link = await m.getMessageLink()
                    link = msg_link.link
                    self._msgs_dict[link] = m.caption
            self._sent_msg = msgs_list[-1]

    async def upload(self):
        await self._user_settings()
        res = await self._msg_to_reply()
        if not res:
            return

        semaphore = Semaphore(8)
        err = [None]

        async def process_file(file_, dirpath):
            async with semaphore:
                up_path = ospath.join(dirpath, file_)
                if not await aiopath.exists(up_path):
                    LOGGER.error(f"{up_path} not exists! Continue uploading!")
                    return
                try:
                    f_size = await aiopath.getsize(up_path)
                    async with self._lock:
                        self._total_files += 1
                    if f_size == 0:
                        LOGGER.error(
                            f"{up_path} size is zero, telegram don't upload zero size files"
                        )
                        async with self._lock:
                            self._corrupted += 1
                        return
                    if self._listener.is_cancelled:
                        return
                    cap_mono, up_path, file_ = await self._prepare_file(file_, dirpath, up_path)

                    user_session = self._user_session
                    if self._listener.hybrid_leech and self._listener.user_transmission:
                        if re_match(r".+(?=\..+\.0*\d+$)|.+(?=\.part\d+\..+$)", file_):
                            user_session = self._listener.split_size > 2097152000
                        else:
                            user_session = f_size > 2097152000
                    sent_msg = await self._upload_file(cap_mono, file_, up_path, user_session)
                    if self._listener.is_cancelled:
                        return
                    if sent_msg:
                        async with self._lock:
                            self._sent_msg = sent_msg
                        if (
                            (self._listener.is_super_chat or self._listener.up_dest)
                            and not self._is_private
                        ):
                            msg_link = await sent_msg.getMessageLink(
                                in_message_thread=bool(
                                    sent_msg.topic_id
                                    and sent_msg.topic_id.getType()
                                    == "messageTopicForum"
                                )
                            )
                            link = msg_link.link
                            async with self._lock:
                                self._msgs_dict[link] = file_
                    await sleep(1)
                except Exception as e:
                    LOGGER.error(f"{e}. Path: {up_path}")
                    err[0] = str(e)
                    async with self._lock:
                        self._corrupted += 1
                    if self._listener.is_cancelled:
                        return
                if not self._listener.is_cancelled and await aiopath.exists(
                    up_path
                ):
                    await remove(up_path)

        for dirpath, _, files in natsorted(await sync_to_async(walk, self._path)):
            if dirpath.strip().endswith("/yt-dlp-thumb"):
                continue
            if dirpath.strip().endswith("_mltbss"):
                await self._send_screenshots(dirpath, files)
                await rmtree(dirpath, ignore_errors=True)
                continue

            tasks = []
            for file_ in natsorted(files):
                tasks.append(process_file(file_, dirpath))

            if tasks:
                await gather(*tasks)
        for key, value in list(self._media_dict.items()):
            for subkey, msgs in list(value.items()):
                if len(msgs) > 1:
                    try:
                        if self._listener.hybrid_leech and self._listener.user_transmission:
                            client = TgManager.user if self._listener.split_size > 2097152000 else self._listener.client
                        else:
                            client = TgManager.user if self._user_session else self._listener.client
                        await self._send_media_group(subkey, key, msgs, client)
                    except Exception as e:
                        LOGGER.info(
                            f"While sending media group at the end of task. Error: {e}"
                        )
        if self._listener.is_cancelled:
            return
        if self._total_files == 0:
            await self._listener.on_upload_error(
                "No files to upload. In case you have filled EXCLUDED_EXTENSIONS, then check if all files have those extensions or not."
            )
            return
        if self._total_files <= self._corrupted:
            await self._listener.on_upload_error(
                f"Files Corrupted or unable to upload. {err[0] or 'Check logs!'}"
            )
            return
        LOGGER.info(f"Leech Completed: {self._listener.name}")
        await self._listener.on_upload_complete(
            None, self._msgs_dict, self._total_files, self._corrupted
        )
        return

    async def _upload_file(self, cap_mono, file, up_path, user_session, force_document=False):
        if (
            self._thumb is not None
            and not await aiopath.exists(self._thumb)
            and self._thumb != "none"
        ):
            self._thumb = None
        thumb = self._thumb
        async with self._lock:
            reply_to = self._sent_msg
        try:
            is_video, is_audio, is_image = await get_document_type(up_path)
            if not is_image and thumb is None:
                file_name = ospath.splitext(file)[0]
                thumb_path = f"{self._path}/yt-dlp-thumb/{file_name}.jpg"
                if await aiopath.isfile(thumb_path):
                    thumb = thumb_path
                elif is_audio and not is_video:
                    thumb = await get_audio_thumbnail(up_path)

            client = (TgManager.user if TgManager.user else self._listener.client) if user_session else self._listener.client
            if (
                self._listener.as_doc
                or force_document
                or (not is_video and not is_audio and not is_image)
            ):
                key = "documents"
                if is_video and thumb is None:
                    thumb = await get_video_thumbnail(up_path, None)
                if self._listener.is_cancelled:
                    return
                if thumb == "none":
                    thumb = None
                caption = await client.parseText(cap_mono)
                th_w, th_h = await sync_to_async(optimize_thumbnail, thumb)
                thumbnail = (
                    InputThumbnail(InputFileLocal(path=thumb), width=th_w, height=th_h)
                    if thumb
                    else None
                )
                content = InputMessageDocument(
                    document=InputFileLocal(path=up_path),
                    thumbnail=thumbnail,
                    disable_content_type_detection=True,
                    caption=caption,
                )
            elif is_video:
                key = "videos"
                duration = (await get_media_info(up_path))[0]
                if thumb is None and self._listener.thumbnail_layout:
                    thumb = await get_multiple_frames_thumbnail(
                        up_path,
                        self._listener.thumbnail_layout,
                        self._listener.screen_shots,
                    )
                if thumb is None:
                    thumb = await get_video_thumbnail(up_path, duration)
                if thumb is not None and thumb != "none":
                    with Image.open(thumb) as img:
                        width, height = img.size
                else:
                    width = 480
                    height = 320
                if self._listener.is_cancelled:
                    return
                if thumb == "none":
                    thumb = None
                caption = await client.parseText(cap_mono)
                th_w, th_h = await sync_to_async(optimize_thumbnail, thumb)
                thumbnail = (
                    InputThumbnail(InputFileLocal(path=thumb), width=th_w, height=th_h)
                    if thumb
                    else None
                )
                content = InputMessageVideo(
                    video=InputFileLocal(path=up_path),
                    thumbnail=thumbnail,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    caption=caption,
                )
            elif is_audio:
                key = "audios"
                duration, artist, title = await get_media_info(up_path)
                if self._listener.is_cancelled:
                    return
                if thumb == "none":
                    thumb = None
                caption = await client.parseText(cap_mono)
                th_w, th_h = await sync_to_async(optimize_thumbnail, thumb)
                thumbnail = (
                    InputThumbnail(InputFileLocal(path=thumb), width=th_w, height=th_h)
                    if thumb
                    else None
                )
                content = InputMessageAudio(
                    audio=InputFileLocal(path=up_path),
                    album_cover_thumbnail=thumbnail,
                    duration=duration,
                    title=title,
                    performer=artist,
                    caption=caption,
                )
            else:
                key = "photos"
                if self._listener.is_cancelled:
                    return
                caption = await client.parseText(cap_mono)
                content = InputMessagePhoto(
                    photo=InputFileLocal(path=up_path),
                    caption=caption,
                )
            await tracker.add_to_progress(
                up_path,
                callback=self._upload_progress,
            )

            sent_msg = await send_message_with_content(
                reply_to, content, client=client
            )
            if sent_msg.is_error:
                raise TgUploadException(sent_msg)

            future = sent_msg._client._create_request_future(
                None, f"{sent_msg.chat_id}:{sent_msg.id}"
            )
            try:
                sent_msg = await future
            finally:
                future = None

            if self._listener.is_cancelled:
                return
            if sent_msg.is_error:
                raise TgUploadException(sent_msg)

            content_type = sent_msg.content.getType()
            if self._media_group and content_type in [
                "messageDocument",
                "messageVideo",
            ]:
                key = "documents" if content_type == "messageDocument" else "videos"
                if match := re_match(r".+(?=\.0*\d+$)|.+(?=\.part\d+\..+$)", up_path):
                    pname = match.group(0)
                    async with self._lock:
                        if pname in self._media_dict[key].keys():
                            self._media_dict[key][pname].append(
                                [sent_msg.chat_id, sent_msg.id]
                            )
                        else:
                            self._media_dict[key][pname] = [
                                [sent_msg.chat_id, sent_msg.id]
                            ]
                        msgs = self._media_dict[key][pname]
                        if len(msgs) == 10:
                            msgs_to_send = msgs.copy()
                            self._media_dict[key].pop(pname)
                        else:
                            msgs_to_send = None
                            self._last_msg_in_group = True

                    if msgs_to_send:
                        await self._send_media_group(pname, key, msgs_to_send, client)

            if (
                self._thumb is None
                and thumb is not None
                and await aiopath.exists(thumb)
            ):
                await remove(thumb)
            return sent_msg
        except Exception as err:
            if (
                self._thumb is None
                and thumb is not None
                and await aiopath.exists(thumb)
            ):
                await remove(thumb)
            raise err

    @property
    def speed(self):
        try:
            return self._processed_bytes / (time() - self._start_time)
        except:
            return 0

    @property
    def processed_bytes(self):
        return self._processed_bytes

    async def cancel_task(self):
        self._listener.is_cancelled = True
        LOGGER.info(f"Cancelling Upload: {self._listener.name}")
        await self._listener.on_upload_error("your upload has been stopped!")
