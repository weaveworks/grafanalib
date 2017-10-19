import json
import re

import grafanalib.core


typeMapping = {
    "datasource": grafanalib.core.DataSourceInput,
    "constant": grafanalib.core.ConstantInput,
    grafanalib.core.DASHBOARD_TYPE: grafanalib.core.DashboardLink,
    "query": grafanalib.core.Template,
    grafanalib.core.EVAL_GT: grafanalib.core.Evaluator,
    grafanalib.core.EVAL_LT: grafanalib.core.Evaluator,
    grafanalib.core.EVAL_WITHIN_RANGE: grafanalib.core.Evaluator,
    grafanalib.core.EVAL_OUTSIDE_RANGE: grafanalib.core.Evaluator,
    grafanalib.core.EVAL_NO_VALUE: grafanalib.core.Evaluator,
    grafanalib.core.GRAPH_TYPE: grafanalib.core.Graph,
    grafanalib.core.TEXT_TYPE: grafanalib.core.Text,
    grafanalib.core.SINGLESTAT_TYPE: grafanalib.core.SingleStat

}


def handleRGBA(r, g, b, a):
    return grafanalib.core.RGBA(int(r), int(g), int(b), float(a))


def handleRGB(r, g, b):
    return grafanalib.core.RGB(int(r), int(g), int(b))


def handlePixels(px):
    return grafanalib.core.Pixels(int(px))


def handlePercent(percent):
    return grafanalib.core.Percent(int(percent))


strRegex = {
    re.compile("^rgba\((\d+), (\d+), (\d+), (\d+(?:\.\d+))\)$"): handleRGBA,
    re.compile("rgb\((\d+), (\d+), (\d+)\)"): handleRGB,
    re.compile("^(\d+)px$"): handlePixels,
    re.compile("(\d+)%"): handlePercent,
}


def processStringType(string):
    for regex, handler in strRegex.items():
        match = regex.match(string)
        if match is not None:
            return handler(*match.groups())

    return string


def handleGraph(obj):
    datasource = obj.pop('datasource')
    obj['dataSource'] = datasource
    linewidth = obj.pop('linewidth')
    obj['lineWidth'] = linewidth
    pointradius = obj.pop('pointradius')
    obj['pointRadius'] = pointradius
    xaxis = obj.pop('xaxis')
    obj['xAxis'] = grafanalib.core.XAxis(**xaxis)
    yaxes = obj.pop('yaxes')
    obj['yAxes'] = yaxes
    obj.pop('type')
    return obj


def handleTime(obj):
    _from = obj.pop('from')
    obj['start'] = _from
    to = obj.pop('to')
    obj['end'] = to
    return obj


def handleTimePicker(obj):
    refresh_intervals = obj.pop('refresh_intervals')
    obj['refreshIntervals'] = refresh_intervals
    time_options = obj.pop('time_options')
    obj['timeOptions'] = time_options
    return obj


def handleDashboard(obj):
    inputs = obj.pop('__inputs')
    obj['inputs'] = inputs
    timepicker = obj.pop('timepicker')
    obj['timePicker'] = timepicker
    annotations = obj.pop('annotations')
    obj['annotations'] = grafanalib.core.Annotations(**annotations)
    templating = obj.pop('templating')
    obj['templating'] = grafanalib.core.Templating(**templating)
    return obj


def removeType(obj):
    obj.pop('type')
    return obj


def handleTooltip(obj):
    value_type = obj.pop('value_type')
    obj['valueType'] = value_type
    return obj


objHelperMapper = {
    grafanalib.core.Graph: handleGraph,
    grafanalib.core.Time: handleTime,
    grafanalib.core.TimePicker: handleTimePicker,
    grafanalib.core.Dashboard: handleDashboard,
    grafanalib.core.DataSourceInput: removeType,
    grafanalib.core.ConstantInput: removeType,
    grafanalib.core.Tooltip: handleTooltip,
}


class DashboardDecoder(json.JSONDecoder):
    """Decode dashboard objects."""
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args,
                                  **kwargs)

    def object_hook(self, obj):
        for key, value in obj.items():
            if isinstance(value, str):
                obj[key] = processStringType(value)

        cls = None
        obj_type = obj.get('type')
        if obj_type is not None:
            cls = typeMapping.get(obj_type)

        if 'threshold1' in obj and 'threshold2' in obj:
            cls = grafanalib.core.Grid
        elif 'msResolution' in obj:
            cls = grafanalib.core.Tooltip
        elif 'alignAsTable' in obj:
            cls = grafanalib.core.Legend
        elif 'refresh_intervals' in obj:
            cls = grafanalib.core.TimePicker
        elif 'legendFormat' in obj:
            cls = grafanalib.core.Target
        elif 'panels' in obj:
            cls = grafanalib.core.Row
        elif 'rows' in obj:
            cls = grafanalib.core.Dashboard
        elif 'logBase' in obj:
            cls = grafanalib.core.YAxis
        elif 'from' in obj and 'text' in obj:
            cls = grafanalib.core.RangeMap
        elif 'from' in obj and 'to' in obj:
            cls = grafanalib.core.Time

        if cls is not None:
            # If necessary fixup the object data
            objHelper = objHelperMapper.get(cls)
            if objHelper is not None:
                obj = objHelper(obj)
            return cls(**obj)

        return obj
