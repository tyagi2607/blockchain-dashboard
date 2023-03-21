import streamlit as st
import pandas as pd
import pymongo

client = pymongo.MongoClient("mongodb+srv://apurvtyagi26:Jonty2020@cluster-blockchain-data.a0jvoed.mongodb.net/?retryWrites=true&w=majority")
db = client["bitcoin_database"]
collection = db["bitcoin_prices"]

data = []
for document in collection.find():
    data.append(document["bpi"]["USD"]["rate_float"])

df = pd.DataFrame(data, columns=["Bitcoin Price (USD)"])
st.table(df)
st.line_chart(df)
