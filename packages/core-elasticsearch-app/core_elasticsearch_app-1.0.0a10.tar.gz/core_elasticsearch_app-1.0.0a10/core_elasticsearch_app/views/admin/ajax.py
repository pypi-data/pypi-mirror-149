""" Elasticsearch Ajax
"""
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.urls import reverse_lazy

from core_elasticsearch_app.components.data.mongodb import get_exists_query_from_path
from core_elasticsearch_app.components.elasticsearch_template import (
    api as elasticsearch_template_api,
)
from core_elasticsearch_app.components.elasticsearch_template.models import (
    ElasticsearchTemplate,
)
from core_elasticsearch_app.tasks import index_all_data_from_template
from core_elasticsearch_app.views.admin.forms import ElasticsearchTemplateForm
from core_main_app.components.data import api as data_api
from core_main_app.views.common.ajax import (
    AddObjectModalView,
    DeleteObjectModalView,
    EditObjectModalView,
)


class AddElasticsearchTemplateView(AddObjectModalView):
    """AddElasticsearchTemplateView"""

    form_class = ElasticsearchTemplateForm
    document = ElasticsearchTemplate
    success_url = reverse_lazy("admin:core_elasticsearch_app_templates")
    success_message = "Template was successfully configured for Elasticsearch."

    def _save(self, form):
        # Save treatment.
        try:
            es_template = ElasticsearchTemplate(
                template=form.cleaned_data["template"],
                title_path=form.cleaned_data["title_path"],
                description_paths=form.cleaned_data["description_paths"],
            )
            elasticsearch_template_api.upsert(es_template)
        except Exception as e:
            form.add_error(None, str(e))

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddElasticsearchTemplateView, self).get_form_kwargs(
            *args, **kwargs
        )
        kwargs["request"] = self.request
        return kwargs


class EditElasticsearchTemplateView(EditObjectModalView):
    """EditElasticsearchTemplateView"""

    form_class = ElasticsearchTemplateForm
    document = ElasticsearchTemplate
    success_url = reverse_lazy("admin:core_elasticsearch_app_templates")
    success_message = "Template Configuration edited with success."

    def _save(self, form):
        # Save treatment.
        try:
            self.object.description_paths = form.cleaned_data["description_paths"]
            elasticsearch_template_api.upsert(self.object)
        except Exception as e:
            form.add_error(None, str(e))

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EditElasticsearchTemplateView, self).get_form_kwargs(
            *args, **kwargs
        )
        kwargs["request"] = self.request
        return kwargs


class DeleteElasticsearchTemplateView(DeleteObjectModalView):
    """DeleteElasticsearchTemplateView"""

    document = ElasticsearchTemplate
    success_url = reverse_lazy("admin:core_elasticsearch_app_templates")
    success_message = "Template Configuration deleted with success."

    def _delete(self, request, *args, **kwargs):
        # Delete treatment.
        elasticsearch_template_api.delete(self.object)

    def _get_object_name(self):
        return "the configuration using the template {0}".format(
            self.object.template.display_name
        )

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DeleteElasticsearchTemplateView, self).get_form_kwargs(
            *args, **kwargs
        )
        kwargs["request"] = self.request
        return kwargs


@staff_member_required
def check_data_from_template(request, pk):
    """Check if data found for provided xpaths

    Args:
        request:
        pk:

    Returns:

    """
    try:
        # Get elasticsearch configuration for the given template
        es_template = elasticsearch_template_api.get_by_id(pk)
        # Check if titles found with given path
        title_results = data_api.execute_query(
            query=get_exists_query_from_path(es_template.title_path), user=request.user
        )
        # Check if descriptions found with given path
        desc_count = 0
        for path in es_template.description_paths:
            description_results = data_api.execute_query(
                query=get_exists_query_from_path(path),
                user=request.user,
            )
            desc_count += description_results.count()
        message = (
            f"Title: {title_results.count()} data found. "
            f"Description: {desc_count} data fields found."
        )
    except Exception as e:
        message = str(e)

    return HttpResponse(json.dumps(message), content_type="application/javascript")


@staff_member_required
def index_data_from_template(request, pk):
    """Index all data from template

    Args:
        request:
        pk:

    Returns:

    """
    # Get elasticsearch configuration for the given template
    es_template = elasticsearch_template_api.get_by_id(pk)
    # Index all data for this template
    index_all_data_from_template.apply_async((str(es_template.template.id),))

    return HttpResponse(
        json.dumps("Indexing data..."), content_type="application/javascript"
    )
