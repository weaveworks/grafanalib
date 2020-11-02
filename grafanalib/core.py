"""Low-level functions for building Grafana dashboards.

The functions in this module don't enforce Weaveworks policy, and only mildly
encourage it by way of some defaults. Rather, they are ways of building
arbitrary Grafana JSON.
"""

import itertools
import math

import string
import warnings
from numbers import Number

import attr
from attr.validators import in_, instance_of


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


@attr.s
class Percent(object):
    num = attr.ib(default=100, validator=instance_of(Number))

    def to_json_data(self):
        return '{}%'.format(self.num)


GREY1 = RGBA(216, 200, 27, 0.27)
GREY2 = RGBA(234, 112, 112, 0.22)
BLUE_RGBA = RGBA(31, 118, 189, 0.18)
BLUE_RGB = RGB(31, 120, 193)
GREEN = RGBA(50, 172, 45, 0.97)
ORANGE = RGBA(237, 129, 40, 0.89)
RED = RGBA(245, 54, 54, 0.9)
BLANK = RGBA(0, 0, 0, 0.0)

INDIVIDUAL = 'individual'
CUMULATIVE = 'cumulative'

NULL_CONNECTED = 'connected'
NULL_AS_ZERO = 'null as zero'
NULL_AS_NULL = 'null'

FLOT = 'flot'

ABSOLUTE_TYPE = 'absolute'
DASHBOARD_TYPE = 'dashboard'
GRAPH_TYPE = 'graph'
STAT_TYPE = 'stat'
SINGLESTAT_TYPE = 'singlestat'
TABLE_TYPE = 'table'
TEXT_TYPE = 'text'
ALERTLIST_TYPE = "alertlist"
BARGAUGE_TYPE = "bargauge"
GAUGE_TYPE = "gauge"
HEATMAP_TYPE = "heatmap"
STATUSMAP_TYPE = "flant-statusmap-panel"
SVG_TYPE = 'marcuscalidus-svg-panel'
PIE_CHART_TYPE = 'grafana-piechart-panel'

DEFAULT_FILL = 1
DEFAULT_REFRESH = '10s'
DEFAULT_ROW_HEIGHT = Pixels(250)
DEFAULT_LINE_WIDTH = 2
DEFAULT_POINT_RADIUS = 5
DEFAULT_RENDERER = FLOT
DEFAULT_STEP = 10
DEFAULT_LIMIT = 10
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
DAYS_FORMAT = "d"
HOURS_FORMAT = "h"
MINUTES_FORMAT = "m"
SECONDS_FORMAT = "s"
MILLISECONDS_FORMAT = "ms"
SHORT_FORMAT = "short"
BYTES_FORMAT = "bytes"
BITS_PER_SEC_FORMAT = "bps"
BYTES_PER_SEC_FORMAT = "Bps"
NONE_FORMAT = "none"
JOULE_FORMAT = "joule"
WATTHOUR_FORMAT = "watth"
WATT_FORMAT = "watt"
KWATT_FORMAT = "kwatt"
KWATTHOUR_FORMAT = "kwatth"
VOLT_FORMAT = "volt"
BAR_FORMAT = "pressurebar"
PSI_FORMAT = "pressurepsi"
CELSIUS_FORMAT = "celsius"
KELVIN_FORMAT = "kelvin"
GRAM_FORMAT = "massg"
EUR_FORMAT = "currencyEUR"
USD_FORMAT = "currencyUSD"
METER_FORMAT = "lengthm"
SQUARE_METER_FORMAT = "areaM2"
CUBIC_METER_FORMAT = "m3"
LITRE_FORMAT = "litre"
PERCENT_FORMAT = "percent"
VOLT_AMPERE_FORMAT = "voltamp"

# Alert rule state
STATE_NO_DATA = "no_data"
STATE_ALERTING = "alerting"
STATE_KEEP_LAST_STATE = "keep_state"
STATE_OK = "ok"

# Evaluator
EVAL_GT = "gt"
EVAL_LT = "lt"
EVAL_WITHIN_RANGE = "within_range"
EVAL_OUTSIDE_RANGE = "outside_range"
EVAL_NO_VALUE = "no_value"

# Reducer Type
# avg/min/max/sum/count/last/median/diff/percent_diff/count_non_null
RTYPE_AVG = "avg"
RTYPE_MIN = "min"
RTYPE_MAX = "max"
RTYPE_SUM = "sum"
RTYPE_COUNT = "count"
RTYPE_LAST = "last"
RTYPE_MEDIAN = "median"
RTYPE_DIFF = "diff"
RTYPE_PERCENT_DIFF = "percent_diff"
RTYPE_COUNT_NON_NULL = "count_non_null"

# Condition Type
CTYPE_QUERY = "query"

# Operator
OP_AND = "and"
OP_OR = "or"

# Text panel modes
TEXT_MODE_MARKDOWN = "markdown"
TEXT_MODE_HTML = "html"
TEXT_MODE_TEXT = "text"

# Datasource plugins
PLUGIN_ID_GRAPHITE = "graphite"
PLUGIN_ID_PROMETHEUS = "prometheus"
PLUGIN_ID_INFLUXDB = "influxdb"
PLUGIN_ID_OPENTSDB = "opentsdb"
PLUGIN_ID_ELASTICSEARCH = "elasticsearch"
PLUGIN_ID_CLOUDWATCH = "cloudwatch"

# Target formats
TIME_SERIES_TARGET_FORMAT = "time_series"
TABLE_TARGET_FORMAT = "table"

# Table Transforms
AGGREGATIONS_TRANSFORM = "timeseries_aggregations"
ANNOTATIONS_TRANSFORM = "annotations"
COLUMNS_TRANSFORM = "timeseries_to_columns"
JSON_TRANSFORM = "json"
ROWS_TRANSFORM = "timeseries_to_rows"
TABLE_TRANSFORM = "table"

# AlertList show selections
ALERTLIST_SHOW_CURRENT = "current"
ALERTLIST_SHOW_CHANGES = "changes"

# AlertList state filter options
ALERTLIST_STATE_OK = "ok"
ALERTLIST_STATE_PAUSED = "paused"
ALERTLIST_STATE_NO_DATA = "no_data"
ALERTLIST_STATE_EXECUTION_ERROR = "execution_error"
ALERTLIST_STATE_ALERTING = "alerting"

# Display Sort Order
SORT_ASC = 1
SORT_DESC = 2
SORT_IMPORTANCE = 3

# Template
REFRESH_NEVER = 0
REFRESH_ON_DASHBOARD_LOAD = 1
REFRESH_ON_TIME_RANGE_CHANGE = 2
SHOW = 0
HIDE_LABEL = 1
HIDE_VARIABLE = 2
SORT_DISABLED = 0
SORT_ALPHA_ASC = 1
SORT_ALPHA_DESC = 2
SORT_NUMERIC_ASC = 3
SORT_NUMERIC_DESC = 4
SORT_ALPHA_IGNORE_CASE_ASC = 5
SORT_ALPHA_IGNORE_CASE_DESC = 6

GAUGE_CALC_LAST = "last"
GAUGE_CALC_FIRST = "first"
GAUGE_CALC_MIN = "min"
GAUGE_CALC_MAX = "max"
GAUGE_CALC_MEAN = "mean"
GAUGE_CALC_TOTAL = "total"
GAUGE_CALC_COUNT = "count"
GAUGE_CALC_RANGE = "range"
GAUGE_CALC_DELTA = "delta"
GAUGE_CALC_STEP = "step"
GAUGE_CALC_DIFFERENCE = "difference"
GAUGE_CALC_LOGMIN = "logmin"
GAUGE_CALC_CHANGE_COUNT = "changeCount"
GAUGE_CALC_DISTINCT_COUNT = "distinctCount"

ORIENTATION_HORIZONTAL = "horizontal"
ORIENTATION_VERTICAL = "vertical"

GAUGE_DISPLAY_MODE_BASIC = "basic"
GAUGE_DISPLAY_MODE_LCD = "lcd"
GAUGE_DISPLAY_MODE_GRADIENT = "gradient"


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
    threshold1Color = attr.ib(
        default=attr.Factory(lambda: GREY1),
        validator=instance_of(RGBA),
    )
    threshold2 = attr.ib(default=None)
    threshold2Color = attr.ib(
        default=attr.Factory(lambda: GREY2),
        validator=instance_of(RGBA),
    )

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
    sort = attr.ib(default=None)
    sortDesc = attr.ib(default=False)

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
            'sort': self.sort,
            'sortDesc': self.sortDesc,
        }


@attr.s
class Target(object):
    """
    Metric to show.

    :param target: Graphite way to select data
    """

    expr = attr.ib(default="")
    format = attr.ib(default=TIME_SERIES_TARGET_FORMAT)
    legendFormat = attr.ib(default="")
    interval = attr.ib(default="", validator=instance_of(str))
    intervalFactor = attr.ib(default=2)
    metric = attr.ib(default="")
    refId = attr.ib(default="")
    step = attr.ib(default=DEFAULT_STEP)
    target = attr.ib(default="")
    instant = attr.ib(validator=instance_of(bool), default=False)
    datasource = attr.ib(default="")

    def to_json_data(self):
        return {
            'expr': self.expr,
            'target': self.target,
            'format': self.format,
            'interval': self.interval,
            'intervalFactor': self.intervalFactor,
            'legendFormat': self.legendFormat,
            'metric': self.metric,
            'refId': self.refId,
            'step': self.step,
            'instant': self.instant,
            'datasource': self.datasource,
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
    """A single Y axis.

    Grafana graphs have two Y axes: one on the left and one on the right.
    """
    decimals = attr.ib(default=None)
    format = attr.ib(default=None)
    label = attr.ib(default=None)
    logBase = attr.ib(default=1)
    max = attr.ib(default=None)
    min = attr.ib(default=0)
    show = attr.ib(default=True, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'decimals': self.decimals,
            'format': self.format,
            'label': self.label,
            'logBase': self.logBase,
            'max': self.max,
            'min': self.min,
            'show': self.show,
        }


@attr.s
class YAxes(object):
    """The pair of Y axes on a Grafana graph.

    Each graph has two Y Axes, a left one and a right one.
    """
    left = attr.ib(default=attr.Factory(lambda: YAxis(format=SHORT_FORMAT)),
                   validator=instance_of(YAxis))
    right = attr.ib(default=attr.Factory(lambda: YAxis(format=SHORT_FORMAT)),
                    validator=instance_of(YAxis))

    def to_json_data(self):
        return [
            self.left,
            self.right,
        ]


def single_y_axis(**kwargs):
    """Specify that a graph has a single Y axis.

    Parameters are those passed to `YAxis`. Returns a `YAxes` object (i.e. a
    pair of axes) that can be used as the yAxes parameter of a graph.
    """
    axis = YAxis(**kwargs)
    return YAxes(left=axis)


def to_y_axes(data):
    """Backwards compatibility for 'YAxes'.

    In grafanalib 0.1.2 and earlier, Y axes were specified as a list of two
    elements. Now, we have a dedicated `YAxes` type.

    This function converts a list of two `YAxis` values to a `YAxes` value,
    silently passes through `YAxes` values, warns about doing things the old
    way, and errors when there are invalid values.
    """
    if isinstance(data, YAxes):
        return data
    if not isinstance(data, (list, tuple)):
        raise ValueError(
            "Y axes must be either YAxes or a list of two values, got %r"
            % data)
    if len(data) != 2:
        raise ValueError(
            "Must specify exactly two YAxes, got %d: %r"
            % (len(data), data))
    warnings.warn(
        "Specify Y axes using YAxes or single_y_axis, rather than a "
        "list/tuple",
        DeprecationWarning, stacklevel=3)
    return YAxes(left=data[0], right=data[1])


def _balance_panels(panels):
    """Resize panels so they are evenly spaced."""
    allotted_spans = sum(panel.span if panel.span else 0 for panel in panels)
    no_span_set = [panel for panel in panels if panel.span is None]
    auto_span = math.ceil(
        (TOTAL_SPAN - allotted_spans) / (len(no_span_set) or 1))
    return [
        attr.evolve(panel, span=auto_span) if panel.span is None else panel
        for panel in panels
    ]


@attr.s
class Row(object):
    # TODO: jml would like to separate the balancing behaviour from this
    # layer.
    panels = attr.ib(default=attr.Factory(list), converter=_balance_panels)
    collapse = attr.ib(
        default=False, validator=instance_of(bool),
    )
    editable = attr.ib(
        default=True, validator=instance_of(bool),
    )
    height = attr.ib(
        default=attr.Factory(lambda: DEFAULT_ROW_HEIGHT),
        validator=instance_of(Pixels),
    )
    showTitle = attr.ib(default=None)
    title = attr.ib(default=None)
    repeat = attr.ib(default=None)

    def _iter_panels(self):
        return iter(self.panels)

    def _map_panels(self, f):
        return attr.evolve(self, panels=list(map(f, self.panels)))

    def to_json_data(self):
        showTitle = False
        title = "New row"
        if self.title is not None:
            showTitle = True
            title = self.title
        if self.showTitle is not None:
            showTitle = self.showTitle
        return {
            'collapse': self.collapse,
            'editable': self.editable,
            'height': self.height,
            'panels': self.panels,
            'showTitle': showTitle,
            'title': title,
            'repeat': self.repeat,
        }


@attr.s
class Annotations(object):
    list = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            'list': self.list,
        }


@attr.s
class DataLink(object):
    title = attr.ib()
    linkUrl = attr.ib(default="", validator=instance_of(str))
    isNewTab = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'title': self.title,
            'url': self.linkUrl,
            'targetBlank': self.isNewTab,
        }


@attr.s
class DataSourceInput(object):
    name = attr.ib()
    label = attr.ib()
    pluginId = attr.ib()
    pluginName = attr.ib()
    description = attr.ib(default="", validator=instance_of(str))

    def to_json_data(self):
        return {
            "description": self.description,
            "label": self.label,
            "name": self.name,
            "pluginId": self.pluginId,
            "pluginName": self.pluginName,
            "type": "datasource",
        }


@attr.s
class ConstantInput(object):
    name = attr.ib()
    label = attr.ib()
    value = attr.ib()
    description = attr.ib(default="", validator=instance_of(str))

    def to_json_data(self):
        return {
            "description": self.description,
            "label": self.label,
            "name": self.name,
            "type": "constant",
            "value": self.value,
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
    type = attr.ib(default=DASHBOARD_TYPE)

    def to_json_data(self):
        title = self.dashboard if self.title is None else self.title
        return {
            "dashUri": self.uri,
            "dashboard": self.dashboard,
            "keepTime": self.keepTime,
            "title": title,
            "type": self.type,
            "url": self.uri,
        }


@attr.s
class ExternalLink(object):
    '''ExternalLink creates a top-level link attached to a dashboard.

        :param url: the URL to link to
        :param title: the text of the link
        :param keepTime: if true, the URL params for the dashboard's
            current time period are appended
    '''
    uri = attr.ib()
    title = attr.ib()
    keepTime = attr.ib(
        default=False,
        validator=instance_of(bool),
    )

    def to_json_data(self):
        return {
            "keepTime": self.keepTime,
            "title": self.title,
            "type": 'link',
            "url": self.uri,
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
        :param refresh: Controls when to update values in the dropdown
        :param allValue: specify a custom all value with regex,
            globs or lucene syntax.
        :param includeAll: Add a special All option whose value includes
            all options.
        :param regex: Regex to filter or capture specific parts of the names
            return by your data source query.
        :param multi: If enabled, the variable will support the selection of
            multiple options at the same time.
        :param type: The template type, can be one of: query (default),
            interval, datasource, custom, constant, adhoc.
        :param hide: Hide this variable in the dashboard, can be one of:
            SHOW (default), HIDE_LABEL, HIDE_VARIABLE
    """

    name = attr.ib()
    query = attr.ib()
    _current = attr.ib(init=False, default=attr.Factory(dict))
    default = attr.ib(default=None)
    dataSource = attr.ib(default=None)
    label = attr.ib(default=None)
    allValue = attr.ib(default=None)
    includeAll = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    multi = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    options = attr.ib(default=attr.Factory(list))
    regex = attr.ib(default=None)
    useTags = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    tagsQuery = attr.ib(default=None)
    tagValuesQuery = attr.ib(default=None)
    refresh = attr.ib(default=REFRESH_ON_DASHBOARD_LOAD,
                      validator=instance_of(int))
    type = attr.ib(default='query')
    hide = attr.ib(default=SHOW)
    sort = attr.ib(default=SORT_ALPHA_ASC)

    def __attrs_post_init__(self):
        if self.type == 'custom':
            if len(self.options) == 0:
                for value in self.query.split(','):
                    is_default = value == self.default
                    option = {
                        "selected": is_default,
                        "text": value,
                        "value": value,
                    }
                    if is_default:
                        self._current = option
                    self.options.append(option)
            else:
                for option in self.options:
                    if option['selected']:
                        self._current = option
                        break
        else:
            self._current = {
                'text': self.default,
                'value': self.default,
                'tags': [],
            }

    def to_json_data(self):
        return {
            'allValue': self.allValue,
            'current': self._current,
            'datasource': self.dataSource,
            'hide': self.hide,
            'includeAll': self.includeAll,
            'label': self.label,
            'multi': self.multi,
            'name': self.name,
            'options': self.options,
            'query': self.query,
            'refresh': self.refresh,
            'regex': self.regex,
            'sort': self.sort,
            'type': self.type,
            'useTags': self.useTags,
            'tagsQuery': self.tagsQuery,
            'tagValuesQuery': self.tagValuesQuery,
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
        queryParams = [
            self.target.refId, self.timeRange.from_time, self.timeRange.to_time
        ]
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
    gracePeriod = attr.ib(default='5m')

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
            "for": self.gracePeriod,
        }


@attr.s
class Dashboard(object):

    title = attr.ib()
    rows = attr.ib()
    annotations = attr.ib(
        default=attr.Factory(Annotations),
        validator=instance_of(Annotations),
    )
    description = attr.ib(default="", validator=instance_of(str))
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
    inputs = attr.ib(default=attr.Factory(list))
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
        default=attr.Factory(Templating),
        validator=instance_of(Templating),
    )
    time = attr.ib(
        default=attr.Factory(lambda: DEFAULT_TIME),
        validator=instance_of(Time),
    )
    timePicker = attr.ib(
        default=attr.Factory(lambda: DEFAULT_TIME_PICKER),
        validator=instance_of(TimePicker),
    )
    timezone = attr.ib(default=UTC)
    version = attr.ib(default=0)
    uid = attr.ib(default=None)

    def _iter_panels(self):
        for row in self.rows:
            for panel in row._iter_panels():
                yield panel

    def _map_panels(self, f):
        return attr.evolve(self, rows=[r._map_panels(f) for r in self.rows])

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
            return panel if panel.id else attr.evolve(panel, id=next(auto_ids))
        return self._map_panels(set_id)

    def to_json_data(self):
        return {
            '__inputs': self.inputs,
            'annotations': self.annotations,
            "description": self.description,
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
            'uid': self.uid,
        }


@attr.s
class Graph(object):
    """
    Generates Graph panel json structure.

    :param dataLinks: list of data links hooked to datapoints on the graph
    :param dataSource: DataSource's name
    :param minSpan: Minimum width for each panel
    :param repeat: Template's name to repeat Graph on
    """

    title = attr.ib()
    targets = attr.ib()
    aliasColors = attr.ib(default=attr.Factory(dict))
    bars = attr.ib(default=False, validator=instance_of(bool))
    dataLinks = attr.ib(default=attr.Factory(list))
    dataSource = attr.ib(default=None)
    description = attr.ib(default=None)
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
    minSpan = attr.ib(default=None)
    nullPointMode = attr.ib(default=NULL_CONNECTED)
    percentage = attr.ib(default=False, validator=instance_of(bool))
    pointRadius = attr.ib(default=DEFAULT_POINT_RADIUS)
    points = attr.ib(default=False, validator=instance_of(bool))
    renderer = attr.ib(default=DEFAULT_RENDERER)
    repeat = attr.ib(default=None)
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
    transparent = attr.ib(default=False, validator=instance_of(bool))
    xAxis = attr.ib(default=attr.Factory(XAxis), validator=instance_of(XAxis))
    # XXX: This isn't a *good* default, rather it's the default Grafana uses.
    yAxes = attr.ib(
        default=attr.Factory(YAxes),
        converter=to_y_axes,
        validator=instance_of(YAxes),
    )
    alert = attr.ib(default=None)

    def to_json_data(self):
        graphObject = {
            'aliasColors': self.aliasColors,
            'bars': self.bars,
            'datasource': self.dataSource,
            'description': self.description,
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
            'minSpan': self.minSpan,
            'nullPointMode': self.nullPointMode,
            'options': {
                'dataLinks': self.dataLinks,
            },
            'percentage': self.percentage,
            'pointradius': self.pointRadius,
            'points': self.points,
            'renderer': self.renderer,
            'repeat': self.repeat,
            'seriesOverrides': self.seriesOverrides,
            'span': self.span,
            'stack': self.stack,
            'steppedLine': self.steppedLine,
            'targets': self.targets,
            'timeFrom': self.timeFrom,
            'timeShift': self.timeShift,
            'title': self.title,
            'tooltip': self.tooltip,
            'transparent': self.transparent,
            'type': GRAPH_TYPE,
            'xaxis': self.xAxis,
            'yaxes': self.yAxes,
        }
        if self.alert:
            graphObject['alert'] = self.alert
        return graphObject

    def _iter_targets(self):
        for target in self.targets:
            yield target

    def _map_targets(self, f):
        return attr.assoc(self, targets=[f(t) for t in self.targets])

    def auto_ref_ids(self):
        """Give unique IDs all the panels without IDs.

        Returns a new ``Graph`` that is the same as this one, except all of
        the metrics have their ``refId`` property set. Any panels which had
        an ``refId`` property set will keep that property, all others will
        have auto-generated IDs provided for them.
        """
        ref_ids = set([t.refId for t in self._iter_targets() if t.refId])
        double_candidate_refs = \
            [p[0] + p[1] for p
                in itertools.product(string.ascii_uppercase, repeat=2)]
        candidate_ref_ids = itertools.chain(
            string.ascii_uppercase,
            double_candidate_refs,
        )

        auto_ref_ids = (i for i in candidate_ref_ids if i not in ref_ids)

        def set_refid(t):
            return t if t.refId else attr.assoc(t, refId=next(auto_ref_ids))
        return self._map_targets(set_refid)


@attr.s
class SparkLine(object):
    fillColor = attr.ib(
        default=attr.Factory(lambda: BLUE_RGBA),
        validator=instance_of(RGBA),
    )
    full = attr.ib(default=False, validator=instance_of(bool))
    lineColor = attr.ib(
        default=attr.Factory(lambda: BLUE_RGB),
        validator=instance_of(RGB),
    )
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
class Text(object):
    """Generates a Text panel."""

    content = attr.ib()
    editable = attr.ib(default=True, validator=instance_of(bool))
    error = attr.ib(default=False, validator=instance_of(bool))
    height = attr.ib(default=None)
    id = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    mode = attr.ib(default=TEXT_MODE_MARKDOWN)
    span = attr.ib(default=None)
    title = attr.ib(default="")
    transparent = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'content': self.content,
            'editable': self.editable,
            'error': self.error,
            'height': self.height,
            'id': self.id,
            'links': self.links,
            'mode': self.mode,
            'span': self.span,
            'title': self.title,
            'transparent': self.transparent,
            'type': TEXT_TYPE,
        }


@attr.s
class AlertList(object):
    """Generates the AlertList Panel."""

    description = attr.ib(default="")
    id = attr.ib(default=None)
    limit = attr.ib(default=DEFAULT_LIMIT)
    links = attr.ib(default=attr.Factory(list))
    onlyAlertsOnDashboard = attr.ib(default=True, validator=instance_of(bool))
    show = attr.ib(default=ALERTLIST_SHOW_CURRENT)
    sortOrder = attr.ib(default=SORT_ASC, validator=in_([1, 2, 3]))
    span = attr.ib(default=6)
    stateFilter = attr.ib(default=attr.Factory(list))
    title = attr.ib(default="")
    transparent = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'description': self.description,
            'id': self.id,
            'limit': self.limit,
            'links': self.links,
            'onlyAlertsOnDashboard': self.onlyAlertsOnDashboard,
            'show': self.show,
            'sortOrder': self.sortOrder,
            'span': self.span,
            'stateFilter': self.stateFilter,
            'title': self.title,
            'transparent': self.transparent,
            'type': ALERTLIST_TYPE,
        }


@attr.s
class Stat(object):
    """Generates Stat panel json structure

    Grafana doc on stat: https://grafana.com/docs/grafana/latest/panels/visualizations/stat-panel/

    :param dataSource: Grafana datasource name
    :param targets: list of metric requests for chosen datasource
    :param title: panel title
    :param colorMode: defines if Grafana will color panel background: keys "value" "background"
    :param graphMode: defines if Grafana will draw graph: keys 'area' 'none'
    :param orientation: Stacking direction in case of multiple series or fields: keys 'auto' 'horizontal' 'vertical'
    :param alignment: defines value & title positioning: keys 'auto' 'centre'
    :param description: optional panel description
    :param editable: defines if panel is editable via web interfaces
    :param format: defines value units
    :param height: defines panel height
    :param id: panel id
    :param decimals: number of decimals to display
    :param interval: defines time interval between metric queries
    :param links: additional web links
    :param mappings: the list of values to text mappings
        This should be a list of StatMapping objects
        https://grafana.com/docs/grafana/latest/panels/field-configuration-options/#value-mapping
    :param reduceCalc: algorithm for reduction to a single value: keys
        'mean' 'lastNotNull' 'last' 'first' 'firstNotNull' 'min' 'max' 'sum' 'total'
    :param span: defines the number of spans that will be used for panel
    :param thresholds: single stat thresholds
    :param transparent: defines if the panel should be transparent
    """

    dataSource = attr.ib()
    targets = attr.ib()
    title = attr.ib()
    description = attr.ib(default=None)
    colorMode = attr.ib(default='value')
    graphMode = attr.ib(default='area')
    orientation = attr.ib(default='auto')
    alignment = attr.ib(default='auto')
    editable = attr.ib(default=True, validator=instance_of(bool))
    format = attr.ib(default='none')
    height = attr.ib(default=None)
    id = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    mappings = attr.ib(default=attr.Factory(list))
    span = attr.ib(default=6)
    thresholds = attr.ib(default='')
    timeFrom = attr.ib(default=None)
    transparent = attr.ib(default=False, validator=instance_of(bool))
    reduceCalc = attr.ib(default='mean', type=str)
    decimals = attr.ib(default=None)

    def to_json_data(self):
        return {
            'datasource': self.dataSource,
            'description': self.description,
            'editable': self.editable,
            'id': self.id,
            'links': self.links,
            'height': self.height,
            'fieldConfig': {
                'defaults': {
                    'custom': {},
                    'decimals': self.decimals,
                    'mappings': self.mappings,
                    'thresholds': {
                        'mode': 'absolute',
                        'steps': self.thresholds,
                    },
                    'unit': self.format
                }
            },
            'options': {
                'colorMode': self.colorMode,
                'graphMode': self.graphMode,
                'justifyMode': self.alignment,
                'orientation': self.orientation,
                'reduceOptions': {
                    'calcs': [
                        self.reduceCalc
                    ],
                    'fields': '',
                    'values': False
                }
            },
            'span': self.span,
            'targets': self.targets,
            'title': self.title,
            'transparent': self.transparent,
            'type': STAT_TYPE,
            'timeFrom': self.timeFrom,
        }


@attr.s
class StatMapping(object):
    """
    Generates json structure for the value mapping for the Stat panel:
    :param text: Sting that will replace input value
    :param value: Value to be replaced
    :param startValue: When using a range, the start value of the range
    :param endValue: When using a range, the end value of the range
    :param id: panel id
    """

    text = attr.ib()
    mapValue = attr.ib(default="", validator=instance_of(str))
    startValue = attr.ib(default="", validator=instance_of(str))
    endValue = attr.ib(default="", validator=instance_of(str))
    id = attr.ib(default=None)

    def to_json_data(self):
        mappingType = MAPPING_TYPE_VALUE_TO_TEXT if self.mapValue else MAPPING_TYPE_RANGE_TO_TEXT

        return {
            'operator': "",
            'text': self.text,
            'type': mappingType,
            'value': self.mapValue,
            'from': self.startValue,
            'to': self.endValue,
            'id': self.id
        }


@attr.s
class StatValueMapping(object):
    """
    Generates json structure for the value mappings for the StatPanel:
    :param text: Sting that will replace input value
    :param value: Value to be replaced
    :param id: panel id
    """

    text = attr.ib()
    mapValue = attr.ib(default="", validator=instance_of(str))
    id = attr.ib(default=None)

    def to_json_data(self):
        return StatMapping(self.text, mapValue=self.mapValue, id=self.id)


@attr.s
class StatRangeMapping(object):
    """
    Generates json structure for the value mappings for the StatPanel:
    :param text: Sting that will replace input value
    :param startValue: When using a range, the start value of the range
    :param endValue: When using a range, the end value of the range
    :param id: panel id
    """

    text = attr.ib()
    startValue = attr.ib(default="", validator=instance_of(str))
    endValue = attr.ib(default="", validator=instance_of(str))
    id = attr.ib(default=None)

    def to_json_data(self):
        return StatMapping(
            self.text,
            startValue=self.startValue,
            endValue=self.endValue,
            id=self.id
        )


@attr.s
class SingleStat(object):
    """Generates Single Stat panel json structure

    This panel was deprecated in Grafana 7.0, please use Stat instead

    Grafana doc on singlestat: https://grafana.com/docs/grafana/latest/features/panels/singlestat/

    :param dataSource: Grafana datasource name
    :param targets: list of metric requests for chosen datasource
    :param title: panel title
    :param cacheTimeout: metric query result cache ttl
    :param colors: the list of colors that can be used for coloring
        panel value or background. Additional info on coloring in docs:
        https://grafana.com/docs/grafana/latest/features/panels/singlestat/#coloring
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
        https://grafana.com/docs/grafana/latest/features/panels/singlestat/#value-to-text-mapping
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
        https://grafana.com/docs/grafana/latest/features/panels/singlestat/#spark-lines
    :param thresholds: single stat thresholds
    :param transparent: defines if panel should be transparent
    :param valueFontSize: defines value font size
    :param valueName: defines value type. possible values are:
        min, max, avg, current, total, name, first, delta, range
    :param valueMaps: the list of value to text mappings
    :param timeFrom: time range that Override relative time
    """

    dataSource = attr.ib()
    targets = attr.ib()
    title = attr.ib()
    cacheTimeout = attr.ib(default=None)
    colors = attr.ib(default=attr.Factory(lambda: [GREEN, ORANGE, RED]))
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
    mappingTypes = attr.ib(
        default=attr.Factory(lambda: [
            MAPPING_VALUE_TO_TEXT,
            MAPPING_RANGE_TO_TEXT,
        ]),
    )
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
    sparkline = attr.ib(
        default=attr.Factory(SparkLine),
        validator=instance_of(SparkLine),
    )
    thresholds = attr.ib(default="")
    transparent = attr.ib(default=False, validator=instance_of(bool))
    valueFontSize = attr.ib(default="80%")
    valueName = attr.ib(default=VTYPE_DEFAULT)
    valueMaps = attr.ib(default=attr.Factory(list))
    timeFrom = attr.ib(default=None)

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
            'valueName': self.valueName,
            'timeFrom': self.timeFrom,
        }


@attr.s
class DateColumnStyleType(object):
    TYPE = 'date'

    dateFormat = attr.ib(default="YYYY-MM-DD HH:mm:ss")

    def to_json_data(self):
        return {
            'dateFormat': self.dateFormat,
            'type': self.TYPE,
        }


@attr.s
class NumberColumnStyleType(object):
    TYPE = 'number'

    colorMode = attr.ib(default=None)
    colors = attr.ib(default=attr.Factory(lambda: [GREEN, ORANGE, RED]))
    thresholds = attr.ib(default=attr.Factory(list))
    decimals = attr.ib(default=2, validator=instance_of(int))
    unit = attr.ib(default=SHORT_FORMAT)

    def to_json_data(self):
        return {
            'colorMode': self.colorMode,
            'colors': self.colors,
            'decimals': self.decimals,
            'thresholds': self.thresholds,
            'type': self.TYPE,
            'unit': self.unit,
        }


@attr.s
class StringColumnStyleType(object):
    TYPE = 'string'
    decimals = attr.ib(default=2, validator=instance_of(int))
    colorMode = attr.ib(default=None)
    colors = attr.ib(default=attr.Factory(lambda: [GREEN, ORANGE, RED]))
    thresholds = attr.ib(default=attr.Factory(list))
    preserveFormat = attr.ib(validator=instance_of(bool), default=False)
    sanitize = attr.ib(validator=instance_of(bool), default=False)
    unit = attr.ib(default=SHORT_FORMAT)
    mappingType = attr.ib(default=MAPPING_TYPE_VALUE_TO_TEXT)
    valueMaps = attr.ib(default=attr.Factory(list))
    rangeMaps = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            'decimals': self.decimals,
            'colorMode': self.colorMode,
            'colors': self.colors,
            'thresholds': self.thresholds,
            'unit': self.unit,
            'mappingType': self.mappingType,
            'valueMaps': self.valueMaps,
            'rangeMaps': self.rangeMaps,
            'preserveFormat': self.preserveFormat,
            'sanitize': self.sanitize,
            'type': self.TYPE,
        }


@attr.s
class HiddenColumnStyleType(object):
    TYPE = 'hidden'

    def to_json_data(self):
        return {
            'type': self.TYPE,
        }


@attr.s
class ColumnStyle(object):

    alias = attr.ib(default="")
    pattern = attr.ib(default="")
    align = attr.ib(default="auto", validator=in_(
        ["auto", "left", "right", "center"]))
    link = attr.ib(validator=instance_of(bool), default=False)
    linkOpenInNewTab = attr.ib(validator=instance_of(bool), default=False)
    linkUrl = attr.ib(validator=instance_of(str), default="")
    linkTooltip = attr.ib(validator=instance_of(str), default="")
    type = attr.ib(
        default=attr.Factory(NumberColumnStyleType),
        validator=instance_of((
            DateColumnStyleType,
            HiddenColumnStyleType,
            NumberColumnStyleType,
            StringColumnStyleType,
        ))
    )

    def to_json_data(self):
        data = {
            'alias': self.alias,
            'pattern': self.pattern,
            'align': self.align,
            'link': self.link,
            'linkTargetBlank': self.linkOpenInNewTab,
            'linkUrl': self.linkUrl,
            'linkTooltip': self.linkTooltip,
        }
        data.update(self.type.to_json_data())
        return data


@attr.s
class ColumnSort(object):
    col = attr.ib(default=None)
    desc = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'col': self.col,
            'desc': self.desc,
        }


@attr.s
class Column(object):
    """Details of an aggregation column in a table panel.

    :param text: name of column
    :param value: aggregation function
    """

    text = attr.ib(default="Avg")
    value = attr.ib(default="avg")

    def to_json_data(self):
        return {
            'text': self.text,
            'value': self.value,
        }


def _style_columns(columns):
    """Generate a list of column styles given some styled columns.

    The 'Table' object in Grafana separates column definitions from column
    style definitions. However, when defining dashboards it can be very useful
    to define the style next to the column. This function helps that happen.

    :param columns: A list of (Column, ColumnStyle) pairs. The associated
        ColumnStyles must not have a 'pattern' specified. You can also provide
       'None' if you want to use the default styles.
    :return: A list of ColumnStyle values that can be used in a Grafana
        definition.
    """
    new_columns = []
    styles = []
    for column, style in columns:
        new_columns.append(column)
        if not style:
            continue
        if style.pattern and style.pattern != column.text:
            raise ValueError(
                "ColumnStyle pattern (%r) must match the column name (%r) if "
                "specified" % (style.pattern, column.text))
        styles.append(attr.evolve(style, pattern=column.text))
    return new_columns, styles


@attr.s
class Table(object):
    """Generates Table panel json structure

    Grafana doc on table: https://grafana.com/docs/grafana/latest/features/panels/table_panel/#table-panel

    :param columns: table columns for Aggregations view
    :param dataSource: Grafana datasource name
    :param description: optional panel description
    :param editable: defines if panel is editable via web interfaces
    :param fontSize: defines value font size
    :param height: defines panel height
    :param hideTimeOverride: hides time overrides
    :param id: panel id
    :param links: additional web links
    :param minSpan: minimum span number
    :param pageSize: rows per page (None is unlimited)
    :param scroll: scroll the table instead of displaying in full
    :param showHeader: show the table header
    :param span: defines the number of spans that will be used for panel
    :param styles: defines formatting for each column
    :param targets: list of metric requests for chosen datasource
    :param timeFrom: time range that Override relative time
    :param title: panel title
    :param transform: table style
    :param transparent: defines if panel should be transparent
    """

    dataSource = attr.ib()
    targets = attr.ib()
    title = attr.ib()
    columns = attr.ib(default=attr.Factory(list))
    description = attr.ib(default=None)
    editable = attr.ib(default=True, validator=instance_of(bool))
    fontSize = attr.ib(default="100%")
    height = attr.ib(default=None)
    hideTimeOverride = attr.ib(default=False, validator=instance_of(bool))
    id = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    minSpan = attr.ib(default=None)
    pageSize = attr.ib(default=None)
    repeat = attr.ib(default=None)
    scroll = attr.ib(default=True, validator=instance_of(bool))
    showHeader = attr.ib(default=True, validator=instance_of(bool))
    span = attr.ib(default=6)
    sort = attr.ib(
        default=attr.Factory(ColumnSort), validator=instance_of(ColumnSort))
    styles = attr.ib()
    timeFrom = attr.ib(default=None)

    transform = attr.ib(default=COLUMNS_TRANSFORM)
    transparent = attr.ib(default=False, validator=instance_of(bool))

    @styles.default
    def styles_default(self):
        return [
            ColumnStyle(
                alias="Time",
                pattern="Time",
                type=DateColumnStyleType(),
            ),
            ColumnStyle(
                alias="time",
                pattern="time",
                type=DateColumnStyleType(),
            ),
            ColumnStyle(
                pattern="/.*/",
            ),
        ]

    @classmethod
    def with_styled_columns(cls, columns, styles=None, **kwargs):
        """Construct a table where each column has an associated style.

        :param columns: A list of (Column, ColumnStyle) pairs, where the
            ColumnStyle is the style for the column and does not have a
            pattern set (or the pattern is set to exactly the column name).
            The ColumnStyle may also be None.
        :param styles: An optional list of extra column styles that will be
            appended to the table's list of styles.
        :param kwargs: Other parameters to the Table constructor.
        :return: A Table.
        """
        extraStyles = styles if styles else []
        columns, styles = _style_columns(columns)
        return cls(columns=columns, styles=styles + extraStyles, **kwargs)

    def to_json_data(self):
        return {
            'columns': self.columns,
            'datasource': self.dataSource,
            'description': self.description,
            'editable': self.editable,
            'fontSize': self.fontSize,
            'height': self.height,
            'hideTimeOverride': self.hideTimeOverride,
            'id': self.id,
            'links': self.links,
            'minSpan': self.minSpan,
            'pageSize': self.pageSize,
            'repeat': self.repeat,
            'scroll': self.scroll,
            'showHeader': self.showHeader,
            'span': self.span,
            'sort': self.sort,
            'styles': self.styles,
            'targets': self.targets,
            'timeFrom': self.timeFrom,
            'title': self.title,
            'transform': self.transform,
            'transparent': self.transparent,
            'type': TABLE_TYPE,
        }


@attr.s
class BarGauge(object):
    """Generates Bar Gauge panel json structure

    :param allValue: If All values should be shown or a Calculation
    :param cacheTimeout: metric query result cache ttl
    :param calc: Calculation to perform on metrics
    :param dataLinks: list of data links hooked to datapoints on the graph
    :param dataSource: Grafana datasource name
    :param decimals: override automatic decimal precision for legend/tooltips
    :param description: optional panel description
    :param displayMode: style to display bar gauge in
    :param editable: defines if panel is editable via web interfaces
    :param format: defines value units
    :param height: defines panel height
    :param hideTimeOverride: hides time overrides
    :param id: panel id
    :param interval: defines time interval between metric queries
    :param labels: oprion to show gauge level labels
    :param limit: limit of number of values to show when not Calculating
    :param links: additional web links
    :param max: maximum value of the gauge
    :param maxDataPoints: maximum metric query results,
        that will be used for rendering
    :param min: minimum value of the gauge
    :param minSpan: minimum span number
    :param orientation: orientation of the bar gauge
    :param rangeMaps: the list of value to text mappings
    :param span: defines the number of spans that will be used for panel
    :param targets: list of metric requests for chosen datasource
    :param thresholdLabel: label for gauge. Template Variables:
        "$__series_namei" "$__field_name" "$__cell_{N} / $__calc"
    :param thresholdMarkers: option to show marker of level on gauge
    :param thresholds: single stat thresholds
    :param timeFrom: time range that Override relative time
    :param title: panel title
    :param transparent: defines if panel should be transparent
    :param valueMaps: the list of value to text mappings
    """

    title = attr.ib()
    targets = attr.ib()
    allValues = attr.ib(default=False, validator=instance_of(bool))
    cacheTimeout = attr.ib(default=None)
    calc = attr.ib(default=GAUGE_CALC_MEAN)
    dataLinks = attr.ib(default=attr.Factory(list))
    dataSource = attr.ib(default=None)
    decimals = attr.ib(default=None)
    description = attr.ib(default=None)
    displayMode = attr.ib(
        default=GAUGE_DISPLAY_MODE_LCD,
        validator=in_(
            [
                GAUGE_DISPLAY_MODE_LCD,
                GAUGE_DISPLAY_MODE_BASIC,
                GAUGE_DISPLAY_MODE_GRADIENT,
            ]
        ),
    )
    editable = attr.ib(default=True, validator=instance_of(bool))
    format = attr.ib(default="none")
    height = attr.ib(default=None)
    hideTimeOverride = attr.ib(default=False, validator=instance_of(bool))
    id = attr.ib(default=None)
    interval = attr.ib(default=None)
    label = attr.ib(default=None)
    limit = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    max = attr.ib(default=100)
    maxDataPoints = attr.ib(default=100)
    min = attr.ib(default=0)
    minSpan = attr.ib(default=None)
    orientation = attr.ib(
        default=ORIENTATION_HORIZONTAL,
        validator=in_([ORIENTATION_HORIZONTAL, ORIENTATION_VERTICAL]),
    )
    rangeMaps = attr.ib(default=attr.Factory(list))
    repeat = attr.ib(default=None)
    span = attr.ib(default=6)
    thresholdLabels = attr.ib(default=False, validator=instance_of(bool))
    thresholdMarkers = attr.ib(default=True, validator=instance_of(bool))
    thresholds = attr.ib(
        default=attr.Factory(
            lambda: [
                Threshold("green", 0, 0.0),
                Threshold("red", 1, 80.0)
            ]
        ),
        validator=instance_of(list),
    )
    timeFrom = attr.ib(default=None)
    timeShift = attr.ib(default=None)
    transparent = attr.ib(default=False, validator=instance_of(bool))
    valueMaps = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            "cacheTimeout": self.cacheTimeout,
            "datasource": self.dataSource,
            "description": self.description,
            "editable": self.editable,
            "height": self.height,
            "hideTimeOverride": self.hideTimeOverride,
            "id": self.id,
            "interval": self.interval,
            "links": self.links,
            "maxDataPoints": self.maxDataPoints,
            "minSpan": self.minSpan,
            "options": {
                "displayMode": self.displayMode,
                "fieldOptions": {
                    "calcs": [self.calc],
                    "defaults": {
                        "decimals": self.decimals,
                        "max": self.max,
                        "min": self.min,
                        "title": self.label,
                        "unit": self.format,
                        "links": self.dataLinks,
                    },
                    "limit": self.limit,
                    "mappings": self.valueMaps,
                    "override": {},
                    "thresholds": self.thresholds,
                    "values": self.allValues,
                },
                "orientation": self.orientation,
                "showThresholdLabels": self.thresholdLabels,
                "showThresholdMarkers": self.thresholdMarkers,
            },
            "repeat": self.repeat,
            "span": self.span,
            "targets": self.targets,
            "timeFrom": self.timeFrom,
            "timeShift": self.timeShift,
            "title": self.title,
            "transparent": self.transparent,
            "type": BARGAUGE_TYPE,
        }


@attr.s
class GaugePanel(object):
    """Generates Gauge panel json structure

    :param allValue: If All values should be shown or a Calculation
    :param cacheTimeout: metric query result cache ttl
    :param calc: Calculation to perform on metrics
    :param dataLinks: list of data links hooked to datapoints on the graph
    :param dataSource: Grafana datasource name
    :param decimals: override automatic decimal precision for legend/tooltips
    :param description: optional panel description
    :param editable: defines if panel is editable via web interfaces
    :param format: defines value units
    :param height: defines panel height
    :param hideTimeOverride: hides time overrides
    :param id: panel id
    :param interval: defines time interval between metric queries
    :param labels: oprion to show gauge level labels
    :param limit: limit of number of values to show when not Calculating
    :param links: additional web links
    :param max: maximum value of the gauge
    :param maxDataPoints: maximum metric query results,
        that will be used for rendering
    :param min: minimum value of the gauge
    :param minSpan: minimum span number
    :param rangeMaps: the list of value to text mappings
    :param span: defines the number of spans that will be used for panel
    :param targets: list of metric requests for chosen datasource
    :param thresholdLabel: label for gauge. Template Variables:
        "$__series_namei" "$__field_name" "$__cell_{N} / $__calc"
    :param thresholdMarkers: option to show marker of level on gauge
    :param thresholds: single stat thresholds
    :param timeFrom: time range that Override relative time
    :param title: panel title
    :param transparent: defines if panel should be transparent
    :param valueMaps: the list of value to text mappings
    """

    title = attr.ib()
    targets = attr.ib()
    allValues = attr.ib(default=False, validator=instance_of(bool))
    cacheTimeout = attr.ib(default=None)
    calc = attr.ib(default=GAUGE_CALC_MEAN)
    dataLinks = attr.ib(default=attr.Factory(list))
    dataSource = attr.ib(default=None)
    decimals = attr.ib(default=None)
    description = attr.ib(default=None)
    editable = attr.ib(default=True, validator=instance_of(bool))
    format = attr.ib(default="none")
    height = attr.ib(default=None)
    hideTimeOverride = attr.ib(default=False, validator=instance_of(bool))
    id = attr.ib(default=None)
    interval = attr.ib(default=None)
    label = attr.ib(default=None)
    limit = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    max = attr.ib(default=100)
    maxDataPoints = attr.ib(default=100)
    min = attr.ib(default=0)
    minSpan = attr.ib(default=None)
    rangeMaps = attr.ib(default=attr.Factory(list))
    repeat = attr.ib(default=None)
    span = attr.ib(default=6)
    thresholdLabels = attr.ib(default=False, validator=instance_of(bool))
    thresholdMarkers = attr.ib(default=True, validator=instance_of(bool))
    thresholds = attr.ib(
        default=attr.Factory(
            lambda: [
                Threshold("green", 0, 0.0),
                Threshold("red", 1, 80.0)
            ]
        ),
        validator=instance_of(list),
    )
    timeFrom = attr.ib(default=None)
    timeShift = attr.ib(default=None)
    transparent = attr.ib(default=False, validator=instance_of(bool))
    valueMaps = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            "cacheTimeout": self.cacheTimeout,
            "datasource": self.dataSource,
            "description": self.description,
            "editable": self.editable,
            "height": self.height,
            "hideTimeOverride": self.hideTimeOverride,
            "id": self.id,
            "interval": self.interval,
            "links": self.links,
            "maxDataPoints": self.maxDataPoints,
            "minSpan": self.minSpan,
            "options": {
                "fieldOptions": {
                    "calcs": [self.calc],
                    "defaults": {
                        "decimals": self.decimals,
                        "max": self.max,
                        "min": self.min,
                        "title": self.label,
                        "unit": self.format,
                        "links": self.dataLinks,
                    },
                    "limit": self.limit,
                    "mappings": self.valueMaps,
                    "override": {},
                    "thresholds": self.thresholds,
                    "values": self.allValues,
                },
                "showThresholdLabels": self.thresholdLabels,
                "showThresholdMarkers": self.thresholdMarkers,
            },
            "repeat": self.repeat,
            "span": self.span,
            "targets": self.targets,
            "timeFrom": self.timeFrom,
            "timeShift": self.timeShift,
            "title": self.title,
            "transparent": self.transparent,
            "type": GAUGE_TYPE,
        }


@attr.s
class HeatmapColor(object):
    """A Color object for heatmaps

    :param cardColor
    :param colorScale
    :param colorScheme
    :param exponent
    :param max
    :param min
    :param mode
    """

    # Maybe cardColor should validate to RGBA object, not sure
    cardColor = attr.ib(default='#b4ff00', validator=instance_of(str))
    colorScale = attr.ib(default='sqrt', validator=instance_of(str))
    colorScheme = attr.ib(default='interpolateOranges')
    exponent = attr.ib(default=0.5, validator=instance_of(float))
    mode = attr.ib(default="spectrum", validator=instance_of(str))
    max = attr.ib(default=None)
    min = attr.ib(default=None)

    def to_json_data(self):
        return {
            "mode": self.mode,
            "cardColor": self.cardColor,
            "colorScale": self.colorScale,
            "exponent": self.exponent,
            "colorScheme": self.colorScheme,
            "max": self.max,
            "min": self.min,
        }


@attr.s
class Heatmap(object):
    """Generates Heatmap panel json structure (https://grafana.com/docs/grafana/latest/features/panels/heatmap/)

    :param heatmap
    :param cards: A heatmap card object: keys "cardPadding", "cardRound"
    :param color: Heatmap color object
    :param dataFormat: 'timeseries' or 'tsbuckets'
    :param yBucketBound: 'auto', 'upper', 'middle', 'lower'
    :param reverseYBuckets: boolean
    :param xBucketSize
    :param xBucketNumber
    :param yBucketSize
    :param yBucketNumber
    :param highlightCards: boolean
    :param hideZeroBuckets: boolean
    :param transparent: defines if the panel should be transparent
    """

    title = attr.ib()
    description = attr.ib(default=None)
    id = attr.ib(default=None)
    # The below does not really like the Legend class we have defined above
    legend = attr.ib(default={"show": False})
    links = attr.ib(default=None)
    targets = attr.ib(default=None)
    tooltip = attr.ib(
        default=attr.Factory(Tooltip),
        validator=instance_of(Tooltip),
    )
    span = attr.ib(default=None)

    cards = attr.ib(
        default={
            "cardPadding": None,
            "cardRound": None
        }
    )

    color = attr.ib(
        default=attr.Factory(HeatmapColor),
        validator=instance_of(HeatmapColor),
    )

    dataFormat = attr.ib(default='timeseries')
    datasource = attr.ib(default=None)
    heatmap = {}
    hideZeroBuckets = attr.ib(default=False)
    highlightCards = attr.ib(default=True)
    options = attr.ib(default=None)
    transparent = attr.ib(default=False, validator=instance_of(bool))

    xAxis = attr.ib(
        default=attr.Factory(XAxis),
        validator=instance_of(XAxis)
    )
    xBucketNumber = attr.ib(default=None)
    xBucketSize = attr.ib(default=None)

    yAxis = attr.ib(
        default=attr.Factory(YAxis),
        validator=instance_of(YAxis)
    )
    yBucketBound = attr.ib(default=None)
    yBucketNumber = attr.ib(default=None)
    yBucketSize = attr.ib(default=None)
    reverseYBuckets = attr.ib(default=False)

    def to_json_data(self):
        return {
            'cards': self.cards,
            'color': self.color,
            'dataFormat': self.dataFormat,
            'datasource': self.datasource,
            'description': self.description,
            'heatmap': self.heatmap,
            'hideZeroBuckets': self.hideZeroBuckets,
            'highlightCards': self.highlightCards,
            'id': self.id,
            'legend': self.legend,
            'links': self.links,
            'options': self.options,
            'reverseYBuckets': self.reverseYBuckets,
            'span': self.span,
            'targets': self.targets,
            'title': self.title,
            'tooltip': self.tooltip,
            'transparent': self.transparent,
            'type': HEATMAP_TYPE,
            'xAxis': self.xAxis,
            'xBucketNumber': self.xBucketNumber,
            'xBucketSize': self.xBucketSize,
            'yAxis': self.yAxis,
            'yBucketBound': self.yBucketBound,
            'yBucketNumber': self.yBucketNumber,
            'yBucketSize': self.yBucketSize
        }


@attr.s
class StatusmapColor(object):
    """A Color object for Statusmaps

    :param cardColor
    :param colorScale
    :param colorScheme
    :param exponent
    :param max
    :param min
    :param mode
    :param thresholds
    """

    # Maybe cardColor should validate to RGBA object, not sure
    cardColor = attr.ib(default='#b4ff00', validator=instance_of(str))
    colorScale = attr.ib(default='sqrt', validator=instance_of(str))
    colorScheme = attr.ib(default='GnYlRd', validator=instance_of(str))
    exponent = attr.ib(default=0.5, validator=instance_of(float))
    mode = attr.ib(default="spectrum", validator=instance_of(str))
    thresholds = attr.ib(default=[], validator=instance_of(list))
    max = attr.ib(default=None)
    min = attr.ib(default=None)

    def to_json_data(self):
        return {
            "mode": self.mode,
            "cardColor": self.cardColor,
            "colorScale": self.colorScale,
            "exponent": self.exponent,
            "colorScheme": self.colorScheme,
            "max": self.max,
            "min": self.min,
            "thresholds": self.thresholds
        }


@attr.s
class Statusmap(object):
    """Generates json structure for the flant-statusmap-panel visualisation plugin (https://grafana.com/grafana/plugins/flant-statusmap-panel/).

    :param alert
    :param cards: A statusmap card object: keys "cardRound", "cardMinWidth", "cardHSpacing", "cardVSpacing"
    :param color: A StatusmapColor object
    :param dataSource: Name of the datasource to use
    :param description: Description of the panel
    :param editable
    :param id
    :param isNew
    :param legend
    :param links
    :param minSpan
    :param nullPointMode
    :param span
    :param targets
    :param timeFrom
    :param timeShift
    :param title: Title of the panel
    :param tooltip
    :param transparent: Set panel transparency on/off
    :param xAxis
    :param yAxis
    """

    targets = attr.ib()
    title = attr.ib()

    alert = attr.ib(default=None)
    cards = attr.ib(
        default={
            "cardRound": None,
            "cardMinWidth": 5,
            "cardHSpacing": 2,
            "cardVSpacing": 2,
        }, validator=instance_of(dict))

    color = attr.ib(
        default=attr.Factory(StatusmapColor),
        validator=instance_of(StatusmapColor),
    )
    dataSource = attr.ib(default=None)
    description = attr.ib(default=None)
    editable = attr.ib(default=True, validator=instance_of(bool))
    id = attr.ib(default=None)

    isNew = attr.ib(default=True, validator=instance_of(bool))
    legend = attr.ib(
        default=attr.Factory(Legend),
        validator=instance_of(Legend),
    )
    links = attr.ib(default=attr.Factory(list))
    minSpan = attr.ib(default=None)
    nullPointMode = attr.ib(default=NULL_AS_ZERO)
    span = attr.ib(default=None)
    timeFrom = attr.ib(default=None)
    timeShift = attr.ib(default=None)
    tooltip = attr.ib(
        default=attr.Factory(Tooltip),
        validator=instance_of(Tooltip),
    )
    transparent = attr.ib(default=False, validator=instance_of(bool))
    xAxis = attr.ib(
        default=attr.Factory(XAxis),
        validator=instance_of(XAxis)
    )
    yAxis = attr.ib(
        default=attr.Factory(YAxis),
        validator=instance_of(YAxis)
    )

    def to_json_data(self):
        graphObject = {
            'datasource': self.dataSource,
            'description': self.description,
            'editable': self.editable,
            'color': self.color,
            'id': self.id,
            'isNew': self.isNew,
            'legend': self.legend,
            'links': self.links,
            'minSpan': self.minSpan,
            'nullPointMode': self.nullPointMode,
            'span': self.span,
            'targets': self.targets,
            'timeFrom': self.timeFrom,
            'timeShift': self.timeShift,
            'title': self.title,
            'tooltip': self.tooltip,
            'transparent': self.transparent,
            'type': STATUSMAP_TYPE,
            'xaxis': self.xAxis,
            'yaxis': self.yAxis,
        }
        if self.alert:
            graphObject['alert'] = self.alert
        return graphObject


@attr.s
class Svg(object):
    """Generates SVG panel json structure
    Grafana doc on SVG: https://grafana.com/grafana/plugins/marcuscalidus-svg-panel
    :param dataSource: Grafana datasource name
    :param targets: list of metric requests for chosen datasource
    :param title: panel title
    :param description: optional panel description
    :param editable: defines if panel is editable via web interfaces
    :param format: defines value units
    :param jsCodeFilePath: path to javascript file to be run on dashboard refresh
    :param jsCodeInitFilePath: path to javascript file to be run after the first initialization of the SVG
    :param height: defines panel height
    :param id: panel id
    :param interval: defines time interval between metric queries
    :param links: additional web links
    :param reduceCalc: algorithm for reduction to a single value: keys 'mean' 'lastNotNull' 'last' 'first' 'firstNotNull' 'min' 'max' 'sum' 'total'
    :param span: defines the number of spans that will be used for panel
    :param svgFilePath: path to SVG image file to be displayed
    """

    dataSource = attr.ib()
    targets = attr.ib()
    title = attr.ib()
    description = attr.ib(default=None)
    editable = attr.ib(default=True, validator=instance_of(bool))
    format = attr.ib(default="none")
    jsCodeFilePath = attr.ib(default="", validator=instance_of(str))
    jsCodeInitFilePath = attr.ib(default="", validator=instance_of(str))
    height = attr.ib(default=None)
    id = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    span = attr.ib(default=6)
    svgFilePath = attr.ib(default="", validator=instance_of(str))

    @staticmethod
    def read_file(file_path):
        if file_path:
            with open(file_path) as f:
                read_data = f.read()
            return read_data
        else:
            return ""

    def to_json_data(self):

        js_code = self.read_file(self.jsCodeFilePath)
        js_init_code = self.read_file(self.jsCodeInitFilePath)
        svg_data = self.read_file(self.svgFilePath)

        return {
            'datasource': self.dataSource,
            'description': self.description,
            'editable': self.editable,
            'id': self.id,
            'links': self.links,
            'height': self.height,
            'format': self.format,
            'js_code': js_code,
            'js_init_code': js_init_code,
            'span': self.span,
            'svg_data': svg_data,
            'targets': self.targets,
            'title': self.title,
            'type': SVG_TYPE,
            'useSVGBuilder': False
        }


@attr.s
class PieChart(object):
    """Generates Pie Chart panel json structure
    Grafana doc on Pie Chart: https://grafana.com/grafana/plugins/grafana-piechart-panel
    :param dataSource: Grafana datasource name
    :param targets: list of metric requests for chosen datasource
    :param title: panel title
    :param description: optional panel description
    :param editable: defines if panel is editable via web interfaces
    :param format: defines value units
    :param height: defines panel height
    :param id: panel id
    :param pieType: defines the shape of the pie chart (pie or donut)
    :param showLegend: defines if the legend should be shown
    :param showLegend: defines if the legend should show values
    :param legendType: defines where the legend position
    :param links: additional web links
    :param span: defines the number of spans that will be used for panel
    :param transparent: defines if the panel is transparent
    """

    dataSource = attr.ib()
    targets = attr.ib()
    title = attr.ib()
    description = attr.ib(default=None)
    editable = attr.ib(default=True, validator=instance_of(bool))
    format = attr.ib(default='none')
    height = attr.ib(default=None)
    id = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    legendType = attr.ib(default='Right side')
    pieType = attr.ib(default='pie')
    showLegend = attr.ib(default=True)
    showLegendValues = attr.ib(default=True)
    span = attr.ib(default=6)
    thresholds = attr.ib(default='')
    timeFrom = attr.ib(default=None)
    transparent = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'datasource': self.dataSource,
            'description': self.description,
            'editable': self.editable,
            'format': self.format,
            'id': self.id,
            'links': self.links,
            'pieType': self.pieType,
            'height': self.height,
            'fieldConfig': {
                'defaults': {
                    'custom': {},
                },
                'overrides': []
            },
            'legend': {
                'show': self.showLegend,
                'values': self.showLegendValues
            },
            'legendType': self.legendType,
            'span': self.span,
            'targets': self.targets,
            'title': self.title,
            'type': PIE_CHART_TYPE,
            'timeFrom': self.timeFrom,
            'transparent': self.transparent
        }


@attr.s
class Threshold(object):
    """Threshold for a gauge

    :param color: color of threshold
    :param index: index of color in gauge
    :param value: when to use this color will be null if index is 0
    """

    color = attr.ib()
    index = attr.ib(validator=instance_of(int))
    value = attr.ib(validator=instance_of(float))
    line = attr.ib(default=True, validator=instance_of(bool))
    op = attr.ib(default="gt")
    yaxis = attr.ib(default="left")

    def to_json_data(self):
        return {
            "op": self.op,
            "yaxis": self.yaxis,
            "color": self.color,
            "line": self.line,
            "index": self.index,
            "value": "null" if self.index == 0 else self.value,
        }


class SeriesOverride(object):
    alias = attr.ib()
    bars = attr.ib(default=False)
    lines = attr.ib(default=True)
    yaxis = attr.ib(default=1)
    color = attr.ib(default=None)

    def to_json_data(self):
        return {
            "alias": self.alias,
            "bars": self.bars,
            "lines": self.lines,
            "yaxis": self.yaxis,
            "color": self.color,
        }
