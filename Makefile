start_boot2docker:
	boot2docker up

build:
	boot2docker build

migrate:
	docker-compose run web python manage.py migrate

run:
	docker-compose up

test:
	docker-compose run web python manage.py test healthcheck
