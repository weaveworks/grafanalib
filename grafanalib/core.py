"""Low-level functions for building Grafana dashboards.

The functions in this module don't enforce Weaveworks policy, and only mildly
encourage it by way of some defaults. Rather, they are ways of building
arbitrary Grafana JSON.
"""

import math


def RGBA(r, g, b, a):
    return "rgba({}, {}, {}, {})".format(r, g, b, a)


def Pixels(num):
    return '{}px'.format(num)


GREY1 = RGBA(216, 200, 27, 0.27)
GREY2 = RGBA(234, 112, 112, 0.22)

INDIVIDUAL = 'individual'
CUMULATIVE = 'cumulative'

NULL_CONNECTED = 'connected'
NULL_AS_ZERO = 'null as zero'

FLOT = 'flot'

DASHBOARD_TYPE = 'dashboard'
GRAPH_TYPE = 'graph'

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


def Graph(title, dataSource, targets, aliasColors=None, bars=False,
          editable=True, error=False, fill=1, grid=None, id=None, isNew=True,
          legend=None, lines=True, lineWidth=DEFAULT_LINE_WIDTH, links=None,
          nullPointMode=NULL_CONNECTED, percentage=False,
          pointRadius=DEFAULT_POINT_RADIUS, points=False,
          renderer=DEFAULT_RENDERER, seriesOverrides=None, span=None,
          stack=False, steppedLine=False, timeFrom=None, timeShift=None,
          tooltip=None, xAxis=None, yAxes=None):
    aliasColors = {} if aliasColors is None else aliasColors
    grid = Grid() if grid is None else grid
    legend = Legend() if legend is None else legend
    links = [] if links is None else links
    seriesOverrides = [] if seriesOverrides is None else seriesOverrides
    tooltip = Tooltip() if tooltip is None else tooltip
    xAxis = XAxis() if xAxis is None else xAxis
    # XXX: This isn't a *good* default, rather it's the default Grafana uses.
    yAxes = [YAxis(format=SHORT_FORMAT)] * 2 if yAxes is None else yAxes
    return {
        'aliasColors': aliasColors,
        'bars': bars,
        'datasource': dataSource,
        'editable': editable,
        'error': error,
        'fill': fill,
        'grid': grid,
        'id': id,
        'isNew': isNew,
        'legend': legend,
        'lines': lines,
        'linewidth': lineWidth,
        'links': links,
        'nullPointMode': nullPointMode,
        'percentage': percentage,
        'pointradius': pointRadius,
        'points': points,
        'renderer': renderer,
        'seriesOverrides': seriesOverrides,
        'span': span,
        'stack': stack,
        'steppedLine': steppedLine,
        'targets': targets,
        'timeFrom': timeFrom,
        'timeShift': timeShift,
        'title': title,
        'tooltip': tooltip,
        'type': GRAPH_TYPE,
        'xaxis': xAxis,
        'yaxes': yAxes,
    }


def Grid(threshold1=None, threshold1Color=GREY1, threshold2=None,
         threshold2Color=GREY2):
    return {
        'threshold1': threshold1,
        'threshold1Color': threshold1Color,
        'threshold2': threshold2,
        'threshold2Color': threshold2Color,
    }


def Legend(avg=False, current=False, max=False, min=False, show=True,
           total=False, values=False):
    return {
        'avg': avg,
        'current': current,
        'max': max,
        'min': min,
        'show': show,
        'total': total,
        'values': values,
    }


def Target(expr, legendFormat="", intervalFactor=2, metric="", refId="",
           step=DEFAULT_STEP):
    return {
        'expr': expr,
        'intervalFactor': intervalFactor,
        'legendFormat': legendFormat,
        'metric': metric,
        'refId': refId,
        'step': step,
    }


def Tooltip(msResolution=True, shared=True, sort=0, valueType=CUMULATIVE):
    return {
        'msResolution': msResolution,
        'shared': shared,
        'sort': sort,
        'value_type': valueType,
    }


def XAxis(show=True):
    return {
        'show': show,
    }


def YAxis(format=None, label=None, logBase=1, max=None, min=0, show=True):
    return {
        'format': format,
        'label': label,
        'logBase': logBase,
        'max': max,
        'min': min,
        'show': show,
    }


def Row(panels, collapse=False, editable=True, height=DEFAULT_ROW_HEIGHT,
        showTitle=None, title=None):
    if showTitle is None:
        showTitle = False if title is None else True
    if title is None:
        title = "New row"

    # Automatically apportion panels amongst the row
    allotted_spans = sum(
        panel.get('span', 0) for panel in panels
        if panel.get('span', 0) is not None)
    no_span_set = [panel for panel in panels if panel['span'] is None]
    auto_span = math.ceil((TOTAL_SPAN - allotted_spans) / len(no_span_set))
    for panel in no_span_set:
        panel['span'] = auto_span

    return {
        'collapse': collapse,
        'editable': editable,
        'height': height,
        'panels': panels,
        'showTitle': showTitle,
        'title': title,
    }


def Annotations(list=None):
    list = [] if list is None else list
    return {
        'list': list,
    }


def DashboardLink(dashboard, uri, keepTime=True, title=None):
    title = dashboard if title is None else title
    return {
        "dashUri": uri,
        "dashboard": dashboard,
        "keepTime": keepTime,
        "title": title,
        "type": DASHBOARD_TYPE,
    }


def Template(default, dataSource, label, name, query):
    """Template create a new 'variable' for the dashboard, defines the variable
    name, human name, query to fetch the values and the default value.

        :param default: the default value for the variable
        :param dataSource: where to fetch the values for the variable from
        :param label: the variable's human label
        :param name: the variable's name
        :param query: the query users to fetch the valid values of the variable
    """

    return {
        'allValue': None,
        'current': {
            'text': default,
            'value': default,
            'tags': [],
        },
        'datasource': dataSource,
        'hide': 0,
        'includeAll': False,
        'label': label,
        'multi': False,
        'name': name,
        'options': [],
        'query': query,
        'refresh': 1,
        'regex': '',
        'sort': 1,
        'tagValuesQuery': None,
        'tagsQuery': None,
        'type': 'query',
    }


def Templating(list=None):
    list = [] if list is None else list
    return {
        'list': list,
    }


def Time(start, end):
    return {
        'from': start,
        'to': end,
    }


DEFAULT_TIME = Time('now-1h', 'now')


def TimePicker(refreshIntervals, timeOptions):
    return {
        'refresh_intervals': refreshIntervals,
        'time_options': timeOptions,
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


def Dashboard(title, rows, annotations=None, editable=True, gnetId=None,
              hideControls=False, id=None, links=None,
              refresh=DEFAULT_REFRESH, schemaVersion=SCHEMA_VERSION,
              sharedCrosshair=False, style=DARK_STYLE, tags=None,
              templating=None, time=None, timePicker=None, timezone=UTC,
              version=0):
    annotations = Annotations() if annotations is None else annotations
    links = [] if links is None else links
    tags = [] if tags is None else tags
    templating = Templating() if templating is None else templating
    time = DEFAULT_TIME if time is None else time
    timePicker = DEFAULT_TIME_PICKER if timePicker is None else timePicker
    return {
        'annotations': annotations,
        'editable': editable,
        'gnetId': gnetId,
        'hideControls': hideControls,
        'id': id,
        'links': links,
        'refresh': refresh,
        'rows': rows,
        'schemaVersion': schemaVersion,
        'sharedCrosshair': sharedCrosshair,
        'style': style,
        'tags': tags,
        'templating': templating,
        'title': title,
        'time': time,
        'timepicker': timePicker,
        'timezone': timezone,
        'version': version,
    }
