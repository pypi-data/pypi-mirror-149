""" Serializers used for the elasticsearch template REST API.
"""
from rest_framework_mongoengine.serializers import DocumentSerializer

from core_elasticsearch_app.components.elasticsearch_template import (
    api as elasticsearch_template_api,
)
from core_elasticsearch_app.components.elasticsearch_template.models import (
    ElasticsearchTemplate,
)


class ElasticsearchTemplateSerializer(DocumentSerializer):
    """ElasticsearchTemplate serializer"""

    class Meta(object):
        model = ElasticsearchTemplate
        fields = ["id", "template", "title_path", "description_paths"]
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Create and return a new `ElasticsearchTemplate` instance, given the validated data."""
        # Create instance from the validated data and insert it in DB
        instance = ElasticsearchTemplate(
            template=validated_data["template"],
            title_path=validated_data["title_path"],
            description_paths=validated_data["description_paths"],
        )
        elasticsearch_template_api.upsert(instance)

        return instance
