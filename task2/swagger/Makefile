.PHONY: all build run stop clean fclean re

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

fclean: clean
	docker system prune -a -f
	docker volume prune -f
	docker network prune -f

re: fclean all
