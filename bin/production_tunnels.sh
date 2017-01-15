#!/usr/bin/env bash
set -ex

ssh -v -2 -o ExitOnForwardFailure=yes \
  -L 0.0.0.0:27017:0.0.0.0:27017 \
  -L 0.0.0.0:6379:0.0.0.0:6379 \
  -L 0.0.0.0:9181:0.0.0.0:9181 a1 cat