import logging
import time
from functools import wraps

from django.db import connection, connections
from httpx import codes, HTTPStatusError

from . import utils
from .exceptions import ApiError, NotAuthorized

logger = logging.getLogger(__name__)


def retry(retry_exceptions, tries=4, delay=1.5, backoff=2, jitter=0.1):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        :param retry_exceptions: Exceptions to retry on before raise
        :param tries: Number of times to try (not retry) before giving up.
        :param delay: Initial delay between retries in seconds.
        :param backoff: Backoff multiplier (e.g. value of 2 will double the delay each retry).
        :param jitter: adds jitter to delay
    """
    def deco_func(func):

        @wraps(func)
        def wrapper_func(*args, **kwargs):

            m_tries, m_delay = tries, delay
            while m_tries > 1:
                try:
                    return func(*args, **kwargs)
                except retry_exceptions as e:
                    j_delay = utils.add_jitter(min_value=0, jitter=jitter, val=m_delay)
                    logger.warning(f'{type(e)} -> {str(e)} -> Retrying in {j_delay} seconds...')
                    time.sleep(j_delay)
                    m_tries -= 1
                    m_delay *= backoff

            logger.warning(f'Max tries reached: {tries}')
            return func(*args, **kwargs)

        return wrapper_func  # true decorator

    return deco_func


def api_error_check(func):

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPStatusError as e:
            status_code = e.response.status_code
            if status_code in (408, 429) or status_code >= 500:     # Retryable status codes
                raise
            if status_code == 401:
                raise NotAuthorized(*args, **kwargs, **e.__dict__)

            raise ApiError(*args, **kwargs, **e.__dict__)

    return wrapper_func


def wrap_exceptions(raise_as):

    def deco_func(func):

        @wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except raise_as:
                raise
            except Exception as e:
                raise raise_as(*args, **kwargs, **e.__dict__)

        return wrapper_func  # true decorator

    return deco_func


def db_conn_close(func):
    """
    Closes open db connection after check if we are in a transaction block.
    This is important to check since TestCases fail if this check isn't performed

    :param func:
    :return:
    """

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        finally:
            if not connection.in_atomic_block:
                connections.close_all()

    return wrapper_func  # true decorator


def timing(func):
    """
    Decorator that times the execution of wrapped function
    """
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        logger.info(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result

    return wrap_func


def delay_fn(seconds=0, jitter=0.1):
    """
    Delays wrapped function

    :param seconds: Delay in seconds
    :param jitter: adds jitter to delay
    :return:
    """

    def deco_func(func):

        @wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            finally:
                j_seconds = utils.add_jitter(min_value=0, jitter=jitter, val=seconds)
                logger.debug(f'Delaying for {j_seconds:.2f} seconds...')
                time.sleep(j_seconds)

        return wrapper_func  # true decorator

    return deco_func
