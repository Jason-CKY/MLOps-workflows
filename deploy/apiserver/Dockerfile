FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as deploy

COPY ./deploy/apiserver/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./apiserver/app /app/app

FROM deploy as dev

COPY ./deploy/apiserver/requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt

COPY ./apiserver /app
