import streamlit as st
import requests
from params import BASE_URL

##### [form example]
st.header("Sending a Form")

with st.form(key="form data",
                clear_on_submit=False):
    st.write("Sample form with POST method")
    col1, col2 = st.columns((1,3))
    with col1: checkbox_val = st.checkbox("Form checkbox")
    with col2: slider_val = st.slider("Form slider")
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
