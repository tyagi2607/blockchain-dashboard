import streamlit as st
import pandas as pd
import pymongo

@st.experimental_singleton(suppress_st_warning=True)
def init_connection():
    return pymongo.MongoClient("mongodb+srv://st.secrets.db_username:st.secrets.db_password@st.secrets.cluster_name.a0jvoed.mongodb.net/?retryWrites=true&w=majority")

client = init_connection()
db = client["bitcoin_database"]
collection = db["bitcoin_prices"]

data = []
for document in collection.find():
    data.append(document["bpi"]["USD"]["rate_float"])

df = pd.DataFrame(data, columns=["Bitcoin Price (USD)"])
st.table(df)
st.line_chart(df)
