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


def test_auto_id():
    """auto_panel_ids() provides IDs for all panels without IDs already set."""
    dashboard = G.Dashboard(
        title="Test dashboard",
        rows=[
            G.Row(panels=[
                G.Graph(
                    title="CPU Usage by Namespace (rate[5m])",
                    dataSource="My data source",
                    targets=[
                        G.Target(
                            expr='whatever',
                            legendFormat='{{namespace}}',
                            refId='A',
                        ),
                    ],
                    yAxes=[
                        G.YAxis(format=G.SHORT_FORMAT, label="CPU seconds"),
                        G.YAxis(format=G.SHORT_FORMAT),
                    ],
                )
            ]),
        ],
    ).auto_panel_ids()
    assert dashboard.rows[0].panels[0].id == 1


def test_row_show_title():
    row = G.Row().to_json_data()
    assert row['title'] == 'New row'
    assert not row['showTitle']

    row = G.Row(title='My title').to_json_data()
    assert row['title'] == 'My title'
    assert row['showTitle']

    row = G.Row(title='My title', showTitle=False).to_json_data()
    assert row['title'] == 'My title'
    assert not row['showTitle']
