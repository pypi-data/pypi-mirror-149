""" Admin views Core Elasticsearch Search App
"""
from django.views.generic import View

from core_elasticsearch_app.components.elasticsearch_template import (
    api as elasticsearch_template_api,
)
from core_main_app.utils.rendering import admin_render
from core_main_app.views.common.ajax import (
    AddObjectModalView,
    DeleteObjectModalView,
    EditObjectModalView,
)


class TemplatesView(View):
    def get(self, request, *args, **kwargs):
        """Configure templates, Display as list.

        Args:
            request:

        Returns:

        """
        context = {
            "object_name": "Template Configuration",
            "es_template_list": elasticsearch_template_api.get_all(),
        }

        modals = [
            DeleteObjectModalView.get_modal_html_path(),
            AddObjectModalView.get_modal_html_path(),
            EditObjectModalView.get_modal_html_path(),
        ]

        assets = {
            "js": [
                {
                    "path": "core_elasticsearch_app/js/admin/es_template.js",
                    "is_raw": False,
                },
                DeleteObjectModalView.get_modal_js_path(),
                AddObjectModalView.get_modal_js_path(),
                EditObjectModalView.get_modal_js_path(),
            ]
        }

        return admin_render(
            request,
            "core_elasticsearch_app/admin/templates/list_templates.html",
            assets=assets,
            context=context,
            modals=modals,
        )
