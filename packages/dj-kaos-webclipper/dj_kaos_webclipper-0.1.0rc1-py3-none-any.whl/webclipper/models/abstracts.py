from django.db import models
from model_utils.models import TimeStampedModel


class AbstractWebClip(
    TimeStampedModel,
    models.Model
):
    class Meta:
        abstract = True

    page_url = models.URLField()
    page_title = models.CharField(max_length=255, blank=True)
    html_content = models.TextField(blank=True)

    def __str__(self):
        return self.page_title or self.page_url


__all__ = [
    'AbstractWebClip',
]
