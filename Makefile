test:
	docker-compose -f local.yml run --rm app python -m pytest
	docker-compose -f local.yml run --rm test python -m pytest
build:
	docker-compose -f local.yml build
