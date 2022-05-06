FROM python:3.9 as deploy

COPY ./deploy/apiserver/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./deploy/apiserver/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./apiserver/app /app/app
WORKDIR /app/
ENV PYTHONPATH=/app

CMD ["/entrypoint.sh"]

FROM deploy as dev

COPY ./deploy/apiserver/requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt

COPY ./apiserver /app
