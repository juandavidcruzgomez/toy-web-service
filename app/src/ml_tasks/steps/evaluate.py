import os
from joblib import load
import json
from pathlib import Path

from sklearn.metrics import accuracy_score

from .helper import load_data

def start_evaluation(repo_path, model_path, metrics_path):
    test_csv_path = repo_path / "prepared/test.csv"
    test_data, labels = load_data(test_csv_path)
    model = load(model_path / "model.joblib")
    predictions = model.predict(test_data)
    accuracy = accuracy_score(labels, predictions)
    metrics = {"accuracy": accuracy}
    accuracy_path = metrics_path / "accuracy.json"
    accuracy_path.write_text(json.dumps(metrics))

if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    start_evaluation(repo_path)
