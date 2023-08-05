from django.utils.functional import cached_property
from scrapy import Selector


class RawItemMixin:
    html_content: str

    @cached_property
    def _selector(self):
        return Selector(text=self.html_content)
