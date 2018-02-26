"""Helpers to create Elasticsearch-specific Grafana queries."""

import attr
import itertools
from attr.validators import instance_of

DATE_HISTOGRAM_DEFAULT_FIELD = "time_iso8601"
ORDER_ASC = "asc"
ORDER_DESC = "desc"


@attr.s
class CountMetricAgg(object):
    """An aggregator that counts the number of values.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-valuecount-aggregation.html

    It's the default aggregator for elasticsearch queries.
    """
    def to_json_data(self):
        return {
            'type': 'count',
            'field': 'select field',
            'settings': {},
        }


@attr.s
class MaxMetricAgg(object):
    """An aggregator that provides the max. value among the values.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-max-aggregation.html

    :param field: name of elasticsearch field to provide the maximum for
    """
    field = attr.ib(default="", validator=instance_of(str))

    def to_json_data(self):
        return {
            'type': 'max',
            'field': self.field,
            'settings': {},
        }


@attr.s
class DateHistogramGroupBy(object):
    """A bucket aggregator that groups results by date.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html

    :param id: ascending unique number per GroupBy clause
    :param field: name of the elasticsearch field to group by
    :param interval: interval to group by
    :param minDocCount: min. amount of records in the timespan to return a
                        result
    """
    id = attr.ib(default=0, validator=instance_of(int))
    field = attr.ib(
        default=DATE_HISTOGRAM_DEFAULT_FIELD,
        validator=instance_of(str),
    )
    interval = attr.ib(default="auto", validator=instance_of(str))
    minDocCount = attr.ib(default=0, validator=instance_of(int))

    def to_json_data(self):
        return {
            'field': self.field,
            'id': str(self.id),
            'settings': {
                'interval': self.interval,
                'min_doc_count': self.minDocCount,
                'trimEdges': 0,
            },
            'type': 'date_histogram',
        }


@attr.s
class Filter(object):
    """ A Filter for a FilterGroupBy aggregator.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-filter-aggregation.html

    :param label: label for the metric that is shown in the graph
    :param query: the query to filter by
    """
    label = attr.ib(default="", validator=instance_of(str))
    query = attr.ib(default="", validator=instance_of(str))

    def to_json_data(self):
        return {
                'label': self.label,
                'query': self.query,
                }


@attr.s
class FiltersGroupBy(object):
    """ A bucket aggregator that groups records by a filter expression.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-filter-aggregation.html

    :param id: ascending unique number per GroupBy clause
    :param filters: list of Filter objects
    """
    id = attr.ib(default=0, validator=instance_of(int))
    filters = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
                'id': str(self.id),
                'settings': {
                             'filters': self.filters,
                             },
                'type': 'filters',
                }


@attr.s
class TermsGroupBy(object):
    """ A multi-bucket aggregator based on field values.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html

    :param id: ascending unique number per GroupBy clause
    :param field: name of the field to group by
    :param minDocCount: min. amount of matching records to return a result
    :param order: ORDER_ASC or ORDER_DESC
    :param orderBy: term to order the bucker
    :param size: how many buckets are returned
    """
    field = attr.ib(validator=instance_of(str))
    id = attr.ib(default=0, validator=instance_of(int))
    minDocCount = attr.ib(default=1, validator=instance_of(int))
    order = attr.ib(default=ORDER_DESC, validator=instance_of(str))
    orderBy = attr.ib(default="_term", validator=instance_of(str))
    size = attr.ib(default=0, validator=instance_of(int))

    def to_json_data(self):
        return {
            'id': str(self.id),
            'type': 'terms',
            'field': self.field,
            'settings': {
                'min_doc_count': self.minDocCount,
                'order': self.order,
                'order_by': self.orderBy,
                'size': self.size,
            },
        }


@attr.s
class ElasticsearchTarget(object):
    """Generates Elasticsearch target JSON structure.

    Grafana docs on using Elasticsearch:
    http://docs.grafana.org/features/datasources/elasticsearch/
    Elasticsearch docs on querying or reading data:
    https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html

    :param alias: legend alias
    :param bucketAggs: Bucket aggregators
    :param metricAggs: Metric Aggregators
    :param query: query
    :param refId: target reference id
    """

    alias = attr.ib(default=None)
    bucketAggs = attr.ib(
        default=attr.Factory(lambda: [DateHistogramGroupBy()]),
    )
    metricAggs = attr.ib(default=attr.Factory(lambda: [CountMetricAgg()]))
    query = attr.ib(default="", validator=instance_of(str))
    refId = attr.ib(default="", validator=instance_of(str))

    def _map_bucket_aggs(self, f):
        return attr.assoc(self, bucketAggs=list(map(f, self.bucketAggs)))

    def auto_bucket_agg_ids(self):
        """Give unique IDs all bucketAggs without ID.

        Returns a new ``ElasticsearchTarget`` that is the same as this one,
        except all of the bucketAggs have their ``id`` property set. Any panels
        which had an ``id`` property set will keep that property, all others
        will have auto-generated IDs provided for them.

        If the bucketAggs don't have unique ID associated with it, the
        generated graph will be broken.
        """
        ids = set([agg.id for agg in self.bucketAggs if agg.id])
        auto_ids = (i for i in itertools.count(1) if i not in ids)

        def set_id(agg):
            if agg.id:
                return agg

            return attr.evolve(agg, id=next(auto_ids))

        return self._map_bucket_aggs(set_id)

    def to_json_data(self):
        return {
            'alias': self.alias,
            'bucketAggs': self.bucketAggs,
            'metrics': self.metricAggs,
            'query': self.query,
            'refId': self.refId,
        }
