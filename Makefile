
start-mlflow:
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml up -d

stop-mlflow:
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml down

destroy-mlflow:
	docker-compose --env-file config/mlflow/creds.env -f docker-compose-mlflow.yml down -v
