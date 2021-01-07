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
