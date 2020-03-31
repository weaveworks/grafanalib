===============================
Getting Started with grafanalib
===============================

.. image:: https://circleci.com/gh/weaveworks/grafanalib.svg?style=shield
    :target: https://circleci.com/gh/weaveworks/grafanalib

Do you like `Grafana <http://grafana.org/>`_ but wish you could version your
dashboard configuration? Do you find yourself repeating common patterns? If
so, grafanalib is for you.

grafanalib lets you generate Grafana dashboards from simple Python scripts.

Writing dashboards
==================

The following will configure a dashboard with a single row, with one QPS graph
broken down by status code and another latency graph showing median and 99th
percentile latency:

.. literalinclude:: ../grafanalib/tests/examples/example.dashboard.py
   :language: python

There is a fair bit of repetition here, but once you figure out what works for
your needs, you can factor that out.
See `our Weave-specific customizations
<https://github.com/weaveworks/grafanalib/blob/master/grafanalib/weave.py>`_
for inspiration.

Generating dashboards
=====================

If you save the above as ``frontend.dashboard.py`` (the suffix must be
``.dashboard.py``), you can then generate the JSON dashboard with:

.. code-block:: console

  $ generate-dashboard -o frontend.json frontend.dashboard.py

Installation
============

grafanalib is just a Python package, so:

.. code-block:: console

  $ pip install grafanalib

Support
=======

This library is in its very early stages. We'll probably make changes that
break backwards compatibility, although we'll try hard not to.

grafanalib works with Python 3.4, 3.5, 3.6 and 3.7.

Developing
==========
If you're working on the project, and need to build from source, it's done as follows:

.. code-block:: console

  $ virtualenv .env
  $ . ./.env/bin/activate
  $ pip install -e .

Configuring Grafana Datasources
===============================

This repo used to contain a program ``gfdatasource`` for configuring
Grafana data sources, but it has been retired since Grafana now has a
built-in way to do it.  See https://grafana.com/docs/administration/provisioning/#datasources
