import streamlit as st
import requests
import pandas as pd
from params import BASE_URL


st.header("Send Dataframe")

intro = st.container(border=True)
intro.write("""Example dataframe for sending to the server""".replace("\t", ""))

df1 = pd.DataFrame({
    "column1": ["value1","value2"],
    "column2": ["first1","second2"],
    "column3": [2,3]
})
intro.write(df1)

##### send dataframe to server
example = st.container(border=True)
example.subheader("upload dataframe to the server")


if example.button("Send dataframe", key="send-df"):
    dataframes = {"df1" : df1.to_dict(),
                  "df2" : {}}
    url_post = BASE_URL+"/dataframe_to_server/"
    response = requests.post(url_post, json={"dfs" : dataframes})
    example.success(response.text)

##### send dataframe to server with data validated
example = st.container(border=True)
example.subheader("upload dataframe to the server")


if example.button("Send dataframe", key="send-df"):
    dataframes = {"df1" : df1.to_dict(),
                  "df2" : {}}
    url_post = BASE_URL+"/dataframe_to_server/"
    response = requests.post(url_post, json={"dfs" : dataframes})
    example.success(response.text)

##### download dataframe to client
example2 = st.container(border=True)
example2.subheader("get dataframe from server")


if example2.button("get dataframe", key="get-df"):
    url_get = BASE_URL+"/dataframe_to_client/"
    response = requests.get(url_get)
    df = pd.DataFrame(response.json())
    example.success("received df")
    example2.write(df)
