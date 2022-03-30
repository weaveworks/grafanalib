"""Tests for Azure Monitor Datasource"""

import grafanalib.core as G
import grafanalib.azuremonitor as A
from grafanalib import _gen
from io import StringIO


def test_serialization_azure_metrics_target():
    """Serializing a graph doesn't explode."""
    graph = G.TimeSeries(
        title="Test Azure Monitor",
        dataSource="default",
        targets=[
            A.AzureMonitorMetricsTarget(
                aggregation="Total",
                metricDefinition="Microsoft.Web/sites",
                metricName="Requests",
                metricNamespace="Microsoft.Web/sites",
                resourceGroup="test-grafana",
                resourceName="test-grafana",
                subscription="3a680d1a-9310-4667-9e6a-9fcd2ecddd86",
                refId="Requests",
            ),
        ],
    )
    stream = StringIO()
    _gen.write_dashboard(graph, stream)
    assert stream.getvalue() != ""


def test_serialization_azure_logs_target():
    """Serializing a graph doesn't explode."""

    logs_query = """AzureMetrics
| where TimeGenerated > ago(30d)
| extend tail_latency = Maximum / Average
| where MetricName == "Http5xx" or (MetricName == "HttpResponseTime" and Average >= 3) or (MetricName == "HttpResponseTime" and tail_latency >= 10 and Average >= 0.5)
| summarize dcount(TimeGenerated) by Resource
| order by dcount_TimeGenerated"""

    graph = G.GaugePanel(
        title="Test Logs",
        dataSource="default",
        targets=[
            A.AzureLogsTarget(
                query=logs_query,
                resource="/subscriptions/3a680d1a-9310-4667-9e6a-9fcd2ecddd86",
                subscription="3a680d1a-9310-4667-9e6a-9fcd2ecddd86",
                refId="Bad Minutes",
            ),
        ],
    )
    stream = StringIO()
    _gen.write_dashboard(graph, stream)
    assert stream.getvalue() != ""


def test_serialization_azure_graph_target():
    """Serializing a graph doesn't explode."""

    graph_query = """Resources
| project name, type, location
| order by name asc"""

    graph = G.GaugePanel(
        title="Test Logs",
        dataSource="default",
        targets=[
            A.AzureLogsTarget(
                query=graph_query,
                subscription="3a680d1a-9310-4667-9e6a-9fcd2ecddd86",
                refId="Resources",
            ),
        ],
    )
    stream = StringIO()
    _gen.write_dashboard(graph, stream)
    assert stream.getvalue() != ""
