from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import Q


class BaseManager(models.Manager):

    def get_by_oid(self, oid):
        return super().get_queryset().get(oid=oid)

      
class AuthUserManager(UserManager):
    def by_id(self, _id):
        q = Q(id=_id)
        return super().get_queryset().filter(q).get()

    def get_service_user(self):
        q = Q(is_superuser=True)
        return super().get_queryset().filter(q).first()



class ListItemManager(BaseManager):

    def get_value(self, group, label):
        q = Q(group=group, label=label)
        li_obj = super().get_queryset().filter(q).only('value').first()
        return li_obj.value if li_obj else None
