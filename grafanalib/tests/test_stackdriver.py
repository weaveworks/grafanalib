"""Tests for Stackdriver Datasource"""

import grafanalib.core as G
import grafanalib.stackdriver as S
from grafanalib import _gen
from io import StringIO


def test_serialization_stackdriver_metrics_target():
    """Serializing a graph doesn't explode."""
    graph = G.Graph(
        title="Stackdriver Logs",
        dataSource="Stackdriver data source",
        targets=[
            S.StackdriverTarget(),
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
