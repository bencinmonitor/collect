#!/usr/bin/env bash

set -ex

# HOST=a1.bencinmonitor.si
HOST=a1.univizor.si
BRANCH=master
REPO_PATH="~/repos/collect"
DATA_PATH="/srv/data/collect"
DOCKER_IMAGE="bencinmonitor/collect"

on_remote () {
  ssh $HOST $@
}

# Checkout code.
on_remote "[ -d "$REPO_PATH" ] || (mkdir -p $REPO_PATH && git clone --depth=1 --branch=master https://$GITHUB_ACCESS_TOKEN@github.com/bencinmonitor/collect.git $REPO_PATH)"

# Pull if composition changes
on_remote "cd $REPO_PATH && git fetch --all && git reset --hard origin/master && git pull"

# Pull image
on_remote "docker pull $DOCKER_IMAGE"

# Crete paths
on_remote "mkdir -p $DATA_PATH/{redis,mongo,images}"

# Volumes
#on_remote "docker volume create --opt type=none --opt device=$DATA_PATH/images --opt o=bind --name collect_images"
#on_remote "docker volume create --opt type=none --opt device=$DATA_PATH/redis --opt o=bind --name collect_redis_data"
#on_remote "docker volume create --opt type=none --opt device=$DATA_PATH/mongo --opt o=bind --name collect_mongo_data"

# Restart
#on_remote "cd $REPO_PATH && docker-compose build scrape_omv && docker-compose up --no-deps -d scrape_omv"
#on_remote "cd $REPO_PATH && docker-compose build scrape_petrol && docker-compose up --no-deps -d scrape_petrol"
#on_remote "cd $REPO_PATH && docker-compose build ocr_worker && docker-compose up --no-deps -d ocr_worker"