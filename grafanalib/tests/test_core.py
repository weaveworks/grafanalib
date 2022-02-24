"""Tests for core."""

import random
import grafanalib.core as G
import pytest


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


def test_table():
    t = G.Table(
        dataSource='some data source',
        targets=[
            G.Target(expr='some expr'),
        ],
        title='table title',
        transformations=[
            {
                "id": "seriesToRows",
                "options": {}
            },
            {
                "id": "organize",
                "options": {
                    "excludeByName": {
                        "Time": True
                    },
                    "indexByName": {},
                    "renameByName": {
                        "Value": "Dummy"
                    }
                }
            }
        ]
    )
    assert len(t.to_json_data()['transformations']) == 2
    assert t.to_json_data()['transformations'][0]["id"] == "seriesToRows"


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


def test_Text_exception_checks():
    with pytest.raises(TypeError):
        G.Text(content=123)

    with pytest.raises(TypeError):
        G.Text(error=123)

    with pytest.raises(ValueError):
        G.Text(mode=123)


def test_Text():
    t = G.Text()

    json_data = t.to_json_data()
    assert json_data['error'] is False
    assert json_data['options']['content'] == ""
    assert json_data['options']['mode'] == G.TEXT_MODE_MARKDOWN

    t = G.Text(content='foo', error=True, mode=G.TEXT_MODE_HTML)

    json_data = t.to_json_data()
    assert json_data['error'] is True
    assert json_data['options']['content'] == "foo"
    assert json_data['options']['mode'] == G.TEXT_MODE_HTML


def test_DiscreteColorMappingItem_exception_checks():
    with pytest.raises(TypeError):
        G.DiscreteColorMappingItem(123)

    with pytest.raises(TypeError):
        G.DiscreteColorMappingItem("foo", color=123)


def test_DiscreteColorMappingItem():
    t = G.DiscreteColorMappingItem('foo')

    json_data = t.to_json_data()
    assert json_data['text'] == 'foo'
    assert json_data['color'] == G.GREY1

    t = G.DiscreteColorMappingItem('foo', color='bar')

    json_data = t.to_json_data()
    assert json_data['text'] == 'foo'
    assert json_data['color'] == 'bar'


def test_Discrete_exceptions():
    with pytest.raises(ValueError):
        G.Discrete(legendSortBy='foo')

    with pytest.raises(TypeError):
        G.Discrete(rangeMaps=[123, 456])

    with pytest.raises(TypeError):
        G.Discrete(valueMaps=['foo', 'bar'])

    with pytest.raises(TypeError):
        G.Discrete(lineColor=123)

    with pytest.raises(TypeError):
        G.Discrete(highlightOnMouseover=123)


def test_Discrete():
    colorMap = [
        G.DiscreteColorMappingItem('bar', color='baz'),
        G.DiscreteColorMappingItem('foz', color='faz')
    ]

    t = G.Discrete(
        title='foo',
        colorMaps=colorMap,
        lineColor='#aabbcc',
        metricNameColor=G.RGBA(1, 2, 3, .5),
        decimals=123,
        highlightOnMouseover=False,
        showDistinctCount=True,
        showLegendCounts=False,
    )

    json_data = t.to_json_data()
    assert json_data['colorMaps'] == colorMap
    assert json_data['title'] == 'foo'
    assert json_data['type'] == G.DISCRETE_TYPE
    assert json_data['rangeMaps'] == []
    assert json_data['valueMaps'] == []

    assert json_data['backgroundColor'] == G.RGBA(128, 128, 128, 0.1)
    assert json_data['lineColor'] == '#aabbcc'
    assert json_data['metricNameColor'] == G.RGBA(1, 2, 3, .5)
    assert json_data['timeTextColor'] == "#d8d9da"
    assert json_data['valueTextColor'] == "#000000"

    assert json_data['decimals'] == 123
    assert json_data['legendPercentDecimals'] == 0
    assert json_data['rowHeight'] == 50
    assert json_data['textSize'] == 24
    assert json_data['textSizeTime'] == 12

    assert json_data['highlightOnMouseover'] is False
    assert json_data['showLegend'] is True
    assert json_data['showLegendPercent'] is True
    assert json_data['showLegendNames'] is True
    assert json_data['showLegendValues'] is True
    assert json_data['showTimeAxis'] is True
    assert json_data['use12HourClock'] is False
    assert json_data['writeMetricNames'] is False
    assert json_data['writeLastValue'] is True
    assert json_data['writeAllValues'] is False

    assert json_data['showDistinctCount'] is True
    assert json_data['showLegendCounts'] is False
    assert json_data['showLegendTime'] is None
    assert json_data['showTransitionCount'] is None


def test_StatValueMappings_exception_checks():
    with pytest.raises(TypeError):
        G.StatValueMappings(
            G.StatValueMappingItem('foo', '0', 'dark-red'),
            "not of type StatValueMappingItem",
        )


def test_StatValueMappings():
    t = G.StatValueMappings(
        G.StatValueMappingItem('foo', '0', 'dark-red'),  # Value must a string
        G.StatValueMappingItem('bar', '1', 'purple'),
    )

    json_data = t.to_json_data()
    assert json_data['type'] == 'value'
    assert json_data['options']['0']['text'] == 'foo'
    assert json_data['options']['0']['color'] == 'dark-red'
    assert json_data['options']['1']['text'] == 'bar'
    assert json_data['options']['1']['color'] == 'purple'


def test_StatRangeMappings():
    t = G.StatRangeMappings(
        'dummy_text',
        startValue=10,
        endValue=20,
        color='dark-red'
    )

    json_data = t.to_json_data()
    assert json_data['type'] == 'range'
    assert json_data['options']['from'] == 10
    assert json_data['options']['to'] == 20
    assert json_data['options']['result']['text'] == 'dummy_text'
    assert json_data['options']['result']['color'] == 'dark-red'


def test_StatMapping():
    t = G.StatMapping(
        'dummy_text',
        startValue='foo',
        endValue='bar',
    )

    json_data = t.to_json_data()
    assert json_data['text'] == 'dummy_text'
    assert json_data['from'] == 'foo'
    assert json_data['to'] == 'bar'


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
    assert data['options']['showCommonLabels'] is False
    assert data['options']['showTime'] is False
    assert data['options']['wrapLogMessage'] is False
    assert data['options']['sortOrder'] == 'Descending'
    assert data['options']['dedupStrategy'] == 'none'
    assert data['options']['enableLogDetails'] is False
    assert data['options']['prettifyLogMessage'] is False


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


def test_panel_extra_json():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    extraJson = {
        'fillGradient': 6,
        'yaxis': {'align': True},
        'legend': {'avg': True},
    }
    graph = G.Graph(data_source, targets, title, extraJson=extraJson)
    data = graph.to_json_data()
    assert data['targets'] == targets
    assert data['datasource'] == data_source
    assert data['title'] == title
    assert 'alert' not in data
    assert data['fillGradient'] == 6
    assert data['yaxis']['align'] is True
    # Nested non-dict object should also be deep-updated
    assert data['legend']['max'] is False
    assert data['legend']['avg'] is True


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


def test_SeriesOverride_exception_checks():
    with pytest.raises(TypeError):
        G.SeriesOverride()

    with pytest.raises(TypeError):
        G.SeriesOverride(123)

    with pytest.raises(TypeError):
        G.SeriesOverride('alias', bars=123)

    with pytest.raises(TypeError):
        G.SeriesOverride('alias', lines=123)

    with pytest.raises(ValueError):
        G.SeriesOverride('alias', yaxis=123)
    with pytest.raises(ValueError):
        G.SeriesOverride('alias', yaxis='abc')

    with pytest.raises(TypeError):
        G.SeriesOverride('alias', fillBelowTo=123)

    with pytest.raises(ValueError):
        G.SeriesOverride('alias', fill="foo")
    with pytest.raises(ValueError):
        G.SeriesOverride('alias', fill=123)
    with pytest.raises(ValueError):
        G.SeriesOverride('alias', fill=-2)
    with pytest.raises(ValueError):
        G.SeriesOverride('alias', zindex=5)

    with pytest.raises(TypeError):
        G.SeriesOverride('alias', dashes="foo")

    with pytest.raises(ValueError):
        G.SeriesOverride('alias', dashLength=-2)
    with pytest.raises(ValueError):
        G.SeriesOverride('alias', dashLength=25)
    with pytest.raises(ValueError):
        G.SeriesOverride('alias', spaceLength=-2)
    with pytest.raises(ValueError):
        G.SeriesOverride('alias', spaceLength=25)

    with pytest.raises(ValueError):
        G.SeriesOverride('alias', dashLength="foo")
    with pytest.raises(ValueError):
        G.SeriesOverride('alias', spaceLength="foo")


def test_SeriesOverride():
    t = G.SeriesOverride('alias').to_json_data()

    assert t['alias'] == 'alias'
    assert t['bars'] is False
    assert t['lines'] is True
    assert t['yaxis'] == 1
    assert t['fill'] == 1
    assert t['color'] is None
    assert t['fillBelowTo'] is None
    assert t['dashes'] is False
    assert t['dashLength'] is None
    assert t['spaceLength'] is None
    assert t['zindex'] == 0

    t = G.SeriesOverride(
        'alias',
        bars=True,
        lines=False,
        yaxis=2,
        fill=7,
        color='#abc',
        fillBelowTo='other_alias',
        dashes=True,
        dashLength=12,
        spaceLength=17,
        zindex=-2,
    ).to_json_data()

    assert t['alias'] == 'alias'
    assert t['bars'] is True
    assert t['lines'] is False
    assert t['yaxis'] == 2
    assert t['fill'] == 7
    assert t['color'] == '#abc'
    assert t['fillBelowTo'] == 'other_alias'
    assert t['dashes'] is True
    assert t['dashLength'] == 12
    assert t['spaceLength'] == 17
    assert t['zindex'] == -2


def test_alert():
    alert = G.Alert(
        name='dummy name',
        message='dummy message',
        alertConditions=dummy_alert_condition(),
        alertRuleTags=dict(alert_rul_dummy_key='alert rul dummy value')
    )
    alert.to_json_data()


def test_worldmap():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    worldmap = G.Worldmap(data_source, targets, title, circleMaxSize=11)
    data = worldmap.to_json_data()
    assert data['targets'] == targets
    assert data['datasource'] == data_source
    assert data['title'] == title
    assert data['circleMaxSize'] == 11


def test_stateTimeline():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    stateTimeline = G.StateTimeline(data_source, targets, title, rowHeight=0.7)
    data = stateTimeline.to_json_data()
    assert data['targets'] == targets
    assert data['datasource'] == data_source
    assert data['title'] == title
    assert data['options']['rowHeight'] == 0.7


def test_timeseries():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    timeseries = G.TimeSeries(data_source, targets, title)
    data = timeseries.to_json_data()
    assert data['targets'] == targets
    assert data['datasource'] == data_source
    assert data['title'] == title
    assert data['fieldConfig']['overrides'] == []


def test_timeseries_with_overrides():
    data_source = 'dummy data source'
    targets = ['dummy_prom_query']
    title = 'dummy title'
    overrides = [
        {
            "matcher": {
                "id": "byName",
                "options": "min"
            },
            "properties": [
                {
                    "id": "custom.fillBelowTo",
                    "value": "min"
                },
                {
                    "id": "custom.lineWidth",
                    "value": 0
                }
            ]
        }
    ]
    timeseries = G.TimeSeries(
        dataSource=data_source,
        targets=targets,
        title=title,
        overrides=overrides,
    )
    data = timeseries.to_json_data()
    assert data["targets"] == targets
    assert data["datasource"] == data_source
    assert data["title"] == title
    assert data["fieldConfig"]["overrides"] == overrides


def test_news():
    title = "dummy title"
    feedUrl = "www.example.com"
    news = G.News(title=title, feedUrl=feedUrl)
    data = news.to_json_data()
    assert data["options"]["feedUrl"] == feedUrl
    assert data["title"] == title


def test_pieChartv2():
    data_source = "dummy data source"
    targets = ["dummy_prom_query"]
    title = "dummy title"
    pie = G.PieChartv2(data_source, targets, title)
    data = pie.to_json_data()
    assert data["targets"] == targets
    assert data["datasource"] == data_source
    assert data["title"] == title


def test_histogram():
    data_source = "dummy data source"
    targets = ["dummy_prom_query"]
    title = "dummy title"
    panel = G.Histogram(data_source, targets, title)
    data = panel.to_json_data()
    assert data["targets"] == targets
    assert data["datasource"] == data_source
    assert data["title"] == title
    assert 'bucketSize' not in data['options']

    bucketSize = 5
    panel = G.Histogram(data_source, targets, title, bucketSize=bucketSize)
    data = panel.to_json_data()
    assert data['options']['bucketSize'] == bucketSize


def test_sql_target():
    t = G.Table(
        dataSource="some data source",
        targets=[
            G.SqlTarget(rawSql="SELECT * FROM example"),
        ],
        title="table title",
    )
    assert t.to_json_data()["targets"][0].rawQuery is True
    assert t.to_json_data()["targets"][0].rawSql == "SELECT * FROM example"
