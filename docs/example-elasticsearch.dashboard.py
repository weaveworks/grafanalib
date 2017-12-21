from grafanalib.core import *
from grafanalib.elasticsearch import *

suc_label = "Success (1XX)"
clt_err_label = "Client Errors (4XX)"
resptime_label = "Max response time"

filterSetting = FiltersAggSettings(filters=[
        Filter(query="response: [200 TO 300]", label=suc_label),
        Filter(query="response: [400 TO 500]", label=clt_err_label)])

tgts = [ElasticsearchTarget(query='request: "/login"',
                            bucket_aggs=[FiltersAgg(settings=filterSetting),
                                         DateTimeAgg(settings=DateTimeAggSettings(interval="10m"))]),
        ElasticsearchTarget(query='request: "/login"',
                            metrics=[MaxMetric(field="resptime")],
                            alias=resptime_label)]

g = Graph(title="login requests",
          dataSource="elasticsearch",
          targets=tgts,
          lines=False,
          legend=Legend(alignAsTable=True, rightSide=True,
                        total=True, current=True, max=True),
          lineWidth=1,
          nullPointMode=NULL_AS_NULL,
          seriesOverrides=[{
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
          yAxes=[YAxis(label="Count",
                       format=SHORT_FORMAT,
                       decimals=0
                       ),
                 YAxis(label="Response Time",
                       format=SECONDS_FORMAT,
                       decimals=2)],
                      transparent=True,
          span=12,
    )

dashboard = Dashboard(title="HTTP dashboard",
                      rows=[Row(panels=[g])])
