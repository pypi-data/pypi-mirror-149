==========
Blob utils
==========

File management utils for the curator core project.

Quick start
===========

1. Add "blob_utils" to your INSTALLED_APPS setting
--------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
        ...
        'blob_utils',
    ]

Tests
=====

Since GridFS cannot be mocked, this set of test has to be run on a live database. The following steps guide you through
the process:

* Setup and start a MongoDB instance
* Set MONGODB_URI in tests/test_settings.py
* Run the tests with :code:`python runtests.py`