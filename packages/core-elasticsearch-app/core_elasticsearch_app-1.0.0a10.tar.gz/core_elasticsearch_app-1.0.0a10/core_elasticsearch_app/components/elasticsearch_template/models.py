""" ElasticsearchTemplate model
"""
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors
from mongoengine.queryset.base import CASCADE

from core_explore_keyword_app.components.search_operator.models import (
    validate_xpath_list,
)
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template


class ElasticsearchTemplate(Document):
    """ElasticsearchTemplate object"""

    template = fields.ReferenceField(
        Template, blank=False, reverse_delete_rule=CASCADE, unique=True
    )
    title_path = fields.StringField(default=None)
    description_paths = fields.ListField(
        blank=False, validation=validate_xpath_list, default=[]
    )

    @staticmethod
    def get_by_id(es_template_id):
        """Returns the object with a given id

        Args:
            es_template_id:

        Returns:
            ElasticsearchTemplate (obj): ElasticsearchTemplate

        """
        try:
            return ElasticsearchTemplate.objects.get(pk=es_template_id)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_by_template(template):
        """Returns the object with a given template

        Args:
            template:

        Returns:
            ElasticsearchTemplate (obj): ElasticsearchTemplate

        """
        try:
            return ElasticsearchTemplate.objects.get(template=template)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_all():
        """Returns all objects"""
        return ElasticsearchTemplate.objects.all()
