# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings


class _DefaultMedia:
    css = {
        'all': ('thk_django_admin/custom_model_admin/custom.css',)
    }


class CustomMediaModelAdmin(admin.ModelAdmin):

    class Media:
        css = getattr(settings, 'CUSTOM_MODEL_ADMIN_CSS', _DefaultMedia.css)
        js = getattr(settings, 'CUSTOM_MODEL_ADMIN_JS', None)
