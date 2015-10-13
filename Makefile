start_boot2docker:
	boot2docker up

build:
	boot2docker build

migrate:
	docker-compose run web python manage.py migrate

shell:
	docker-compose run web python manage.py shell

run:
	docker-compose up

test:
	docker-compose run web python manage.py test healthcheck -v 2
