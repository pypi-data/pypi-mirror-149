""" ElasticsearchTemplate api
"""
from core_elasticsearch_app.components.elasticsearch_template.models import (
    ElasticsearchTemplate,
)


def upsert(elasticsearch_template):
    """Save or Update Elasticsearch Template

    Args:
        elasticsearch_template:

    Returns:

    """
    elasticsearch_template.save()


def delete(elasticsearch_template):
    """Delete Elasticsearch Template

    Args:
        elasticsearch_template:

    Returns:

    """
    elasticsearch_template.delete()


def get_by_template(template):
    """Get Elasticsearch Template

    Args:
        template:

    Returns:

    """
    return ElasticsearchTemplate.get_by_template(template)


def get_all():
    """Get all Elasticsearch Template

    Returns:

    """
    return ElasticsearchTemplate.get_all()


def get_by_id(es_template_id):
    """Get Elasticsearch Template by id

    Args:
        es_template_id:


    Returns:

    """
    return ElasticsearchTemplate.get_by_id(es_template_id)
