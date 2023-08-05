""" Watchers for the data collection
"""

from core_elasticsearch_app.settings import ELASTICSEARCH_AUTO_INDEX
from core_elasticsearch_app.tasks import index_data
from core_main_app.components.data.models import Data
from signals_utils.signals.mongo import connector, signals


def post_save_data(sender, document, **kwargs):
    """Method executed after a saving of a Data object.
    Args:
        sender: Class.
        document: Data document.
        **kwargs: Args.

    """
    # only deal with data in a workspace
    if not document.workspace:
        return

    # only deal with public data
    from core_main_app.components.workspace import api as workspace_api

    public_workspaces = workspace_api.get_all_public_workspaces().values_list("id")
    if document.workspace.id not in public_workspaces:
        return

    # Creates or updates a document in the index.
    index_data.apply_async((str(document.id),))


def init():
    """Connect to Data object events."""
    if ELASTICSEARCH_AUTO_INDEX:
        connector.connect(post_save_data, signals.post_save, Data)
