# -*- coding: utf-8 -*-
from urllib.parse import urljoin
from django.conf import settings
from django.utils.safestring import mark_safe


class UrlImageField(object):

    def __init__(self, field_name: str, short_description):
        self.field_name = field_name
        self.short_description = short_description

    def __call__(self, obj) -> str:
        fv = getattr(obj, self.field_name, None)
        if fv is None:
            return ''
        return mark_safe(f'<img class="auto-size" src="{fv}" />')


class ImageFileField(object):

    def __init__(self, field_name: str, short_description):
        self.field_name = field_name
        self.short_description = short_description

    def __call__(self, obj) -> str:
        fv = getattr(obj, self.field_name, None)
        if not bool(fv):
            return ''
        src = urljoin(settings.MEDIA_URL, fv.url)
        return mark_safe(f'<img class="auto-size" src="{src}" />')
