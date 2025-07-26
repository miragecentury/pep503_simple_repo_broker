#!/usr/bin/env bash

set -eo pipefail

skaffold build -p prd-mgt -q | skaffold deploy -p prd-mgt --build-artifacts -
