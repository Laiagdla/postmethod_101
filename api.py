from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks
from fastapi.responses import FileResponse, PlainTextResponse
from PIL import Image as PILimage
from io import BytesIO
from typing import List, Annotated
from pathlib import Path
from glob import glob
from time import sleep
import json

api = FastAPI()
#load the model
#api.state.model = load_model()

Path.mkdir(Path("images"), exist_ok=True)

@api.get("/")
def read_root():
    return {"postmethod_101": "simple app to test post methods api requests",
            "docs": "http://localhost:8000/docs"}


##### [EASY]
# simple save and return, in a single request
@api.post("/simple/")
def simple_save(image: UploadFile = File(...)):
    img = PILimage.open(BytesIO(image.file.read()))
    img.save(f"images/{image.filename}")
    # MODEL PREDICTION
    # prediction = api.state.model.predict(img)
    return {"status": "completed",
            "prediction": "model prediction",}


##### [ADVANCED]
# simple database to track predictions and retrieve them
def load_predictions():
    if Path.is_file(Path("predictions.json")):
        with open("predictions.json", "r") as f:
            return json.load(f)
    else:
        return {} #dictionary to store the predictions

def save_predictions(predictions):
    with open("predictions.json", "w") as f:
        json.dump(predictions, f)

api.state.predictions = load_predictions()

# simulated long running model prediction
def run_model_prediction(name):
    # MODEL PREDICTION
    # prediction = api.state.model.predict(img)
    sleep(10)  # Simulate a long-running task
    api.state.predictions[name] = "model prediction" #prediction
    save_predictions(api.state.predictions)


# single file upload to server with additional fields (name, optional)
@api.post("/save_image/")
async def save_image(image: Annotated[UploadFile, File()],
               name:  Annotated[str, Form()], # mandatory field
               optional:  Annotated[str, Form()] = None, # optional field
               background_tasks: BackgroundTasks = None): # optional field
    img = PILimage.open(BytesIO(image.file.read()))
    renamed = name + Path(image.filename).suffix
    img.save(f"images/{renamed}")

    # running model in the background
    background_tasks.add_task(run_model_prediction, name)

    return {"status": "image saved to server",
            "filename": renamed,
            "url": f"http://localhost:8000/get_image?name={name}"}

# get the image with the name coming from the post method
@api.get("/get_image")
async def get_image(name: str):
    print(api.state.predictions)
    while api.state.predictions.get(name) is None:
        sleep(1)
        return PlainTextResponse("processing", status_code=202)

    filename = Path(glob(f"images/{name}.*")[0])
    status = "completed"
    headers = { "filename": str(filename),
                "status": status,
                "prediction": api.state.predictions[name]}
    return FileResponse(filename, headers=headers)

# upload multiple files to server
@api.post("/save_images/")
def save_images(images: List[UploadFile] = File(...)):
    for image in images:
        img = PILimage.open(BytesIO(image.file.read()))
        img.save(f"images/{image.filename}")

    return {"status": "images saved to server",
            "filenames": [image.filename for image in images]}
