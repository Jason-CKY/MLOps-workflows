import os
import mlflow
from mlflow.tracking import MlflowClient

model_path = os.environ['MODEL_PATH']
mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])

loaded_model = mlflow.pyfunc.load_model(model_path)
client = MlflowClient()

production_run_id = [
    model.run_id for model in
    client.get_registered_model(model_path.split('/')[1]).latest_versions
    if model.current_stage == model_path.split('/')[-1]
][0]

local_path = client.download_artifacts(
    production_run_id, "imagenet_classes.txt"
)
with open(local_path, "r") as f:
    categories = [s.strip() for s in f.readlines()]
