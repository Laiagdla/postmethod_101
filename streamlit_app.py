import streamlit as st
from params import BASE_URL
import requests

dataframe = st.Page("nav/dataframe.py", title="Dataframes", icon=":material/database:")
form = st.Page("nav/form.py", title="Forms", icon=":material/list_alt:")
post = st.Page("nav/post.py", title="Files with POST", icon=":material/package_2:")
postget = st.Page("nav/postget.py", title="Files with POST and GET", icon=":material/deployed_code_update:")
multi = st.Page("nav/multiplefiles.py", title="Multiple files with POST", icon=":material/delivery_truck_bolt:")

st.set_page_config(layout="wide")
pg = st.navigation([dataframe, form, post, postget, multi])
pg.run()

################### [footer] ####################
st.divider()

@st.cache_data
def server_check():
    return requests.get(BASE_URL)
check = requests.get(BASE_URL)

footer = st.container(border=True)
col1, col2, col3 = footer.columns((1, 1, 3))
with col1: st.info("Api Status Check:", icon="🦝")
with col2: st.warning(check.status_code, icon="💌")
jsoncont = st.container(border=True)
with col3: st.container(border=True).json(check.json(), expanded=False)
