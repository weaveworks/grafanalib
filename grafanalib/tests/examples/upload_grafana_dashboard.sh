#!/usr/bin/env bash

show_help_info () {
echo -e "\n\tERROR: $1"

cat <<HELPINFO
---
Usage:

Define environment variables: GRAFANA_SERVER and GRAFANA_API_KEY, e.g.

    https://grafana.com/docs/grafana/latest/http_api/auth/#create-api-token

    export GRAFANA_SERVER=grafana_server:3000
    export GRAFANA_API_KEY=asdf23vsd23

    ./upload_grafana_dashboard.sh </path/to/dashboard.json>

Example:

    ./upload_grafana_dashboard.sh dash.json

HELPINFO
}

function msg () { echo -e "$*"; }
function bail () { msg "\nError: ${1:-Unknown Error}\n"; exit ${2:-1}; }

# -------------------------------------------------------------------------
if [ -z "$1" ];then
    show_help_info "No dashboard parameter received"
    exit 1
fi

GRAFANA_API_KEY=${GRAFANA_API_KEY:-Unset}
if [[ $GRAFANA_API_KEY == Unset ]]; then
    echo -e "\\nError: GRAFANA_API_KEY environment variable not define.\\n"
    exit 1
fi
GRAFANA_SERVER=${GRAFANA_SERVER:-Unset}
if [[ $GRAFANA_SERVER == Unset ]]; then
    echo -e "\\nError: GRAFANA_SERVER environment variable not define.\\n"
    exit 1
fi
logfile="grafana_upload.log"

# Get path/file parm
DASHBOARD=$1

# Pull through jq to validate json
payload="$(jq . ${DASHBOARD}) >> $logfile"

# Upload the JSON to Grafana
curl -X POST \
  -H 'Content-Type: application/json' \
  -d "${payload}" \
  "http://api_key:$GRAFANA_API_KEY@$GRAFANA_SERVER/api/dashboards/db" -w "\n" | tee -a "$logfile"
