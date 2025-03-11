import streamlit as st
import requests

tab1, tab2, tab3 = st.tabs(["send file with POST", "send file with POST and GET", "Multiple files with POST"])


##### [EASY] send and retrieve info in a single POST request
with tab1:
    st.markdown(""" Sending image and processing happens on the same request,
                this is the simplest way, but not the best. \n
                Because the user will have to wait for the processing to finish,
                and the server will be busy processing the image. \n
                The best way is to send the image in a POST request,
                and the server will process the image and return a link. \n
                The user can do other things while the server is processing the image
                and the server can process other requests.
                Refer to the next tab for the best way""".replace("\t", ""))

    image_name_simple = st.text_input("Enter image name for simple request")
    with st.expander("POST upload and receive"):
        col1, col2 = st.columns(2, gap="large")
        st.subheader("SEND IMAGE AND RECEIVE A PREDECTION IN THE SAME REQUEST")
        with col1:
            image_simple = st.file_uploader("select Image for request", type=["jpg", "png", "jpeg"])
        with col2:
            if st.button("Send Image and predict"):
                if image_simple is not None:
                    files = {"image": (image_simple.name, image_simple.getvalue())}
                    url_post = "http://localhost:8000/simple/"
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
            image = st.file_uploader("select Image", type=["jpg", "png", "jpeg"])

            st.write("You can upload an image and save it to the server")

        with col2:
            if st.button("Save Image"):
                if image is not None:
                    files = {"image": (image.name, image.getvalue()),
                            "name": (None, image_name)}
                    url_post = "http://localhost:8000/save_image/"
                    response = requests.post(url_post, files=files)
                    st.write(response.json())
                else:
                    st.write("No image uploaded")

    with st.expander("GET download"):
        st.subheader("DOWNLOAD IMAGE FROM SERVER")
        if st.button("Get Image"):
            url_get = "http://localhost:8000/get_image/"
            getimage = requests.get(url_get, params={"name": image_name})
            col1, col2 = st.columns(2, gap="large")
            with col1:
                if getimage.status_code == 202:
                    st.write("Processing")
                if getimage.status_code == 200:
                    st.write(dict(getimage.headers))
            with col2:
                if getimage.status_code == 200:
                    st.image(getimage.content)

#####
with tab3:
    images = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    st.write("You can upload multiple images and save them to the server")

    if st.button("Save Images"):
        if images is not None:
            files = [("images", (image.name, image.getvalue())) for image in images]
            response = requests.post("http://localhost:8000/save_images/",
                                                    files=files)
            st.write(response.json())
        else:
            st.write("No images uploaded")
