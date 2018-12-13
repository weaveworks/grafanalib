"""Tests for core."""

import pytest

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


CW_TESTDATA = [
    pytest.param(
        {},
        {'region': '',
         'namespace': '',
         'metricName': '',
         'statistics': [],
         'dimensions': {},
         'id': '',
         'expression': '',
         'period': '',
         'alias': '',
         'highResolution': False,
         'refId': '',
         'datasource': '',
         'hide': False},
        id='defaults',
    ),
    pytest.param(
        {'region': 'us-east-1',
         'namespace': 'AWS/RDS',
         'metricName': 'CPUUtilization',
         'statistics': ['Average'],
         'dimensions': {'DBInstanceIdentifier': 'foo'},
         'id': 'id',
         'expression': 'expr',
         'period': 'period',
         'alias': 'alias',
         'highResolution': True,
         'refId': 'A',
         'datasource': 'CloudWatch',
         'hide': True,
        },
        {'region': 'us-east-1',
         'namespace': 'AWS/RDS',
         'metricName': 'CPUUtilization',
         'statistics': ['Average'],
         'dimensions': {'DBInstanceIdentifier': 'foo'},
         'id': 'id',
         'expression': 'expr',
         'period': 'period',
         'alias': 'alias',
         'highResolution': True,
         'refId': 'A',
         'datasource': 'CloudWatch',
         'hide': True,
        },
        id='custom',
    )
]

@pytest.mark.parametrize("attrs,expected", CW_TESTDATA)
def test_cloud_watch_target_json_data(attrs, expected):
    assert G.CloudWatchTarget(**attrs).to_json_data() == expected
