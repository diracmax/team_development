# docker commands
up:
	make migrations
	make migrate
	docker-compose up

build:
	docker-compose build

stop:
	docker-compose stop

down:
	docker-compose down --rmi all --volumes --remove-orphans

clean:
	make cprune
	make iprune

iprune:
	docker image prune

cprune:
	docker container prune

ps:
	docker-compose ps

app:
	docker-compose exec app bash

# django commands
migrations:
	python django/manage.py makemigrations

migrate:
	python django/manage.py migrate
