FROM python:3.8-slim-buster

COPY ./deploy/modelserver/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./modelserver /app

WORKDIR /app

CMD ["python", "/app/main.py"]
