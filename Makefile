
start-mlflow:
	docker-compose -f docker-compose-mlflow.yml up -d

stop-mlflow:
	docker-compose -f docker-compose-mlflow.yml down

destroy-mlflow:
	docker-compose -f docker-compose-mlflow.yml down -v
