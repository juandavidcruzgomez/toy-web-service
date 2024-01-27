import os
from dotenv import load_dotenv
from skimage.io import imread_collection
from skimage.transform import resize
from joblib import load
from pathlib import Path
import numpy as np

load_dotenv()

def preprocess(image):
    resized = resize(image, (100, 100, 3))
    reshaped = resized.reshape((1, 30000))
    return reshaped

def load_image(image_path):
    image = imread_collection([str(image_path)])
    print(image)
    processed_image = preprocess(image[0])
    data = np.concatenate(processed_image, axis=0)
    print(data)
    return data
    
def test_image(image_path):
    model_path = Path(os.getenv("MODEL_PATH"))
    print(model_path)
    test_data = load_image(image_path)
    model = load(model_path / "model.joblib")
    predictions = model.predict(test_data.reshape(1, -1)) # This is done because in this case tere's just one sample
    return predictions