""" Settings for core_elasticsearch_app.

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

ELASTICSEARCH_HOST = getattr(settings, "ELASTICSEARCH_HOST", "localhost")
""" :py:class:`str`: Elasticsearch host
"""

ELASTICSEARCH_PORT = getattr(settings, "ELASTICSEARCH_PORT", 9200)
""" :py:class:`int`: Elasticsearch port
"""

CAN_SET_PUBLIC_DATA_TO_PRIVATE = getattr(
    settings, "CAN_SET_PUBLIC_DATA_TO_PRIVATE", False
)
""" :py:class:`boolean`: True if public data can be unpublished
"""

CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = getattr(
    settings, "CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT", False
)
""" :py:class:`bool`: Can anonymous user access public document.
"""

ELASTICSEARCH_CDCS_DATA_INDEX = getattr(
    settings, "ELASTICSEARCH_CDCS_DATA_INDEX", "cdcs-data"
)
""" :py:class:`str`: Name of the Elasticsearch index for CDCS data
"""

ELASTICSEARCH_AUTO_INDEX = getattr(settings, "ELASTICSEARCH_AUTO_INDEX", True)
""" :py:class:`boolean`: True if data should be automatically indexed in Elasticsearch
"""
