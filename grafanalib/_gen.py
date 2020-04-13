"""Generate JSON Grafana dashboards."""

import argparse
import json
import os
import sys


DASHBOARD_SUFFIX = '.dashboard.py'


class DashboardError(Exception):
    """Raised when there is something wrong with a dashboard."""


def load_dashboard(path):
    """Load a ``Dashboard`` from a Python definition.

    :param str path: Path to a *.dashboard.py file that defines a variable,
        ``dashboard``.
    :return: A ``Dashboard``
    """
    if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
        import importlib.util
        spec = importlib.util.spec_from_file_location("dashboard", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        import importlib
        module = importlib.load_source("dashboard", path)
    marker = object()
    dashboard = getattr(module, 'dashboard', marker)
    if dashboard is marker:
        raise DashboardError(
            "Dashboard definition {} does not define 'dashboard'".format(path))
    return dashboard


class DashboardEncoder(json.JSONEncoder):
    """Encode dashboard objects."""

    def default(self, obj):
        to_json_data = getattr(obj, 'to_json_data', None)
        if to_json_data:
            return to_json_data()
        return json.JSONEncoder.default(self, obj)


def write_dashboard(dashboard, stream):
    json.dump(
        dashboard.to_json_data(), stream, sort_keys=True, indent=2,
        cls=DashboardEncoder)
    stream.write('\n')


def print_dashboard(dashboard):
    write_dashboard(dashboard, stream=sys.stdout)


def write_dashboards(paths):
    for path in paths:
        dashboard = load_dashboard(path)
        with open(get_json_path(path), 'w') as json_file:
            write_dashboard(dashboard, json_file)


def get_json_path(path):
    assert path.endswith(DASHBOARD_SUFFIX)
    return '{}.json'.format(path[:-len(DASHBOARD_SUFFIX)])


def dashboard_path(path):
    abspath = os.path.abspath(path)
    if not abspath.endswith(DASHBOARD_SUFFIX):
        raise argparse.ArgumentTypeError(
            'Dashboard file {} does not end with {}'.format(
                path, DASHBOARD_SUFFIX))
    return abspath


def generate_dashboards(args):
    """Script for generating multiple dashboards at a time."""
    parser = argparse.ArgumentParser(prog='generate-dashboards')
    parser.add_argument(
        'dashboards', metavar='DASHBOARD', type=os.path.abspath,
        nargs='+', help='Path to dashboard definition',
    )
    opts = parser.parse_args(args)
    try:
        write_dashboards(opts.dashboards)
    except DashboardError as e:
        sys.stderr.write('ERROR: {}\n'.format(e))
        return 1
    return 0


def generate_dashboard(args):
    parser = argparse.ArgumentParser(prog='generate-dashboard')
    parser.add_argument(
        '--output', '-o', type=os.path.abspath,
        help='Where to write the dashboard JSON'
    )
    parser.add_argument(
        'dashboard', metavar='DASHBOARD', type=os.path.abspath,
        help='Path to dashboard definition',
    )
    opts = parser.parse_args(args)
    try:
        dashboard = load_dashboard(opts.dashboard)
        if not opts.output:
            print_dashboard(dashboard)
        else:
            with open(opts.output, 'w') as output:
                write_dashboard(dashboard, output)
    except DashboardError as e:
        sys.stderr.write('ERROR: {}\n'.format(e))
        return 1
    return 0


def run_script(f):
    sys.exit(f(sys.argv[1:]))


def generate_dashboards_script():
    """Entry point for generate-dashboards."""
    run_script(generate_dashboards)


def generate_dashboard_script():
    """Entry point for generate-dasboard."""
    run_script(generate_dashboard)
