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
<https://grafanalib.readthedocs.io/en/main/api/modules.html>`_ for information
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

Alternatively Grafana supports file based provisioning, where dashboard files
are periodically loaded into the Grafana database. Tools like Anisble can
assist with the deployment.

Writing Alerts
==============

Between Grafana versions there have been significant changes in how alerts
are managed. Bellow are some example of how to configure alerting in
Grafana v8 and Grafana v9.

Alerts in Grafana v8
--------------------

The following will configure a couple of alerts inside a group.

.. literalinclude:: ../grafanalib/tests/examples/example.alertsv8.alertgroup.py
   :language: python

Although this example has a fair amount of boilerplate, when creating large numbers
of similar alerts it can save lots of time to programmatically fill these fields.

Each ``AlertGroup`` represents a folder within Grafana's alerts tab. This consists
of one or more ``AlertRulev8``, which contains one or more triggers. Triggers define
what will cause the alert to fire.

A trigger is made up of a ``Target`` (a Grafana query on a datasource) and an
``AlertCondition`` (a condition this query must satisfy in order to alert).

Finally, there are additional settings like:

* How the alert will behave when data sources have problems (``noDataAlertState`` and ``errorAlertState``)

* How frequently the trigger is evaluated (``evaluateInterval``)

* How long the AlertCondition needs to be met before the alert fires (``evaluateFor``)

* Annotations and labels, which help provide contextual information and direct where
  your alerts will go

Alerts in Grafana v9
--------------------

The following will configure a couple of alerts inside a group for Grafana v9.x+.

.. literalinclude:: ../grafanalib/tests/examples/example.alertsv9.alertgroup.py
   :language: python

Although this example has a fair amount of boilerplate, when creating large numbers
of similar alerts it can save lots of time to programmatically fill these fields.

Each ``AlertGroup`` represents a folder within Grafana's alerts tab. This consists
of one or more ``AlertRulev9``, which contains a list of triggers, that define what
will cause the alert to fire.

A trigger can either be a ``Target`` (a Grafana query on a datasource) or an
``AlertExpression`` (a expression performed on one of the triggers).

An ``AlertExpression`` can be one of 4 types

* Classic - Contains and list of ``AlertCondition``'s that are evaluated
* Reduce - Reduce the queried data
* Resample - Resample the queried data
* Math - Expression with the condition for the rule

Finally, there are additional settings like:

* How the alert will behave when data sources have problems (``noDataAlertState`` and ``errorAlertState``)

* How frequently the each rule in the Alert Group is evaluated (``evaluateInterval``)

* How long the AlertCondition needs to be met before the alert fires (``evaluateFor``)

* Annotations and labels, which help provide contextual information and direct where
  your alerts will go


Generating Alerts
=================

If you save either of the above examples for Grafana v8 or v9 as ``example.alertgroup.py``
(the suffix must be ``.alertgroup.py``), you can then generate the JSON alert with:

.. code-block:: console

  $ generate-alertgroup -o alerts.json example.alertgroup.py

Uploading alerts from code
==========================

As Grafana does not currently have a user interface for importing alertgroup JSON,
you must either upload the alerts via Grafana's REST API or use file based provisioning.

Uploading alerts from code using REST API
-----------------------------------------

The following example provides minimal code boilerplate for it:

.. literalinclude:: ../grafanalib/tests/examples/example.upload-alerts.py
   :language: python

Uploading alerts from code using File Based Provisioning
--------------------------------------------------------

The alternative to using Grafana's REST API is to use its file based provisioning for
alerting.

The following example uses the ``AlertFileBasedProvisioning`` class to provision a list
of alert groups:

.. literalinclude:: ../grafanalib/tests/examples/example.alertsv9.alertfilebasedprovisioning.py
   :language: python

Save the above example as ``example.alertfilebasedprovisioning.py``
(the suffix must be ``.alertfilebasedprovisioning.py``), you can then generate the JSON alert with:

.. code-block:: console

  $ generate-alertgroup -o alerts.json example.alertfilebasedprovisioning.py

Then place the file in the ``provisioning/alerting`` directory and start Grafana
Tools like Anisble can assist with the deployment of the alert file.

Installation
============

grafanalib is just a Python package, so:

.. code-block:: console

  $ pip install grafanalib

Support
=======

This library is in its very early stages. We'll probably make changes that
break backwards compatibility, although we'll try hard not to.

grafanalib works with Python 3.7, 3.8, 3.9, 3.10 and 3.11.

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
