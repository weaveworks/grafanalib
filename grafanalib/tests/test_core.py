"""Tests for core."""

import grafanalib.core as G


def test_template_defaults():
    t = G.Template(
        name='test',
        query='1m,5m,10m,30m,1h,3h,12h,1d',
        type='interval',
        default='1m',
    )

    assert t.to_json_data()['current']['text'] == '1m'
    assert t.to_json_data()['current']['value'] == '1m'


def test_custom_template_ok():
    t = G.Template(
        name='test',
        query='1,2,3',
        default='1',
        type='custom',
    )

    assert len(t.to_json_data()['options']) == 3
    assert t.to_json_data()['current']['text'] == '1'
    assert t.to_json_data()['current']['value'] == '1'


def test_custom_template_dont_override_options():
    t = G.Template(
        name='test',
        query='1,2,3',
        default='1',
        options=[
            {
                "value": '1',
                "selected": True,
                "text": 'some text 1',
            },
            {
                "value": '2',
                "selected": False,
                "text": 'some text 2',
            },
            {
                "value": '3',
                "selected": False,
                "text": 'some text 3',
            },
        ],
        type='custom',
    )

    assert len(t.to_json_data()['options']) == 3
    assert t.to_json_data()['current']['text'] == 'some text 1'
    assert t.to_json_data()['current']['value'] == '1'


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


def test_stat_no_repeat():
    t = G.Stat(
        title='dummy',
        dataSource='data source',
        targets=[
            G.Target(expr='some expr')
        ]
    )

    assert t.to_json_data()['repeat'] == None
    assert t.to_json_data()['repeatDirection'] == None
    assert t.to_json_data()['maxPerRow'] == None


def test_stat_with_repeat():
    t = G.Stat(
        title='dummy',
        dataSource='data source',
        targets=[
            G.Target(expr='some expr')
        ],
        repeat=G.Repeat(
            variable="repetitionVariable",
            direction='h',
            maxPerRow=10
        )
    )

    assert t.to_json_data()['repeat'] == 'repetitionVariable'
    assert t.to_json_data()['repeatDirection'] == 'h'
    assert t.to_json_data()['maxPerRow'] == 10


def test_single_stat():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    single_stat = G.SingleStat(data_source, targets, title)
    data = single_stat.to_json_data()
    assert data['targets'] == targets
    assert data['datasource'] == data_source
    assert data['title'] == title
