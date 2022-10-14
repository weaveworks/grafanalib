===============================
Getting Started with grafanalib
===============================

Do you like `Grafana <http://grafana.org/>`_ but wish you could version your
dashboard configuration? Do you find yourself repeating common patterns? If
so, grafanalib is for you.

grafanalib lets you generate Grafana dashboards from simple Python scripts.

Grafana migrates dashboards to the latest Grafana schema version on import,
meaning that dashboards created with grafanalib are supported by
all versions of Grafana. You may find that some of the latest features are
missing from grafanalib, please refer to the `module documentation
<https://grafanalib.readthedocs.io/en/latest/api/modules.html>`_ for information
about supported features. If you find a missing feature please raise an issue
or submit a PR to the GitHub `repository <https://github.com/weaveworks/grafanalib>`_

Writing dashboards
==================

The following will configure a dashboard with a couple of example panels that
use the random walk and Prometheus datasources.

.. literalinclude:: ../grafanalib/tests/examples/example.dashboard.py
   :language: python

There is a fair bit of repetition here, but once you figure out what works for
your needs, you can factor that out.
See `our Weave-specific customizations
<https://github.com/weaveworks/grafanalib/blob/main/grafanalib/weave.py>`_
for inspiration.

Generating dashboards
=====================

If you save the above as ``example.dashboard.py`` (the suffix must be
``.dashboard.py``), you can then generate the JSON dashboard with:

.. code-block:: console

  $ generate-dashboard -o frontend.json example.dashboard.py

Uploading dashboards from code
===============================

Sometimes you may need to generate and upload dashboard directly from Python
code. The following example provides minimal code boilerplate for it:

.. literalinclude:: ../grafanalib/tests/examples/example.upload-dashboard.py
   :language: python

Writing Alerts
==================

The following will configure a couple of alerts inside a group.

.. literalinclude:: ../grafanalib/tests/examples/example.alertgroup.py
   :language: python

Although this example has a fair amount of boilerplate, when creating large numbers
of similar alerts it can save lots of time to programatically fill these fields.

Each ``AlertGroup`` represents a folder within Grafana's alerts tab. This consists
of one or more ``AlertRule``, which contains one or more triggers. Triggers define
what will cause the alert to fire.

A trigger is made up of a ``Target`` (a Grafana query on a datasource) and an
`AlertCondition` (a condition this query must satisfy in order to alert).

Finally, there are additional settings like:

* How the alert will behave when data sources have problems (``noDataAlertState`` and ``errorAlertState``)

* How frequently the trigger is evaluated (``evaluateInterval``)

* How long the AlertCondition needs to be met before the alert fires (``evaluateFor``)

* Annotations and labels, which help provide contextual information and direct where
  your alerts will go

Generating Alerts
=====================

If you save the above as ``example.alertgroup.py`` (the suffix must be
``.alertgroup.py``), you can then generate the JSON dashboard with:

.. code-block:: console

  $ generate-alertgroups -o alerts.json example.alertgroup.py

Uploading alerts from code
===============================

As Grafana does not currently have a user interface for importing alertgroup JSON,
you must upload the alerts via Grafana's REST API.

The following example provides minimal code boilerplate for it:

.. literalinclude:: ../grafanalib/tests/examples/example.upload-alerts.py
   :language: python

Installation
============

grafanalib is just a Python package, so:

.. code-block:: console

  $ pip install grafanalib

Support
=======

This library is in its very early stages. We'll probably make changes that
break backwards compatibility, although we'll try hard not to.

grafanalib works with Python 3.6, 3.7, 3.8 and 3.9.

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
