"""Helpers for Prometheus-driven graphs."""

import string

import grafanalib.core as G


def PromGraph(data_source, title, expressions, **kwargs):
    """Create a graph that renders Prometheus data.

    :param str data_source: The name of the data source that provides
        Prometheus data.
    :param title: The title of the graph.
    :param expressions: List of tuples of (legend, expr), where 'expr' is a
        Prometheus expression.
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
        dataSource=data_source,
        targets=targets,
        **kwargs
    )
