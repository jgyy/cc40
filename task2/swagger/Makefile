.PHONY: all build run stop clean

all: build run

build:
	docker compose build

run:
	docker compose up -d

log:
	docker compose logs swagger-ui

stop:
	docker compose down

clean:
	docker compose down --volumes --rmi all --remove-orphans

