"""
Model server script that polls Redis for images to classify

Adapted from https://www.pyimagesearch.com/2018/02/05/deep-learning-production-keras-redis-flask-apache/
"""
import base64
import json
import os
import logging
import time
import io
import numpy as np
import redis

import torch
from torchvision import transforms
from PIL import Image

logging.basicConfig(level=logging.INFO)

logging.info("Downloading model")
from download_model import loaded_model, categories
logging.info("Model downloaded")

# Connect to Redis server
db = redis.StrictRedis(host=os.environ.get("REDIS_HOST"))
preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    ),
])


def prepare_image(img, shape):
    img = Image.open(io.BytesIO(base64.b64decode(img)))
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(shape)
    img = preprocess(img).unsqueeze(0).numpy()
    return img


def classify_process():
    # Continually poll for new images to classify
    while True:
        # Pop off multiple images from Redis queue atomically
        with db.pipeline() as pipe:
            pipe.lrange(
                os.environ.get("REDIS_QUEUE"), 0,
                int(os.environ.get("BATCH_SIZE")) - 1
            )
            pipe.ltrim(
                os.environ.get("REDIS_QUEUE"),
                int(os.environ.get("BATCH_SIZE")), -1
            )
            queue, _ = pipe.execute()

        imageIDs = []
        batch = None
        for q in queue:
            # Deserialize the object and obtain the input image
            q = json.loads(q.decode("utf-8"))
            image = prepare_image(
                q['image'], (
                    int(os.environ.get("IMAGE_WIDTH")),
                    int(os.environ.get("IMAGE_HEIGHT"))
                )
            )

            # Check to see if the batch list is None
            if batch is None:
                batch = image

            # Otherwise, stack the data
            else:
                batch = np.vstack([batch, image])

            # Update the list of image IDs
            imageIDs.append(q["id"])

        # Check to see if we need to process the batch
        if len(imageIDs) > 0:
            # Classify the batch
            logging.info("* Batch size: {}".format(batch.shape))
            preds = loaded_model.predict(batch)
            for (imageID, result) in zip(imageIDs, preds):
                # Initialize the list of output predictions
                output = []

                probabilities = torch.nn.functional.softmax(
                    torch.tensor(result), dim=0
                )
                top5_prob, top5_catid = torch.topk(probabilities, 5)
                for i in range(top5_prob.size(0)):
                    r = {
                        "label": categories[top5_catid[i]],
                        "probability": top5_prob[i].item()
                    }
                    output.append(r)

                # Store the output predictions in the database, using image ID as the key so we can fetch the results
                db.set(imageID, json.dumps(output))

        # Sleep for a small amount
        time.sleep(float(os.environ.get("SERVER_SLEEP")))


if __name__ == "__main__":
    classify_process()
