from joblib import dump
from pathlib import Path

from sklearn.linear_model import SGDClassifier

from .helper import load_data


def start_training(repo_path, model_path):
    train_csv_path = repo_path / "prepared/train.csv"
    train_data, labels = load_data(train_csv_path)
    sgd = SGDClassifier(max_iter=100)
    trained_model = sgd.fit(train_data, labels)
    dump(trained_model, model_path / "model.joblib")


if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    start_training(repo_path)
