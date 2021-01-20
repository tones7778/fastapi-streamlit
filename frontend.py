import streamlit as st
import requests

st.write("Get Cisco data from switch.")

mycommand = st.selectbox("Command:", ["getversion", "getinterfaces"])

url = ("http://manager1:8001/cisco/{}".format(mycommand))
st.write(url)
response = requests.get(url)
results = response.json()
st.write(results)
