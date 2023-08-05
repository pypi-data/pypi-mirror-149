""" Utils for the elasticsearch package
"""

import re
from functools import reduce


def clean_keyword(keyword):
    """Remove extra characters and format keyword

    Args:
        keyword:

    Returns:

    """
    # lowercase
    keyword = keyword.lower()

    # remove extra characters
    regex = re.compile("<em>.*</em>")
    keyword = re.search(regex, keyword).group()

    # remove highlight tags
    keyword = keyword.replace("<em>", "").replace("</em>", "")

    return keyword


def get_nested_value(dictionary, keys, default=None):
    """Get value in nested dictionary

    From https://stackoverflow.com/a/46890853

    Args:
        dictionary:
        keys:
        default:

    Returns:

    """
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("/"),
        dictionary,
    )
