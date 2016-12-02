#!/usr/bin/env bash
set -e
LOG_LEVEL="INFO"

while true; do
    echo "Starting Petrol crawl"
    scrapy crawl petrol -L $LOG_LEVEL
    echo "Starting OMV crawl"
    scrapy crawl omv -L $LOG_LEVEL
    echo "Going to sleep for 10 seconds,..."
    sleep 10
done