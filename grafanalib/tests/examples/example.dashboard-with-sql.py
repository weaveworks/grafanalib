from grafanalib.core import (
    Dashboard,
    Graph,
    GridPos,
    OPS_FORMAT,
    RowPanel,
    SHORT_FORMAT,
    SqlTarget,
    YAxes,
    YAxis,
)


dashboard = Dashboard(
    title="Random stats from SQL DB",
    panels=[
        RowPanel(title="New row", gridPos=GridPos(h=1, w=24, x=0, y=8)),
        Graph(
            title="Some SQL Queries",
            dataSource="Your SQL Source",
            targets=[
                SqlTarget(
                    rawSql='SELECT date as "time", metric FROM example WHERE $__timeFilter("time")',
                    refId="A",
                ),
            ],
            yAxes=YAxes(
                YAxis(format=OPS_FORMAT),
                YAxis(format=SHORT_FORMAT),
            ),
            gridPos=GridPos(h=8, w=24, x=0, y=9),
        ),
    ],
).auto_panel_ids()
