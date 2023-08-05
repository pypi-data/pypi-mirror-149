core_module_auto_keyref_app
===========================

Auto Keyref module for the parser core project.

Quick start
===========

1. Add "core_module_auto_keyref_app" to your INSTALLED_APPS setting
-------------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_module_auto_keyref_app',
    ]

    PARSER_AUTO_KEY_KEYREF = True

2. Include the core_module_auto_keyref_app URLconf in your project urls.py
--------------------------------------------------------------------------

.. code:: python

    url(r'^', include('core_module_auto_keyref_app.urls')),