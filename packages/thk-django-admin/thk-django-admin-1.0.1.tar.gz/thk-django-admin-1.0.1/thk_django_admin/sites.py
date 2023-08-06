# -*- coding: utf-8 -*-
import warnings

from django.contrib.admin.sites import AdminSite
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.contrib.auth.apps import AuthConfig
from django.contrib.auth.admin import GroupAdmin, Group, UserAdmin, User


_DEFAULT_ORDERING = 99999


class OrderedAdminSite(AdminSite):
    include_default_auth = True
    ordered_apps = list()
    _ordered_apps = dict()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.include_default_auth:
            self._include_default_auth()
        self._rebuild_ordered_apps()

    def _get_app_ordering(self, x_app: dict):
        app_info = self._ordered_apps.get(x_app['name'])
        if app_info is not None and app_info.get('ordering') is not None:
            return app_info['ordering']
        warnings.warn("APP: {name} not set ordering".format(name=x_app['name']))
        return _DEFAULT_ORDERING

    def _get_model_ordering_by_app(self, x_app: dict):
        app_info = self._ordered_apps.get(x_app['name'])
        if app_info is not None and app_info.get('models') is not None:
            models_ordering_mapping = app_info['models']
        else:
            models_ordering_mapping = None

        def _get_model_ordering(x_model):
            if models_ordering_mapping is not None and models_ordering_mapping.get(x_model['model']) is not None:
                return models_ordering_mapping[x_model['model']]
            warnings.warn("Model: {name} not set ordering".format(name=x_model['model']))
            return _DEFAULT_ORDERING
        return _get_model_ordering

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)
        app_dict_list = list(app_dict.values())

        # Modification: Sort by ordering.
        app_list = sorted(app_dict_list, key=self._get_app_ordering)

        # Modification: Sort by ordering.
        for app in app_list:
            app["models"].sort(key=self._get_model_ordering_by_app(app))

        return app_list

    def app_index(self, request, app_label, extra_context=None):
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404("The requested admin page does not exist.")
        # Modification: Sort by ordering.
        app_dict["models"].sort(key=self._get_model_ordering_by_app(app_dict))
        context = {
            **self.each_context(request),
            "title": _("%(app)s administration") % {"app": app_dict["name"]},
            "subtitle": None,
            "app_list": [app_dict],
            "app_label": app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(
            request,
            self.app_index_template
            or ["admin/%s/app_index.html" % app_label, "admin/app_index.html"],
            context,
        )

    def _include_default_auth(self):
        self.register(Group, GroupAdmin)
        self.register(User, UserAdmin)

        self.ordered_apps.append({
            'verbose_name': AuthConfig.verbose_name,
            'ordering': _DEFAULT_ORDERING,
            'models': [
                {'model': User, 'ordering': 0},
                {'model': Group, 'ordering': 1}
            ]
        })

    def _rebuild_ordered_apps(self):
        self._ordered_apps = dict()
        for app_dict in self.ordered_apps:

            md = dict()
            for model_dict in app_dict['models']:
                md[model_dict['model']] = model_dict['ordering']

            self._ordered_apps[app_dict['verbose_name']] = {
                'ordering': app_dict['ordering'],
                'models': md
            }
