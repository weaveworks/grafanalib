"""Weave-specific dashboard configuration.

Unlike 'core', which has logic for building generic Grafana dashboards, this
has our Weave-specific preferences.
"""

import grafanalib.core as G

import string


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
}


def PromGraph(title, expressions, id, **kwargs):
    """Create a graph that renders Prometheus data.

    :param title: The title of the graph.
    :param expressions: List of tuples of (legend, expr), where 'expr' is a
        Prometheus expression.
    :param id: The id for the graph, unique within the dashboard.
    :param kwargs: Passed on to Graph.
    """
    letters = string.ascii_uppercase
    expressions = list(expressions)
    if len(expressions) > len(letters):
        raise ValueError(
            'Too many expressions. Can support at most {}, but got {}'.format(
                len(letters), len(expressions)))
    targets = [
        G.Target(expr, legend, refId=refId)
        for ((legend, expr), refId) in zip(expressions, letters)]
    return G.Graph(
        title=title,
        dataSource=PROMETHEUS,
        targets=targets,
        id=id,
        **kwargs
    )


def QPSGraph(title, expressions, id, **kwargs):
    """Create a graph of QPS, broken up by response code.

    Data is drawn from Prometheus.

    :param title: Title of the graph.
    :param expressions: List of Prometheus expressions. Must be 5.
    :param id: The id for the graph, unique within the dashboard.
    :param kwargs: Passed on to Graph.
    """
    if len(expressions) != 5:
        raise ValueError('Expected 5 expressions, got {}: {}'.format(
            len(expressions), expressions))
    legends = sorted(ALIAS_COLORS.keys())
    exprs = zip(legends, expressions)
    return PromGraph(
        title=title,
        expressions=exprs,
        aliasColors=ALIAS_COLORS,
        id=id,
        yAxes=[
            G.YAxis(format=G.OPS_FORMAT),
            G.YAxis(format=G.SHORT_FORMAT),
        ],
        **kwargs
    )


def stacked(graph):
    """Turn a graph into a stacked graph."""
    newGraph = dict(graph)  # Shallow copy.
    newGraph.update(dict(
        # Bit of a gotcha here. `graph` is a Python dictionary form of the
        # Grafana JSON object (i.e. an AST). In the Python DSL, we use
        # consistent camelCase naming, but Grafana itself is inconsistent.
        # Thus, what was specified as `lineWidth` when passed to Graph is
        # overridden as `linewidth` here.
        linewidth=0,
        nullPointMode=G.NULL_AS_ZERO,
        stack=True,
        fill=10,
        tooltip=G.Tooltip(
            valueType=G.INDIVIDUAL,
        ),
    ))
    return newGraph


def PercentUnitAxis(label=None):
    """A Y axis that shows a percentage based on a unit value."""
    return G.YAxis(
        format=G.PERCENT_UNIT_FORMAT,
        label=label,
        logBase=1,
        max=1,
        min=0,
    )
