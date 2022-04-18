.DEFAULT_GOAL := help

# declares .PHONY which will run the make command even if a file of the same name exists
.PHONY: help
help:			## Help command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

start-mlflow:	## Start mlflow deployment via docker-compose
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml up -d

stop-mlflow:	## Stop mlflow deployment via docker-compose
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml down

destroy-mlflow:	## Destroy mlflow deployment via docker-compose with volumes
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml down -v
