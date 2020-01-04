=========
Changelog
=========


0.5.8 (TBD)
===========

Changes
-------

TBA
=======
* Add Elasticsearch bucket script pipeline aggregator
* Added ability to hide metrics for Elasticsearch MetricAggs
* Add derivative metric aggregation for Elasticsearch
* Add ``Stat`` class (and ``StatMapping``, ``StatValueMapping``, ``StatRangeMapping``) to support the Stat panel
* Add ``Svg`` class to support the SVG panel
* Add ``PieChart`` class for creating Pie Chart panels
* Add `transparent` setting to classes that were missing it (Heatmap, PieChart)
* Add InfluxDB data source
* Add ``auto_ref_ids`` to ``Graph``s
* ...


0.5.7 (2020-05-11)
==================

Changes
-------

* Fix crasher instatiating elasticsearch panels.
* Remove unused ``tools/`` directory.

Thanks a lot for your contributions to this release, @DWalker487, @dholbach and @matthewmrichter.


0.5.6 (2020-05-05)
==================

Changes
-------

* Add ``Heatmap`` class (and ``HeatmapColor``) to support the Heatmap panel (#170)
* Add ``BarGuage`` for creating bar guages panels in grafana 6
* Add ``GuagePanel`` for creating guages in grafana 6
* Add data links support to ``Graph``, ``BarGuage``, and ``GuagePanel`` panels
* Removed gfdatasource - feature is built in to Grafana since v5.
* Generate API docs for readthedocs.org
* Fix AlertList panel generation
* Add both upper and lower case `"time"` pattern for time_series column format in Table class
* Drop testing of Python 2.7, it has been EOL'ed and CI was broken
  due to this.
* Automatically test documentation examples.
* Point to dev meeting resources.
* Add description attribute to Dashboard.
* Add support for custom variables.
* Point out documentation on readthedocs more clearly.
* Add average metric aggregation for elastic search
* Bugfix to query ordering in Elasticsearch TermsGroupBy
* Added all parameters for StringColumnStyle
* Add Elasticsearch Sum metric aggregator
* Add ``Statusmap`` class (and ``StatusmapColor``) to support the Statusmap panel plugin
* Bugfix to update default ``Threshold`` values for ``GaugePanel`` and ``BarGauge``
* Use Github Actions for CI.
* Fix test warnings.
* Update ``BarGauge`` and ``GaugePanel`` default Threshold values.
* Update release instructions.

Thanks a lot to the contributions from @DWalker487, @bboreham, @butlerx, @dholbach, @franzs, @jaychitalia95, @matthewmrichter and @number492 for this release!

0.5.5 (2020-02-17)
==================

It's been a while since the last release and we are happy to get this one into your hands.
0.5.5 is a maintenance release, most importantly it adds support for Python >= 3.5.

We are very delighted to welcome Matt Richter on board as maintainer.

Changes
-------

* Automate publishing to PyPI with GitHub Actions
* Update README.rst to make the example work
* Bump Dockerfile to use Alpine 3.10 as base
* Fix up ``load_source()`` call which doesn't exist in Python 3.5
* Update versions of Python tested
* Repair tests
* pin to attrs 19.2 and fix deprecated arguments

Many thanks to contributors @bboreham, @dholbach, @ducksecops, @kevingessner, @matthewmrichter, @uritau.

0.5.4 (2019-08-30)
==================

Changes
-------

* Add 'diff', 'percent_diff' and 'count_non_null' as RTYPE
* Support for changing sort value in Template Variables.
* Sort tooltips by value in Weave/Stacked-Charts
* Add ``for`` parameter for alerts on Grafana 6.X
* Add ``STATE_OK`` for alerts
* Add named values for the Template.hide parameter
* Add cardinality metric aggregator for ElasticSearch
* Add Threshold and Series Override types
* Add more YAxis formats

Many thanks to contributors @kevingessner, @2easy, @vicmarbev, @butlerx.

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
