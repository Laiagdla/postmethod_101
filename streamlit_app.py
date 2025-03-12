import streamlit as st
import requests
from time import sleep
import json

tab1, tab2, tab3, tab4 = st.tabs(["send file with POST", "send file with POST and GET", "Multiple files with POST", "sending a Form"])
BASE_URL="http://localhost:8000"

##### [EASY] send and retrieve info in a single POST request
with tab1:
    st.markdown(""" Sending an image and processing happens on the same request,
                this is the simplest way, but not the best. \n
                Because the user will have to wait for the processing to finish,
                and the server will be busy processing the image. \n
                The best way is to send the image in a POST request,
                and the server will return a link and process the image in the background. \n
                The user can do other things while the server is processing the image
                and the server can process other requests.
                Refer to the next tab for the best way""".replace("\t", ""))

    image_name_simple = st.text_input("Enter image name for simple request", key="simple-image-name")
    with st.expander("POST upload and receive"):
        col1, col2 = st.columns(2, gap="large")
        st.subheader("SEND IMAGE AND RECEIVE A PREDECTION IN THE SAME REQUEST")
        with col1:
            image_simple = st.file_uploader("select Image for request", type=["jpg", "png", "jpeg"], key="simple uploader")
        with col2:
            if st.button("Send Image and predict", key="simple-post"):
                if image_simple is not None:
                    files = {"image": (image_simple.name, image_simple.getvalue())}
                    url_post = BASE_URL+"/simple/"
                    response = requests.post(url_post, files=files)
                    st.write(response.json())
                else:
                    st.write("No image uploaded")

##### [ADVANCED] send and retrieve indo with POST and GET
with tab2:
    st.write("""sending image and processing happens on different requests, \n
                the file is sent in a POST request, that will return a link, \n
                then the user can get the image using the link, \n""")

    image_name = st.text_input("Enter image name for POST and GET request")
    with st.expander("POST upload"):
        st.subheader("UPLOAD IMAGE TO SERVER")

        col1, col2 = st.columns(2, gap="large")
        with col1:
            image = st.file_uploader("select Image", type=["jpg", "png", "jpeg"], key="post-uploader")

            st.write("You can upload an image and save it to the server")

        with col2:
            if st.button("Save Image", key="post"):
                if image is not None:
                    files = {"image": (image.name, image.getvalue()),
                            "name": (None, image_name)}
                    url_post = BASE_URL+"/save_image/"
                    response = requests.post(url_post, files=files)
                    st.write(response.json())
                else:
                    st.write("No image uploaded")

    with st.expander("GET download"):
        st.subheader("DOWNLOAD IMAGE FROM SERVER")
        if st.button("Get Image", key='get'):
            url_get = BASE_URL+"/get_image/"
            getimage = requests.get(url_get, params={"name": image_name})
            col1, col2 = st.columns(2, gap="large")
            with col1:
                while getimage.status_code != 200:
                    with st.spinner("Processing"):
                        getimage = requests.get(url_get, params={"name": image_name})
                        sleep(1)
                if getimage.status_code == 200:
                    st.write(dict(getimage.headers))
            with col2:
                if getimage.status_code == 200:
                    st.image(getimage.content)

##### [multiple file upload]
with tab3:
    images = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    st.write("You can upload multiple images and save them to the server")

    if st.button("Save Images", key='multiple'):
        if images is not None:
            files = [("images", (image.name, image.getvalue())) for image in images]
            response = requests.post(BASE_URL+"/save_images/",
                                                    files=files)
            st.write(response.json())
        else:
            st.write("No images uploaded")

##### [form example]
with tab4:
    with st.form(key="form data",
                 clear_on_submit=False):
        st.write("sample form for POST method")
        slider_val = st.slider("Form slider")
        checkbox_val = st.checkbox("Form checkbox")
        description = st.text_input("description", key="description")
        date = st.date_input("date")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

        if submitted:
            payload = {
                "slider" : slider_val,
                "check" : checkbox_val,
                "description" : description,
                "day" : str(date)
            }
            form_url = BASE_URL+"/form_submission/"
            response = requests.post(form_url, json=payload)
            st.write(response.json())
            st.success(f"'slider': {slider_val}  \n 'checkbox': {checkbox_val}  \n 'description': {description}  \n'date': {date}")
