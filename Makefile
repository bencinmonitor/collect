.PHONY: clean docker-clean docker-clean-volumes

docker-clean-volumes:
	docker volume ls -q | xargs -n1 docker volume rm

docker-clean-containers:
	docker ps -aq | xargs -n1 docker rm -vf

docker-clean: | docker-clean-containers docker-clean-volumes

clean: docker-clean
	rm -rf data-redis/*
	rm -rf data/full/*
