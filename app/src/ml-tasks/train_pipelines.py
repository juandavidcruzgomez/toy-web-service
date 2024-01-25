import os
from dotenv import load_dotenv

from pathlib import Path
import steps.prepare as prepare
import steps.train as train
import steps.evaluate as evaluate

load_dotenv()

DATA_PATH = os.getenv("DATA_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")
METRICS_PATH = os.getenv("METRICS_PATH")
#Prepare
repo_path = Path(str(Path(__file__).parent.parent.parent) + "/" + DATA_PATH)
print(repo_path)
prepare.start_preparation(repo_path)
#Train
model_path = Path(str(Path(__file__).parent.parent.parent) + "/" + MODEL_PATH)
print(model_path)
train.start_training(repo_path, model_path)
#Evaluate
metrics_path = Path(str(Path(__file__).parent.parent.parent) + "/" + METRICS_PATH)
evaluate.start_evaluation(repo_path, model_path, metrics_path)