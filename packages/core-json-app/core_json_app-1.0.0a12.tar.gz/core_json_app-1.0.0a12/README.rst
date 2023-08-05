=============
Core JSON App
=============

Add JSON support to the curator core project.

Quick start
===========

1. Add "core_json_app" to your INSTALLED_APPS setting
-----------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_json_app',
    ]

2. Include the core_json_app URLconf in your project urls.py
------------------------------------------------------------

.. code:: python

    re_path(r'^', include('core_json_app.urls')),
    re_path(r'^', include("core_main_app.urls")),

Url for core_json_app should be placed above core_main_app.