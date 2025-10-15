#!/usr/bin/env sh

cd "$(dirname "$0")" || return

./build.sh
cd public && python3 -m http.server 8888
