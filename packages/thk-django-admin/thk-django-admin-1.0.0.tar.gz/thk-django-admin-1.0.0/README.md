# 如何使用thk-django-admin

[功能历史与规划](HISTORY.md)

## 0. 基础配置

### 配置settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 依赖django-simple-captcha
    'captcha',
    # 添加thk_django_admin
    'thk_django_admin',
]
```

## 1. 登录时有验证码

### 1.1 配置urls.py

```python
from django.contrib import admin
from django.urls import path, include

from thk_django_admin.forms import AdminLoginWithCaptchaForm
# 还有一种写法，见功能2
admin.site.login_form = AdminLoginWithCaptchaForm
admin.site.login_template = 'thk_django_admin/admin_captcha/login.html'

urlpatterns = [
    path('admin/', admin.site.urls),
    # 使captcha启效
    path('captcha/', include('captcha.urls')),
]

```

## 2. app与model可调顺序

### 2.1 继承OrderedAdminSite，并按格式配置子类

```python
from thk_django_admin.sites import OrderedAdminSite
from thk_django_admin.forms import AdminLoginWithCaptchaForm
# 样例app与model
from ordered.models import ModelOne, ModelTwo, ModelThree
from ordered.apps import OrderedConfig


class TestProjectAdminSite(OrderedAdminSite):
    # 功能1(登录时有验证码)，也可以这么写
    login_form = AdminLoginWithCaptchaForm
    login_template = 'thk_django_admin/admin_captcha/login.html'
    # 配置顺序，ordering越小越靠前
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

# 实例化，用于注册admin与配置urls
test_project_admin_site = TestProjectAdminSite(name='test_project_admin_site')

```

### 2.2 配置urls.py

```python
from django.urls import path, include
from test_project.site import test_project_admin_site


urlpatterns = [
    path('admin/', test_project_admin_site.urls),
    path('captcha/', include('captcha.urls')),
]

```

### 2.3 使用

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
