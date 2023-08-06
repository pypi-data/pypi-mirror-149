# -*- coding: utf-8 -*-
from django.contrib.admin.forms import AdminAuthenticationForm
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField


class AdminLoginWithCaptchaForm(AdminAuthenticationForm):
    captcha = CaptchaField(label=_("CAPTCHA"))
