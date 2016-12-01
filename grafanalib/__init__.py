"""Routines for building Grafana dashboards."""

# TODO
# - [ ] Automatically calculate `id`, rather than requiring it to be specified
# - [ ] Do something about having to specify two Y axes.
#
# Possibly:
# - [ ] Change core.py to return custom objects that are then rendered to JSON,
#       rather than naive dicts. This will make other things much easier (auto
#       id, linter, better errors)
# - [ ] `RedRow` function to make QPS & latency row?
# - [ ] Auto scale span size to match row?
# - [ ] Linter that operates on Python rather than generated JSON?
# - [ ] Drop the `as G` import and have a custom linter detect undefined names
# - [ ] Open source & blog
