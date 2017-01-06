.PHONY: clean docker-clean docker-clean-volumes test

COLLECT_IMAGE=bencinmonitor/collect

docker-up-local:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.local.yml up

build:
	docker build -t $(COLLECT_IMAGE):latest .

docker-clean-volumes:
	docker volume ls -q | xargs -n1 docker volume rm

docker-clean-containers:
	docker ps -aq | xargs -n1 docker rm -vf

docker-clean: | docker-clean-containers docker-clean-volumes

test:
	docker-compose -f docker-compose.test.yml run scraper

clean: docker-clean
	rm -rf data-redis/*
	rm -rf data/full/*
