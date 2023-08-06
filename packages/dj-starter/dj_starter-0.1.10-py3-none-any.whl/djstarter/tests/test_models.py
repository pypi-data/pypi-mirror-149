import datetime

from django.test import TestCase
from django.utils import timezone

from djstarter.models import Task, ListItem
from djstarter.exceptions import AppError


class ListItemTests(TestCase):

    """
    List Item Model Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.group = 'group_1'
        cls.label = 'label_1'
        cls.value = 'value_1'

    def test_list_item_str(self):
        list_item = ListItem(group=self.group, label=self.label, value=self.value)
        self.assertEquals(str(list_item), f'ListItem: {self.label} / {self.value}')


class TaskTests(TestCase):
    """
    Task Tests
    """

    def test_actions_remaining(self):
        task = Task.objects.create(action_count=16, target_action_count=52)
        self.assertEquals(task.actions_remaining, 36)

    def test_percent_done(self):
        task = Task.objects.create(target_action_count=0)
        self.assertEquals(task.percent_done, 0)
        task = Task.objects.create(target_action_count=15)
        task.increment_action_count(increment_by=3)
        self.assertEquals(task.percent_done, 20)

    def test_time_elapsed(self):
        ms_offset = 982
        started_at = timezone.now()
        ended_at = started_at + datetime.timedelta(milliseconds=ms_offset)
        task = Task.objects.create(
            target_action_count=15
        )
        self.assertIsNone(task.time_elapsed)

        task.set_started_at(started_at=started_at)
        self.assertIsNone(task.time_elapsed)

        task.set_ended_at(ended_at=ended_at)
        self.assertEquals(task.time_elapsed, f'0:00:00.{ms_offset}000')

    def test_set_target_action_count(self):
        task = Task.objects.create(target_action_count=5)
        self.assertEquals(task.target_action_count, 5)
        task.set_target_action_count(12)
        self.assertEquals(task.target_action_count, 12)

    def test_set_thread_count(self):
        task = Task.objects.create(thread_count=17)
        self.assertEquals(task.thread_count, 17)

    def test_did_reach_target_action_count(self):
        task = Task.objects.create(target_action_count=15)
        task.increment_action_count(increment_by=4)
        self.assertFalse(task.did_reach_target_action_count)
        task.increment_action_count(increment_by=11)
        self.assertTrue(task.did_reach_target_action_count)

    def test_task_is_waiting(self):
        task = Task.objects.create()
        task.set_init_status()
        self.assertTrue(task.is_waiting)

    def test_task_is_running(self):
        task = Task.objects.create()
        self.assertFalse(task.is_running)
        task.start()
        self.assertTrue(task.is_running)

    def test_task_has_error(self):
        task = Task.objects.create()
        self.assertFalse(task.has_error)
        task.set_error_shutdown_status(e=AppError)
        self.assertTrue(task.has_error)

    def test_task_is_finished(self):
        task = Task.objects.create()
        self.assertFalse(task.is_finished)

        task.set_error_shutdown_status(e=ValueError)
        task.set_finished()
        self.assertFalse(task.is_finished)

        task.set_cancelled_status()
        task.set_finished()
        self.assertTrue(task.is_finished)

    def test_task_is_stopping(self):
        task = Task.objects.create()
        self.assertFalse(task.is_stopping)
        task.set_stopping_status()
        self.assertTrue(task.is_stopping)

    def test_task_is_cancelled(self):
        task = Task.objects.create()
        self.assertFalse(task.is_cancelled)
        task.set_cancelled_status()
        self.assertTrue(task.is_cancelled)

    def test_pretty_status(self):
        task = Task.objects.create()
        task.set_finished()
        self.assertEquals(task.pretty_status, 'finished')
