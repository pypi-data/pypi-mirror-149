======================
Core Elasticsearch App
======================

Elasticsearch utils for the curator core project.

Quick start
===========

1. Add "core_elasticsearch_app" to your INSTALLED_APPS setting
--------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_elasticsearch_app',
    ]

The package should be placed above `core_explore_keyword_app` in the `INSTALLED_APPS` to enable autocomplete powered
by elasticsearch.

2. Include the core_elasticsearch_app URLconf in your project urls.py
---------------------------------------------------------------------

.. code:: python

    re_path(r'^elasticsearch/', include('core_elasticsearch_app.urls')),


3. Deploy an instance of Elasticsearch
--------------------------------------

Recommended version: 7.14.1
See https://github.com/usnistgov/cdcs-docker#elasticsearch for help with Elasticsearch deployment.

4. Configure what should be indexed in Elasticsearch
----------------------------------------------------

It is recommended to configure the mapping between the CDCS templates and the Elasticsearch indices before starting to
insert data, so that data can be indexed as soon as they are published in the CDCS. For that, set the following setting:

.. code:: python

    ELASTICSEARCH_AUTO_INDEX = True

Then, configure the mapping between the XSD templates and the Elasticsearch indices. Documents stored in Elasticsearch
have a common structure. They are composed of a `data_id`, a `title` and a `description` field. A mapping can be
defined to tell where in the XML data the values for the `title` and for the `description` of a resource can be found.
Below is an example to set this mapping via REST, for a given template:

.. code:: python

    import requests
    payload = {
        "template": "5f43ba192b8fd5c092e30e62",
        "title_path": "Resource/identity/title",
        "description_paths": ["Resource/content/description", "Resource/content/subject"],
    }

    requests.post(
        SERVER_URI + "/elasticsearch/rest/elasticsearch_template/", data=payload, auth=(USER, PASSWORD)
    )