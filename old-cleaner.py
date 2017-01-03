#!/usr/bin/env python

from glob import glob
from os.path import getmtime
from os import stat, getenv
import logging as log
from datetime import datetime, timedelta
from time import sleep

FULL_IMAGES_PATH = "data/full/*"
MAX_IMAGES_AGE = {'days': 1}
SLEEP_TIME = int(getenv("SLEEP_TIME", str(60 * 60 * 2)))  # Every 2 hours


def main():
    log.basicConfig(level=log.DEBUG, format='%(levelname)s:%(message)s')
    now = datetime.today()
    max_age = timedelta(**MAX_IMAGES_AGE)

    log.info("Removing old images.")
    for file, m_time in [(file, datetime.fromtimestamp(stat(file).st_mtime)) for file in glob(FULL_IMAGES_PATH)
                         if now - datetime.fromtimestamp(stat(file).st_mtime) > max_age]:
        log.info("Removing %s" % file)

    log.info("Going to sleep.")
    sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
