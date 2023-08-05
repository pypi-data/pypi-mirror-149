""" Url router for the core elasticsearch app
"""
from django.urls import re_path

from core_elasticsearch_app.rest.elasticsearch_template.views import (
    ElasticsearchTemplateList,
)
from core_elasticsearch_app.rest.views import DocumentSuggestion, KeywordSuggestion

urlpatterns = [
    re_path(
        r"^elasticsearch_template/$",
        ElasticsearchTemplateList.as_view(),
        name="core_elasticsearch_app_rest_elasticsearch_template_list",
    ),
    re_path(
        r"^document/suggest",
        DocumentSuggestion.as_view(),
        name="core_elasticsearch_document_suggestion_view",
    ),
    re_path(
        r"^keyword/suggest",
        KeywordSuggestion.as_view(),
        name="core_elasticsearch_keyword_suggestion_view",
    ),
]
