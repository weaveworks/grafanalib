from grafanalib.core import *


dashboard = Dashboard(
  title="Frontend Stats",
  rows=[
    Row(panels=[
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
        yAxes=[
          YAxis(format=OPS_FORMAT),
          YAxis(format=SHORT_FORMAT),
        ],
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
        )
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
      ),
    ]),
  ],
).auto_panel_ids()
