import math
from time import time, sleep
from typing import Union, Callable, Any, Optional

NUMBER = Union[int, float]
FUNC = Callable[[], Any]


class WaitTimeoutError(TimeoutError):
    """Base Wait Exception"""


def wait_for(func: FUNC, timeout: NUMBER = 30, interval: NUMBER = .5, err_msg: Optional[str] = None) -> Any:
    _exc = None
    raise_time = time() + timeout
    while time() < raise_time:
        try:
            if result := func():
                return result
        except Exception as ex:
            _exc = ex
        sleep(interval)
    err_msg = err_msg or 'Wait time out'
    raise WaitTimeoutError(err_msg) if _exc is None else _exc


def factorial(x: int) -> float:
    return math.ldexp(math.factorial(x), 0)
