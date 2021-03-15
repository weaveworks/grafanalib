"""Tests for Humio Datasource"""

import grafanalib.core as G
import grafanalib.humio as H
from grafanalib import _gen
from io import StringIO


def test_serialization_humio_metrics_target():
    """Serializing a graph doesn't explode."""
    graph = G.Graph(
        title="Humio Logs",
        dataSource="Humio data source",
        targets=[
            H.HumioTarget(),
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
