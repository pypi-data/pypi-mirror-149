from building_blocks.admin import HasUUIDAdmin
from django.contrib import admin

from .helpers import WebClipAdminHelper
from ..models import WebClip


@admin.register(WebClip)
class WebClipAdmin(
    HasUUIDAdmin,
    WebClipAdminHelper,
    admin.ModelAdmin
):
    search_fields = (
        *HasUUIDAdmin.search_fields,
        *WebClipAdminHelper.search_fields,
    )
    list_display = (
        *WebClipAdminHelper.list_display,
        'owner',
    )
    autocomplete_fields = ('owner',)
    fields = None
    fieldsets = (
        (None, {'fields': WebClipAdminHelper.fields}),
        ("Misc", {'fields': ('owner',)}),
        *HasUUIDAdmin.fieldsets,
    )


__all__ = [
    'WebClipAdmin',
]
