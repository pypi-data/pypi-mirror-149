from rest_framework import viewsets

from ..permissions import *
from ..serializers import *
from ...models import *


class BaseWebClipViewSet(
    viewsets.GenericViewSet
):
    permission_classes = (WebClipPermissions,)
    queryset = WebClip.objects.select_related(
        'owner',
    ).all()
    serializer_class = WebClipSerializer
    lookup_field = 'uuid'
    search_fields = (
        'page_url',
        'page_title',
    )
    filterset_fields = (
        'owner',
    )

    def get_queryset(self):
        qs = super(BaseWebClipViewSet, self).get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(owner=self.request.user)
        return qs


__all__ = [
    'BaseWebClipViewSet',
]
