FROM continuumio/miniconda3

WORKDIR /app

COPY ./deploy/mlflow/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
