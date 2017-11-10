"""Tests for OpenTSDB datasource"""

from io import StringIO

import grafanalib.core as G
from grafanalib.opentsdb import (
    OpenTSDBFilter,
    OpenTSDBTarget,
)
from grafanalib import _gen


def test_serialization_opentsdb_target():
    """Serializing a graph doesn't explode."""
    graph = G.Graph(
        title="CPU Usage",
        dataSource="OpenTSDB data source",
        targets=[
            OpenTSDBTarget(
                metric='cpu',
                alias='$tag_instance',
                filters=[
                    OpenTSDBFilter(value='*', tag='instance',
                                   type='wildcard', groupBy=True),
                ]),
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
