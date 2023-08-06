import csv
import itertools
import time
from urllib.parse import parse_qs

from django.conf.locale.en import formats as en_formats
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse

from . import models

en_formats.DATETIME_FORMAT = "M d y H:i"


class ExportCsvMixin:
    @classmethod
    def field_values(cls, obj, field_names, query_fields=None):
        vals = [getattr(obj, field) for field in field_names]
        if query_fields:
            queries = [q.replace('?', '') for q in vals if '=' in str(q)]
            parts = [[v[0] for k, v in parse_qs(q).items() if k in query_fields] for q in queries]
            return list(itertools.chain.from_iterable(parts))
        return vals

    def export_as_csv(self, request, queryset, query_fields=None):
        meta = self.model._meta
        model_name = str(meta).split('.')[1]
        field_names = [field.name for field in meta.fields]

        rows = [self.field_values(obj, field_names, query_fields) for obj in queryset]
        return self.write_to_csv(model_name, query_fields or field_names, rows)

    @classmethod
    def write_to_csv(cls, filename, field_names, rows):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={filename}_{time.strftime("%Y%m%d")}.csv'
        writer = csv.writer(response, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(field_names)
        for row in rows:
            writer.writerow(row)

        return response

    export_as_csv.short_description = "Export Selected To CSV"


class BaseAdmin(admin.ModelAdmin, ExportCsvMixin):
    read_only_exclude = ()
    show_full_result_count = False

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields if f.name not in self.read_only_exclude]

    def bulk_delete(self, request, queryset):
        queryset.delete()

    bulk_delete.short_description = 'Bulk Delete'

    actions = ('export_as_csv', bulk_delete, )


@admin.register(models.AuthUser)
class AuthUserAdmin(UserAdmin):
    list_display = ['date_joined', 'username', 'email', 'is_staff', 'is_superuser']
    list_filter = ('is_staff', 'is_superuser')
    ordering = ['-username']
    search_fields = ['username', ]

    show_full_result_count = False

    def bulk_delete(self, request, queryset):
        queryset.delete()

    bulk_delete.short_description = 'Bulk Delete'

    def unlock_user(self, request, queryset):
        queryset.update(is_locked=False, locked_at=None)

    unlock_user.short_description = 'Unlock User'

    actions = ['export_as_csv', bulk_delete, unlock_user, ]
