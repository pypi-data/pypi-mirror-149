# thk-django-admin

[History](HISTORY.md)

## 0. Install

```shell script
pip install thk-django-admin
```

### settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # depend on django-simple-captcha
    'captcha',
    
    'thk_django_admin',
]
```

## 1. Login with CAPTCHA

### 1.1 urls.py

```python
from django.contrib import admin
from django.urls import path, include

from thk_django_admin.forms import AdminLoginWithCaptchaForm
# There is another method, see below 2
admin.site.login_form = AdminLoginWithCaptchaForm
admin.site.login_template = 'thk_django_admin/admin_captcha/login.html'

urlpatterns = [
    path('admin/', admin.site.urls),
    # enable django-simple-captcha
    path('captcha/', include('captcha.urls')),
]

```

## 2. Change apps and models order

### 2.1 Inherit OrderedAdminSite

```python
from thk_django_admin.sites import OrderedAdminSite
from thk_django_admin.forms import AdminLoginWithCaptchaForm
# example apps and models
from ordered.models import ModelOne, ModelTwo, ModelThree
from ordered.apps import OrderedConfig


class TestProjectAdminSite(OrderedAdminSite):
    # This is the another method
    login_form = AdminLoginWithCaptchaForm
    login_template = 'thk_django_admin/admin_captcha/login.html'
    # Configuration order by ordering
    ordered_apps = [
        {
            'verbose_name': OrderedConfig.verbose_name,
            'ordering': 2,
            'models': [
                {'model': ModelOne, 'ordering': 1},
                {'model': ModelTwo, 'ordering': 2},
                {'model': ModelThree, 'ordering': 3}
            ]
        },
    ]

# The instance can be used for register admin
test_project_admin_site = TestProjectAdminSite(name='test_project_admin_site')

```

### 2.2 urls.py

```python
from django.urls import path, include
from test_project.site import test_project_admin_site


urlpatterns = [
    path('admin/', test_project_admin_site.urls),
    path('captcha/', include('captcha.urls')),
]

```

### 2.3 Usage

```python
from django.contrib import admin
from test_project.site import test_project_admin_site

from ordered.models import ModelOne


@admin.register(ModelOne, site=test_project_admin_site)
class ModelOneAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name'
    )

```
