"""Tests for core."""

import random
import grafanalib.core as G


def dummy_grid_pos() -> G.GridPos:
    return G.GridPos(h=1, w=2, x=3, y=4)


def dummy_data_link() -> G.DataLink:
    return G.DataLink(
        title='dummy title',
        linkUrl='https://www.dummy-link-url.com',
        isNewTab=True
    )


def dummy_evaluator() -> G.Evaluator:
    return G.Evaluator(
        type=G.EVAL_GT,
        params=42
    )


def dummy_alert_condition() -> G.AlertCondition:
    return G.AlertCondition(
        target=G.Target(),
        evaluator=G.Evaluator(
            type=G.EVAL_GT,
            params=42),
        timeRange=G.TimeRange(
            from_time='5m',
            to_time='now'
        ),
        operator=G.OP_AND,
        reducerType=G.RTYPE_AVG,
    )


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

    assert t.to_json_data()['repeat'] is None
    assert t.to_json_data()['repeatDirection'] is None
    assert t.to_json_data()['maxPerRow'] is None


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


def test_dashboard_list():
    title = 'dummy title'
    dashboard_list = G.DashboardList(title=title)
    data = dashboard_list.to_json_data()
    assert data['targets'] == []
    assert data['datasource'] is None
    assert data['title'] == title
    assert data['starred'] is True


def test_logs_panel():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    logs = G.Logs(data_source, targets, title)
    data = logs.to_json_data()
    assert data['targets'] == targets
    assert data['datasource'] == data_source
    assert data['title'] == title
    assert data['options']['showLabels'] is False
    assert data['options']['showTime'] is False
    assert data['options']['wrapLogMessage'] is False
    assert data['options']['sortOrder'] == 'Descending'


def test_notification():
    uid = 'notification_channel'
    notification = G.Notification(uid)
    data = notification.to_json_data()
    assert data['uid'] == uid


def test_graph_panel():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    graph = G.Graph(data_source, targets, title)
    data = graph.to_json_data()
    assert data['targets'] == targets
    assert data['datasource'] == data_source
    assert data['title'] == title
    assert 'alert' not in data


def test_graph_panel_threshold():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    thresholds = [
        G.GraphThreshold(20.0),
        G.GraphThreshold(40.2, colorMode="ok")
    ]
    graph = G.Graph(data_source, targets, title, thresholds=thresholds)
    data = graph.to_json_data()
    assert data['targets'] == targets
    assert data['datasource'] == data_source
    assert data['title'] == title
    assert 'alert' not in data
    assert data['thresholds'] == thresholds


def test_graph_panel_alert():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    alert = [
        G.AlertCondition(G.Target(), G.Evaluator('a', 'b'), G.TimeRange('5', '6'), 'd', 'e')
    ]
    thresholds = [
        G.GraphThreshold(20.0),
        G.GraphThreshold(40.2, colorMode="ok")
    ]
    graph = G.Graph(data_source, targets, title, thresholds=thresholds, alert=alert)
    data = graph.to_json_data()
    assert data['targets'] == targets
    assert data['datasource'] == data_source
    assert data['title'] == title
    assert data['alert'] == alert
    assert data['thresholds'] == []


def test_graph_threshold():
    value = 20.0
    colorMode = "ok"
    threshold = G.GraphThreshold(value, colorMode=colorMode)
    data = threshold.to_json_data()

    assert data['value'] == value
    assert data['colorMode'] == colorMode
    assert data['fill'] is True
    assert data['line'] is True
    assert data['op'] == G.EVAL_GT
    assert 'fillColor' not in data
    assert 'lineColor' not in data


def test_graph_threshold_custom():
    value = 20.0
    colorMode = "custom"
    color = G.GREEN
    threshold = G.GraphThreshold(value, colorMode=colorMode, fillColor=color)
    data = threshold.to_json_data()

    assert data['value'] == value
    assert data['colorMode'] == colorMode
    assert data['fill'] is True
    assert data['line'] is True
    assert data['op'] == G.EVAL_GT
    assert data['fillColor'] == color
    assert data['lineColor'] == G.RED


def test_alert_list():
    alert_list = G.AlertList(
        dashboardTags=['dummy tag'],
        description='dummy description',
        gridPos=dummy_grid_pos(),
        id=random.randint(1, 10),
        links=[dummy_data_link(), dummy_data_link()],
        nameFilter='dummy name filter',
        stateFilter=[G.ALERTLIST_STATE_ALERTING, G.ALERTLIST_STATE_OK],
        title='dummy title'
    )
    alert_list.to_json_data()


def test_alert():
    alert = G.Alert(
        name='dummy name',
        message='dummy message',
        alertConditions=dummy_alert_condition(),
        alertRuleTags=dict(alert_rul_dummy_key='alert rul dummy value')
    )
    alert.to_json_data()
