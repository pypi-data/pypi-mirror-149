import datetime
import json
import logging
import math
import mimetypes
import os
import queue
import random
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from enum import Enum
from threading import BoundedSemaphore
from urllib.parse import urlparse

from django.utils import dateparse

logger = logging.getLogger(__name__)


class QueuedThreadExecutor(ThreadPoolExecutor):
    """
    Limits the queue size so all futures don't get created at once

    :param max_workers: Integer - the size of the thread pool
    """

    def __init__(self, max_workers=5, *args, **kwargs):
        super().__init__(max_workers=max_workers, *args, **kwargs)
        self._work_queue = queue.Queue(maxsize=max_workers)


class SerializerMixin:
    @property
    def as_dict(self):
        return json.loads(self.as_json)

    @property
    def as_json(self):
        return obj_to_json(self)


class BoundedThreadExecutor:
    """
    BoundedExecutor behaves as a ThreadPoolExecutor which will block on
    calls to submit() once the limit given as "bound" work items are queued for
    execution. Closes db connections on add_done_callback

    :param max_workers: Integer - the size of the thread pool
    :param bound: Integer - the maximum number of items in the work queue
    """

    def __init__(self, max_workers=5, bound=0):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.semaphore = BoundedSemaphore(bound + max_workers)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.shutdown(wait=True)
        return False

    """See concurrent.futures.Executor#submit"""

    def submit(self, fn, *args, **kwargs):
        self.semaphore.acquire()
        try:
            future = self.executor.submit(fn, *args, **kwargs)
        except Exception:
            self.semaphore.release()
            raise
        else:
            future.add_done_callback(lambda x: self.semaphore.release())
            return future

    """See concurrent.futures.Executor#shutdown"""

    def shutdown(self, wait=True):
        self.executor.shutdown(wait)


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]

    @classmethod
    def labels(cls):
        return [tag.name for tag in cls]

    @classmethod
    def by_label(cls, label):
        return [tag.value for tag in cls if label == tag.name][0]


class Pager:
    """
    Facilitates paging of generic apis.
    Page count starts at 1
    """

    def __init__(self, items_per_page=100, items_count=1):
        self.items_per_page = items_per_page
        self.items_count = items_count

    @property
    def items_count(self):
        return self._items_count

    @items_count.setter
    def items_count(self, items_count):
        if items_count < 1:
            raise ValueError('Items Count must be integer greater than zero')
        self._items_count = items_count

    @property
    def last_page_number(self):
        return math.ceil(self.items_count / self.items_per_page)

    @property
    def last_page_items_count(self):
        return self.items_on_page(self.last_page_number)

    def validate_page_number(self, page_number):
        if page_number < 1:
            raise ValueError('Page Number must be integer greater than zero')

        if page_number > self.last_page_number:
            raise ValueError(f'Page Number must be integer less than {self.last_page_number}.')

    def offset(self, page_number):
        self.validate_page_number(page_number)

        return (page_number - 1) * self.items_per_page

    def items_on_page(self, page_number):
        self.validate_page_number(page_number)

        if page_number == self.last_page_number:
            return self.items_count % self.items_per_page or self.items_per_page

        return self.items_per_page


def abbrev_str(s: str, max_length) -> str:
    return f'{s[:max_length]}...' if len(s) > max_length else s


def eye_catcher_line(msg):
    edge = '####'
    return f'{edge}  {msg}  {edge}'


def get_file_ext(uri):
    return os.path.splitext(urlparse(uri).path)[1]


def get_path(uri):
    return urlparse(uri).path


def get_mimetype(uri):
    return mimetypes.guess_type(get_path(uri))[0]


def get_weighted_item(items):
    return random.choices(population=[p[0] for p in items], weights=[p[1] for p in items], k=1)[0]


def obj_to_json(obj):
    return json.dumps(obj, default=lambda x: x.__dict__, separators=(',', ':'))


def pretty_dict(data):
    return json.dumps(
        data,
        default=lambda x: x.__dict__,
        sort_keys=True,
        indent=4
    )


def past_unix_timestamp_ss(unix_timestamp, **kwargs):
    dt = datetime.fromtimestamp(unix_timestamp) - timedelta(**kwargs)
    return int(dt.timestamp())


def utf_16_decode(msg):
    return msg.encode('utf-16', 'surrogatepass').decode('utf-16')


def iso8601_timestamp_to_unix(timestamp):
    return iso8601_timestamp_to_datetime(timestamp).timestamp() if timestamp else timestamp


def iso8601_timestamp_to_datetime(timestamp):
    return dateparse.parse_datetime(timestamp) if timestamp else timestamp


def exponential_decay(y_init, y_min, t, tau):
    """
    :param y_init:  Y-axis starting point
    :param y_min:   Y-axis minimum value
    :param t:       Time factor -> Higher = Lower y-axis value
    :param tau:     Decay factor -> Lower = faster decay

    :return:
    """
    y_scaled = y_init - y_min
    return (y_scaled * math.exp(-t / tau)) + y_min


def add_jitter(min_value, jitter, val):
    return max(min_value, val + random.uniform(-jitter, +jitter))


def dice_roll(chance):
    if chance > 1 or chance < 0:
        raise ValueError(f'{chance} is not a valid value')
    return random.random() <= chance
