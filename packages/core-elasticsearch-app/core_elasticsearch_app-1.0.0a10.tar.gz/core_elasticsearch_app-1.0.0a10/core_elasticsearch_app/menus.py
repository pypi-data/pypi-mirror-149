""" Elasticsearch menu
"""
from django.urls import reverse
from menu import Menu, MenuItem


elasticsearch_children = (
    MenuItem(
        "Configure Templates",
        reverse("admin:core_elasticsearch_app_templates"),
        icon="list",
    ),
)

Menu.add_item("admin", MenuItem("ELASTICSEARCH", None, children=elasticsearch_children))
