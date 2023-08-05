# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from tempfile import TemporaryFile

from .base import Utils
from .task import IntervalTask

from hagworm.extend.base import ContextManager


class _DataBase:

    def __init__(self):

        self._data_list = []

    def _on_add_data(self):
        pass

    def append(self, data):

        self._data_list.append(data)

        self._on_add_data()

    def extend(self, data_list):

        self._data_list.extend(data_list)

        self._on_add_data()


class DataQueue(_DataBase):

    def __init__(self, handler, maxsize=1):

        super().__init__()

        self._handler = handler

        self._task_list = set()

        self._task_maxsize = maxsize

    @property
    def maxsize(self):
        return self._task_maxsize

    @maxsize.setter
    def maxsize(self, val):
        self._task_maxsize = val

    def _on_add_data(self):

        while len(self._task_list) < self._task_maxsize:
            if not self._create_task():
                break

    def _create_task(self):

        if len(self._data_list) > 0:

            task = Utils.create_task(
                self._handler(
                    self._data_list.pop(0)
                )
            )

            task.add_done_callback(self._done_callback)

            self._task_list.add(task)

            return True

        else:

            return False

    def _done_callback(self, task):

        if task in self._task_list:
            self._task_list.remove(task)

        self._on_add_data()


class QueueBuffer(_DataBase):

    def __init__(self, handler, maxsize, timeout=0, task_limit=0):

        super().__init__()

        self._timer = None
        self._handler = handler

        self._maxsize = maxsize
        self._task_queue = None

        if timeout > 0:
            self._timer = IntervalTask.create(timeout, self._handle_buffer)
            self._timer.start()

        if task_limit > 0:
            self._task_queue = DataQueue(handler, task_limit)

    def _on_add_data(self):

        if len(self._data_list) >= self._maxsize:
            self._handle_buffer()

    def _handle_buffer(self):

        if len(self._data_list) > 0:

            data_list, self._data_list = self._data_list, []

            if self._task_queue is not None:
                self._task_queue.append(data_list)
            else:
                Utils.call_soon(self._run, data_list)


class FileBuffer(ContextManager):
    """文件缓存类
    """

    def __init__(self, slice_size=0x1000000):

        self._buffers = []

        self._slice_size = slice_size

        self._read_offset = 0

        self._append_buffer()

    def _context_release(self):

        self.close()

    def _append_buffer(self):

        self._buffers.append(TemporaryFile())

    def close(self):

        while len(self._buffers) > 0:
            self._buffers.pop(0).close()

        self._read_offset = 0

    def write(self, data):

        buffer = self._buffers[-1]

        buffer.seek(0, 2)
        buffer.write(data)

        if buffer.tell() >= self._slice_size:
            buffer.flush()
            self._append_buffer()

    def read(self, size=None):

        buffer = self._buffers[0]

        buffer.seek(self._read_offset, 0)

        result = buffer.read(size)

        if len(result) == 0 and len(self._buffers) > 1:
            self._buffers.pop(0).close()
            self._read_offset = 0
        else:
            self._read_offset = buffer.tell()

        return result
