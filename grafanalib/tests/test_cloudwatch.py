"""Tests for Cloudwatch Datasource"""

import grafanalib.core as G
import grafanalib.cloudwatch as C
from grafanalib import _gen
from io import StringIO


def test_serialization_cloudwatch_metrics_target():
    """Serializing a graph doesn't explode."""
    graph = G.Graph(
        title="Lambda Duration",
        dataSource="Cloudwatch data source",
        targets=[
            C.CloudwatchMetricsTarget(),
        ],
        id=1,
        yAxes=G.YAxes(
            G.YAxis(format=G.SHORT_FORMAT, label="ms"),
            G.YAxis(format=G.SHORT_FORMAT),
        ),
    )
    stream = StringIO()
    _gen.write_dashboard(graph, stream)
    assert stream.getvalue() != ''


def test_serialization_cloudwatch_logs_insights_target():
    """Serializing a graph doesn't explode."""
    graph = G.Logs(
        title="Lambda Duration",
        dataSource="Cloudwatch data source",
        targets=[
            C.CloudwatchLogsInsightsTarget(),
        ],
        id=1,
        wrapLogMessages=True
    )
    stream = StringIO()
    _gen.write_dashboard(graph, stream)
    assert stream.getvalue() != ''


def test_cloudwatch_logs_insights_target():
    """Test Cloudwatch Logs Insights target"""
    cloudwatch_logs_insights_expression = "fields @timestamp, @xrayTraceId, @message | filter @message like /^(?!.*(START|END|REPORT|LOGS|EXTENSION)).*$/ | sort @timestamp desc"
    ref_id = "A"
    log_group_names = ["/aws/lambda/foo", "/aws/lambda/bar"]

    target = C.CloudwatchLogsInsightsTarget(
        expression=cloudwatch_logs_insights_expression,
        logGroupNames=log_group_names,
        refId=ref_id
    )

    data = target.to_json_data()

    assert data["expression"] == cloudwatch_logs_insights_expression
    assert data["id"] == ""
    assert data["logGroupNames"] == log_group_names
    assert data["namespace"] == ""
    assert data["queryMode"] == "Logs"
    assert data["refId"] == ref_id
    assert data["region"] == "default"
    assert data["statsGroups"] == []
    assert data["hide"] is False
