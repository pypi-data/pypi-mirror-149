import rules
from building_blocks.models import HasUUID
from django.conf import settings
from django.db import models
from rules.contrib.models import RulesModel

from .abstracts import AbstractWebClip


class WebClip(
    HasUUID,
    AbstractWebClip,
    RulesModel
):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        rules_permissions = {
            'add': rules.always_allow,
            'view': rules.is_staff,
            'change': rules.is_staff,
            'delete': rules.is_staff,
        }


__all__ = [
    'WebClip',
]
