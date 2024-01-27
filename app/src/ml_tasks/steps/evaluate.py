import os
from joblib import load
import json
from pathlib import Path

from sklearn.metrics import accuracy_score

from .helper import load_data, load_one_image

def start_evaluation(repo_path, model_path, metrics_path):
    test_csv_path = repo_path / "prepared/test.csv"
    test_data, labels = load_data(test_csv_path)
    model = load(model_path / "model.joblib")
    predictions = model.predict(test_data)
    accuracy = accuracy_score(labels, predictions)
    metrics = {"accuracy": accuracy}
    accuracy_path = metrics_path / "accuracy.json"
    accuracy_path.write_text(json.dumps(metrics))

def test_one_image(image_path, model_path):
    test_data = load_one_image(image_path)
    model = load(model_path / "model.joblib")
    predictions = model.predict(test_data.reshape(1, -1))
    print(predictions)
    return predictions

if __name__ == "__main__":
    #repo_path = Path(__file__).parent.parent
    #start_evaluation(repo_path)
    MODEL_PATH = "models"
    model_path = Path(str(Path(__file__).parent.parent.parent.parent) + "/" + MODEL_PATH)
    image_path = "/Users/juandavidcruzgomez/Documents/perso/IMT/CursoIntersemestre2024/Tests/n03445777_70.JPEG"
    image = Path(image_path)
    test_one_image(image, model_path)
