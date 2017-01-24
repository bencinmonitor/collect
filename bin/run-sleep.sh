#!/usr/bin/env bash
set -e

while true; do
  $@
  echo "Sleeping with " $SLEEP_TIME
  sleep $SLEEP_TIME
done

