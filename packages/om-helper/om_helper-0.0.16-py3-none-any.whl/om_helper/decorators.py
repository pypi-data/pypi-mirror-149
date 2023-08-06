import signal
import time
from functools import wraps

from om_helper.helper import run, base_error_cb
from om_helper.exceptions import TimeoutException


def run_decorator(onerror=None, onsuccess=None):
    def inner(f):
        @wraps(f)
        def _inner(*args, **kwargs):
            try:
                ret = f(*args, **kwargs)
                if callable(onsuccess):
                    return onsuccess(ret)
                return ret
            except Exception as e:
                if callable(onerror):
                    return onerror(e)
                raise e

        return _inner

    return inner


def retry_decorator(times=0, interval=0, onerror=None, onretry=None, onsuccess=None):
    def _retry(f, _times, *args, **kwargs):
        try:
            ret = f(*args, **kwargs)
            if callable(onsuccess):
                return run(onsuccess, ret, onerror=base_error_cb)
            return ret
        except Exception as exc:
            if _times > 0:
                if callable(onretry):
                    run(onretry, exc=exc, onerror=base_error_cb)
                if interval > 0:
                    time.sleep(interval)
                return _retry(f, _times - 1, *args, **kwargs)
            if callable(onerror):
                return run(onerror, exc=exc, onerror=base_error_cb)
            raise exc

    def inner(f):
        @wraps(f)
        def _inner(*args, **kwargs):
            return _retry(f, times, *args, **kwargs)

        return _inner

    return inner


def timeout_decorator(seconds=None, cb=None):
    """函数执行时间控制，超时抛出异常
        ITIMER_REAL: 以逝去时间递减
        ITIMER_VIRTUAL： 计算在应用层递减的时间不计算在内核层的递减的时间
        ITIMER_PROF： 递减时间更为精确 会减去在系统中阻塞的时间
    signal.setitimer(
        signum, # 信号量
        timeout, # 超时间隔
        interval, # 多久之后开始计时
    )
    """

    def _cb(n, f):
        raise TimeoutException(TimeoutException.err_msg)

    def _decorator(f):
        @wraps(f)
        def __decorator(*args, **kwargs):
            old = None
            if seconds:
                old = signal.signal(signal.SIGALRM, cb or _cb)
                signal.setitimer(signal.ITIMER_PROF, seconds)

            ret = run(f, *args, **kwargs, onerror=base_error_cb)
            if seconds:
                # timer时间设置为0，对应的事件会被取消
                signal.setitimer(signal.ITIMER_PROF, 0)
                signal.signal(signal.SIGALRM, old)
            return ret

        return __decorator

    return _decorator
