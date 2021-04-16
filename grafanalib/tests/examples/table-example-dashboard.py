#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NAME:
    table-example-dashboard.py

DESCRIPTION:
    This script creates Grafana dashboards using Grafanalib, and a static table
    which defines metrics/dashboards.

    The resulting dashboard can be easily uploaded to Grafana with associated script:

        upload_grafana_dashboard.sh

USAGE:
    Create and upload the dashboard:

    ./table-example-dashboard.py --title "My python dashboard" > dash.json
    ./upload_grafana_dashboard.sh dash.json

"""

import textwrap
import argparse
import sys
import io
import grafanalib.core as G
from grafanalib._gen import write_dashboard

DEFAULT_TITLE = "Python Example Dashboard"

# Simple example of table drive - good to enhance with Grid position, Legend etc.
metrics = [
    {'section': 'Monitor Tracking'},
    {'row': 1},
    {'title': 'Monitor Processes (by cmd)',
     'expr': ['monitor_by_cmd{serverid="$serverid"}',
              'sum(monitor_by_cmd{serverid="$serverid"})']},
    {'title': 'Monitor Processes (by user)',
     'expr': ['monitor_by_user{serverid="$serverid"}',
              'sum(monitor_by_user{serverid="$serverid"})']},
]


class CreateDashboard():
    "See module doc string for details"

    def __init__(self, *args, **kwargs):
        self.parse_args(__doc__, args)

    def parse_args(self, doc, args):
        "Common parsing and setting up of args"
        desc = textwrap.dedent(doc)
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=desc)
        parser.add_argument('-t', '--title', default=DEFAULT_TITLE,
                            help="Dashboard title. Default: " + DEFAULT_TITLE)
        self.options = parser.parse_args(args=args)

    def run(self):
        templateList = [G.Template(default="",
                                   dataSource="default",
                                   name="serverid",
                                   label="ServerID",
                                   query="label_values(serverid)")]

        dashboard = G.Dashboard(title=self.options.title,
                                templating=G.Templating(list=templateList))

        # Simple table processing - could be enhanced to use GridPos etc.
        for metric in metrics:
            if 'section' in metric:
                dashboard.rows.append(G.Row(title=metric['section'], showTitle=True))
                continue
            if 'row' in metric:
                dashboard.rows.append(G.Row(title='', showTitle=False))
                continue
            graph = G.Graph(title=metric['title'],
                            dataSource='default',
                            maxDataPoints=1000,
                            legend=G.Legend(show=True, alignAsTable=True,
                                            min=True, max=True, avg=True, current=True, total=True,
                                            sort='max', sortDesc=True),
                            yAxes=G.single_y_axis())
            ref_id = 'A'
            for texp in metric['expr']:
                graph.targets.append(G.Target(expr=texp,
                                              refId=ref_id))
                ref_id = chr(ord(ref_id) + 1)
            dashboard.rows[-1].panels.append(graph)

        # Auto-number panels - returns new dashboard
        dashboard = dashboard.auto_panel_ids()

        s = io.StringIO()
        write_dashboard(dashboard, s)
        print("""{
        "dashboard": %s
        }
        """ % s.getvalue())


if __name__ == '__main__':
    """ Main Program"""
    obj = CreateDashboard(*sys.argv[1:])
    obj.run()
