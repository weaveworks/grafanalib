=========
Changelog
=========

Next release
=======

Changes
-------

TBA

0.5.4 (2019-07-3)
=======

Changes
-------

* Add 'diff', 'percent_diff' and 'count_non_null' as RTYPE
* Support for changing sort value in Template Variables.
* Sort tooltips by value in Weave/Stacked-Charts
* Add ``for`` parameter for alerts on Grafana 6.X
* Add named values for the Template.hide parameter

0.5.3 (2018-07-19)
==================

Changes
-------

* Minor markup tweaks to the README

0.5.2 (2018-07-19)
==================

Fixes
-----

* ``PromGraph`` was losing all its legends. It doesn't any more. (`#130`_)

.. _`#130`: https://github.com/weaveworks/grafanalib/pull/130

Changes
-------

* Add ``AlertList`` panel support
* Add support for mixed data sources
* Add ``ExternalLink`` class for dashboard-level links to other pages
* Template now supports 'type' and 'hide' attributes
* Legend now supports ``sort`` and ``sortDesc`` attributes
* Tables now support ``timeFrom`` attribute
* Update README.rst with information on how to get help.


0.5.1 (2018-02-27)
==================

Fixes
-----

* Fix for crasher bug that broke ``SingleStat``, introduced by `#114`_

.. _`#114`: https://github.com/weaveworks/grafanalib/pull/114


0.5.0 (2018-02-26)
==================

New features
------------

* grafanalib now supports Python 2.7. This enables it to be used within `Bazel <https://bazel.build>`_.
* Partial support for graphs against Elasticsearch datasources (https://github.com/weaveworks/grafanalib/pull/99)

Extensions
----------

* Constants for days, hours, and minutes (https://github.com/weaveworks/grafanalib/pull/98)
* Groups and tags can now be used with templates (https://github.com/weaveworks/grafanalib/pull/97)


0.4.0 (2017-11-23)
==================

Massive release!

It's Thanksgiving today, so more than ever I want to express my gratitude to
all the people who have contributed to this release!

* @aknuds1
* @atopuzov
* @bboreham
* @fho
* @filippog
* @gaelL
* @lalinsky
* @leth
* @lexfrei
* @mikebryant

New features
------------

* Support for ``Text`` panels
  (https://github.com/weaveworks/grafanalib/pull/63)
* ``PromGraph`` is now more powerful.
  If you want to pass extra parameters like ``intervalFactor`` to your
  targets, you can do so by listing targets as dictionaries,
  rather than tuples.
  (https://github.com/weaveworks/grafanalib/pull/66)
* Support for absolute links to drill-down in graphs
  (https://github.com/weaveworks/grafanalib/pull/86)

Changes
-------

* Breaking change to ``weave.QPSGraph()`` - added ``data_source``
  parameter and removed old hard-coded setting.
  (https://github.com/weaveworks/grafanalib/pull/77)

Extensions
----------

Generally adding more parameters to existing things:

* Graphs can now have descriptions or be transparent
  (https://github.com/weaveworks/grafanalib/pull/62 https://github.com/weaveworks/grafanalib/pull/89)
* New formats: "bps" and "Bps"
  (https://github.com/weaveworks/grafanalib/pull/68)
* Specify the "Min step" for a ``Target``
  using the ``interval`` attribute.
* Specify the number of decimals shown on the ``YAxis``
  with the ``decimals`` attribute
* Specify multiple ``Dashboard`` inputs,
  allowing dashboards to be parametrized by data source.
  (https://github.com/weaveworks/grafanalib/pull/83)
* Templates
  * ``label`` is now optional (https://github.com/weaveworks/grafanalib/pull/92)
  * ``allValue`` and ``includeAll`` attributes now available (https://github.com/weaveworks/grafanalib/pull/67)
  * ``regex`` and ``multi`` attributes now available (https://github.com/weaveworks/grafanalib/pull/82)
* Rows can now repeat (https://github.com/weaveworks/grafanalib/pull/82)
* Add missing ``NULL_AS_NULL`` constant
* Specify the "Instant" for a ``Target`` using the ``instant`` attribute.

Fixes
-----

* The ``showTitle`` parameter in ``Row`` is now respected
  (https://github.com/weaveworks/grafanalib/pull/80)



0.3.0 (2017-07-27)
==================

New features
------------

* OpenTSDB datasource support (https://github.com/weaveworks/grafanalib/pull/27)
* Grafana Zabbix plugin support
  (https://github.com/weaveworks/grafanalib/pull/31, https://github.com/weaveworks/grafanalib/pull/36)
* ``Dashboard`` objects now have an ``auto_panel_id`` method which will
  automatically supply unique panel (i.e. graph) IDs for any panels that don't
  have one set. Dashboard config files no longer need to track their own
  ``GRAPH_ID`` counter.
* Support for ``SingleStat`` panels
  (https://github.com/weaveworks/grafanalib/pull/22)
* ``single_y_axis`` helper for the common case of a graph that has only one Y axis

Improvements
------------

* ``PromGraph`` now lives in ``grafanalib.prometheus``, and takes a
  ``data_source`` parameter
* Additional fields for ``Legend``  (https://github.com/weaveworks/grafanalib/pull/25)
* Additional fields for ``XAxis``
  (https://github.com/weaveworks/grafanalib/pull/28)
* Get an error when you specify the wrong number of Y axes

Changes
-------

* New ``YAxes`` type for specifying Y axes. Using a list of two ``YAxis``
  objects is deprecated.


0.1.2 (2017-01-02)
==================

* Add support for Grafana Templates (https://github.com/weaveworks/grafanalib/pull/9)

0.1.1 (2016-12-02)
==================

* Include README on PyPI page

0.1.0 (2016-12-02)
==================

Initial release.
