from asyncio import sleep, TimeoutError, gather, Semaphore
from aiohttp.client_exceptions import ClientError

from ... import LOGGER
from ...core.torrent_manager import TorrentManager, aria2_name


class DirectListener:
    def __init__(self, path, listener, a2c_opt):
        self.listener = listener
        self._path = path
        self._a2c_opt = a2c_opt
        self._proc_bytes = 0
        self._failed = 0
        self.active_tasks = {}
        self.name = self.listener.name
        self._lock = Semaphore(1)

    @property
    def processed_bytes(self):
        completed = self._proc_bytes
        for task in self.active_tasks.values():
            completed += int(task.get("completedLength", "0"))
        return completed

    @property
    def speed(self):
        spd = 0
        for task in self.active_tasks.values():
            spd += int(task.get("downloadSpeed", "0"))
        return spd

    async def _download_file(self, content, semaphore):
        async with semaphore:
            if self.listener.is_cancelled:
                return

            a2c_opt = self._a2c_opt.copy()
            if content["path"]:
                a2c_opt["dir"] = f"{self._path}/{content['path']}"
            else:
                a2c_opt["dir"] = self._path

            filename = content["filename"]
            a2c_opt["out"] = filename

            try:
                gid = await TorrentManager.aria2.addUri(
                    uris=[content["url"]], options=a2c_opt, position=0
                )
            except (TimeoutError, ClientError, Exception) as e:
                async with self._lock:
                    self._failed += 1
                LOGGER.error(f"Unable to download {filename} due to: {e}")
                return

            while True:
                if self.listener.is_cancelled:
                    await TorrentManager.aria2.remove(gid)
                    break

                task = await TorrentManager.aria2.tellStatus(gid)
                async with self._lock:
                    self.active_tasks[gid] = task

                if error_message := task.get("errorMessage"):
                    async with self._lock:
                        self._failed += 1
                        self.active_tasks.pop(gid, None)
                    LOGGER.error(
                        f"Unable to download {aria2_name(task)} due to: {error_message}"
                    )
                    await TorrentManager.aria2_remove(task)
                    break
                elif task.get("status", "") == "complete":
                    async with self._lock:
                        self._proc_bytes += int(task.get("totalLength", "0"))
                        self.active_tasks.pop(gid, None)
                    await TorrentManager.aria2_remove(task)
                    break
                await sleep(1)

    async def download(self, contents):
        semaphore = Semaphore(50)
        tasks = []
        for content in contents:
            tasks.append(self._download_file(content, semaphore))

        await gather(*tasks)

        if self.listener.is_cancelled:
            return
        if self._failed == len(contents):
            await self.listener.on_download_error("All files failed to download!")
            return
        await self.listener.on_download_complete()

    async def cancel_task(self):
        self.listener.is_cancelled = True
        LOGGER.info(f"Cancelling Download: {self.listener.name}")
        await self.listener.on_download_error("Download Cancelled by User!")
        for gid in list(self.active_tasks.keys()):
            try:
                await TorrentManager.aria2.remove(gid)
            except:
                pass
