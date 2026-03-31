from time import time

from .... import LOGGER
from ...ext_utils.status_utils import (
    get_readable_file_size,
    MirrorStatus,
    get_readable_time,
)


class JoinStatus:
    def __init__(self, listener, obj, gid):
        self.listener = listener
        self._obj = obj
        self._gid = gid
        self._start_time = time()
        self.tool = "cat"

    def gid(self):
        return self._gid

    def progress(self):
        return "0%"

    def speed(self):
        return "-"

    def processed_bytes(self):
        return "-"

    def name(self):
        return self.listener.name

    def size(self):
        return get_readable_file_size(self.listener.size)

    def eta(self):
        return "-"

    def status(self):
        return MirrorStatus.STATUS_JOIN

    def task(self):
        return self

    async def cancel_task(self):
        LOGGER.info(f"Cancelling Join: {self.listener.name}")
        self.listener.is_cancelled = True
        if (
            self.listener.subproc is not None
            and self.listener.subproc.returncode is None
        ):
            try:
                self.listener.subproc.kill()
            except:
                pass
        await self.listener.on_upload_error("Join stopped by user!")
