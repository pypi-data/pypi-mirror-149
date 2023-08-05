""" Elasticsearch tasks
"""
import logging

from celery import shared_task

from core_elasticsearch_app.components.data import elasticsearch
from core_main_app.system import api as data_system_api

logger = logging.getLogger(__name__)


@shared_task
def index_all_data_from_template(template):
    """Index all data"""
    try:
        data = data_system_api.get_all_by_template(
            template=template, order_by_field=None
        )
        for document in data:
            try:
                elasticsearch.index_data(document)
            except Exception as e:
                logger.error(
                    f"ERROR : An error occurred while indexing data : {str(e)}"
                )
    except Exception as e:
        logger.error(f"ERROR : An error occurred while indexing data : {str(e)}")


@shared_task
def index_data(data_id):
    """Index a data"""
    try:
        data = data_system_api.get_data_by_id(data_id)
        try:
            elasticsearch.index_data(data)
        except Exception as e:
            logger.error(f"ERROR : An error occurred while indexing data : {str(e)}")
    except Exception as e:
        logger.error(f"ERROR : An error occurred while indexing data : {str(e)}")
