from gettext import ngettext

from building_blocks.admin.mixins import DjangoObjectActionsPermissionsMixin
from django.contrib import admin, messages
from django_object_actions import takes_instance_or_queryset


class WebClipAdminHelper(admin.ModelAdmin):
    search_fields = (
        'page_url',
        'page_title',
    )
    list_display = (
        '__str__',
        'page_url',
    )
    fields = ('page_url', 'page_title', 'html_content')


class RawItemAdmin(DjangoObjectActionsPermissionsMixin, admin.ModelAdmin):
    PROCESS = 'process'

    actions = (PROCESS,)
    change_actions = (PROCESS,)

    @takes_instance_or_queryset
    @admin.action
    def process(self, request, queryset):
        count_all = queryset.count()
        count_created = 0
        for item in queryset:
            _, created = item.process(update=True)
            if created:
                count_created += 1

        message = f"{count_all} raw item{ngettext('', 's', count_all)} processed."
        message += f" {count_created} new item{ngettext('', 's', count_created)} created."
        self.message_user(request, message, messages.SUCCESS)
