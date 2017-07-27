"""Weave-specific dashboard configuration.

Unlike 'core', which has logic for building generic Grafana dashboards, this
has our Weave-specific preferences.
"""

import attr
import functools

import grafanalib.core as G
from grafanalib import prometheus


"""The name of the data source for our Prometheus service."""
PROMETHEUS = "Scope-as-a-Service Prometheus"


YELLOW = "#EAB839"
GREEN = "#7EB26D"
BLUE = "#6ED0E0"
ORANGE = "#EF843C"
RED = "#E24D42"

ALIAS_COLORS = {
  "1xx": YELLOW,
  "2xx": GREEN,
  "3xx": BLUE,
  "4xx": ORANGE,
  "5xx": RED,
  "success": GREEN,
  "error": RED,
}


PromGraph = functools.partial(prometheus.PromGraph, PROMETHEUS)


def QPSGraph(title, expressions, **kwargs):
    """Create a graph of QPS, broken up by response code.

    Data is drawn from Prometheus.

    :param title: Title of the graph.
    :param expressions: List of Prometheus expressions. Must be 5.
    :param kwargs: Passed on to Graph.
    """
    if len(expressions) != 5 and len(expressions) != 7:
        raise ValueError('Expected 5 or 7 expressions, got {}: {}'.format(
            len(expressions), expressions))
    legends = sorted(ALIAS_COLORS.keys())
    exprs = zip(legends, expressions)
    return stacked(PromGraph(
        title=title,
        expressions=exprs,
        aliasColors=ALIAS_COLORS,
        yAxes=[
            G.YAxis(format=G.OPS_FORMAT),
            G.YAxis(format=G.SHORT_FORMAT),
        ],
        **kwargs
    ))


def stacked(graph):
    """Turn a graph into a stacked graph."""
    return attr.assoc(
        graph,
        lineWidth=0,
        nullPointMode=G.NULL_AS_ZERO,
        stack=True,
        fill=10,
        tooltip=G.Tooltip(
            valueType=G.INDIVIDUAL,
        ),
    )


def PercentUnitAxis(label=None):
    """A Y axis that shows a percentage based on a unit value."""
    return G.YAxis(
        format=G.PERCENT_UNIT_FORMAT,
        label=label,
        logBase=1,
        max=1,
        min=0,
    )
