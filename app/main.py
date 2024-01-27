import os
import shutil
from typing import Union
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

from fastapi import FastAPI, Request, Form, UploadFile, File

from src.modules.image_classification import test_image

load_dotenv()

DATA_PATH = os.getenv("DATA_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")
METRICS_PATH = os.getenv("METRICS_PATH")

templates = Jinja2Templates(directory="src/templates")

app = FastAPI()

@app.get("/")
def read_form(request: Request):
    result = {"done":False}
    return templates.TemplateResponse("form.html", {"request": request, "result": result})

@app.post("/")
def form_post(request: Request, num: int = Form(...)):
    result = f"You entered {num}"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post("/uploadfile/")
async def create_upload_file(request: Request, ufile: UploadFile = File(...)):
    path = f"temp/{ufile.filename}"
    with open(path, 'w+b') as file:
        shutil.copyfileobj(ufile.file, file)
    result = test_image(path)
    if len(result) > 0:
        result = result[0]
    else:
        result = "Couldn't classify the image :()"
    result = {"done":True, "classification": result}
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})
    
