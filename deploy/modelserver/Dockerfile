FROM bitnami/pytorch:latest

COPY ./deploy/modelserver/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./modelserver /app

WORKDIR /app

CMD ["python", "/app/main.py"]
