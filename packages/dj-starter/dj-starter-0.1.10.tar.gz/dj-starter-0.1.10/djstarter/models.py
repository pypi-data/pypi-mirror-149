import logging
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from . import managers, utils

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    oid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def oid_str(self):
        return str(self.oid)


class BaseTask(BaseModel):
    """
    Base task model
    """

    class Statuses(utils.ChoiceEnum):
        INIT = 0
        RUNNING = 1
        ERROR = 2
        FINISHED = 3
        STOPPING = 4
        STOPPED = 5
        CANCELLED = 6
        SCHEDULED = 7

    scheduled_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=Statuses.INIT.value, choices=Statuses.choices(), db_index=True)
    action_count = models.IntegerField(default=0)
    target_action_count = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(200)], )
    thread_count = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)], )
    parameters = models.JSONField(null=False, default=dict)
    results = models.JSONField(null=False, default=dict)

    class Meta:
        abstract = True

    @property
    def actions_remaining(self):
        return self.target_action_count - self.action_count

    @property
    def percent_done(self):
        try:
            return int(min(self.action_count / self.target_action_count * 100, 100))
        except ZeroDivisionError:
            return 0

    @property
    def time_elapsed(self):
        if not (self.started_at and self.ended_at):
            return None
        return str(self.ended_at - self.started_at)

    @property
    def did_reach_target_action_count(self):
        return self.action_count >= self.target_action_count

    # Status Checks

    @property
    def is_waiting(self):
        return self.status in (self.Statuses.INIT.value, self.Statuses.SCHEDULED.value)

    @property
    def is_running(self):
        return self.status == self.Statuses.RUNNING.value

    @property
    def has_error(self):
        return self.status == self.Statuses.ERROR.value

    @property
    def is_finished(self):
        return self.status == self.Statuses.FINISHED.value

    @property
    def is_stopping(self):
        return self.status == self.Statuses.STOPPING.value

    @property
    def is_cancelled(self):
        return self.status == self.Statuses.CANCELLED.value

    # Field Prettifiers

    @property
    def pretty_status(self):
        return self.get_status_display().lower()

    @property
    def pretty_parameters(self):
        return utils.pretty_dict(self.parameters)   # pragma: no cover

    @property
    def pretty_results(self):
        return utils.pretty_dict(self.results)  # pragma: no cover

    def set_target_action_count(self, target_action_count):
        self.target_action_count = target_action_count
        self.save()

    def set_thread_count(self, thread_count):
        self.thread_count = thread_count
        self.save()

    def set_started_at(self, started_at=timezone.now):
        self.started_at = started_at
        self.save()

    def set_ended_at(self, ended_at=timezone.now):
        self.ended_at = ended_at
        self.save()

    def increment_action_count(self, increment_by=1):
        self.action_count += increment_by
        if self.did_reach_target_action_count:
            self.set_stopping_status()
            logger.info(f'{self} reached target action count: {self.action_count}')
        self.save()
        logger.info(f'{self} action count: {self.action_count}')

    def set_init_status(self):
        self.status = self.Statuses.INIT.value
        self.results = dict()
        self.save()

    def set_error_shutdown_status(self, e):
        self.results['error'] = str(e)
        self.status = self.Statuses.ERROR.value
        self.save()
        logger.exception(f'{self} Error Event: {type(e)}')

    def set_finished(self, results=None):
        if not self.has_error:
            self.status = self.Statuses.FINISHED.value
        self.results.update(results or dict())
        self.ended_at = timezone.now()
        self.save()

    def set_stopping_status(self):
        self.status = self.Statuses.STOPPING.value
        self.save()

    def set_cancelled_status(self):
        self.status = self.Statuses.CANCELLED.value
        self.save()

    def start(self):
        self.status = self.Statuses.RUNNING.value
        self.started_at = timezone.now()
        self.save()


class Task(BaseTask):

    class Meta:
        db_table = 'core_task'
        ordering = ['-created']
        app_label = 'djstarter'


class AuthUser(AbstractUser):
    objects = managers.AuthUserManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        db_table = 'core_authuser'
        ordering = ['-username']
        app_label = 'djstarter'


class ListItem(BaseModel):
    group = models.CharField(max_length=20)
    label = models.CharField(max_length=64)
    value = models.CharField(max_length=64)

    objects = managers.ListItemManager()

    class Meta:
        db_table = 'core_listitem'
        ordering = ['-created']
        app_label = 'djstarter'
        constraints = [
            models.UniqueConstraint(fields=['group', 'label'], name='list_item_unique'),
        ]

    def __str__(self):
        return f'ListItem: {self.label} / {self.value}'
