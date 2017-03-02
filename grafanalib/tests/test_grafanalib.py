"""Tests for Grafanalib."""

from io import StringIO

import grafanalib.core as G
from grafanalib import _gen

# TODO: Use Hypothesis to generate a more thorough battery of smoke tests.


def test_serialization():
    """Serializing a graph doesn't explode."""
    graph = G.Graph(
        title="CPU Usage by Namespace (rate[5m])",
        dataSource="My data source",
        targets=[
            G.Target(
                expr='namespace:container_cpu_usage_seconds_total:sum_rate',
                legendFormat='{{namespace}}',
                refId='A',
            ),
        ],
        id=1,
        yAxes=[
            G.YAxis(format=G.SHORT_FORMAT, label="CPU seconds / second"),
            G.YAxis(format=G.SHORT_FORMAT),
        ],
    )
    stream = StringIO()
    _gen.write_dashboard(graph, stream)
    assert stream.getvalue() != ''
