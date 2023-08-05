""" REST views for the elasticsearch template.
"""
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core_elasticsearch_app.components.elasticsearch_template import (
    api as elasticsearch_template_api,
)
from core_elasticsearch_app.rest.elasticsearch_template.serializers import (
    ElasticsearchTemplateSerializer,
)
from core_main_app.commons import exceptions
from core_main_app.utils.decorators import api_staff_member_required


class ElasticsearchTemplateList(APIView):
    """List elasticsearch template configuration"""

    @method_decorator(api_staff_member_required())
    def get(self, request):
        """Get all elasticsearch template configuration

        Args:
            request: HTTP request

        Returns:

            - code: 200
              content: List of elasticsearch template configurations
            - code: 500
              content: Internal server error
        """
        try:
            object_list = elasticsearch_template_api.get_all()

            # Serialize object
            serializer = ElasticsearchTemplateSerializer(object_list, many=True)

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def post(self, request):
        """Create an elasticsearch template configuration

        Parameters:
            {
                "template": "template_id",
                "title_path": "/x/path/title",
                "description_paths": ["/x/path/desc_one", "/x/path/desc_two"],
            }

        Args:
            request: HTTP request

        Returns:

            - code: 201
              content: Created elasticsearch template
            - code: 400
              content: Validation error / not unique / model error
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            serializer = ElasticsearchTemplateSerializer(data=request.data)

            # Validate data
            serializer.is_valid(True)

            # Save data
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.ModelError as model_exception:
            content = {"message": str(model_exception)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.NotUniqueError as not_unique_error:
            content = {"message": str(not_unique_error)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.ApiError as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
