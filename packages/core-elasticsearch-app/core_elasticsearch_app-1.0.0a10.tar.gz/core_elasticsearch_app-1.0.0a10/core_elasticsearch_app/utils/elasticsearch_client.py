""" Elasticsearch client for the CDCS
"""
from elasticsearch import Elasticsearch

from core_elasticsearch_app.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT


class ElasticsearchClient(object):
    """Elasticsearch client"""

    _es = None

    @classmethod
    def es(cls):
        """Return Elasticsearch connection
        Returns:
        """
        if cls._es is None:
            cls._es = Elasticsearch(
                [{"host": ELASTICSEARCH_HOST, "port": ELASTICSEARCH_PORT}]
            )
        return cls._es

    @classmethod
    def delete_index(cls, index_name):
        return cls.es().indices.delete(index=index_name, ignore=[400, 404])

    @classmethod
    def create_index(cls, index_name, settings=None):
        return cls.es().indices.create(index=index_name, body=settings, ignore=400)

    @classmethod
    def index_document(cls, index_name, document_id, document):
        return cls.es().index(index=index_name, id=document_id, body=document)

    @classmethod
    def delete_document(cls, index_name, document_id):
        return cls.es().delete(index=index_name, id=document_id)

    @classmethod
    def update_document(cls, index_name, document_id, document):
        return cls.es().update(index=index_name, id=document_id, body=document)

    @classmethod
    def search(cls, index_name, query):
        return cls.es().search(index=index_name, body=query)
