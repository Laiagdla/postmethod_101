from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks
from fastapi.responses import FileResponse, PlainTextResponse
from PIL import Image as PILimage
from io import BytesIO
from pydantic import BaseModel
from typing import List, Annotated
from pathlib import Path
from glob import glob
from time import sleep
from datetime import date
import json
import pandas as pd

api = FastAPI()
#load the model
#api.state.model = load_model()

Path.mkdir(Path("images"), exist_ok=True)

@api.get("/")
def read_root():
    return {"postmethod_101": "simple app to test post methods api requests",
            "docs": "http://localhost:8000/docs"}

##### receive dataframe
class MultiDataframe(BaseModel):
    dfs: dict

@api.post("/dataframe_to_server")
def incoming_dataframe(data: MultiDataframe):
    df = pd.DataFrame(data.dfs["df1"])
    df.to_csv("example.csv", index=False)
    print(df)
    return "received df and saved as csv on server"

##### send dataframe
@api.get("/dataframe_to_client")
def outgoing_dataframe():
    df = pd.read_csv("example.csv")
    return df.to_dict()

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

#receive form data
class Stform(BaseModel):
    slider: int = 0
    check: bool = True
    description: str = "optional text"
    day: date # extra datatype

@api.post("/form_submission")
def form_submission(received: Stform):
    print(received)
    return "all check"
