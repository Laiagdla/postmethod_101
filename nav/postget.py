import streamlit as st
import requests
from time import sleep
from params import BASE_URL
##### [ADVANCED] send and retrieve indo with POST and GET

st.header("Send file with POST and GET")
intro = st.container(border=True)
intro.success("The advanced way")
intro.write("""Sending image and processing happens on different requests,
            the file is sent in a POST request, that will return a link,
            then the user can get the image using the link""")
image_name = intro.text_input("Enter image name for POST and GET request")

with st.expander("POST upload"):
    st.subheader("UPLOAD IMAGE TO SERVER")

    col1, col2 = st.columns(2, gap="medium", border=True)
    with col1:
        image = st.file_uploader("select Image", type=["jpg", "png", "jpeg"], key="post-uploader")

        st.write("You can upload an image and save it to the server")

    with col2:
        if st.button("Save Image", key="post"):
            if image is not None:
                files = {"image": (image.name, image.getvalue()),
                        "name": image_name}
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
        col1, col2 = st.columns(2, gap="medium", border=True)
        with col1:
            with st.spinner("Processing"):
                while getimage.status_code != 200:
                    getimage = requests.get(url_get, params={"name": image_name})
                    sleep(1)
            if getimage.status_code == 200:
                st.write(dict(getimage.headers))
        with col2:
            if getimage.status_code == 200:
                st.image(getimage.content)
