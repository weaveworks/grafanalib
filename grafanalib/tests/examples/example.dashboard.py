from grafanalib.core import (
    Alert, AlertCondition, Dashboard, Graph, GridPos,
    GreaterThan, Notification, OP_AND, OPS_FORMAT, RowPanel, RTYPE_SUM, SECONDS_FORMAT,
    SHORT_FORMAT, single_y_axis, Target, TimeRange, YAxes, YAxis
)


dashboard = Dashboard(
    title="Frontend Stats",
    panels=[
        RowPanel(
            title="New row",
            gridPos=GridPos(h=1, w=24, x=0, y=8)
        ),
        Graph(
            title="Frontend QPS",
            dataSource='My Prometheus',
            targets=[
                Target(
                    expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"1.."}[1m]))',
                    legendFormat="1xx",
                    refId='A',
                ),
                Target(
                    expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"2.."}[1m]))',
                    legendFormat="2xx",
                    refId='B',
                ),
                Target(
                    expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"3.."}[1m]))',
                    legendFormat="3xx",
                    refId='C',
                ),
                Target(
                    expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"4.."}[1m]))',
                    legendFormat="4xx",
                    refId='D',
                ),
                Target(
                    expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"5.."}[1m]))',
                    legendFormat="5xx",
                    refId='E',
                ),
            ],
            yAxes=YAxes(
                YAxis(format=OPS_FORMAT),
                YAxis(format=SHORT_FORMAT),
            ),
            alert=Alert(
                name="Too many 500s on Nginx",
                message="More than 5 QPS of 500s on Nginx for 5 minutes",
                alertConditions=[
                    AlertCondition(
                        Target(
                            expr='sum(irate(nginx_http_requests_total{job="default/frontend",status=~"5.."}[1m]))',
                            legendFormat="5xx",
                            refId='A',
                        ),
                        timeRange=TimeRange("5m", "now"),
                        evaluator=GreaterThan(5),
                        operator=OP_AND,
                        reducerType=RTYPE_SUM,
                    ),
                ],
                notifications=[
                    Notification("notification_channel_uid"),
                ]
            ),
            gridPos=GridPos(h=1, w=12, x=0, y=9)
        ),
        Graph(
            title="Frontend latency",
            dataSource='My Prometheus',
            targets=[
                Target(
                    expr='histogram_quantile(0.5, sum(irate(nginx_http_request_duration_seconds_bucket{job="default/frontend"}[1m])) by (le))',
                    legendFormat="0.5 quantile",
                    refId='A',
                ),
                Target(
                    expr='histogram_quantile(0.99, sum(irate(nginx_http_request_duration_seconds_bucket{job="default/frontend"}[1m])) by (le))',
                    legendFormat="0.99 quantile",
                    refId='B',
                ),
            ],
            yAxes=single_y_axis(format=SECONDS_FORMAT),
            gridPos=GridPos(h=8, w=12, x=0, y=0)
        )
    ],
).auto_panel_ids()
