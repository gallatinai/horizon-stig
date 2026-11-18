#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

step() {
  local name=$1
  shift
  if "$@"; then
    echo "PASS: $name"
  else
    echo "FAIL: $name" >&2
    exit 1
  fi
}

step build_review python3 scripts/build_review.py
step summarize_review python3 scripts/summarize_review.py
step generate_cklb python3 scripts/generate_cklb.py
step validate python3 scripts/validate.py
step unittest python3 -m unittest discover -s tests
