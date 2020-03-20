"""
This is an exemplary Grafana board that uses an elasticsearch datasource.

The graph shows the following metrics for HTTP requests to the URL path "/login":
- number of successful requests resulted in a HTTP response code between 200-300
- number of failed requests resulted in a HTTP response code between 400-500,
- Max. response time per point of time of HTTP requests
"""

from grafanalib.core import (
    Dashboard, Graph, Legend, NULL_AS_NULL, Row, SECONDS_FORMAT,
    SHORT_FORMAT, YAxes, YAxis
)

from grafanalib.elasticsearch import (
    DateHistogramGroupBy, ElasticsearchTarget, Filter,
    FiltersGroupBy, MaxMetricAgg
)

suc_label = "Success (200-300)"
clt_err_label = "Client Errors (400-500)"
resptime_label = "Max response time"

filters = [
    Filter(query="response: [200 TO 300]", label=suc_label),
    Filter(query="response: [400 TO 500]", label=clt_err_label),
]

tgts = [
    ElasticsearchTarget(
        query='request: "/login"',
        bucketAggs=[
            FiltersGroupBy(filters=filters),
            DateHistogramGroupBy(interval="10m")],
    ).auto_bucket_agg_ids(),
    ElasticsearchTarget(
        query='request: "/login"',
        metricAggs=[MaxMetricAgg(field="resptime")],
        alias=resptime_label,
    ).auto_bucket_agg_ids(),
]

g = Graph(
    title="login requests",
    dataSource="elasticsearch",
    targets=tgts,
    lines=False,
    legend=Legend(alignAsTable=True, rightSide=True,
                  total=True, current=True, max=True),
    lineWidth=1,
    nullPointMode=NULL_AS_NULL,
    seriesOverrides=[
        {
            "alias": suc_label,
            "bars": True,
            "lines": False,
            "stack": "A",
            "yaxis": 1,
            "color": "#629E51"
        },
        {
            "alias": clt_err_label,
            "bars": True,
            "lines": False,
            "stack": "A",
            "yaxis": 1,
            "color": "#E5AC0E"
        },
        {
            "alias": resptime_label,
            "lines": True,
            "fill": 0,
            "nullPointMode": "connected",
            "steppedLine": True,
            "yaxis": 2,
            "color": "#447EBC"
        },
    ],
    yAxes=YAxes(
        YAxis(
            label="Count",
            format=SHORT_FORMAT,
            decimals=0
        ),
        YAxis(
            label="Response Time",
            format=SECONDS_FORMAT,
            decimals=2
        ),
    ),
    transparent=True,
    span=12,
)

dashboard = Dashboard(title="HTTP dashboard", rows=[Row(panels=[g])])
