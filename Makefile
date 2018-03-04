.PHONY: all run-dev tests build

all: build insert-users run-dev

build:
	docker-compose build; \

insert-users:
	docker-compose run api python users_stub/stub_data.py; \

run-dev:
	docker-compose up; \

tests:
	docker-compose run api nosetests; \
