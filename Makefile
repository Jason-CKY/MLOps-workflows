.DEFAULT_GOAL := help

# declares .PHONY which will run the make command even if a file of the same name exists
.PHONY: help
help:			## Help command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

lint:			## Lint check
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src odinuge/yapf:latest yapf \
	--style '{based_on_style: pep8, dedent_closing_brackets: true, coalesce_brackets: true}' \
	--no-local-style --verbose --recursive --diff --parallel apiserver modelserver

format:			## Format code in place to conform to lint check
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src odinuge/yapf:latest yapf \
	--style '{based_on_style: pep8, dedent_closing_brackets: true, coalesce_brackets: true}' \
	--no-local-style --verbose --recursive --in-place --parallel apiserver modelserver

pyflakes:		## Pyflakes check for any unused variables/classes
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src python:3.8 \
	/bin/bash -c "pip install --upgrade pyflakes && python -m pyflakes /src && echo 'pyflakes passed!'"
	
start-mlflow:	## Start mlflow deployment via docker-compose
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml up -d

stop-mlflow:	## Stop mlflow deployment via docker-compose
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml down

destroy-mlflow:	## Destroy mlflow deployment via docker-compose with volumes
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml down -v
