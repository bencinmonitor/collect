#!/usr/bin/env bash
set -ex

while true; do
  $@
  echo "Sleeping with " $SLEEP_TIME
  sleep
done

