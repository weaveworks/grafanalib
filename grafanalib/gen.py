# -*- mode: python; python-indent-offset: 2 -*-

"""Generate JSON Grafana dashboards."""

import json
import sys
from importlib.machinery import SourceFileLoader


class DashboardError(Exception):
  """Raised when there is something wrong with a dashboard."""


def load_dashboard(path):
  module = SourceFileLoader("dashboard", path).load_module()
  marker = object()
  dashboard = getattr(module, 'dashboard', marker)
  if dashboard is marker:
    raise DashboardError(
      "Dashboard definition {} does not define 'dashboard'".format(path))
  return dashboard


def write_dashboard(dashboard, stream):
  json.dump(dashboard, stream, sort_keys=True, indent=2)
  stream.write('\n')


def print_dashboard(dashboard):
  write_dashboard(dashboard, stream=sys.stdout)
