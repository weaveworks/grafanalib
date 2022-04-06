"""Tests for Elasticsearch datasource"""

import grafanalib.core as G
import grafanalib.elasticsearch as E
from grafanalib import _gen
from io import StringIO


def test_serialization_elasticsearch_expression_target():
    """Serializing a graph doesn't explode."""
    graph = G.Graph(
        title="Elastic panel title",
        dataSource="elastic-datasource",
        targets=[
            E.ExpressionTarget(),
        ],
        id=1,
        yAxes=G.YAxes(
            G.YAxis(format=G.SHORT_FORMAT, label="ms"),
            G.YAxis(format=G.SHORT_FORMAT),
        ),
    )
    stream = StringIO()
    _gen.write_dashboard(graph, stream)
    assert stream.getvalue() != ''


def test_serialization_elasticsearch_expression_target_with_parameters():
    """Test Elasticsearch Expression target"""
    elastic_expression = "(1-($B+0.000001)/($A+$B+0.001))*100"
    ref_id = "C"

    target = E.ExpressionTarget(
        expression=elastic_expression,
        hide=False,
        refId=ref_id
    )

    data = target.to_json_data()

    assert data["expression"] == elastic_expression
    assert data["datasource"] == "__expr__"
    assert data["mode"] == "math"
    assert data["refId"] == ref_id
    assert data["hide"] is False
