import streamlit as st
import requests
from params import BASE_URL


##### [EASY] send and retrieve info in a single POST request
st.header("Send file with POST")

intro = st.container(border=True)
intro.warning("The easy way")
intro.write(""" Sending an image and processing happens on the same request,
            this is the simplest way, but not the best.
            Because the user will have to wait for the processing to finish,
            and the server will be busy processing the image.
            The best way is to send the image in a POST request,
            and the server will return a link and process the image in the background.
            The user can do other things while the server is processing the image
            and the server can process other requests.
            Refer to sending files with POST and GET for the best way""".replace("\t", ""))



example = st.container(border=True)
example.subheader("Send image and receive a text reply in same request")
image_name_simple = example.text_input("Enter image name.", key="simpleimageupload")

col1, col2 = example.columns(2, gap="medium", border=True)
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
