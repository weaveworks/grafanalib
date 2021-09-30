
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
        return "{}px".format(self.num)


@attr.s
class Percent(object):
    num = attr.ib(default=100, validator=instance_of(Number))

    def to_json_data(self):
        return "{}%".format(self.num)


GREY1 = RGBA(216, 200, 27, 0.27)
GREY2 = RGBA(234, 112, 112, 0.22)
BLUE_RGBA = RGBA(31, 118, 189, 0.18)
BLUE_RGB = RGB(31, 120, 193)
GREEN = RGBA(50, 172, 45, 0.97)
ORANGE = RGBA(237, 129, 40, 0.89)
RED = RGBA(245, 54, 54, 0.9)
BLANK = RGBA(0, 0, 0, 0.0)
WHITE = RGB(255, 255, 255)

INDIVIDUAL = 'individual'
CUMULATIVE = 'cumulative'

NULL_CONNECTED = 'connected'
NULL_AS_ZERO = 'null as zero'
NULL_AS_NULL = 'null'

FLOT = 'flot'

ABSOLUTE_TYPE = 'absolute'
DASHBOARD_TYPE = 'dashboard'
ROW_TYPE = 'row'
GRAPH_TYPE = 'graph'
DISCRETE_TYPE = 'natel-discrete-panel'
STAT_TYPE = 'stat'
SINGLESTAT_TYPE = 'singlestat'
TABLE_TYPE = 'table'
TEXT_TYPE = 'text'
ALERTLIST_TYPE = 'alertlist'
BARGAUGE_TYPE = 'bargauge'
GAUGE_TYPE = 'gauge'
DASHBOARDLIST_TYPE = 'dashlist'
LOGS_TYPE = 'logs'
HEATMAP_TYPE = 'heatmap'
STATUSMAP_TYPE = 'flant-statusmap-panel'
SVG_TYPE = 'marcuscalidus-svg-panel'
PIE_CHART_TYPE = 'grafana-piechart-panel'
WORLD_MAP_TYPE = 'grafana-worldmap-panel'

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

# (DEPRECATED: use formatunits.py) Y Axis formats
DURATION_FORMAT = 'dtdurations'
NO_FORMAT = 'none'
OPS_FORMAT = 'ops'
PERCENT_UNIT_FORMAT = 'percentunit'
DAYS_FORMAT = 'd'
HOURS_FORMAT = 'h'
MINUTES_FORMAT = 'm'
SECONDS_FORMAT = 's'
MILLISECONDS_FORMAT = 'ms'
SHORT_FORMAT = 'short'
BYTES_FORMAT = 'bytes'
BITS_PER_SEC_FORMAT = 'bps'
BYTES_PER_SEC_FORMAT = 'Bps'
NONE_FORMAT = 'none'
JOULE_FORMAT = 'joule'
WATTHOUR_FORMAT = 'watth'
WATT_FORMAT = 'watt'
KWATT_FORMAT = 'kwatt'
KWATTHOUR_FORMAT = 'kwatth'
VOLT_FORMAT = 'volt'
BAR_FORMAT = 'pressurebar'
PSI_FORMAT = 'pressurepsi'
CELSIUS_FORMAT = 'celsius'
KELVIN_FORMAT = 'kelvin'
GRAM_FORMAT = 'massg'
EUR_FORMAT = 'currencyEUR'
USD_FORMAT = 'currencyUSD'
METER_FORMAT = 'lengthm'
SQUARE_METER_FORMAT = 'areaM2'
CUBIC_METER_FORMAT = 'm3'
LITRE_FORMAT = 'litre'
PERCENT_FORMAT = 'percent'
VOLT_AMPERE_FORMAT = 'voltamp'

# Alert rule state
STATE_NO_DATA = 'no_data'
STATE_ALERTING = 'alerting'
STATE_KEEP_LAST_STATE = 'keep_state'
STATE_OK = 'ok'

# Evaluator
EVAL_GT = 'gt'
EVAL_LT = 'lt'
EVAL_WITHIN_RANGE = 'within_range'
EVAL_OUTSIDE_RANGE = 'outside_range'
EVAL_NO_VALUE = 'no_value'

# Reducer Type
# avg/min/max/sum/count/last/median/diff/percent_diff/count_non_null
RTYPE_AVG = 'avg'
RTYPE_MIN = 'min'
RTYPE_MAX = 'max'
RTYPE_SUM = 'sum'
RTYPE_COUNT = 'count'
RTYPE_LAST = 'last'
RTYPE_MEDIAN = 'median'
RTYPE_DIFF = 'diff'
RTYPE_PERCENT_DIFF = 'percent_diff'
RTYPE_COUNT_NON_NULL = 'count_non_null'

# Condition Type
CTYPE_QUERY = 'query'

# Operator
OP_AND = 'and'
OP_OR = 'or'

# Text panel modes
TEXT_MODE_MARKDOWN = 'markdown'
TEXT_MODE_HTML = 'html'
TEXT_MODE_TEXT = 'text'

# Datasource plugins
PLUGIN_ID_GRAPHITE = 'graphite'
PLUGIN_ID_PROMETHEUS = 'prometheus'
PLUGIN_ID_INFLUXDB = 'influxdb'
PLUGIN_ID_OPENTSDB = 'opentsdb'
PLUGIN_ID_ELASTICSEARCH = 'elasticsearch'
PLUGIN_ID_CLOUDWATCH = 'cloudwatch'

# Target formats
TIME_SERIES_TARGET_FORMAT = 'time_series'
TABLE_TARGET_FORMAT = 'table'

# Table Transforms
AGGREGATIONS_TRANSFORM = 'timeseries_aggregations'
ANNOTATIONS_TRANSFORM = 'annotations'
COLUMNS_TRANSFORM = 'timeseries_to_columns'
JSON_TRANSFORM = 'json'
ROWS_TRANSFORM = 'timeseries_to_rows'
TABLE_TRANSFORM = 'table'

# AlertList show selections
ALERTLIST_SHOW_CURRENT = 'current'
ALERTLIST_SHOW_CHANGES = 'changes'

# AlertList state filter options
ALERTLIST_STATE_OK = 'ok'
ALERTLIST_STATE_PAUSED = 'paused'
ALERTLIST_STATE_NO_DATA = 'no_data'
ALERTLIST_STATE_EXECUTION_ERROR = 'execution_error'
ALERTLIST_STATE_ALERTING = 'alerting'
ALERTLIST_STATE_PENDING = 'pending'

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

GAUGE_CALC_LAST = 'last'
GAUGE_CALC_FIRST = 'first'
GAUGE_CALC_MIN = 'min'
GAUGE_CALC_MAX = 'max'
GAUGE_CALC_MEAN = 'mean'
GAUGE_CALC_TOTAL = 'total'
GAUGE_CALC_COUNT = 'count'
GAUGE_CALC_RANGE = 'range'
GAUGE_CALC_DELTA = 'delta'
GAUGE_CALC_STEP = 'step'
GAUGE_CALC_DIFFERENCE = 'difference'
GAUGE_CALC_LOGMIN = 'logmin'
GAUGE_CALC_CHANGE_COUNT = 'changeCount'
GAUGE_CALC_DISTINCT_COUNT = 'distinctCount'

ORIENTATION_HORIZONTAL = 'horizontal'
ORIENTATION_VERTICAL = 'vertical'

GAUGE_DISPLAY_MODE_BASIC = 'basic'
GAUGE_DISPLAY_MODE_LCD = 'lcd'
GAUGE_DISPLAY_MODE_GRADIENT = 'gradient'

DEFAULT_AUTO_COUNT = 30
DEFAULT_MIN_AUTO_INTERVAL = '10s'


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

MAPPING_VALUE_TO_TEXT = Mapping('value to text', MAPPING_TYPE_VALUE_TO_TEXT)
MAPPING_RANGE_TO_TEXT = Mapping('range to text', MAPPING_TYPE_RANGE_TO_TEXT)


# Value types min/max/avg/current/total/name/first/delta/range
VTYPE_MIN = 'min'
VTYPE_MAX = 'max'
VTYPE_AVG = 'avg'
VTYPE_CURR = 'current'
VTYPE_TOTAL = 'total'
VTYPE_NAME = 'name'
VTYPE_FIRST = 'first'
VTYPE_DELTA = 'delta'
VTYPE_RANGE = 'range'
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


def is_valid_max_per_row(instance, attribute, value):
    if ((value is not None) and not isinstance(value, int)):
        raise ValueError("{attr} should either be None or an integer".format(
            attr=attribute))


@attr.s
class Repeat(object):
    """
    Panel repetition settings.

    :param direction: The direction into which to repeat ('h' or 'v')
    :param variable: The name of the variable over whose values to repeat
    :param maxPerRow: The maximum number of panels per row in horizontal repetition
    """

    direction = attr.ib(default=None)
    variable = attr.ib(default=None)
    maxPerRow = attr.ib(default=None, validator=is_valid_max_per_row)


def is_valid_target(instance, attribute, value):
    """
    Check if a given attribute is a valid target
    """
    if not hasattr(value, "refId"):
        raise ValueError(f"{attribute.name} should have 'refId' attribute")


@attr.s
class Target(object):
    """
    Metric to show.

    :param target: Graphite way to select data
    """

    expr = attr.ib(default="")
    format = attr.ib(default=TIME_SERIES_TARGET_FORMAT)
    hide = attr.ib(default=False, validator=instance_of(bool))
    legendFormat = attr.ib(default="")
    interval = attr.ib(default="", validator=instance_of(str))
    intervalFactor = attr.ib(default=2)
    metric = attr.ib(default="")
    refId = attr.ib(default="")
    step = attr.ib(default=DEFAULT_STEP)
    target = attr.ib(default="")
    instant = attr.ib(validator=instance_of(bool), default=False)
    datasource = attr.ib(default=None)

    def to_json_data(self):
        return {
            'expr': self.expr,
            'target': self.target,
            'format': self.format,
            'hide': self.hide,
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
    XAXIS_MODES = ('time', 'series')
    if value not in XAXIS_MODES:
        raise ValueError("{attr} should be one of {choice}".format(
            attr=attribute, choice=XAXIS_MODES))


@attr.s
class XAxis(object):
    """
    X Axis

    :param mode: Mode of axis can be time, series or histogram
    :param name: X axis name
    :param value: list of values eg. ["current"] or ["avg"]
    :param show: show X axis
    """

    mode = attr.ib(default='time', validator=is_valid_xaxis_mode)
    name = attr.ib(default=None)
    values = attr.ib(default=attr.Factory(list))
    show = attr.ib(validator=instance_of(bool), default=True)

    def to_json_data(self):
        return {
            'mode': self.mode,
            'name': self.name,
            'values': self.values,
            'show': self.show,
        }


@attr.s
class YAxis(object):
    """A single Y axis.

    Grafana graphs have two Y axes: one on the left and one on the right.

    :param decimals: Defines how many decimals are displayed for Y value. (default auto)
    :param format: The display unit for the Y value
    :param label: The Y axis label. (default “")
    :param logBase: The scale to use for the Y value, linear, or logarithmic. (default linear)
    :param max: The maximum Y value
    :param min: The minimum Y value
    :param show: Show or hide the axis
    """

    decimals = attr.ib(default=None)
    format = attr.ib(default=None)
    label = attr.ib(default=None)
    logBase = attr.ib(default=1)
    max = attr.ib(default=None)
    min = attr.ib(default=None)
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
class GridPos(object):
    """GridPos describes the panel size and position in grid coordinates.

    :param h: height of the panel, grid height units each represents
        30 pixels
    :param w: width of the panel 1-24 (the width of the dashboard
        is divided into 24 columns)
    :param x: x cordinate of the panel, in same unit as w
    :param y: y cordinate of the panel, in same unit as h
    """

    h = attr.ib()
    w = attr.ib()
    x = attr.ib()
    y = attr.ib()

    def to_json_data(self):
        return {
            'h': self.h,
            'w': self.w,
            'x': self.x,
            'y': self.y
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
            'description': self.description,
            'label': self.label,
            'name': self.name,
            'pluginId': self.pluginId,
            'pluginName': self.pluginName,
            'type': 'datasource',
        }


@attr.s
class ConstantInput(object):
    name = attr.ib()
    label = attr.ib()
    value = attr.ib()
    description = attr.ib(default="", validator=instance_of(str))

    def to_json_data(self):
        return {
            'description': self.description,
            'label': self.label,
            'name': self.name,
            'type': 'constant',
            'value': self.value,
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
            'dashUri': self.uri,
            'dashboard': self.dashboard,
            'keepTime': self.keepTime,
            'title': title,
            'type': self.type,
            'url': self.uri,
        }


@attr.s
class ExternalLink(object):
    """ExternalLink creates a top-level link attached to a dashboard.

    :param url: the URL to link to
    :param title: the text of the link
    :param keepTime: if true, the URL params for the dashboard's
        current time period are appended
    """
    uri = attr.ib()
    title = attr.ib()
    keepTime = attr.ib(
        default=False,
        validator=instance_of(bool),
    )

    def to_json_data(self):
        return {
            'keepTime': self.keepTime,
            'title': self.title,
            'type': 'link',
            'url': self.uri,
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
    :param auto: Interval will be dynamically calculated by dividing time range by the count specified in auto_count.
    :param autoCount: Number of intervals for dividing the time range.
    :param autoMin: Smallest interval for auto interval generator.
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
    auto = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    autoCount = attr.ib(
        default=DEFAULT_AUTO_COUNT,
        validator=instance_of(int)
    )
    autoMin = attr.ib(default=DEFAULT_MIN_AUTO_INTERVAL)

    def __attrs_post_init__(self):
        if self.type == 'custom':
            if len(self.options) == 0:
                for value in self.query.split(','):
                    is_default = value == self.default
                    option = {
                        'selected': is_default,
                        'text': value,
                        'value': value,
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
                'selected': False if self.default is None or not self.default else True,
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
            'auto': self.auto,
            'auto_min': self.autoMin,
            'auto_count': self.autoCount
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
    """
    Time Picker

    :param refreshIntervals: dashboard auto-refresh interval options
    :param timeOptions: dashboard time range options
    :param hidden: hide the time picker from dashboard
    """
    refreshIntervals = attr.ib()
    timeOptions = attr.ib()
    hidden = attr.ib(
        default=False,
        validator=instance_of(bool),
    )

    def to_json_data(self):
        return {
            'refresh_intervals': self.refreshIntervals,
            'time_options': self.timeOptions,
            'hidden': self.hidden
        }


DEFAULT_TIME_PICKER = TimePicker(
    refreshIntervals=[
        '5s',
        '10s',
        '30s',
        '1m',
        '5m',
        '15m',
        '30m',
        '1h',
        '2h',
        '1d'
    ],
    timeOptions=[
        '5m',
        '15m',
        '1h',
        '6h',
        '12h',
        '24h',
        '2d',
        '7d',
        '30d'
    ]
)


@attr.s
class Evaluator(object):
    type = attr.ib()
    params = attr.ib()

    def to_json_data(self):
        return {
            'type': self.type,
            'params': self.params,
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

    target = attr.ib(validator=is_valid_target)
    evaluator = attr.ib(validator=instance_of(Evaluator))
    timeRange = attr.ib(validator=instance_of(TimeRange))
    operator = attr.ib()
    reducerType = attr.ib()
    type = attr.ib(default=CTYPE_QUERY, kw_only=True)

    def to_json_data(self):
        queryParams = [
            self.target.refId, self.timeRange.from_time, self.timeRange.to_time
        ]
        return {
            'evaluator': self.evaluator,
            'operator': {
                'type': self.operator,
            },
            'query': {
                'model': self.target,
                'params': queryParams,
            },
            'reducer': {
                'params': [],
                'type': self.reducerType,
            },
            'type': self.type,
        }


@attr.s
class Alert(object):
    """
    :param alertRuleTags: Key Value pairs to be sent with Alert notifications.
    """
    name = attr.ib()
    message = attr.ib()
    alertConditions = attr.ib()
    executionErrorState = attr.ib(default=STATE_ALERTING)
    frequency = attr.ib(default='60s')
    handler = attr.ib(default=1)
    noDataState = attr.ib(default=STATE_NO_DATA)
    notifications = attr.ib(default=attr.Factory(list))
    gracePeriod = attr.ib(default='5m')
    alertRuleTags = attr.ib(
        default=attr.Factory(dict),
        validator=attr.validators.deep_mapping(
            key_validator=attr.validators.instance_of(str),
            value_validator=attr.validators.instance_of(str),
            mapping_validator=attr.validators.instance_of(dict),
        )
    )

    def to_json_data(self):
        return {
            'conditions': self.alertConditions,
            'executionErrorState': self.executionErrorState,
            'frequency': self.frequency,
            'handler': self.handler,
            'message': self.message,
            'name': self.name,
            'noDataState': self.noDataState,
            'notifications': self.notifications,
            'for': self.gracePeriod,
            'alertRuleTags': self.alertRuleTags,
        }


@attr.s
class Notification(object):

    uid = attr.ib()

    def to_json_data(self):
        return {
            'uid': self.uid,
        }


@attr.s
class Dashboard(object):

    title = attr.ib()
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
    panels = attr.ib(default=attr.Factory(list), validator=instance_of(list))
    refresh = attr.ib(default=DEFAULT_REFRESH)
    rows = attr.ib(default=attr.Factory(list), validator=instance_of(list))
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

        for panel in self.panels:
            if hasattr(panel, 'panels'):
                yield panel
                for row_panel in panel._iter_panels():
                    yield panel
            else:
                yield panel

    def _map_panels(self, f):
        return attr.evolve(
            self,
            rows=[r._map_panels(f) for r in self.rows],
            panels=[p._map_panels(f) for p in self.panels]
        )

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
        if self.panels and self.rows:
            print(
                "Warning: You are using both panels and rows in this dashboard, please use one or the other. "
                "Panels should be used in preference over rows, see example dashboard for help."
            )
        return {
            '__inputs': self.inputs,
            'annotations': self.annotations,
            'description': self.description,
            'editable': self.editable,
            'gnetId': self.gnetId,
            'hideControls': self.hideControls,
            'id': self.id,
            'links': self.links,
            'panels': self.panels if not self.rows else [],
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


def _deep_update(base_dict, extra_dict):
    if extra_dict is None:
        return base_dict

    for k, v in extra_dict.items():
        if k in base_dict and hasattr(base_dict[k], "to_json_data"):
            base_dict[k] = base_dict[k].to_json_data()

        if k in base_dict and isinstance(base_dict[k], dict):
            _deep_update(base_dict[k], v)
        else:
            base_dict[k] = v


@attr.s
class Panel(object):
    """
    Generic panel for shared defaults

    :param cacheTimeout: metric query result cache ttl
    :param dataSource: Grafana datasource name
    :param description: optional panel description
    :param editable: defines if panel is editable via web interfaces
    :param height: defines panel height
    :param hideTimeOverride: hides time overrides
    :param id: panel id
    :param interval: defines time interval between metric queries
    :param links: additional web links
    :param maxDataPoints: maximum metric query results,
           that will be used for rendering
    :param minSpan: minimum span number
    :param repeat: Template's name to repeat Graph on
    :param span: defines the number of spans that will be used for panel
    :param targets: list of metric requests for chosen datasource
    :param timeFrom: time range that Override relative time
    :param title: of the panel
    :param transparent: defines if panel should be transparent
    :param transformations: defines transformations applied to the table
    :param extraJson: raw JSON additions or overrides added to the JSON output
           of this panel, can be used for using unsupported features
    """

    dataSource = attr.ib(default=None)
    targets = attr.ib(default=attr.Factory(list), validator=instance_of(list))
    title = attr.ib(default="")
    cacheTimeout = attr.ib(default=None)
    description = attr.ib(default=None)
    editable = attr.ib(default=True, validator=instance_of(bool))
    error = attr.ib(default=False, validator=instance_of(bool))
    height = attr.ib(default=None)
    gridPos = attr.ib(default=None)
    hideTimeOverride = attr.ib(default=False, validator=instance_of(bool))
    id = attr.ib(default=None)
    interval = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    maxDataPoints = attr.ib(default=100)
    minSpan = attr.ib(default=None)
    repeat = attr.ib(default=attr.Factory(Repeat), validator=instance_of(Repeat))
    span = attr.ib(default=None)
    timeFrom = attr.ib(default=None)
    timeShift = attr.ib(default=None)
    transparent = attr.ib(default=False, validator=instance_of(bool))
    transformations = attr.ib(default=attr.Factory(list), validator=instance_of(list))
    extraJson = attr.ib(default=None, validator=attr.validators.optional(instance_of(dict)))

    def _map_panels(self, f):
        return f(self)

    def panel_json(self, overrides):
        res = {
            'cacheTimeout': self.cacheTimeout,
            'datasource': self.dataSource,
            'description': self.description,
            'editable': self.editable,
            'error': self.error,
            'height': self.height,
            'gridPos': self.gridPos,
            'hideTimeOverride': self.hideTimeOverride,
            'id': self.id,
            'interval': self.interval,
            'links': self.links,
            'maxDataPoints': self.maxDataPoints,
            'minSpan': self.minSpan,
            'repeat': self.repeat.variable,
            'repeatDirection': self.repeat.direction,
            'maxPerRow': self.repeat.maxPerRow,
            'span': self.span,
            'targets': self.targets,
            'timeFrom': self.timeFrom,
            'timeShift': self.timeShift,
            'title': self.title,
            'transparent': self.transparent,
            'transformations': self.transformations
        }
        res.update(overrides)
        _deep_update(res, self.extraJson)
        return res


@attr.s
class RowPanel(Panel):
    """
    Generates Row panel json structure.

    :param title: title of the panel
    :param panels: list of panels in the row
    """

    panels = attr.ib(default=attr.Factory(list), validator=instance_of(list))

    def _iter_panels(self):
        return iter(self.panels)

    def _map_panels(self, f):
        self = f(self)
        return attr.evolve(self, panels=list(map(f, self.panels)))

    def to_json_data(self):
        return self.panel_json(
            {
                'collapsed': False,
                'panels': self.panels,
                'type': ROW_TYPE
            }
        )


@attr.s
class Row(object):
    """
    Legacy support for old row, when not used with gridpos
    """
    # TODO: jml would like to separate the balancing behaviour from this
    # layer.
    try:
        panels = attr.ib(default=attr.Factory(list), converter=_balance_panels)
    except TypeError:
        panels = attr.ib(default=attr.Factory(list), convert=_balance_panels)
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
class Graph(Panel):
    """
    Generates Graph panel json structure.

    :param alert: List of AlertConditions
    :param align: Select to align left and right Y-axes by value
    :param alignLevel: Available when Align is selected. Value to use for alignment of left and right Y-axes
    :param bars: Display values as a bar chart
    :param dataLinks: List of data links hooked to datapoints on the graph
    :param fill: Area fill, amount of color fill for a series. (default 1, 0 is none)
    :param fillGradient: Degree of gradient on the area fill. (0 is no gradient, 10 is a steep gradient. Default is 0.)
    :param lines: Display values as a line graph
    :param points: Display points for values (default False)
    :param pointRadius: Controls how large the points are
    :param stack: Each series is stacked on top of another
    :param percentage: Available when Stack is selected. Each series is drawn as a percentage of the total of all series
    :param thresholds: List of GraphThresholds - Only valid when alert not defined
    """

    alert = attr.ib(default=None)
    alertThreshold = attr.ib(default=True, validator=instance_of(bool))
    aliasColors = attr.ib(default=attr.Factory(dict))
    align = attr.ib(default=False, validator=instance_of(bool))
    alignLevel = attr.ib(default=0, validator=instance_of(int))
    bars = attr.ib(default=False, validator=instance_of(bool))
    dataLinks = attr.ib(default=attr.Factory(list))
    error = attr.ib(default=False, validator=instance_of(bool))
    fill = attr.ib(default=1, validator=instance_of(int))
    fillGradient = attr.ib(default=0, validator=instance_of(int))
    grid = attr.ib(default=attr.Factory(Grid), validator=instance_of(Grid))
    isNew = attr.ib(default=True, validator=instance_of(bool))
    legend = attr.ib(
        default=attr.Factory(Legend),
        validator=instance_of(Legend),
    )
    lines = attr.ib(default=True, validator=instance_of(bool))
    lineWidth = attr.ib(default=DEFAULT_LINE_WIDTH)
    nullPointMode = attr.ib(default=NULL_CONNECTED)
    percentage = attr.ib(default=False, validator=instance_of(bool))
    pointRadius = attr.ib(default=DEFAULT_POINT_RADIUS)
    points = attr.ib(default=False, validator=instance_of(bool))
    renderer = attr.ib(default=DEFAULT_RENDERER)
    seriesOverrides = attr.ib(default=attr.Factory(list))
    stack = attr.ib(default=False, validator=instance_of(bool))
    steppedLine = attr.ib(default=False, validator=instance_of(bool))
    tooltip = attr.ib(
        default=attr.Factory(Tooltip),
        validator=instance_of(Tooltip),
    )
    thresholds = attr.ib(default=attr.Factory(list))
    xAxis = attr.ib(default=attr.Factory(XAxis), validator=instance_of(XAxis))
    try:
        yAxes = attr.ib(
            default=attr.Factory(YAxes),
            converter=to_y_axes,
            validator=instance_of(YAxes),
        )
    except TypeError:
        yAxes = attr.ib(
            default=attr.Factory(YAxes),
            convert=to_y_axes,
            validator=instance_of(YAxes),
        )

    def to_json_data(self):
        graphObject = {
            'aliasColors': self.aliasColors,
            'bars': self.bars,
            'error': self.error,
            'fill': self.fill,
            'grid': self.grid,
            'isNew': self.isNew,
            'legend': self.legend,
            'lines': self.lines,
            'linewidth': self.lineWidth,
            'minSpan': self.minSpan,
            'nullPointMode': self.nullPointMode,
            'options': {
                'dataLinks': self.dataLinks,
                'alertThreshold': self.alertThreshold,
            },
            'percentage': self.percentage,
            'pointradius': self.pointRadius,
            'points': self.points,
            'renderer': self.renderer,
            'seriesOverrides': self.seriesOverrides,
            'stack': self.stack,
            'steppedLine': self.steppedLine,
            'tooltip': self.tooltip,
            'thresholds': self.thresholds,
            'type': GRAPH_TYPE,
            'xaxis': self.xAxis,
            'yaxes': self.yAxes,
            'yaxis': {
                'align': self.align,
                'alignLevel': self.alignLevel
            }
        }
        if self.alert:
            graphObject['alert'] = self.alert
            graphObject['thresholds'] = []
        if self.thresholds and self.alert:
            print("Warning: Graph threshold ignored as Alerts defined")
        return self.panel_json(graphObject)

    def _iter_targets(self):
        for target in self.targets:
            yield target

    def _map_targets(self, f):
        return attr.evolve(self, targets=[f(t) for t in self.targets])

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
            return t if t.refId else attr.evolve(t, refId=next(auto_ref_ids))

        return self._map_targets(set_refid)


@attr.s
class DiscreteColorMappingItem(object):
    """
    Generates json structure for the value mapping item for the StatValueMappings class:

    :param text: String to color
    :param color: To color the text with
    """

    text = attr.ib(validator=instance_of(str))
    color = attr.ib(default=GREY1, validator=instance_of((str, RGBA)))

    def to_json_data(self):
        return {
            "color": self.color,
            "text": self.text,
        }


@attr.s
class Discrete(Panel):
    """
    Generates Discrete panel json structure.

    :param colorMaps: List of DiscreteColorMappingItem, to color values.
    """

    colorMapsItems = attr.ib(
        default=[],
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(DiscreteColorMappingItem),
            iterable_validator=attr.validators.instance_of(list),
        ),
    )

    def to_json_data(self):
        graphObject = {
            'colorMaps': self.colorMapsItems,
            'type': DISCRETE_TYPE,
        }
        return self.panel_json(graphObject)


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
class Text(Panel):
    """Generates a Text panel."""

    content = attr.ib(default="")
    error = attr.ib(default=False, validator=instance_of(bool))
    mode = attr.ib(default=TEXT_MODE_MARKDOWN)

    def to_json_data(self):
        return self.panel_json(
            {
                'content': self.content,
                'error': self.error,
                'mode': self.mode,
                'type': TEXT_TYPE,
            }
        )


@attr.s
class AlertList(object):
    """Generates the AlertList Panel.

    :param dashboardTags: A list of tags (strings) for the panel.
    :param description: Panel description, supports markdown and links.
    :param gridPos: describes the panel size and position in grid coordinates.
    :param id: panel id
    :param limit: Max number of alerts that can be displayed in the list.
    :param nameFilter: Show only alerts that contain nameFilter in their name.
    :param onlyAlertsOnDashboard: If true, shows only alerts from the current dashboard.
    :param links: Additional web links to be presented in the panel. A list of instantiation of
        DataLink objects.
    :param show: Show the current alert list (ALERTLIST_SHOW_CURRENT) or only the alerts that were
        changed (ALERTLIST_SHOW_CHANGES).
    :param sortOrder: Defines the sorting order of the alerts. Gets one of the following values as
        input: SORT_ASC, SORT_DESC and SORT_IMPORTANCE.
    :param span: Defines the number of spans that will be used for the panel.
    :param stateFilter: Show alerts with statuses from the stateFilter list. The list can contain a
        subset of the following statuses:
        [ALERTLIST_STATE_ALERTING, ALERTLIST_STATE_OK, ALERTLIST_STATE_NO_DATA,
        ALERTLIST_STATE_PAUSED, ALERTLIST_STATE_EXECUTION_ERROR, ALERTLIST_STATE_PENDING].
        An empty list means all alerts.
    :param title: The panel title.
    :param transparent: If true, display the panel without a background.
    """

    dashboardTags = attr.ib(
        default=attr.Factory(list),
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(str),
            iterable_validator=attr.validators.instance_of(list)))
    description = attr.ib(default="", validator=instance_of(str))
    gridPos = attr.ib(
        default=None, validator=attr.validators.optional(attr.validators.instance_of(GridPos)))
    id = attr.ib(default=None)
    limit = attr.ib(default=DEFAULT_LIMIT)
    links = attr.ib(
        default=attr.Factory(list),
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(DataLink),
            iterable_validator=attr.validators.instance_of(list)))
    nameFilter = attr.ib(default="", validator=instance_of(str))
    onlyAlertsOnDashboard = attr.ib(default=True, validator=instance_of(bool))
    show = attr.ib(default=ALERTLIST_SHOW_CURRENT)
    sortOrder = attr.ib(default=SORT_ASC, validator=in_([1, 2, 3]))
    span = attr.ib(default=6)
    stateFilter = attr.ib(default=attr.Factory(list))
    title = attr.ib(default="")
    transparent = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'dashboardTags': self.dashboardTags,
            'description': self.description,
            'gridPos': self.gridPos,
            'id': self.id,
            'limit': self.limit,
            'links': self.links,
            'nameFilter': self.nameFilter,
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
class Stat(Panel):
    """Generates Stat panel json structure

    Grafana doc on stat: https://grafana.com/docs/grafana/latest/panels/visualizations/stat-panel/

    :param alignment: defines value & title positioning: keys 'auto' 'centre'
    :param colorMode: defines if Grafana will color panel background: keys "value" "background"
    :param decimals: number of decimals to display
    :param format: defines value units
    :param graphMode: defines if Grafana will draw graph: keys 'area' 'none'
    :param mappings: the list of values to text mappings
        This should be a list of StatMapping objects
        https://grafana.com/docs/grafana/latest/panels/field-configuration-options/#value-mapping
    :param orientation: Stacking direction in case of multiple series or fields: keys 'auto' 'horizontal' 'vertical'
    :param reduceCalc: algorithm for reduction to a single value: keys
        'mean' 'lastNotNull' 'last' 'first' 'firstNotNull' 'min' 'max' 'sum' 'total'
    :param textMode: define Grafana will show name or value: keys: 'auto' 'name' 'none' 'value' 'value_and_name'
    :param thresholds: single stat thresholds
    """

    alignment = attr.ib(default='auto')
    colorMode = attr.ib(default='value')
    decimals = attr.ib(default=None)
    format = attr.ib(default='none')
    graphMode = attr.ib(default='area')
    mappings = attr.ib(default=attr.Factory(list))
    orientation = attr.ib(default='auto')
    reduceCalc = attr.ib(default='mean', type=str)
    textMode = attr.ib(default='auto')
    thresholds = attr.ib(default="")

    def to_json_data(self):
        return self.panel_json(
            {
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
                    'textMode': self.textMode,
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
                'type': STAT_TYPE,
            }
        )


@attr.s
class StatValueMappingItem(object):
    """
    Generates json structure for the value mapping item for the StatValueMappings class:

    :param text: String that will replace input value
    :param mapValue: Value to be replaced
    :param color: How to color the text if mapping occurs
    :param index: index
    """

    text = attr.ib()
    mapValue = attr.ib(default="", validator=instance_of(str))
    color = attr.ib(default="", validator=instance_of(str))
    index = attr.ib(default=None)

    def to_json_data(self):
        return {
            self.mapValue: {
                'text': self.text,
                'color': self.color,
                'index': self.index
            }
        }


@attr.s(init=False)
class StatValueMappings(object):
    """
    Generates json structure for the value mappings for the StatPanel:

    :param mappingItems: List of StatValueMappingItem objects

    mappings=[
        core.StatValueMappings(
            core.StatValueMappingItem('Offline', '0', 'red'),  # Value must a string
            core.StatValueMappingItem('Online', '1', 'green')
        ),
    ],
    """

    mappingItems = attr.ib(
        default=[],
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(StatValueMappingItem),
            iterable_validator=attr.validators.instance_of(list),
        ),
    )

    def __init__(self, *mappings: StatValueMappingItem):
        self.__attrs_init__([*mappings])

    def to_json_data(self):
        ret_dict = {
            'type': 'value',
            'options': {
            }
        }

        for item in self.mappingItems:
            ret_dict['options'].update(item.to_json_data())

        return ret_dict


@attr.s
class StatRangeMappings(object):
    """
    Generates json structure for the range mappings for the StatPanel:

    :param text: Sting that will replace input value
    :param startValue: When using a range, the start value of the range
    :param endValue: When using a range, the end value of the range
    :param color: How to color the text if mapping occurs
    :param index: index
    """

    text = attr.ib()
    startValue = attr.ib(default=0, validator=instance_of(int))
    endValue = attr.ib(default=0, validator=instance_of(int))
    color = attr.ib(default="", validator=instance_of(str))
    index = attr.ib(default=None)

    def to_json_data(self):
        return {
            'type': 'range',
            'options': {
                'from': self.startValue,
                'to': self.endValue,
                'result': {
                    'text': self.text,
                    'color': self.color,
                    'index': self.index
                }
            }
        }


@attr.s
class StatMapping(object):
    """
    Deprecated Grafana v8
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

        ret_dict = {
            'operator': '',
            'text': self.text,
            'type': mappingType,
            'value': self.mapValue,
            'from': self.startValue,
            'to': self.endValue,
            'id': self.id
        }

        return ret_dict


@attr.s
class StatValueMapping(object):
    """
    Deprecated Grafana v8
    Generates json structure for the value mappings for the StatPanel:

    :param text: Sting that will replace input value
    :param mapValue: Value to be replaced
    :param id: panel id
    """

    text = attr.ib()
    mapValue = attr.ib(default="", validator=instance_of(str))
    id = attr.ib(default=None)

    def to_json_data(self):
        return StatMapping(
            self.text,
            mapValue=self.mapValue,
            id=self.id,
        )


@attr.s
class StatRangeMapping(object):
    """
    Deprecated Grafana v8
    Generates json structure for the range mappings for the StatPanel:

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
class SingleStat(Panel):
    """Generates Single Stat panel json structure

    This panel was deprecated in Grafana 7.0, please use Stat instead

    Grafana doc on singlestat: https://grafana.com/docs/grafana/latest/features/panels/singlestat/

    :param cacheTimeout: metric query result cache ttl
    :param colors: the list of colors that can be used for coloring
        panel value or background. Additional info on coloring in docs:
        https://grafana.com/docs/grafana/latest/features/panels/singlestat/#coloring
    :param colorBackground: defines if grafana will color panel background
    :param colorValue: defines if grafana will color panel value
    :param decimals: override automatic decimal precision for legend/tooltips
    :param format: defines value units
    :param gauge: draws and additional speedometer-like gauge based
    :param mappingType: defines panel mapping type.
        Additional info can be found in docs:
        https://grafana.com/docs/grafana/latest/features/panels/singlestat/#value-to-text-mapping
    :param mappingTypes: the list of available mapping types for panel
    :param nullText: defines what to show if metric query result is undefined
    :param nullPointMode: defines how to render undefined values
    :param postfix: defines postfix that will be attached to value
    :param postfixFontSize: defines postfix font size
    :param prefix: defines prefix that will be attached to value
    :param prefixFontSize: defines prefix font size
    :param rangeMaps: the list of value to text mappings
    :param sparkline: defines if grafana should draw an additional sparkline.
        Sparkline grafana documentation:
        https://grafana.com/docs/grafana/latest/features/panels/singlestat/#spark-lines
    :param thresholds: single stat thresholds
    :param valueFontSize: defines value font size
    :param valueName: defines value type. possible values are:
        min, max, avg, current, total, name, first, delta, range
    :param valueMaps: the list of value to text mappings
    """

    cacheTimeout = attr.ib(default=None)
    colors = attr.ib(default=attr.Factory(lambda: [GREEN, ORANGE, RED]))
    colorBackground = attr.ib(default=False, validator=instance_of(bool))
    colorValue = attr.ib(default=False, validator=instance_of(bool))
    decimals = attr.ib(default=None)
    format = attr.ib(default='none')
    gauge = attr.ib(default=attr.Factory(Gauge),
                    validator=instance_of(Gauge))
    mappingType = attr.ib(default=MAPPING_TYPE_VALUE_TO_TEXT)
    mappingTypes = attr.ib(
        default=attr.Factory(lambda: [
            MAPPING_VALUE_TO_TEXT,
            MAPPING_RANGE_TO_TEXT,
        ]),
    )
    minSpan = attr.ib(default=None)
    nullText = attr.ib(default=None)
    nullPointMode = attr.ib(default='connected')
    postfix = attr.ib(default="")
    postfixFontSize = attr.ib(default='50%')
    prefix = attr.ib(default="")
    prefixFontSize = attr.ib(default='50%')
    rangeMaps = attr.ib(default=attr.Factory(list))
    sparkline = attr.ib(
        default=attr.Factory(SparkLine),
        validator=instance_of(SparkLine),
    )
    thresholds = attr.ib(default="")
    valueFontSize = attr.ib(default='80%')
    valueName = attr.ib(default=VTYPE_DEFAULT)
    valueMaps = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return self.panel_json(
            {
                'cacheTimeout': self.cacheTimeout,
                'colorBackground': self.colorBackground,
                'colorValue': self.colorValue,
                'colors': self.colors,
                'decimals': self.decimals,
                'format': self.format,
                'gauge': self.gauge,
                'mappingType': self.mappingType,
                'mappingTypes': self.mappingTypes,
                'minSpan': self.minSpan,
                'nullPointMode': self.nullPointMode,
                'nullText': self.nullText,
                'postfix': self.postfix,
                'postfixFontSize': self.postfixFontSize,
                'prefix': self.prefix,
                'prefixFontSize': self.prefixFontSize,
                'rangeMaps': self.rangeMaps,
                'sparkline': self.sparkline,
                'thresholds': self.thresholds,
                'type': SINGLESTAT_TYPE,
                'valueFontSize': self.valueFontSize,
                'valueMaps': self.valueMaps,
                'valueName': self.valueName,
            }
        )


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
    align = attr.ib(default='auto', validator=in_(
        ['auto', 'left', 'right', 'center']))
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

    text = attr.ib(default='Avg')
    value = attr.ib(default='avg')

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
class Table(Panel):
    """Generates Table panel json structure

    Grafana doc on table: https://grafana.com/docs/grafana/latest/features/panels/table_panel/#table-panel

    :param columns: table columns for Aggregations view
    :param fontSize: defines value font size
    :param pageSize: rows per page (None is unlimited)
    :param scroll: scroll the table instead of displaying in full
    :param showHeader: show the table header
    :param sort: table sorting
    :param styles: defines formatting for each column
    :param transform: table style
    """

    columns = attr.ib(default=attr.Factory(list))
    fontSize = attr.ib(default='100%')
    pageSize = attr.ib(default=None)
    scroll = attr.ib(default=True, validator=instance_of(bool))
    showHeader = attr.ib(default=True, validator=instance_of(bool))
    span = attr.ib(default=6)
    sort = attr.ib(
        default=attr.Factory(ColumnSort), validator=instance_of(ColumnSort))
    styles = attr.ib()

    transform = attr.ib(default=COLUMNS_TRANSFORM)

    @styles.default
    def styles_default(self):
        return [
            ColumnStyle(
                alias='Time',
                pattern='Time',
                type=DateColumnStyleType(),
            ),
            ColumnStyle(
                alias='time',
                pattern='time',
                type=DateColumnStyleType(),
            ),
            ColumnStyle(
                pattern='/.*/',
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
        return self.panel_json(
            {
                'columns': self.columns,
                'fontSize': self.fontSize,
                'hideTimeOverride': self.hideTimeOverride,
                'minSpan': self.minSpan,
                'pageSize': self.pageSize,
                'scroll': self.scroll,
                'showHeader': self.showHeader,
                'sort': self.sort,
                'styles': self.styles,
                'transform': self.transform,
                'type': TABLE_TYPE,
            }
        )


@attr.s
class BarGauge(Panel):
    """Generates Bar Gauge panel json structure

    :param allValue: If All values should be shown or a Calculation
    :param calc: Calculation to perform on metrics
    :param dataLinks: list of data links hooked to datapoints on the graph
    :param decimals: override automatic decimal precision for legend/tooltips
    :param displayMode: style to display bar gauge in
    :param format: defines value units
    :param labels: option to show gauge level labels
    :param limit: limit of number of values to show when not Calculating
    :param max: maximum value of the gauge
    :param min: minimum value of the gauge
    :param orientation: orientation of the bar gauge
    :param rangeMaps: the list of value to text mappings
    :param thresholdLabel: label for gauge. Template Variables:
        "$__series_namei" "$__field_name" "$__cell_{N} / $__calc"
    :param thresholdMarkers: option to show marker of level on gauge
    :param thresholds: single stat thresholds
    :param valueMaps: the list of value to text mappings
    """

    allValues = attr.ib(default=False, validator=instance_of(bool))
    calc = attr.ib(default=GAUGE_CALC_MEAN)
    dataLinks = attr.ib(default=attr.Factory(list))
    decimals = attr.ib(default=None)
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
    format = attr.ib(default='none')
    label = attr.ib(default=None)
    limit = attr.ib(default=None)
    max = attr.ib(default=100)
    min = attr.ib(default=0)
    orientation = attr.ib(
        default=ORIENTATION_HORIZONTAL,
        validator=in_([ORIENTATION_HORIZONTAL, ORIENTATION_VERTICAL]),
    )
    rangeMaps = attr.ib(default=attr.Factory(list))
    thresholdLabels = attr.ib(default=False, validator=instance_of(bool))
    thresholdMarkers = attr.ib(default=True, validator=instance_of(bool))
    thresholds = attr.ib(
        default=attr.Factory(
            lambda: [
                Threshold('green', 0, 0.0),
                Threshold('red', 1, 80.0)
            ]
        ),
        validator=instance_of(list),
    )
    valueMaps = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return self.panel_json(
            {
                'options': {
                    'displayMode': self.displayMode,
                    'fieldOptions': {
                        'calcs': [self.calc],
                        'defaults': {
                            'decimals': self.decimals,
                            'max': self.max,
                            'min': self.min,
                            'title': self.label,
                            'unit': self.format,
                            'links': self.dataLinks,
                        },
                        'limit': self.limit,
                        'mappings': self.valueMaps,
                        'override': {},
                        'thresholds': self.thresholds,
                        'values': self.allValues,
                    },
                    'orientation': self.orientation,
                    'showThresholdLabels': self.thresholdLabels,
                    'showThresholdMarkers': self.thresholdMarkers,
                },
                'type': BARGAUGE_TYPE,
            }
        )


@attr.s
class GaugePanel(Panel):
    """Generates Gauge panel json structure

    :param allValue: If All values should be shown or a Calculation
    :param calc: Calculation to perform on metrics
    :param dataLinks: list of data links hooked to datapoints on the graph
    :param decimals: override automatic decimal precision for legend/tooltips
    :param format: defines value units
    :param labels: option to show gauge level labels
    :param limit: limit of number of values to show when not Calculating
    :param max: maximum value of the gauge
    :param min: minimum value of the gauge
    :param rangeMaps: the list of value to text mappings
    :param thresholdLabel: label for gauge. Template Variables:
        "$__series_namei" "$__field_name" "$__cell_{N} / $__calc"
    :param thresholdMarkers: option to show marker of level on gauge
    :param thresholds: single stat thresholds
    :param valueMaps: the list of value to text mappings
    """

    allValues = attr.ib(default=False, validator=instance_of(bool))
    calc = attr.ib(default=GAUGE_CALC_MEAN)
    dataLinks = attr.ib(default=attr.Factory(list))
    decimals = attr.ib(default=None)
    format = attr.ib(default='none')
    label = attr.ib(default=None)
    limit = attr.ib(default=None)
    max = attr.ib(default=100)
    min = attr.ib(default=0)
    rangeMaps = attr.ib(default=attr.Factory(list))
    thresholdLabels = attr.ib(default=False, validator=instance_of(bool))
    thresholdMarkers = attr.ib(default=True, validator=instance_of(bool))
    thresholds = attr.ib(
        default=attr.Factory(
            lambda: [
                Threshold('green', 0, 0.0),
                Threshold('red', 1, 80.0)
            ]
        ),
        validator=instance_of(list),
    )
    valueMaps = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return self.panel_json(
            {
                'options': {
                    'fieldOptions': {
                        'calcs': [self.calc],
                        'defaults': {
                            'decimals': self.decimals,
                            'max': self.max,
                            'min': self.min,
                            'title': self.label,
                            'unit': self.format,
                            'links': self.dataLinks,
                        },
                        'limit': self.limit,
                        'mappings': self.valueMaps,
                        'override': {},
                        'thresholds': self.thresholds,
                        'values': self.allValues,
                    },
                    'showThresholdLabels': self.thresholdLabels,
                    'showThresholdMarkers': self.thresholdMarkers,
                },
                'type': GAUGE_TYPE,
            }
        )


@attr.s
class HeatmapColor(object):
    """A Color object for heatmaps

    :param cardColor: color
    :param colorScale: scale
    :param colorScheme: scheme
    :param exponent: exponent
    :param max: max
    :param min: min
    :param mode: mode
    """

    # Maybe cardColor should validate to RGBA object, not sure
    cardColor = attr.ib(default='#b4ff00', validator=instance_of(str))
    colorScale = attr.ib(default='sqrt', validator=instance_of(str))
    colorScheme = attr.ib(default='interpolateOranges')
    exponent = attr.ib(default=0.5, validator=instance_of(float))
    mode = attr.ib(default='spectrum', validator=instance_of(str))
    max = attr.ib(default=None)
    min = attr.ib(default=None)

    def to_json_data(self):
        return {
            'mode': self.mode,
            'cardColor': self.cardColor,
            'colorScale': self.colorScale,
            'exponent': self.exponent,
            'colorScheme': self.colorScheme,
            'max': self.max,
            'min': self.min,
        }


@attr.s
class Heatmap(Panel):
    """Generates Heatmap panel json structure (https://grafana.com/docs/grafana/latest/features/panels/heatmap/)

    :param heatmap: dict
    :param cards: A heatmap card object: keys "cardPadding", "cardRound"
    :param color: Heatmap color object
    :param dataFormat: 'timeseries' or 'tsbuckets'
    :param yBucketBound: 'auto', 'upper', 'middle', 'lower'
    :param reverseYBuckets: boolean
    :param xBucketSize: Size
    :param xBucketNumber: Number
    :param yBucketSize: Size
    :param yBucketNumber: Number
    :param highlightCards: boolean
    :param hideZeroBuckets: boolean
    :param transparent: defines if the panel should be transparent
    """

    # The below does not really like the Legend class we have defined above
    legend = attr.ib(default={'show': False})
    tooltip = attr.ib(
        default=attr.Factory(Tooltip),
        validator=instance_of(Tooltip),
    )
    cards = attr.ib(
        default={
            'cardPadding': None,
            'cardRound': None
        }
    )

    color = attr.ib(
        default=attr.Factory(HeatmapColor),
        validator=instance_of(HeatmapColor),
    )

    dataFormat = attr.ib(default='timeseries')
    heatmap = {}
    hideZeroBuckets = attr.ib(default=False)
    highlightCards = attr.ib(default=True)
    options = attr.ib(default=None)

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
        return self.panel_json(
            {
                'cards': self.cards,
                'color': self.color,
                'dataFormat': self.dataFormat,
                'heatmap': self.heatmap,
                'hideZeroBuckets': self.hideZeroBuckets,
                'highlightCards': self.highlightCards,
                'legend': self.legend,
                'options': self.options,
                'reverseYBuckets': self.reverseYBuckets,
                'tooltip': self.tooltip,
                'type': HEATMAP_TYPE,
                'xAxis': self.xAxis,
                'xBucketNumber': self.xBucketNumber,
                'xBucketSize': self.xBucketSize,
                'yAxis': self.yAxis,
                'yBucketBound': self.yBucketBound,
                'yBucketNumber': self.yBucketNumber,
                'yBucketSize': self.yBucketSize
            }
        )


@attr.s
class StatusmapColor(object):
    """A Color object for Statusmaps

    :param cardColor: colour
    :param colorScale: scale
    :param colorScheme: scheme
    :param exponent: exponent
    :param max: max
    :param min: min
    :param mode: mode
    :param thresholds: threshold
    """

    # Maybe cardColor should validate to RGBA object, not sure
    cardColor = attr.ib(default='#b4ff00', validator=instance_of(str))
    colorScale = attr.ib(default='sqrt', validator=instance_of(str))
    colorScheme = attr.ib(default='GnYlRd', validator=instance_of(str))
    exponent = attr.ib(default=0.5, validator=instance_of(float))
    mode = attr.ib(default='spectrum', validator=instance_of(str))
    thresholds = attr.ib(default=[], validator=instance_of(list))
    max = attr.ib(default=None)
    min = attr.ib(default=None)

    def to_json_data(self):
        return {
            'mode': self.mode,
            'cardColor': self.cardColor,
            'colorScale': self.colorScale,
            'exponent': self.exponent,
            'colorScheme': self.colorScheme,
            'max': self.max,
            'min': self.min,
            'thresholds': self.thresholds
        }


@attr.s
class Statusmap(Panel):
    """Generates json structure for the flant-statusmap-panel visualisation plugin
    (https://grafana.com/grafana/plugins/flant-statusmap-panel/).

    :param alert: Alert
    :param cards: A statusmap card object: keys 'cardRound', 'cardMinWidth', 'cardHSpacing', 'cardVSpacing'
    :param color: A StatusmapColor object
    :param isNew: isNew
    :param legend: Legend object
    :param nullPointMode: null
    :param tooltip: Tooltip object
    :param xAxis: XAxis object
    :param yAxis: YAxis object
    """

    alert = attr.ib(default=None)
    cards = attr.ib(
        default={
            'cardRound': None,
            'cardMinWidth': 5,
            'cardHSpacing': 2,
            'cardVSpacing': 2,
        }, validator=instance_of(dict))

    color = attr.ib(
        default=attr.Factory(StatusmapColor),
        validator=instance_of(StatusmapColor),
    )

    isNew = attr.ib(default=True, validator=instance_of(bool))
    legend = attr.ib(
        default=attr.Factory(Legend),
        validator=instance_of(Legend),
    )
    nullPointMode = attr.ib(default=NULL_AS_ZERO)
    tooltip = attr.ib(
        default=attr.Factory(Tooltip),
        validator=instance_of(Tooltip),
    )
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
            'color': self.color,
            'isNew': self.isNew,
            'legend': self.legend,
            'minSpan': self.minSpan,
            'nullPointMode': self.nullPointMode,
            'tooltip': self.tooltip,
            'type': STATUSMAP_TYPE,
            'xaxis': self.xAxis,
            'yaxis': self.yAxis,
        }
        if self.alert:
            graphObject['alert'] = self.alert
        return self.panel_json(graphObject)


@attr.s
class Svg(Panel):
    """Generates SVG panel json structure
    Grafana doc on SVG: https://grafana.com/grafana/plugins/marcuscalidus-svg-panel

    :param format: defines value units
    :param jsCodeFilePath: path to javascript file to be run on dashboard refresh
    :param jsCodeInitFilePath: path to javascript file to be run after the first initialization of the SVG
    :param reduceCalc: algorithm for reduction to a single value,
        keys 'mean' 'lastNotNull' 'last' 'first' 'firstNotNull' 'min' 'max' 'sum' 'total'
    :param svgFilePath: path to SVG image file to be displayed
    """

    format = attr.ib(default='none')
    jsCodeFilePath = attr.ib(default="", validator=instance_of(str))
    jsCodeInitFilePath = attr.ib(default="", validator=instance_of(str))
    height = attr.ib(default=None)
    svgFilePath = attr.ib(default="", validator=instance_of(str))

    @staticmethod
    def read_file(file_path):
        if file_path:
            with open(file_path) as f:
                read_data = f.read()
            return read_data
        else:
            return ''

    def to_json_data(self):

        js_code = self.read_file(self.jsCodeFilePath)
        js_init_code = self.read_file(self.jsCodeInitFilePath)
        svg_data = self.read_file(self.svgFilePath)

        return self.panel_json(
            {
                'format': self.format,
                'js_code': js_code,
                'js_init_code': js_init_code,
                'svg_data': svg_data,
                'type': SVG_TYPE,
                'useSVGBuilder': False
            }
        )


@attr.s
class PieChart(Panel):
    """Generates Pie Chart panel json structure
    Grafana doc on Pie Chart: https://grafana.com/grafana/plugins/grafana-piechart-panel

    :param aliasColors: dictionary of color overrides
    :param format: defines value units
    :param pieType: defines the shape of the pie chart (pie or donut)
    :param percentageDecimals: Number of decimal places to show if percentages shown in legned
    :param showLegend: defines if the legend should be shown
    :param showLegendValues: defines if the legend should show values
    :param showLegendPercentage: Show percentages in the legend
    :param legendType: defines where the legend position
    :param thresholds: defines thresholds
    """

    aliasColors = attr.ib(default=attr.Factory(dict))
    format = attr.ib(default='none')
    legendType = attr.ib(default='Right side')
    pieType = attr.ib(default='pie')
    percentageDecimals = attr.ib(default=0, validator=instance_of(int))
    showLegend = attr.ib(default=True)
    showLegendValues = attr.ib(default=True)
    showLegendPercentage = attr.ib(default=False, validator=instance_of(bool))
    thresholds = attr.ib(default="")

    def to_json_data(self):
        return self.panel_json(
            {
                'aliasColors': self.aliasColors,
                'format': self.format,
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
                    'values': self.showLegendValues,
                    'percentage': self.showLegendPercentage,
                    'percentageDecimals': self.percentageDecimals
                },
                'legendType': self.legendType,
                'type': PIE_CHART_TYPE,
            }
        )


@attr.s
class DashboardList(Panel):
    """Generates Dashboard list panel json structure
    Grafana doc on Dashboard list: https://grafana.com/docs/grafana/latest/panels/visualizations/dashboard-list-panel/

    :param showHeadings: The chosen list selection (Starred, Recently viewed, Search) is shown as a heading
    :param showSearch: Display dashboards by search query or tags.
        Requires you to enter at least one value in Query or Tags
    :param showRecent: Display recently viewed dashboards in alphabetical order
    :param showStarred: Display starred dashboards in alphabetical order
    :param maxItems: Sets the maximum number of items to list per section
    :param searchQuery: Enter the query you want to search by
    :param searchTags: List of tags you want to search by
    """
    showHeadings = attr.ib(default=True, validator=instance_of(bool))
    showSearch = attr.ib(default=False, validator=instance_of(bool))
    showRecent = attr.ib(default=False, validator=instance_of(bool))
    showStarred = attr.ib(default=True, validator=instance_of(bool))
    maxItems = attr.ib(default=10, validator=instance_of(int))
    searchQuery = attr.ib(default='', validator=instance_of(str))
    searchTags = attr.ib(default=attr.Factory(list), validator=instance_of(list))

    def to_json_data(self):
        return self.panel_json(
            {
                'fieldConfig': {
                    'defaults': {
                        'custom': {},
                    },
                    'overrides': []
                },
                'headings': self.showHeadings,
                'search': self.showSearch,
                'recent': self.showRecent,
                'starred': self.showStarred,
                'limit': self.maxItems,
                'query': self.searchQuery,
                'tags': self.searchTags,
                'type': DASHBOARDLIST_TYPE,
            }
        )


@attr.s
class Logs(Panel):
    """Generates Logs panel json structure
    Grafana doc on Logs panel: https://grafana.com/docs/grafana/latest/panels/visualizations/logs-panel/

    :param showLabels: Show or hide the unique labels column, which shows only non-common labels
    :param showTime: Show or hide the log timestamp column
    :param wrapLogMessages: Toggle line wrapping
    :param sortOrder: Display results in 'Descending' or 'Ascending' time order. The default is Descending,
        showing the newest logs first.
    """
    showLabels = attr.ib(default=False, validator=instance_of(bool))
    showTime = attr.ib(default=False, validator=instance_of(bool))
    wrapLogMessages = attr.ib(default=False, validator=instance_of(bool))
    sortOrder = attr.ib(default='Descending', validator=instance_of(str))

    def to_json_data(self):
        return self.panel_json(
            {
                'fieldConfig': {
                    'defaults': {
                        'custom': {},
                    },
                    'overrides': []
                },
                'options': {
                    'showLabels': self.showLabels,
                    'showTime': self.showTime,
                    'sortOrder': self.sortOrder,
                    'wrapLogMessage': self.wrapLogMessages
                },
                'type': LOGS_TYPE,
            }
        )


@attr.s
class Threshold(object):
    """Threshold for for panels
    (https://grafana.com/docs/grafana/latest/panels/thresholds/)

    :param color: Color of threshold
    :param index: Index of color in panel
    :param line: Display Threshold line, defaults to True
    :param value: When to use this color will be null if index is 0
    :param op: EVAL_LT for less than or EVAL_GT for greater than to indicate what the threshold applies to.
    :param yaxis: Choose left or right for panels

    Care must be taken in the order in which the Threshold objects are specified,
    Grafana expects the value to increase.

    Example::
        thresholds = [
            Threshold('green', 0, 0.0),
            Threshold('red', 1, 80.0)]

    """

    color = attr.ib()
    index = attr.ib(validator=instance_of(int))
    value = attr.ib(validator=instance_of(float))
    line = attr.ib(default=True, validator=instance_of(bool))
    op = attr.ib(default=EVAL_GT)
    yaxis = attr.ib(default='left')

    def to_json_data(self):
        return {
            'op': self.op,
            'yaxis': self.yaxis,
            'color': self.color,
            'line': self.line,
            'index': self.index,
            'value': 'null' if self.index == 0 else self.value,
        }


@attr.s
class GraphThreshold(object):
    """Threshold for for Graph panel
    (https://grafana.com/docs/grafana/latest/panels/thresholds/)

    :param colorMode: Color mode of the threshold, value can be `ok`, `warning`, `critical` or `custom`.
        If `custom` is selcted a lineColor and fillColor should be provided
    :param fill: Display threshold fill, defaults to True
    :param line: Display threshold line, defaults to True
    :param value: When to use this color will be null if index is 0
    :param op: EVAL_LT for less than or EVAL_GT for greater than to indicate what the threshold applies to.
    :param yaxis: Choose left or right for Graph panels
    :param fillColor: Fill color of the threshold, when colorMode = "custom"
    :param lineColor: Line color of the threshold, when colorMode = "custom"

    Example:
        thresholds = [
            GraphThreshold(colorMode="ok", value=10.0),
            GraphThreshold(colorMode="critical", value=90.0)
            ]

    """

    value = attr.ib(validator=instance_of(float))
    colorMode = attr.ib(default="critical")
    fill = attr.ib(default=True, validator=instance_of(bool))
    line = attr.ib(default=True, validator=instance_of(bool))
    op = attr.ib(default=EVAL_GT)
    yaxis = attr.ib(default='left')
    fillColor = attr.ib(default=RED)
    lineColor = attr.ib(default=RED)

    def to_json_data(self):
        data = {
            'value': self.value,
            'colorMode': self.colorMode,
            'fill': self.fill,
            'line': self.line,
            'op': self.op,
            'yaxis': self.yaxis,
        }

        if self.colorMode == "custom":
            data['fillColor'] = self.fillColor
            data['lineColor'] = self.lineColor

        return data


@attr.s
class SeriesOverride(object):
    alias = attr.ib()
    bars = attr.ib(default=False)
    lines = attr.ib(default=True)
    yaxis = attr.ib(default=1)
    color = attr.ib(default=None)

    def to_json_data(self):
        return {
            'alias': self.alias,
            'bars': self.bars,
            'lines': self.lines,
            'yaxis': self.yaxis,
            'color': self.color,
        }


WORLDMAP_CENTER = ['(0°, 0°)', 'North America', 'Europe', 'West Asia', 'SE Asia', 'Last GeoHash', 'custom']
WORLDMAP_LOCATION_DATA = ['countries', 'countries_3letter', 'states', 'probes', 'geohash', 'json_endpoint', 'jsonp endpoint', 'json result', 'table']


@attr.s
class Worldmap(Panel):
    """Generates Worldmap panel json structure
    Grafana doc on Worldmap: https://grafana.com/grafana/plugins/grafana-worldmap-panel/

    :param aggregation: metric aggregation: min, max, avg, current, total
    :param circleMaxSize: Maximum map circle size
    :param circleMinSize: Minimum map circle size
    :param decimals: Number of decimals to show
    :param geoPoint: Name of the geo_point/geohash column. This is used to calculate where the circle should be drawn.
    :param locationData: Format of the location data, options in `WORLDMAP_LOCATION_DATA`
    :param locationName: Name of the Location Name column. Used to label each circle on the map. If it is empty then the geohash value is used.
    :param metric: Name of the metric column. This is used to give the circle a value - this determines how large the circle is.
    :param mapCenter: Where to centre the map, default center (0°, 0°). Options: North America, Europe, West Asia, SE Asia, Last GeoHash, custom
    :param mapCenterLatitude: If mapCenter=custom set the initial map latitude
    :param mapCenterLongitude: If mapCenter=custom set the initial map longitude
    :param hideEmpty: Hide series with only nulls
    :param hideZero: Hide series with only zeros
    :param initialZoom: Initial map zoom
    :param jsonUrl: URL for JSON location data if `json_endpoint` or `jsonp endpoint` used
    :param jsonpCallback: Callback if `jsonp endpoint` used
    :param mouseWheelZoom: Zoom map on scroll of mouse wheel
    :param stickyLabels: Sticky map labels
    :param thresholds: String of thresholds eg. '0,10,20'
    :param thresholdsColors: List of colors to be used in each threshold
    :param unitPlural: Units plural
    :param unitSingle: Units single
    :param unitSingular: Units singular
    """

    circleMaxSize = attr.ib(default=30, validator=instance_of(int))
    circleMinSize = attr.ib(default=2, validator=instance_of(int))
    decimals = attr.ib(default=0, validator=instance_of(int))
    geoPoint = attr.ib(default='geohash', validator=instance_of(str))
    locationData = attr.ib(default='countries', validator=attr.validators.in_(WORLDMAP_LOCATION_DATA))
    locationName = attr.ib(default='')
    hideEmpty = attr.ib(default=False, validator=instance_of(bool))
    hideZero = attr.ib(default=False, validator=instance_of(bool))
    initialZoom = attr.ib(default=1, validator=instance_of(int))
    jsonUrl = attr.ib(default='', validator=instance_of(str))
    jsonpCallback = attr.ib(default='', validator=instance_of(str))
    mapCenter = attr.ib(default='(0°, 0°)', validator=attr.validators.in_(WORLDMAP_CENTER))
    mapCenterLatitude = attr.ib(default=0, validator=instance_of(int))
    mapCenterLongitude = attr.ib(default=0, validator=instance_of(int))
    metric = attr.ib(default='Value')
    mouseWheelZoom = attr.ib(default=False, validator=instance_of(bool))
    stickyLabels = attr.ib(default=False, validator=instance_of(bool))
    thresholds = attr.ib(default='0,100,150', validator=instance_of(str))
    thresholdColors = attr.ib(default=["#73BF69", "#73BF69", "#FADE2A", "#C4162A"], validator=instance_of(list))
    unitPlural = attr.ib(default='', validator=instance_of(str))
    unitSingle = attr.ib(default='', validator=instance_of(str))
    unitSingular = attr.ib(default='', validator=instance_of(str))
    aggregation = attr.ib(default='total', validator=instance_of(str))

    def to_json_data(self):
        return self.panel_json(
            {
                'circleMaxSize': self.circleMaxSize,
                'circleMinSize': self.circleMinSize,
                'colors': self.thresholdColors,
                'decimals': self.decimals,
                'esGeoPoint': self.geoPoint,
                'esMetric': self.metric,
                'locationData': self.locationData,
                'esLocationName': self.locationName,
                'hideEmpty': self.hideEmpty,
                'hideZero': self.hideZero,
                'initialZoom': self.initialZoom,
                'jsonUrl': self.jsonUrl,
                'jsonpCallback': self.jsonpCallback,
                'mapCenter': self.mapCenter,
                'mapCenterLatitude': self.mapCenterLatitude,
                'mapCenterLongitude': self.mapCenterLongitude,
                'mouseWheelZoom': self.mouseWheelZoom,
                'stickyLabels': self.stickyLabels,
                'thresholds': self.thresholds,
                'unitPlural': self.unitPlural,
                'unitSingle': self.unitSingle,
                'unitSingular': self.unitSingular,
                'valueName': self.aggregation,
                'tableQueryOptions': {
                    'queryType': 'geohash',
                    'geohashField': 'geohash',
                    'latitudeField': 'latitude',
                    'longitudeField': 'longitude',
                    'metricField': 'metric'
                },
                'type': WORLD_MAP_TYPE
            }
        )
