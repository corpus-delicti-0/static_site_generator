#!/usr/bin/env sh

cd "$(dirname "$0")" || return

python3 src/main.py "$1"
