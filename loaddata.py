import streamlit as st
import pymongo
import requests


@st.cache_resource
def init_connection():
    return pymongo.MongoClient("mongodb+srv://st.secrets.db_username:st.secrets.db_password@st.secrets.cluster_name.a0jvoed.mongodb.net/?retryWrites=true&w=majority")

client = init_connection()

db = client["bitcoin_database"]
collection = db["bitcoin_prices"]

response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
data = response.json()

collection.insert_one(data)