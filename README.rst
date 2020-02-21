==========
grafanalib
==========

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

.. code-block:: python

  from grafanalib.core import *


  dashboard = Dashboard(
    title="Frontend Stats",
    rows=[
      Row(panels=[
        Graph(
          title="Frontend QPS",
          dataSource='My Prometheus',
          targets=[
            Target(
              expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"1.."}[1m]))',
              legendFormat="1xx",
              refId='A',
            ),
            Target(
              expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"2.."}[1m]))',
              legendFormat="2xx",
              refId='B',
            ),
            Target(
              expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"3.."}[1m]))',
              legendFormat="3xx",
              refId='C',
            ),
            Target(
              expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"4.."}[1m]))',
              legendFormat="4xx",
              refId='D',
            ),
            Target(
              expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"5.."}[1m]))',
              legendFormat="5xx",
              refId='E',
            ),
          ],
          yAxes=YAxes(
            YAxis(format=OPS_FORMAT),
            YAxis(format=SHORT_FORMAT),
          ),
          alert=Alert(
            name="Too many 500s on Nginx",
            message="More than 5 QPS of 500s on Nginx for 5 minutes",
            alertConditions=[
              AlertCondition(
                Target(
                  expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"5.."}[1m]))',
                  legendFormat="5xx",
                  refId='A',
                ),
                timeRange=TimeRange("5m", "now"),
                evaluator=GreaterThan(5),
                operator=OP_AND,
                reducerType=RTYPE_SUM,
              ),
            ],
          )
        ),
        Graph(
          title="Frontend latency",
          dataSource='My Prometheus',
          targets=[
            Target(
              expr='histogram_quantile(0.5, sum(irate(nginx_http_request_duration_seconds_bucket{job="default/frontend"}[1m])) by (le))',
              legendFormat="0.5 quantile",
              refId='A',
            ),
            Target(
              expr='histogram_quantile(0.99, sum(irate(nginx_http_request_duration_seconds_bucket{job="default/frontend"}[1m])) by (le))',
              legendFormat="0.99 quantile",
              refId='B',
            ),
          ],
          yAxes=single_y_axis(format=SECONDS_FORMAT),
        ),
      ]),
    ],
  ).auto_panel_ids()

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

grafanalib works with Python 2.7, 3.4, 3.5, 3.6 and 3.7.

Developing
==========
If you're working on the project, and need to build from source, it's done as follows:

.. code-block:: console

  $ virtualenv .env
  $ . ./.env/bin/activate
  $ pip install -e .

Configuring Grafana Datasources
===============================

This repo used to contain a program `gfdatasource` for configuring
Grafana data sources, but it has been retired since Grafana now has a
built-in way to do it.  See https://grafana.com/docs/administration/provisioning/#datasources

Getting Help
============

If you have any questions about, feedback for or problems with ``grafanalib``:

- Invite yourself to the `Weave Users Slack <https://slack.weave.works/>`_.
- Ask a question on the `#grafanalib <https://weave-community.slack.com/messages/grafanalib/>`_ slack channel.
- `File an issue <https://github.com/weaveworks/grafanalib/issues/new>`_.

Your feedback is always welcome!
