"""
This is an exemplary Grafana board that uses a Cloudwatch datasource.

The graph shows the Average CPU utilization  from an ASG named "frontend-asg"
"""

from grafanalib.core import *
from grafanalib.cloudwatch import CloudwatchTarget


dashboard = Dashboard(
    title="Clowdwatch Stats",
    rows=[
        Row(panels=[
            Graph(
                title="Cloudwatch ASG",
                dataSource='Cloudwatch',
                targets=[
                    CloudwatchTarget(
                        dimensions={
                            "AutoScalingGroupName": "frontend-asg",
                        },
                        metricName="CPUUtilization",
                        namespace="AWS/EC2",
                        region="eu-west-1",
                        statistics=["Average"],
                        checkParams=True,
                    ),
                ],
                yAxes=G.YAxes(
                    YAxis(format=PERCENT_UNIT_FORMAT),
                    YAxis(format=SHORT_FORMAT),
                ),
            ),
        ]),
    ],
).auto_panel_ids()
