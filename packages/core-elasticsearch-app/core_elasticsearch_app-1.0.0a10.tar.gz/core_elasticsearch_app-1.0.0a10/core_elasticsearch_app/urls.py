""" Url router for the core elasticsearch app
"""
from django.conf.urls import url, include


urlpatterns = [
    url(r"rest/", include("core_elasticsearch_app.rest.urls")),
]
