"""Tests for core."""

import grafanalib.core as G


def test_table_styled_columns():
    t = G.Table.with_styled_columns(
        columns=[
            (G.Column('Foo', 'foo'), G.ColumnStyle()),
            (G.Column('Bar', 'bar'), None),
        ],
        dataSource='some data source',
        targets=[
            G.Target(expr='some expr'),
        ],
        title='table title',
    )
    assert t.columns == [
        G.Column('Foo', 'foo'),
        G.Column('Bar', 'bar'),
    ]
    assert t.styles == [
        G.ColumnStyle(pattern='Foo'),
    ]


def test_single_stat():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    single_stat = G.SingleStat(data_source, targets, title)
    data = single_stat.to_json_data()
    assert data['targets'] == targets
    assert data['datasource'] == data_source
    assert data['title'] == title

def test_grid_position():
    x = '10'
    y = '10'
    w = '20'
    h = '20'
    grid_position = G.GridPosition(x, y, w, h)
    data = grid_position.to_json_data()
    assert data['x'] == x
    assert data['y'] == y
    assert data['w'] == w
    assert data['h'] == h


def test_row_grid():
    title = 'dummy title'
    gridPos = G.GridPosition()
    row_grid = G.RowGrid(title=title, gridPos=gridPos)
    data = row_grid.to_json_data()
    assert data['title'] == title
    assert data['gridPos'] == gridPos
