#!/usr/bin/env bash
set -ex
find ./data/full/*.jpg | parallel --verbose --progress -j 7 \
  './ocr-machine.sh --image {} > {.}.txt'