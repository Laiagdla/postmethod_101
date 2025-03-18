import streamlit as st
import requests
import pandas as pd
from params import BASE_URL

##### example dataframes
st.header("Send Dataframe")
intro = st.container(border=True)
intro.write("""Example dataframe for sending to the server""".replace("\t", ""))

col1, col2 = intro.columns(2, gap="medium")
with col1:
    st.write("1️⃣ Example dataframe 1:")
    df1 = pd.DataFrame({
        "column1": ["value1","value2"],
        "column2": ["first1","second2"],
        "column3": [2,3]
    })
    st.write(df1)
with col2:
    st.write("2️⃣ Example dataframe 2:")
    df2 = pd.DataFrame({
        "column7": ["1234","2345"],
        "column8": ["abcd","efgh"],
        "column9": [2222,3333]
    })
    st.write(df2)



##### send dataframe to server
col1, col2, col3 = st.columns(3)
with col1:
    example = st.container(border=True)
    example.subheader("Upload dataframe to the server")

    if example.button("Send dataframe", key="send-df"):
        url_post = BASE_URL+"/dataframe_to_server/"
        response = requests.post(url_post, json={"df" : df1.to_dict()} )
        example.success(response.text)


##### send multiple dataframes to server
with col2:
    example = st.container(border=True)
    example.subheader("Upload multiple dataframes")

    if example.button("Send dataframes", key="send-multi-df"):
        dataframes = {"df1" : df1.to_dict(),
                      "df2" : df2.to_dict()}
        url_post = BASE_URL+"/mlt_dataframes_to_server/"
        response = requests.post(url_post, json={"dfs" : dataframes})
        example.success(response.text)


##### send dataframe to server with data validated
with col3:
    example = st.container(border=True)
    example.subheader("Upload with validation")

    if example.button("Send & validate", key="send-df-val"):
        url_post = BASE_URL+"/dataframe_to_server_validated/"
        response = requests.post(url_post, json=df1.to_dict(orient="list"))
        example.success(response.text)


##### download dataframe to client
example2 = st.container(border=True)
example2.subheader("Get dataframe from server")

if example2.button("get dataframe", key="get-df"):
    url_get = BASE_URL+"/dataframe_to_client/"
    response = requests.get(url_get)
    df = pd.DataFrame(response.json())
    example.success("received df")
    example2.write(df)
