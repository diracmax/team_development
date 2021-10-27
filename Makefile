# docker commands
up:
	docker-compose -f django/docker-compose.yml up --build

build:
	docker-compose -f django/docker-compose.yml build

re:
	make down
	make

stop:
	docker-compose -f django/docker-compose.yml stop

down:
	docker-compose -f django/docker-compose.yml down --rmi all --volumes --remove-orphans

clean:
	make cprune
	make iprune

iprune:
	docker image prune

cprune:
	docker container prune

ps:
	docker-compose -f django/docker-compose.yml ps

app:
	docker-compose -f django/docker-compose.yml exec app bash

test:
	docker-compose -f django/docker-compose.yml exec app python manage.py test

migrate:
	docker-compose -f django/docker-compose.yml exec app python manage.py makemigrations
	docker-compose -f django/docker-compose.yml exec app python manage.py migrate

superuser:
	docker-compose -f django/docker-compose.yml exec app python manage.py createsuperuser

backup_all:
	docker-compose -f django/docker-compose.yml exec app python manage.py dumpdata --indent=2 --exclude=admin --exclude=auth --exclude=contenttypes --exclude=sessions > backup_all.json

backup_category:
	docker-compose -f django/docker-compose.yml exec app python manage.py dumpdata --indent=2 timeline.category > django\timeline\fixtures\category_backup.json

setup_category:
	docker-compose -f django/docker-compose.yml exec app python manage.py loaddata category_initial.json

populate_user:
	docker-compose -f django/docker-compose.yml exec app python populate.py user 5

populate_post:
	docker-compose -f django/docker-compose.yml exec app python populate.py post 100

populate_apply:
	docker-compose -f django/docker-compose.yml exec app python populate.py apply 1000

populate_like:
	docker-compose -f django/docker-compose.yml exec app python populate.py like 1000

populate:
	docker-compose -f django/docker-compose.yml exec app python populate.py user 10
	docker-compose -f django/docker-compose.yml exec app python populate.py post 100
	docker-compose -f django/docker-compose.yml exec app python populate.py follow 50
	docker-compose -f django/docker-compose.yml exec app python populate.py apply 1000
	docker-compose -f django/docker-compose.yml exec app python populate.py like 1000

python:
	docker-compose -f django/docker-compose.yml exec app python