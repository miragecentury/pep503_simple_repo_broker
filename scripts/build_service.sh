#!/usr/bin/env bash

set -euo pipefail

pack build \
  -B paketobuildpacks/builder-jammy-base \
  --buildpack paketo-buildpacks/python \
  --trust-builder \
  --publish \
  ghcr.io/miragecentury/pep503_simple_repo_brokers
