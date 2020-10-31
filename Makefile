test:
	docker-compose -f local.yml run --rm test python -m pytest
build:
	docker-compose -f local.yml build
run:
	docker-compose -f local.yml up -d
run:
	docker-compose -f local.yml down
precom:
    pre-commit run -a
