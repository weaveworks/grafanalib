=========
Changelog
=========

0.4.0 (2017-08-02)
==================

New features
------------

* Support for ``Text`` panels
  (https://github.com/weaveworks/grafanalib/pull/63)


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
