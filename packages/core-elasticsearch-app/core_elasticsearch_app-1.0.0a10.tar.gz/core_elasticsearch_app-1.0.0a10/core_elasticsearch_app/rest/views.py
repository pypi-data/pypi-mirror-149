""" REST views for the elasticsearch package
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_elasticsearch_app.components.data.elasticsearch import get_suggestions
from core_elasticsearch_app.utils.utils import clean_keyword


class DocumentSuggestion(APIView):
    """Get document suggestions from keywords."""

    def get(self, request):
        """Get all Suggestions

        Url Parameters:

            keywords: keywords

        Examples:

            ../suggestions?keywords=[keywords]

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of suggestions
            - code: 500
              content: Internal server error
        """
        try:
            # Get objects
            keywords = self.request.query_params.get("keywords", [])
            if keywords:
                keywords = keywords.split(",")
            suggestions = get_suggestions(" ".join(keywords))
            return Response(suggestions, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class KeywordSuggestion(APIView):
    """Get Keyword suggestions from keywords."""

    def get(self, request):
        """Get all Suggestions

        Url Parameters:

            keywords: keywords

        Examples:

            ../suggestions?keywords=[keywords]

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of keywords
            - code: 400
              content: Bad Request
            - code: 500
              content: Internal server error
        """
        try:
            # Get keyword parameter
            keyword = self.request.query_params.get("keyword", None)
            if keyword:
                # get suggestions from elasticsearch
                suggestions = get_suggestions(keyword, fragment_size=1)
                # build a list of formatted keywords
                suggestions = [
                    clean_keyword(s["highlight"]["description"][0])
                    for s in suggestions
                    if "description" in s["highlight"]
                ]
                # get list of unique keywords
                suggestions = set(suggestions)
                return Response(suggestions, status=status.HTTP_200_OK)
            else:
                content = {"message": "Keyword parameter is missing"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
