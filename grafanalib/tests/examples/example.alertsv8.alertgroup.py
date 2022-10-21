"""Example grafana 8.x+ Alert"""


from grafanalib.core import (
    AlertGroup,
    AlertRulev8,
    Target,
    AlertCondition,
    LowerThan,
    OP_OR,
    OP_AND,
    RTYPE_LAST
)

# An AlertGroup is one group contained in an alert folder.
alertgroup = AlertGroup(
    name="Production Alerts",
    # Each AlertRule forms a separate alert.
    rules=[
        AlertRulev8(
            # Each rule must have a unique title
            title="Database is unresponsive",
            # Several triggers can be used per alert, a trigger is a combination of a Target and its AlertCondition in a tuple.
            triggers=[
                (
                    # A target refId must be assigned, and exist only once per AlertRule.
                    Target(
                        expr='sum(kube_pod_container_status_ready{exported_pod=~"database-/*"})',
                        # Set datasource to name of your datasource
                        datasource="VictoriaMetrics",
                        refId="A",
                    ),
                    AlertCondition(
                        evaluator=LowerThan(1),
                        # To have the alert fire when either of the triggers are met in the rule, set both AlertCondition operators to OP_OR.
                        operator=OP_OR,
                        reducerType=RTYPE_LAST
                    )
                ),
                (
                    Target(
                        expr='sum by (app) (count_over_time({app="database"}[5m]))',
                        # Set datasource to name of your datasource
                        datasource="Loki",
                        refId="B",
                    ),
                    AlertCondition(
                        evaluator=LowerThan(1000),
                        operator=OP_OR,
                        reducerType=RTYPE_LAST
                    )
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
            evaluateInterval="1m",
            evaluateFor="3m",
        ),

        # Second alert
        AlertRulev8(
            title="Service API blackbox failure",
            triggers=[
                (
                    Target(
                        expr='probe_success{instance="my-service.foo.com/ready"}',
                        # Set datasource to name of your datasource
                        datasource="VictoriaMetrics",
                        refId="A",
                    ),
                    AlertCondition(
                        evaluator=LowerThan(1),
                        operator=OP_AND,
                        reducerType=RTYPE_LAST,
                    )
                )
            ],
            annotations={
                "summary": "Service API has been unavailable for 3 minutes",
                "runbook_url": "runbook-for-this-scenario.com/foo",
            },
            labels={
                "environment": "prod",
                "slack": "prod-alerts",
            },
            evaluateInterval="1m",
            evaluateFor="3m",
        )
    ]
)
