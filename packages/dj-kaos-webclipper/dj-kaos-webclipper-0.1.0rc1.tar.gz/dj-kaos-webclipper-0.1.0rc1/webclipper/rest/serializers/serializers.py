from building_blocks.rest.serializers import UUIDLookupSerializerMixin
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .base import *
from ...models import WebClip

User = get_user_model()


class WebClipSerializer(BaseWebClipSerializer):
    owner = serializers.SlugRelatedField(
        slug_field=User.USERNAME_FIELD,
        default=CurrentUserDefault(),
        queryset=User.objects.all(),
    )

    class Meta(
        UUIDLookupSerializerMixin.Meta,
        BaseWebClipSerializer.Meta
    ):
        model = WebClip
        fields = [
            *UUIDLookupSerializerMixin.Meta.fields,
            *BaseWebClipSerializer.Meta.fields,
            'owner',
        ]


__all__ = [
    'WebClipSerializer',
]
