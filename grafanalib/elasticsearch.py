"""Support for Elasticsearch."""

import attr
import itertools
import grafanalib.validators as validators
from attr.validators import instance_of


@attr.s
class CountMetric(object):
    field = attr.ib(default="select field", validator=instance_of(str))
    type = attr.ib(default="count", validator=instance_of(str))

    def to_json_data(self):
        return {
            'field': self.field,
            'type': self.type,
        }


@attr.s
class MaxMetric(object):
    field = attr.ib(default="select field", validator=instance_of(str))
    type = attr.ib(default="max", validator=instance_of(str))
    # without an empty settings key, it's not displayed correctly in the
    # dashboard's "Metrics" view in the webinterface
    settings = attr.ib(default=attr.Factory(dict))

    def to_json_data(self):
        return {
            'field': self.field,
            'type': self.type,
            'settings': self.settings
        }


@attr.s
class DateTimeAggSettings(object):
    interval = attr.ib(default="auto", validator=instance_of(str))
    min_doc_count = attr.ib(default=0, validator=instance_of(int))
    trimEdges = attr.ib(default=0, validator=instance_of(int))

    def to_json_data(self):
        return {
                'interval': self.interval,
                'min_doc_count': self.min_doc_count,
                'trimEdges': self.trimEdges,
                }


@attr.s
class DateTimeAgg(object):
    field = attr.ib(default="time_iso8601", validator=instance_of(str))
    id = attr.ib(default=0, validator=instance_of(int))
    settings = attr.ib(default=DateTimeAggSettings())
    type = attr.ib(default="date_histogram", validator=instance_of(str))

    def to_json_data(self):
        return {
                'field': self.field,
                'id': str(self.id),
                'settings': self.settings,
                'type': self.type
                }


@attr.s
class Filter(object):
    label = attr.ib(default="", validator=instance_of(str))
    query = attr.ib(default="", validator=instance_of(str))

    def to_json_data(self):
        return {
                'label': self.label,
                'query': self.query
                }


@attr.s
class FiltersAggSettings(object):
    filters = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
                'filters': self.filters
               }


@attr.s
class FiltersAgg(object):
    field = attr.ib(default="time_iso8601", validator=instance_of(str))
    id = attr.ib(default=0, validator=instance_of(int))
    settings = attr.ib(default=FiltersAggSettings())
    type = attr.ib(default="filters", validator=instance_of(str))

    def to_json_data(self):
        return {
                'field': self.field,
                'id': str(self.id),
                'settings': self.settings,
                'type': self.type
                }


@attr.s
class ElasticsearchTarget(object):
    """Generates Elasticsearch target JSON structure.

    Grafana docs on using Elasticsearch:
    http://docs.grafana.org/features/datasources/elasticsearch/
    Elasticsearch docs on querying or reading data:
    https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html

    :param alias: legend alias
    :param bucketAggs: Group by query aggregators
    :param metrics: Elasticsearch metric
    :param query: query
    :param refId: target reference id
    """

    alias = attr.ib(default=None)
    bucket_aggs = attr.ib(default=[DateTimeAgg()])
    metrics = attr.ib(default=[CountMetric()])
    query = attr.ib(default="", validator=instance_of(str))
    refId = attr.ib(default="", validator=instance_of(str))

    def auto_bucket_aggs_id(self):
        ids = set([agg.id for agg in self.bucket_aggs if agg.id])
        auto_ids = (i for i in itertools.count(1) if i not in ids)

        def set_id(agg):
            if agg.id:
                return agg

            agg.id = next(auto_ids)
            return agg

        return list(map(set_id, self.bucket_aggs))

    def to_json_data(self):
        return {
            'alias': self.alias,
            'bucketAggs': self.auto_bucket_aggs_id(),
            'metrics': self.metrics,
            'query': self.query,
            'refId': self.refId,
        }
