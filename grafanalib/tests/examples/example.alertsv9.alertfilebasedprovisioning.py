"""Example grafana 9.x+ Alert"""


from grafanalib.core import (
    AlertGroup,
    AlertRulev9,
    Target,
    AlertCondition,
    AlertExpression,
    AlertFileBasedProvisioning,
    GreaterThan,
    OP_AND,
    RTYPE_LAST,
    EXP_TYPE_CLASSIC,
    EXP_TYPE_REDUCE,
    EXP_TYPE_MATH
)

# An AlertGroup is one group contained in an alert folder.
alertgroup = AlertGroup(
    name="Production Alerts",
    # Each AlertRule forms a separate alert.
    rules=[
        # Alert rule using classic condition > 3
        AlertRulev9(
            # Each rule must have a unique title
            title="Alert for something 3",
            uid='alert3',
            # Several triggers can be used per alert
            condition='B',
            triggers=[
                # A target refId must be assigned, and exist only once per AlertRule.
                Target(
                    expr="from(bucket: \"sensors\")\n  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)\n  |> filter(fn: (r) => r[\"_measurement\"] == \"remote_cpu\")\n  |> filter(fn: (r) => r[\"_field\"] == \"usage_system\")\n  |> filter(fn: (r) => r[\"cpu\"] == \"cpu-total\")\n  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)\n  |> yield(name: \"mean\")",
                    # Set datasource to name of your datasource
                    datasource="influxdb",
                    refId="A",
                ),
                AlertExpression(
                    refId="B",
                    expressionType=EXP_TYPE_CLASSIC,
                    expression='A',
                    conditions=[
                        AlertCondition(
                            evaluator=GreaterThan(3),
                            operator=OP_AND,
                            reducerType=RTYPE_LAST
                        )
                    ]
                )
            ],
            annotations={
                "summary": "The database is down",
                "runbook_url": "runbook-for-this-scenario.com/foo",
            },
            labels={
                "environment": "prod",
                "slack": "prod-alerts",
            },
            evaluateFor="3m",
        ),
        # Alert rule using reduce and Math
        AlertRulev9(
            # Each rule must have a unique title
            title="Alert for something 4",
            uid='alert4',
            condition='C',
            # Several triggers can be used per alert
            triggers=[
                # A target refId must be assigned, and exist only once per AlertRule.
                Target(
                    expr="from(bucket: \"sensors\")\n  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)\n  |> filter(fn: (r) => r[\"_measurement\"] == \"remote_cpu\")\n  |> filter(fn: (r) => r[\"_field\"] == \"usage_system\")\n  |> filter(fn: (r) => r[\"cpu\"] == \"cpu-total\")\n  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)\n  |> yield(name: \"mean\")",
                    # Set datasource to name of your datasource
                    datasource="influxdb",
                    refId="A",
                ),
                AlertExpression(
                    refId="B",
                    expressionType=EXP_TYPE_REDUCE,
                    expression='A',
                    reduceFunction='mean',
                    reduceMode='dropNN'
                ),
                AlertExpression(
                    refId="C",
                    expressionType=EXP_TYPE_MATH,
                    expression='$B < 3'
                )
            ],
            annotations={
                "summary": "The database is down",
                "runbook_url": "runbook-for-this-scenario.com/foo",
            },
            labels={
                "environment": "prod",
                "slack": "prod-alerts",
            },
            evaluateFor="3m",
        )
    ]
)

alertfilebasedprovisioning = AlertFileBasedProvisioning([alertgroup])
