=========
Changelog
=========

NEXT (YYYY-MM-DD)
-----------------

* ``PromGraph`` now lives in ``grafanalib.prometheus``, and takes a
  ``data_source`` parameter
* ``Dashboard`` objects now have an ``auto_panel_id`` method which will
  automatically supply unique panel (i.e. graph) IDs for any panels that don't
  have one set. Dashboard config files no longer need to track their own
  ``GRAPH_ID`` counter.
* ``SingleStat`` panel class added  (https://github.com/weaveworks/grafanalib/pull/22)
* Additional fields for ``Legend``  (https://github.com/weaveworks/grafanalib/pull/25)
* OpenTSDB datasource support added (https://github.com/weaveworks/grafanalib/pull/27)
* Additional fields for ``XAxis``   (https://github.com/weaveworks/grafanalib/pull/28)
* Add support for Grafana Zabbix plugin (https://github.com/weaveworks/grafanalib/pull/31)
* Add support for Grafana Zabbix Triggers panel (https://github.com/weaveworks/grafanalib/pull/36)


0.1.2 (2017-01-02)
------------------

* Add support for Grafana Templates (https://github.com/weaveworks/grafanalib/pull/9)

0.1.1 (2016-12-02)
------------------

* Include README on PyPI page

0.1.0 (2016-12-02)
------------------

Initial release.
