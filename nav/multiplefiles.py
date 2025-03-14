import streamlit as st
import requests
from params import BASE_URL

##### [multiple file upload]
st.header("Multiple files with POST")
example = st.container(border=True)
images = example.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

example.write("You can upload multiple images and save them to the server")

if example.button("Save Images", key='multiple'):
    if images is not None:
        files = [("images", (image.name, image.getvalue())) for image in images]
        response = requests.post(BASE_URL+"/save_images/",
                                                files=files)
        st.write(response.json())
    else:
        st.write("No images uploaded")
