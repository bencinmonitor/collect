#!/usr/bin/env bash
set -e

ssh -o ExitOnForwardFailure=yes \
  -L 27017:localhost:27017 \
  -L 6379:localhost:6379 \
  -L 9181:localhost:9181 a1 cat