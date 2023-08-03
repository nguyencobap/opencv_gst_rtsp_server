import ctypes
import inspect
import threading
from typing import Optional, Type

class ThreadUtilities:

    @staticmethod
    def is_alive(tid: int) -> bool:
        thread = ThreadUtilities.get_thread_by_id(tid=tid)
        if thread:
            return thread.is_alive()
        else:
            return False

    @staticmethod
    def get_thread_by_id(tid: int) -> Optional[threading.Thread]:
        for thread in threading.enumerate():
            if thread.ident == tid:
                return thread
        return None

    @staticmethod
    def async_raise(tid: int, exception_type: Type[BaseException] = SystemExit) -> bool:
        if not inspect.isclass(exception_type):
            raise TypeError("Only types can be raised (not instances)")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exception_type))
        if res == 0:
            raise ValueError("Invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")
        return True
