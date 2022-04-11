=========
Changelog
=========

x.x.x (TBC)
===========

* Added ...


0.6.3 (2022-03-30)
==================

* Added Azure Monitor Target
* Added ``legendCalcs`` parameter to TimeSeries Panel
* Added ``hide`` parameter to ElasticsearchTarget
* Added ExpressionTarget support for ElasticSearch data sources


0.6.2 (2022-02-24)
==================

* Added percentage type for thresholds
* Added ``datasource`` parameter to CloudWatch targets
* Added support for auto panels ids to AlertList panel
* Added ``SeriesOverride`` options (dashes and Z-index)
* Added support for fields value in Stat panel
* Added ``alertName`` parameter to AlertList panel
* Added ``thresholdsStyleMode`` parameter to TimeSeries panel
* Added Histogram panel support
* Dashboard upload script updated to support overwriting dashboards

0.6.1 (2021-11-23)
==================

* Added new SqlTarget to core to be able to define SQL queries as well
* Added missing attributes to the Logs panel
* Added Cloudwatch Logs Insights Target
* Added overrides to panels
* Extend ``SeriesOverride`` options

Changes
-------

* Fix Text panel (and add tests)

  **ATTENTION:** This might break panels generated for Grafana <8.0.6

0.6.0 (2021-10-26)
===================

* Added Discrete panel (https://grafana.com/grafana/plugins/natel-discrete-panel/)
* Added support for colors in stat mapping panel with StatValueMappings & StatRangeMappings
* Added missing auto interval properties in Template
* Added param to RowPanel to collapse the row
* Added StateTimeline panel which was added in Grafana v8
* Added support for timeseries panel added in Grafana v8
* Added MinMetricAgg and PercentilesMetricAgg to Elasticsearch
* Added support for News panel
* Added support for Pie Chart v2 from Grafana v8

Changes
-------

* Refine expectations of is_color_code
* Deprecated StatMapping, StatValueMapping & StatRangeMapping
* Change YAxis min value default from 0 to None
* Support for Table panel for Grafana v8 may have broken backwards compatibility in old Table panel
* Breaking change, support for styled columns in tables removed, no longer used in Grafana v8 new Table
* Move development to ``main`` branch on GitHub. If you have work tracking the ``master`` you will need to update this.

0.5.14 (2021-09-14)
==================

* Added colour overrides to pie chart panel
* Added missing attributes from xAxis class
* Added transformations for the Panel class (https://grafana.com/docs/grafana/next/panels/reference-transformation-functions/)
* Added Worldmap panel (https://grafana.com/grafana/plugins/grafana-worldmap-panel/)
* Added missing fill gradient to Graph panel
* Added missing align to graph panel
* Added missing show percentage attribute to Pie chart panel
* Added ``extraJson`` attribute to the Panel class for overriding the panel with raw JSON
* Added inline script support for Elasticsearch metrics
* Selected needs to be set as a bool value for templating to work.

0.5.13 (2021-05-17)
===================

* Added a test for the Alert class.

Changes
-------

* Bugfix: changed 'target' validator in AlertNotification to accept CloudwatchMetricsTarget
* Moved the alertRuleTag field from Graph to Alert.

0.5.12 (2021-04-24)
===================

* Added hide parameter to CloudwatchMetricsTarget class
* Added table-driven example dashboard and upload script

Changes
-------

* bugfix load_dashboard add support for old python version 2.x, 3.3 and 3.4
* Fix default target datasource to work with newer versions of Grafana
* Removed re-defined maxDataPoints field from multiple panels
* Fix the AlertList class and add a test for it

Thanks to all those who have contributed to this release.


0.5.11 (2021-04-06)
===================

* Added timeField field for the Elasticsearch target to allow the alert to change its state
* Added nameFilter field for the AlertList panel
* Added dashboardTags field for the AlertList panel

Thanks a lot for your contributions to this release, @dafna-starkware

0.5.10 (2021-03-21)
===================

* Added Logs panel (https://grafana.com/docs/grafana/latest/panels/visualizations/logs-panel/)
* Added Cloudwatch metrics datasource (https://grafana.com/docs/grafana/latest/datasources/cloudwatch/)
* Added option to hide dashboard time picker
* Added Notification for Alert
* Added alertRuleTags field to the graph panel
* Added support for thresholds to graph panel
* Added support for Elasticsearch alert condition
* Added support for using gridPos for dashboard panels
* Added support for Humio Data Source. (https://grafana.com/grafana/plugins/humio-datasource/)


Changes
-------

* Replace deprecated attr.assoc with attr.evolve



0.5.9 (2020-12-18)
==================

* Added Alert Threshold enabled/disabled to Graphs.
* Added constants for all Grafana value formats
* Added support for repetitions to Stat Panels
* Added textMode option to Stat Panels
* Add Panel object for all panels to inherit from
* Add Dashboard list panel (https://grafana.com/docs/grafana/latest/panels/visualizations/dashboard-list-panel/)


Changes
-------

* Change supported python versions from 3.6 to 3.9
* Added hide parameter to Target
* Updated dependencies (docs, build, CI)
* Consistent coding style


0.5.8 (2020-11-02)
==================

This release adds quite a few new classes to grafanalib, ElasticSearch support was improved and support for InfluxDB data sources was added.

We would also very much like to welcome James Gibson as new maintainer of grafanalib. Thanks a lot for stepping up to this role!

Changes
-------

* Added more YAxis formats, added Threshold and SeriesOverride types
* dataLinks support in graphs
* Add Elasticsearch bucket script pipeline aggregator
* Added ability to hide metrics for Elasticsearch MetricAggs
* Add derivative metric aggregation for Elasticsearch
* Add ``Stat`` class (and ``StatMapping``, ``StatValueMapping``, ``StatRangeMapping``) to support the Stat panel
* Add ``Svg`` class to support the SVG panel
* Add ``PieChart`` class for creating Pie Chart panels
* Add `transparent` setting to classes that were missing it (Heatmap, PieChart)
* Add InfluxDB data source
* Add ``auto_ref_ids`` to ``Graph``

Thanks a lot for your contributions to this release, @DWalker487, @JamesGibo, @daveworth, @dholbach, @fauust, @larsderidder, @matthewmrichter.


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
