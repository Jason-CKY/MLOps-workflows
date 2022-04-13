# MLOps Workflows

This repository contains workflows to version data with dvc, store models with Mlflow, deploy them with a scalable deployment architecture.

## Deployment Architecture
Serve a production-ready and scalable Keras-based deep learning model image classification using FastAPI, Redis and Docker Swarm. Based off this [series of blog posts](https://www.pyimagesearch.com/2018/02/05/deep-learning-production-keras-redis-flask-apache/).

## How to Use

### Prerequisites
Make sure you have a modern version of `docker` (>1.13.0)and `docker-compose` installed.

### Run with Docker Compose
Simply run `docker-compose up` to spin up all the services on your local machine.

### Test Service
* Test the `/predict` endpoint by passing in the included `doge.jpg` as parameter `img_file`:

```bash
curl -X POST -F img_file=@doge.jpg http://localhost/predict
```

You should see the predictions returned as a JSON response.

## Load Testing
We can use [locust](https://locust.io) and the included `locustfile.py` to load test our service. Run the following command to spin up `20` concurrent users immediately:

```bash
locust --host=http://localhost --no-web -c 20 -r 20
```

The `--no-web` flag runs locust in CLI mode. You may also want to use locust's web interface with all its pretty graphs, if so, just run `local --host=http://localhost`.


## TODOs:
* add mlflow integration (https://github.com/Toumash/mlflow-docker)
* add dvc
* add starting container to train a model and publish to mlflow
* Makefile
* readme documentation
