"""Tests for Grafanalib."""

import grafanalib.core as G
from grafanalib import _gen

import sys
if sys.version_info[0] < 3:
    from io import BytesIO as StringIO
else:
    from io import StringIO

# TODO: Use Hypothesis to generate a more thorough battery of smoke tests.


def test_serialization():
    """Serializing a graph doesn't explode."""
    graph = G.Graph(
        title="CPU Usage by Namespace (rate[5m])",
        datasource="My data source",
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
        gridPos=G.GridPos(h=8, w=12, x=0, y=0)
    )
    stream = StringIO()
    _gen.write_dashboard(graph, stream)
    assert stream.getvalue() != ''


def test_auto_id():
    """auto_panel_ids() provides IDs for all panels without IDs already set."""
    dashboard = G.Dashboard(
        title="Test dashboard",
        panels=[
            G.Row(
                panels=[
                    G.Graph(
                        title="CPU Usage by Namespace (rate[5m])",
                        datasource="My data source",
                        targets=[
                            G.Target(
                                expr='whatever',
                                legendFormat='{{namespace}}',
                                refId='A',
                            ),
                        ],
                        yAxes=[
                            G.YAxis(
                                format=G.SHORT_FORMAT, label="CPU seconds"
                            ),
                            G.YAxis(format=G.SHORT_FORMAT),
                        ],
                        gridPos=G.GridPos(h=8, w=12, x=0, y=0)
                    )
                ],
                gridPos=G.GridPos(h=1, w=24, x=0, y=0)
            ),
        ],
    ).auto_panel_ids()
    assert dashboard.panels[0].id == 1


def test_row_show_title():
    row = G.Row(gridPos=G.GridPos(h=1, w=24, x=0, y=0)).to_json_data()
    assert row['title'] == 'New row'

    row = G.Row(gridPos=G.GridPos(h=1, w=24, x=0, y=0), title='My title')\
        .to_json_data()
    assert row['title'] == 'My title'
