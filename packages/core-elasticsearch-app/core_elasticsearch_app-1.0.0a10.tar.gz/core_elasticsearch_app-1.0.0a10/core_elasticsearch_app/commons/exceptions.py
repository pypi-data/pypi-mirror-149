""" Elasticsearch Exceptions
"""


class ElasticsearchError(Exception):
    """Exception raised by the Elasctisearch app."""

    def __init__(self, message):
        self.message = message
