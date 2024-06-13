# DeliveryService/decorators.py
import time
import logging
from typing import Callable
from functools import wraps

logger = logging.getLogger("main")

def retry(attempts: int) -> Callable | None:
    """
    Function retry decorator.

    Args:
        attempts: Attempt count of retying.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as err:
                    logger.error(f"Attepmt {i+1} of {attempts} finished with exception: {err}.")
                    time.sleep(0.5)
            return None
        return wrapper
    return decorator


# def log_request(func):
#     @wraps(func)
#     def wrapped(self, request, *args, **kwargs):
#         logger.info(f"Request Method: {request.method}, Request Path: {request.get_full_path()}")
#         return func(self, request, *args, **kwargs)
#     return wrapped