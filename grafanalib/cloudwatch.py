"""Helpers to create Cloudwatch-specific Grafana queries."""

import attr

from attr.validators import instance_of


@attr.s
class CloudwatchMetricsTarget(object):
    """
    Generates Cloudwatch target JSON structure.

    Grafana docs on using Cloudwatch:
    https://grafana.com/docs/grafana/latest/datasources/cloudwatch/

    AWS docs on Cloudwatch metrics:
    https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html

    :param alias: legend alias
    :param dimensions: Cloudwatch dimensions dict
    :param expression: Cloudwatch Metric math expressions
    :param id: unique id
    :param matchExact: Only show metrics that exactly match all defined dimension names.
    :param metricName: Cloudwatch metric name
    :param namespace: Cloudwatch namespace
    :param period: Cloudwatch data period
    :param refId: target reference id
    :param region: Cloudwatch region
    :param statistics: Cloudwatch mathematic statistic
    :param hide: controls if given metric is displayed on visualization
    """
    alias = attr.ib(default="")
    dimensions = attr.ib(default={}, validator=instance_of(dict))
    expression = attr.ib(default="")
    id = attr.ib(default="")
    matchExact = attr.ib(default=True, validator=instance_of(bool))
    metricName = attr.ib(default="")
    namespace = attr.ib(default="")
    period = attr.ib(default="")
    refId = attr.ib(default="")
    region = attr.ib(default="default")
    statistics = attr.ib(default=["Average"], validator=instance_of(list))
    hide = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):

        return {
            "alias": self.alias,
            "dimensions": self.dimensions,
            "expression": self.expression,
            "id": self.id,
            "matchExact": self.matchExact,
            "metricName": self.metricName,
            "namespace": self.namespace,
            "period": self.period,
            "refId": self.refId,
            "region": self.region,
            "statistics": self.statistics,
            "hide": self.hide,
        }
