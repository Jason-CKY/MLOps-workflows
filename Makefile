.DEFAULT_GOAL := help

# declares .PHONY which will run the make command even if a file of the same name exists
.PHONY: help
help:			## Help command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: lint
lint:			## Lint check
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src odinuge/yapf:latest yapf \
	--style '{based_on_style: pep8, dedent_closing_brackets: true, coalesce_brackets: true}' \
	--no-local-style --verbose --recursive --diff --parallel apiserver modelserver

.PHONY: format
format:			## Format code in place to conform to lint check
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src odinuge/yapf:latest yapf \
	--style '{based_on_style: pep8, dedent_closing_brackets: true, coalesce_brackets: true}' \
	--no-local-style --verbose --recursive --in-place --parallel apiserver modelserver

.PHONY: pyflakes
pyflakes:		## Pyflakes check for any unused variables/classes
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src python:3.8 \
	/bin/bash -c "pip install --upgrade pyflakes && python -m pyflakes /src && echo 'pyflakes passed!'"

.PHONY: start-mlflow	
start-mlflow:	## Start mlflow deployment via docker-compose
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml up -d

.PHONY: stop-mlflow
stop-mlflow:	## Stop mlflow deployment via docker-compose
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml down

.PHONY: destroy-mlflow
destroy-mlflow:	## Destroy mlflow deployment via docker-compose with volumes
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml down -v

.PHONY: deploy
deploy:		## deploy api with models in mlflow and monitoring deployed
	docker-compose --env-file config/mlflow/creds.env \
	-f docker-compose-mlflow.yml \
	-f docker-compose.yml \
	-f docker-compose-monitoring.yml \
	up --build -d

.PHONY: destroy
destroy:		## Bring down all hosted services with their volumes
	docker-compose --env-file config/mlflow/creds.env \
	-f docker-compose-mlflow.yml \
	-f docker-compose.yml \
	-f docker-compose-monitoring.yml \
	down -v

.PHONY: get-config
get-config:		## Get config by combining all the docker-compose files by running docker-compose config
	docker-compose --env-file config/mlflow/creds.env \
	-f docker-compose-mlflow.yml \
	-f docker-compose.yml  \
	-f docker-compose-monitoring.yml \
	config > config.yaml