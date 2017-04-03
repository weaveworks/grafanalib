"""Low-level functions for building Grafana dashboards.

The functions in this module don't enforce Weaveworks policy, and only mildly
encourage it by way of some defaults. Rather, they are ways of building
arbitrary Grafana JSON.
"""

import attr
from attr.validators import instance_of
import itertools
import math


@attr.s
class RGBA(object):
    r = attr.ib(validator=instance_of(int))
    g = attr.ib(validator=instance_of(int))
    b = attr.ib(validator=instance_of(int))
    a = attr.ib(validator=instance_of(float))

    def to_json_data(self):
        return "rgba({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)


@attr.s
class RGB(object):
    r = attr.ib(validator=instance_of(int))
    g = attr.ib(validator=instance_of(int))
    b = attr.ib(validator=instance_of(int))

    def to_json_data(self):
        return "rgb({}, {}, {})".format(self.r, self.g, self.b)


@attr.s
class Pixels(object):
    num = attr.ib(validator=instance_of(int))

    def to_json_data(self):
        return '{}px'.format(self.num)


GREY1 = RGBA(216, 200, 27, 0.27)
GREY2 = RGBA(234, 112, 112, 0.22)
BLUE_RGBA = RGBA(31, 118, 189, 0.18)
BLUE_RGB = RGB(31, 120, 193)
GREEN = RGBA(50, 172, 45, 0.97)
ORANGE = RGBA(237, 129, 40, 0.89)
RED = RGBA(245, 54, 54, 0.9)

INDIVIDUAL = 'individual'
CUMULATIVE = 'cumulative'

NULL_CONNECTED = 'connected'
NULL_AS_ZERO = 'null as zero'

FLOT = 'flot'

DASHBOARD_TYPE = 'dashboard'
GRAPH_TYPE = 'graph'
SINGLESTAT_TYPE = 'singlestat'

DEFAULT_FILL = 1
DEFAULT_REFRESH = '10s'
DEFAULT_ROW_HEIGHT = Pixels(250)
DEFAULT_LINE_WIDTH = 2
DEFAULT_POINT_RADIUS = 5
DEFAULT_RENDERER = FLOT
DEFAULT_STEP = 10
TOTAL_SPAN = 12

DARK_STYLE = 'dark'
LIGHT_STYLE = 'light'

UTC = 'utc'

SCHEMA_VERSION = 12

# Y Axis formats
DURATION_FORMAT = "dtdurations"
NO_FORMAT = "none"
OPS_FORMAT = "ops"
PERCENT_UNIT_FORMAT = "percentunit"
SECONDS_FORMAT = "s"
MILLISECONDS_FORMAT = "ms"
SHORT_FORMAT = "short"
BYTES_FORMAT = "bytes"

# Alert rule state
STATE_NO_DATA = "no_data"
STATE_ALERTING = "alerting"
STATE_KEEP_LAST_STATE = "keep_state"

# Evaluator
EVAL_GT = "gt"
EVAL_LT = "lt"
EVAL_WITHIN_RANGE = "within_range"
EVAL_OUTSIDE_RANGE = "outside_range"
EVAL_NO_VALUE = "no_value"

# Reducer Type avg/min/max/sum/count/last/median
RTYPE_AVG = "avg"
RTYPE_MIN = "min"
RTYPE_MAX = "max"
RTYPE_SUM = "sum"
RTYPE_COUNT = "count"
RTYPE_LAST = "last"
RTYPE_MEDIAN = "median"

# Condition Type
CTYPE_QUERY = "query"

# Operator
OP_AND = "and"
OP_OR = "or"


@attr.s
class Mapping(object):

    name = attr.ib()
    value = attr.ib(validator=instance_of(int))

    def to_json_data(self):
        return {
            'name': self.name,
            'value': self.value,
        }


MAPPING_TYPE_VALUE_TO_TEXT = 1
MAPPING_TYPE_RANGE_TO_TEXT = 2

MAPPING_VALUE_TO_TEXT = Mapping("value to text", MAPPING_TYPE_VALUE_TO_TEXT)
MAPPING_RANGE_TO_TEXT = Mapping("range to text", MAPPING_TYPE_RANGE_TO_TEXT)


# Value types min/max/avg/current/total/name/first/delta/range
VTYPE_MIN = "min"
VTYPE_MAX = "max"
VTYPE_AVG = "avg"
VTYPE_CURR = "current"
VTYPE_TOTAL = "total"
VTYPE_NAME = "name"
VTYPE_FIRST = "first"
VTYPE_DELTA = "delta"
VTYPE_RANGE = "range"
VTYPE_DEFAULT = VTYPE_AVG


@attr.s
class Grid(object):

    threshold1 = attr.ib(default=None)
    threshold1Color = attr.ib(default=GREY1, validator=instance_of(RGBA))
    threshold2 = attr.ib(default=None)
    threshold2Color = attr.ib(default=GREY2, validator=instance_of(RGBA))

    def to_json_data(self):
        return {
            'threshold1': self.threshold1,
            'threshold1Color': self.threshold1Color,
            'threshold2': self.threshold2,
            'threshold2Color': self.threshold2Color,
        }


@attr.s
class Legend(object):
    avg = attr.ib(default=False, validator=instance_of(bool))
    current = attr.ib(default=False, validator=instance_of(bool))
    max = attr.ib(default=False, validator=instance_of(bool))
    min = attr.ib(default=False, validator=instance_of(bool))
    show = attr.ib(default=True, validator=instance_of(bool))
    total = attr.ib(default=False, validator=instance_of(bool))
    values = attr.ib(default=None)
    alignAsTable = attr.ib(default=False, validator=instance_of(bool))
    hideEmpty = attr.ib(default=False, validator=instance_of(bool))
    hideZero = attr.ib(default=False, validator=instance_of(bool))
    rightSide = attr.ib(default=False, validator=instance_of(bool))
    sideWidth = attr.ib(default=None)

    def to_json_data(self):
        values = ((self.avg or self.current or self.max or self.min)
                  if self.values is None else self.values)

        return {
            'avg': self.avg,
            'current': self.current,
            'max': self.max,
            'min': self.min,
            'show': self.show,
            'total': self.total,
            'values': values,
            'alignAsTable': self.alignAsTable,
            'hideEmpty': self.hideEmpty,
            'hideZero': self.hideZero,
            'rightSide': self.rightSide,
            'sideWidth': self.sideWidth,
        }


@attr.s
class Target(object):

    expr = attr.ib()
    legendFormat = attr.ib(default="")
    intervalFactor = attr.ib(default=2)
    metric = attr.ib(default="")
    refId = attr.ib(default="")
    step = attr.ib(default=DEFAULT_STEP)

    def to_json_data(self):
        return {
            'expr': self.expr,
            'intervalFactor': self.intervalFactor,
            'legendFormat': self.legendFormat,
            'metric': self.metric,
            'refId': self.refId,
            'step': self.step,
        }


@attr.s
class Tooltip(object):

    msResolution = attr.ib(default=True, validator=instance_of(bool))
    shared = attr.ib(default=True, validator=instance_of(bool))
    sort = attr.ib(default=0)
    valueType = attr.ib(default=CUMULATIVE)

    def to_json_data(self):
        return {
            'msResolution': self.msResolution,
            'shared': self.shared,
            'sort': self.sort,
            'value_type': self.valueType,
        }


def is_valid_xaxis_mode(instance, attribute, value):
    XAXIS_MODES = ("time", "series")
    if value not in XAXIS_MODES:
        raise ValueError("{attr} should be one of {choice}".format(
            attr=attribute, choice=XAXIS_MODES))


@attr.s
class XAxis(object):

    mode = attr.ib(default="time", validator=is_valid_xaxis_mode)
    name = attr.ib(default=None)
    values = attr.ib(default=attr.Factory(list))
    show = attr.ib(validator=instance_of(bool), default=True)

    def to_json_data(self):
        return {
            'show': self.show,
        }


@attr.s
class YAxis(object):
    format = attr.ib(default=None)
    label = attr.ib(default=None)
    logBase = attr.ib(default=1)
    max = attr.ib(default=None)
    min = attr.ib(default=0)
    show = attr.ib(default=True, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'format': self.format,
            'label': self.label,
            'logBase': self.logBase,
            'max': self.max,
            'min': self.min,
            'show': self.show,
        }


def _balance_panels(panels):
    """Resize panels so they are evenly spaced."""
    allotted_spans = sum(panel.span if panel.span else 0 for panel in panels)
    no_span_set = [panel for panel in panels if panel.span is None]
    auto_span = math.ceil(
        (TOTAL_SPAN - allotted_spans) / (len(no_span_set) or 1))
    return [
        attr.assoc(panel, span=auto_span) if panel.span is None else panel
        for panel in panels
    ]


@attr.s
class Row(object):
    # TODO: jml would like to separate the balancing behaviour from this
    # layer.
    panels = attr.ib(default=attr.Factory(list), convert=_balance_panels)
    collapse = attr.ib(
        default=False, validator=instance_of(bool),
    )
    editable = attr.ib(
        default=True, validator=instance_of(bool),
    )
    height = attr.ib(default=DEFAULT_ROW_HEIGHT, validator=instance_of(Pixels))
    showTitle = attr.ib(default=None)
    title = attr.ib(default=None)

    def _iter_panels(self):
        return iter(self.panels)

    def _map_panels(self, f):
        return attr.assoc(self, panels=list(map(f, self.panels)))

    def to_json_data(self):
        showTitle = False if self.title is None else True
        title = "New row" if self.title is None else self.title
        return {
            'collapse': self.collapse,
            'editable': self.editable,
            'height': self.height,
            'panels': self.panels,
            'showTitle': showTitle,
            'title': title,
        }


@attr.s
class Annotations(object):
    list = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            'list': self.list,
        }


@attr.s
class DashboardLink(object):
    dashboard = attr.ib()
    uri = attr.ib()
    keepTime = attr.ib(
        default=True,
        validator=instance_of(bool),
    )
    title = attr.ib(default=None)

    def to_json_data(self):
        title = self.dashboard if self.title is None else self.title
        return {
            "dashUri": self.uri,
            "dashboard": self.dashboard,
            "keepTime": self.keepTime,
            "title": title,
            "type": DASHBOARD_TYPE,
        }


@attr.s
class Template(object):
    """Template create a new 'variable' for the dashboard, defines the variable
    name, human name, query to fetch the values and the default value.

        :param default: the default value for the variable
        :param dataSource: where to fetch the values for the variable from
        :param label: the variable's human label
        :param name: the variable's name
        :param query: the query users to fetch the valid values of the variable
    """

    default = attr.ib()
    dataSource = attr.ib()
    label = attr.ib()
    name = attr.ib()
    query = attr.ib()

    def to_json_data(self):
        return {
            'allValue': None,
            'current': {
                'text': self.default,
                'value': self.default,
                'tags': [],
            },
            'datasource': self.dataSource,
            'hide': 0,
            'includeAll': False,
            'label': self.label,
            'multi': False,
            'name': self.name,
            'options': [],
            'query': self.query,
            'refresh': 1,
            'regex': '',
            'sort': 1,
            'tagValuesQuery': None,
            'tagsQuery': None,
            'type': 'query',
        }


@attr.s
class Templating(object):
    list = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            'list': self.list,
        }


@attr.s
class Time(object):
    start = attr.ib()
    end = attr.ib()

    def to_json_data(self):
        return {
            'from': self.start,
            'to': self.end,
        }


DEFAULT_TIME = Time('now-1h', 'now')


@attr.s
class TimePicker(object):
    refreshIntervals = attr.ib()
    timeOptions = attr.ib()

    def to_json_data(self):
        return {
            'refresh_intervals': self.refreshIntervals,
            'time_options': self.timeOptions,
        }


DEFAULT_TIME_PICKER = TimePicker(
    refreshIntervals=[
        "5s",
        "10s",
        "30s",
        "1m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "1d"
    ],
    timeOptions=[
        "5m",
        "15m",
        "1h",
        "6h",
        "12h",
        "24h",
        "2d",
        "7d",
        "30d"
    ]
)


@attr.s
class Evaluator(object):
    type = attr.ib()
    params = attr.ib()

    def to_json_data(self):
        return {
            "type": self.type,
            "params": self.params,
        }


def GreaterThan(value):
    return Evaluator(EVAL_GT, [value])


def LowerThan(value):
    return Evaluator(EVAL_LT, [value])


def WithinRange(from_value, to_value):
    return Evaluator(EVAL_WITHIN_RANGE, [from_value, to_value])


def OutsideRange(from_value, to_value):
    return Evaluator(EVAL_OUTSIDE_RANGE, [from_value, to_value])


def NoValue():
    return Evaluator(EVAL_NO_VALUE, [])


@attr.s
class TimeRange(object):
    """A time range for an alert condition.

    A condition has to hold for this length of time before triggering.

    :param str from_time: Either a number + unit (s: second, m: minute,
        h: hour, etc)  e.g. ``"5m"`` for 5 minutes, or ``"now"``.
    :param str to_time: Either a number + unit (s: second, m: minute,
        h: hour, etc)  e.g. ``"5m"`` for 5 minutes, or ``"now"``.
    """

    from_time = attr.ib()
    to_time = attr.ib()

    def to_json_data(self):
        return [self.from_time, self.to_time]


@attr.s
class AlertCondition(object):
    """
    A condition on an alert.

    :param Target target: Metric the alert condition is based on.
    :param Evaluator evaluator: How we decide whether we should alert on the
        metric. e.g. ``GreaterThan(5)`` means the metric must be greater than 5
        to trigger the condition. See ``GreaterThan``, ``LowerThan``,
        ``WithinRange``, ``OutsideRange``, ``NoValue``.
    :param TimeRange timeRange: How long the condition must be true for before
        we alert.
    :param operator: One of ``OP_AND`` or ``OP_OR``. How this condition
        combines with other conditions.
    :param reducerType: RTYPE_*
    :param type: CTYPE_*
    """

    target = attr.ib(validator=instance_of(Target))
    evaluator = attr.ib(validator=instance_of(Evaluator))
    timeRange = attr.ib(validator=instance_of(TimeRange))
    operator = attr.ib()
    reducerType = attr.ib()
    type = attr.ib(default=CTYPE_QUERY)

    def to_json_data(self):
        queryParams = [self.target.refId] + self.timeRange
        return {
            "evaluator": self.evaluator,
            "operator": {
                "type": self.operator,
            },
            "query": {
                "model": self.target,
                "params": queryParams,
            },
            "reducer": {
                "params": [],
                "type": self.reducerType,
            },
            "type": self.type,
        }


@attr.s
class Alert(object):

    name = attr.ib()
    message = attr.ib()
    alertConditions = attr.ib()
    executionErrorState = attr.ib(default=STATE_ALERTING)
    frequency = attr.ib(default="60s")
    handler = attr.ib(default=1)
    noDataState = attr.ib(default=STATE_NO_DATA)
    notifications = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            "conditions": self.alertConditions,
            "executionErrorState": self.executionErrorState,
            "frequency": self.frequency,
            "handler": self.handler,
            "message": self.message,
            "name": self.name,
            "noDataState": self.noDataState,
            "notifications": self.notifications,
        }


@attr.s
class Dashboard(object):

    title = attr.ib()
    rows = attr.ib()
    annotations = attr.ib(
        default=Annotations(),
        validator=instance_of(Annotations),
    )
    editable = attr.ib(
        default=True,
        validator=instance_of(bool),
    )
    gnetId = attr.ib(default=None)
    hideControls = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    id = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    refresh = attr.ib(default=DEFAULT_REFRESH)
    schemaVersion = attr.ib(default=SCHEMA_VERSION)
    sharedCrosshair = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    style = attr.ib(default=DARK_STYLE)
    tags = attr.ib(default=attr.Factory(list))
    templating = attr.ib(
        default=Templating(),
        validator=instance_of(Templating),
    )
    time = attr.ib(
        default=DEFAULT_TIME,
        validator=instance_of(Time),
    )
    timePicker = attr.ib(
        default=DEFAULT_TIME_PICKER,
        validator=instance_of(TimePicker),
    )
    timezone = attr.ib(default=UTC)
    version = attr.ib(default=0)

    def _iter_panels(self):
        for row in self.rows:
            for panel in row._iter_panels():
                yield panel

    def _map_panels(self, f):
        return attr.assoc(self, rows=[r._map_panels(f) for r in self.rows])

    def auto_panel_ids(self):
        """Give unique IDs all the panels without IDs.

        Returns a new ``Dashboard`` that is the same as this one, except all
        of the panels have their ``id`` property set. Any panels which had an
        ``id`` property set will keep that property, all others will have
        auto-generated IDs provided for them.
        """
        ids = set([panel.id for panel in self._iter_panels() if panel.id])
        auto_ids = (i for i in itertools.count(1) if i not in ids)

        def set_id(panel):
            return panel if panel.id else attr.assoc(panel, id=next(auto_ids))
        return self._map_panels(set_id)

    def to_json_data(self):
        return {
            'annotations': self.annotations,
            'editable': self.editable,
            'gnetId': self.gnetId,
            'hideControls': self.hideControls,
            'id': self.id,
            'links': self.links,
            'refresh': self.refresh,
            'rows': self.rows,
            'schemaVersion': self.schemaVersion,
            'sharedCrosshair': self.sharedCrosshair,
            'style': self.style,
            'tags': self.tags,
            'templating': self.templating,
            'title': self.title,
            'time': self.time,
            'timepicker': self.timePicker,
            'timezone': self.timezone,
            'version': self.version,
        }


@attr.s
class Graph(object):

    title = attr.ib()
    dataSource = attr.ib()
    targets = attr.ib()
    aliasColors = attr.ib(default=attr.Factory(dict))
    bars = attr.ib(default=False, validator=instance_of(bool))
    editable = attr.ib(default=True, validator=instance_of(bool))
    error = attr.ib(default=False, validator=instance_of(bool))
    fill = attr.ib(default=1, validator=instance_of(int))
    grid = attr.ib(default=attr.Factory(Grid), validator=instance_of(Grid))
    id = attr.ib(default=None)
    isNew = attr.ib(default=True, validator=instance_of(bool))
    legend = attr.ib(
        default=attr.Factory(Legend),
        validator=instance_of(Legend),
    )
    lines = attr.ib(default=True, validator=instance_of(bool))
    lineWidth = attr.ib(default=DEFAULT_LINE_WIDTH)
    links = attr.ib(default=attr.Factory(list))
    nullPointMode = attr.ib(default=NULL_CONNECTED)
    percentage = attr.ib(default=False, validator=instance_of(bool))
    pointRadius = attr.ib(default=DEFAULT_POINT_RADIUS)
    points = attr.ib(default=False, validator=instance_of(bool))
    renderer = attr.ib(default=DEFAULT_RENDERER)
    seriesOverrides = attr.ib(default=attr.Factory(list))
    span = attr.ib(default=None)
    stack = attr.ib(default=False, validator=instance_of(bool))
    steppedLine = attr.ib(default=False, validator=instance_of(bool))
    timeFrom = attr.ib(default=None)
    timeShift = attr.ib(default=None)
    tooltip = attr.ib(
        default=attr.Factory(Tooltip),
        validator=instance_of(Tooltip),
    )
    xAxis = attr.ib(default=attr.Factory(XAxis), validator=instance_of(XAxis))
    # XXX: This isn't a *good* default, rather it's the default Grafana uses.
    yAxes = attr.ib(
        default=attr.Factory(lambda: [YAxis(format=SHORT_FORMAT)] * 2))
    alert = attr.ib(default=None)

    def to_json_data(self):
        graphObject = {
            'aliasColors': self.aliasColors,
            'bars': self.bars,
            'datasource': self.dataSource,
            'editable': self.editable,
            'error': self.error,
            'fill': self.fill,
            'grid': self.grid,
            'id': self.id,
            'isNew': self.isNew,
            'legend': self.legend,
            'lines': self.lines,
            'linewidth': self.lineWidth,
            'links': self.links,
            'nullPointMode': self.nullPointMode,
            'percentage': self.percentage,
            'pointradius': self.pointRadius,
            'points': self.points,
            'renderer': self.renderer,
            'seriesOverrides': self.seriesOverrides,
            'span': self.span,
            'stack': self.stack,
            'steppedLine': self.steppedLine,
            'targets': self.targets,
            'timeFrom': self.timeFrom,
            'timeShift': self.timeShift,
            'title': self.title,
            'tooltip': self.tooltip,
            'type': GRAPH_TYPE,
            'xaxis': self.xAxis,
            'yaxes': self.yAxes,
        }
        if self.alert:
            graphObject['alert'] = self.alert
        return graphObject


@attr.s
class SparkLine(object):
    fillColor = attr.ib(default=BLUE_RGBA, validator=instance_of(RGBA))
    full = attr.ib(default=False, validator=instance_of(bool))
    lineColor = attr.ib(default=BLUE_RGB, validator=instance_of(RGB))
    show = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'fillColor': self.fillColor,
            'full': self.full,
            'lineColor': self.lineColor,
            'show': self.show,
        }


@attr.s
class ValueMap(object):
    op = attr.ib()
    text = attr.ib()
    value = attr.ib()

    def to_json_data(self):
        return {
            'op': self.op,
            'text': self.text,
            'value': self.value,
        }


@attr.s
class RangeMap(object):
    start = attr.ib()
    end = attr.ib()
    text = attr.ib()

    def to_json_data(self):
        return {
            'from': self.start,
            'to': self.end,
            'text': self.text,
        }


@attr.s
class Gauge(object):

    minValue = attr.ib(default=0, validator=instance_of(int))
    maxValue = attr.ib(default=100, validator=instance_of(int))
    show = attr.ib(default=False, validator=instance_of(bool))
    thresholdLabels = attr.ib(default=False, validator=instance_of(bool))
    thresholdMarkers = attr.ib(default=True, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'maxValue': self.maxValue,
            'minValue': self.minValue,
            'show': self.show,
            'thresholdLabels': self.thresholdLabels,
            'thresholdMarkers': self.thresholdMarkers,
        }


@attr.s
class SingleStat(object):
    """Generates Signle Stat panel json structure

    Grafana doc on singlestat: http://docs.grafana.org/reference/singlestat/

    :param dataSource: Grafana datasource name
    :param targets: list of metric requests for chousen datasource
    :param title: panel title
    :param cacheTimeout: metric query result cache ttl
    :param colors: the list of colors that can be used for coloring
        panel value or background. Additional info on coloring in docs:
        http://docs.grafana.org/reference/singlestat/#coloring
    :param colorBackground: defines if grafana will color panel background
    :param colorValue: defines if grafana will color panel value
    :param description: optional panel description
    :param decimals: override automatic decimal precision for legend/tooltips
    :param editable: defines if panel is editable via web interfaces
    :param format: defines value units
    :param gauge: draws and additional speedometer-like gauge based
    :param height: defines panel height
    :param hideTimeOverride: hides time overrides
    :param id: panel id
    :param interval: defines time interval between metric queries
    :param links: additional web links
    :param mappingType: defines panel mapping type.
        Additional info can be found in docs:
        http://docs.grafana.org/reference/singlestat/#value-to-text-mapping
    :param mappingTypes: the list of available mapping types for panel
    :param maxDataPoints: maximum metric query results,
        that will be used for rendering
    :param minSpan: minimum span number
    :param nullText: defines what to show if metric query result is undefined
    :param nullPointMode: defines how to render undefined values
    :param postfix: defines postfix that will be attached to value
    :param postfixFontSize: defines postfix font size
    :param prefix: defines prefix that will be attached to value
    :param prefixFontSize: defines prefix font size
    :param rangeMaps: the list of value to text mappings
    :param span: defines the number of spans that will be used for panel
    :param sparkline: defines if grafana should draw an additional sparkline.
        Sparkline grafana documentation:
        http://docs.grafana.org/reference/singlestat/#spark-lines
    :param thresholds: single stat thresholds
    :param transparent: defines if panel should be transparent
    :param valueFontSize: defines value font size
    :param valueName: defines value type. possible values are:
        min, max, avg, current, total, name, first, delta, range
    :param valueMaps: the list of value to text mappings
    """

    dataSource = attr.ib()
    targets = attr.ib()
    title = attr.ib()
    cacheTimeout = attr.ib(default=None)
    colors = attr.ib(default=[GREEN, ORANGE, RED])
    colorBackground = attr.ib(default=False, validator=instance_of(bool))
    colorValue = attr.ib(default=False, validator=instance_of(bool))
    description = attr.ib(default=None)
    decimals = attr.ib(default=None)
    editable = attr.ib(default=True, validator=instance_of(bool))
    format = attr.ib(default="none")
    gauge = attr.ib(default=attr.Factory(Gauge),
                    validator=instance_of(Gauge))
    height = attr.ib(default=None)
    hideTimeOverride = attr.ib(default=False, validator=instance_of(bool))
    id = attr.ib(default=None)
    interval = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    mappingType = attr.ib(default=MAPPING_TYPE_VALUE_TO_TEXT)
    mappingTypes = attr.ib(default=[MAPPING_VALUE_TO_TEXT,
                                    MAPPING_RANGE_TO_TEXT])
    maxDataPoints = attr.ib(default=100)
    minSpan = attr.ib(default=None)
    nullText = attr.ib(default=None)
    nullPointMode = attr.ib(default="connected")
    postfix = attr.ib(default="")
    postfixFontSize = attr.ib(default="50%")
    prefix = attr.ib(default="")
    prefixFontSize = attr.ib(default="50%")
    rangeMaps = attr.ib(default=attr.Factory(list))
    repeat = attr.ib(default=None)
    span = attr.ib(default=6)
    sparkline = attr.ib(default=attr.Factory(SparkLine),
                        validator=instance_of(SparkLine))
    thresholds = attr.ib(default="")
    transparent = attr.ib(default=False, validator=instance_of(bool))
    valueFontSize = attr.ib(default="80%")
    valueName = attr.ib(default=VTYPE_DEFAULT)
    valueMaps = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            'cacheTimeout': self.cacheTimeout,
            'colorBackground': self.colorBackground,
            'colorValue': self.colorValue,
            'colors': self.colors,
            'datasource': self.dataSource,
            'decimals': self.decimals,
            'description': self.description,
            'editable': self.editable,
            'format': self.format,
            'gauge': self.gauge,
            'id': self.id,
            'interval': self.interval,
            'links': self.links,
            'height': self.height,
            'hideTimeOverride': self.hideTimeOverride,
            'mappingType': self.mappingType,
            'mappingTypes': self.mappingTypes,
            'maxDataPoints': self.maxDataPoints,
            'minSpan': self.minSpan,
            'nullPointMode': self.nullPointMode,
            'nullText': self.nullText,
            'postfix': self.postfix,
            'postfixFontSize': self.postfixFontSize,
            'prefix': self.prefix,
            'prefixFontSize': self.prefixFontSize,
            'rangeMaps': self.rangeMaps,
            'repeat': self.repeat,
            'span': self.span,
            'sparkline': self.sparkline,
            'targets': self.targets,
            'thresholds': self.thresholds,
            'title': self.title,
            'transparent': self.transparent,
            'type': SINGLESTAT_TYPE,
            'valueFontSize': self.valueFontSize,
            'valueMaps': self.valueMaps,
            'valueName': self.valueName
        }
