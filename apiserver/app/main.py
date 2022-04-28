"""
Web server script that exposes endpoints and pushes images to Redis for classification by model server. Polls
Redis for response from model server.

Adapted from https://www.pyimagesearch.com/2018/02/05/deep-learning-production-keras-redis-flask-apache/
"""
import base64
import io
import json
import time
import uuid
import logging

from PIL import Image
from pathlib import Path
import redis

from fastapi import FastAPI, File, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from app.core.settings import settings
from app.core.custom_metrics import model_metrics_f1, model_metrics_precision, model_metrics_recall
from prometheus_fastapi_instrumentator import Instrumentator, metrics


logger = logging.getLogger(settings.app_name)

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=None,
    redoc_url=None
)
app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')

db = redis.StrictRedis(host=settings.redis_host)

# Prometheus instrumentator
instrument = Instrumentator()
instrument.instrumentations.append(metrics.default())
instrument.add(model_metrics_f1())    
instrument.add(model_metrics_precision())
instrument.add(model_metrics_recall())
instrument.instrument(app).expose(app)

@app.get("/", include_in_schema=False)
def custom_docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        swagger_favicon_url='/static/logo.png'
    )

@app.post("/predict")
def predict(request: Request, img_file: bytes=File(...)):
    data = {"success": False}

    if request.method == "POST":
        image = Image.open(io.BytesIO(img_file))

        # Generate an ID for the classification then add the classification ID + image to the queue
        k = str(uuid.uuid4())
        image = base64.b64encode(img_file).decode("utf-8")
        d = {"id": k, "image": image}
        db.rpush(settings.redis_queue, json.dumps(d))

        # Keep looping for CLIENT_MAX_TRIES times
        num_tries = 0
        while num_tries < settings.client_max_tries:
            num_tries += 1

            # Attempt to grab the output predictions
            output = db.get(k)

            # Check to see if our model has classified the input image
            if output is not None:
                # Add the output predictions to our data dictionary so we can return it to the client
                output = output.decode("utf-8")
                data["predictions"] = json.loads(output)

                # Delete the result from the database and break from the polling loop
                db.delete(k)
                break

            # Sleep for a small amount to give the model a chance to classify the input image
            time.sleep(settings.client_sleep)

            # Indicate that the request was a success
            data["success"] = True
        else:
            raise HTTPException(status_code=400, detail="Request failed after {} tries".format(settings.client_max_tries))

    # Return the data dictionary as a JSON response
    return data
