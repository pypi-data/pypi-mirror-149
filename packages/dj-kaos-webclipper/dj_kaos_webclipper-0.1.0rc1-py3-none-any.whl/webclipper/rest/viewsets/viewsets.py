from rest_framework import mixins

from .base import *


class WebClipViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    BaseWebClipViewSet
):
    pass


__all__ = [
    'WebClipViewSet',
]
