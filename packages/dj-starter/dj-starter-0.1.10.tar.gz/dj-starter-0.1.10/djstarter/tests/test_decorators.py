from http import HTTPStatus
from unittest.mock import Mock

import httpx
from django.test import TestCase
from httpx import Request, Response

from djstarter import decorators, exceptions


class RetryTests(TestCase):
    """
    Decorator Tests
    """

    def test_retry(self):
        tries = 5
        func = Mock(side_effect=exceptions.ApiError("Test"))
        decorated_function = decorators.retry(
            retry_exceptions=(exceptions.ApiError,),
            tries=tries,
            delay=0,
            backoff=1,
            jitter=0,
        )(func)
        with self.assertRaises(exceptions.ApiError):
            decorated_function()
        self.assertEquals(func.call_count, tries)


class APIErrorCheckTests(TestCase):

    def test_check_response_400(self):
        request = Request(url='', method='')
        func = Mock(side_effect=httpx.HTTPStatusError(
            request=request,
            response=Response(
                request=request,
                status_code=HTTPStatus.BAD_REQUEST,
            ),
            message='test'
        ))
        decorated_function = decorators.api_error_check(func)
        with self.assertRaises(exceptions.ApiError):
            decorated_function()

    def test_check_response_502(self):
        request = Request(url='', method='')
        func = Mock(side_effect=httpx.HTTPStatusError(
            request=request,
            response=Response(
                request=request,
                status_code=HTTPStatus.BAD_GATEWAY,
            ),
            message='test'
        ))
        decorated_function = decorators.api_error_check(func)
        with self.assertRaises(httpx.HTTPStatusError):
            decorated_function()


class WrapExceptions(TestCase):
    def test_ok(self):
        func = Mock()
        decorated_function = decorators.wrap_exceptions(raise_as=BlockingIOError)
        decorated_function(func)()
        self.assertTrue(func.called)

    def test_pass_thru(self):
        func = Mock(side_effect=BlockingIOError)
        decorated_function = decorators.wrap_exceptions(raise_as=OSError)
        with self.assertRaises(BlockingIOError):
            decorated_function(func)()

    def test_runtime_error(self):
        func = Mock(side_effect=RuntimeError)
        decorated_function = decorators.wrap_exceptions(raise_as=OSError)
        with self.assertRaises(OSError):
            decorated_function(func)()


class DBConnCloseExceptions(TestCase):

    def test_db_conn_close(self):
        func = Mock()
        decorators.db_conn_close(func)()
        self.assertEquals(func.call_count, 1)


class TimingTests(TestCase):

    def test_timing(self):
        func = Mock(return_value=True)
        func.__name__ = 'test_func'
        decorators.timing(func)()
        self.assertEquals(func.call_count, 1)


class DelayFnTests(TestCase):

    def test_delay_fn(self):
        def double(x): return 2 * x
        decorated_function = decorators.delay_fn(seconds=0)(double)
        self.assertEquals(decorated_function(31), 62)
