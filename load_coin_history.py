import requests
import pandas as pd
import pymongo
from pymongo import MongoClient
import streamlit as st


def get_coin_daily_history(coinid, days):
    # define CoinGecko API endpoint and parameters
    url = "https://api.coingecko.com/api/v3/coins/"+coinid+"/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    # fetch data from CoinGecko API and store in Pandas DataFrame
    response = requests.get(url, params=params)
    data = response.json()
    prices_df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    market_caps_df = pd.DataFrame(data["market_caps"], columns=["timestamp", "market_cap"])
    total_volumes_df = pd.DataFrame(data["total_volumes"], columns=["timestamp", "total_volume"])

    # merge the dataframes into one dataframe using timestamp as the key
    merged_df = pd.merge(prices_df, market_caps_df, on="timestamp")
    merged_df = pd.merge(merged_df, total_volumes_df, on="timestamp")
    merged_df = merged_df[:-1]
    return merged_df

def coin_marketdata_to_mongodb(coinid, days):
    data = get_coin_daily_history(coinid, days)
    #send_coin_daily_history_to_mongodb(data,coinid)
    records = data.to_dict(orient="records")
    # connect to MongoDB database and insert data
    connection_string = "mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority".format(
    username=st.secrets.db_username,
    password=st.secrets.db_password,
    cluster=st.secrets.cluster_name
    )
    client = pymongo.MongoClient(connection_string)
    db = client[coinid+"_database"]
    collection_name = coinid+"_market1"
    if collection_name in db.list_collection_names():
        # If the collection exists, drop it
        db[collection_name].drop()
    collection = db[coinid+"_market1"]
    collection.insert_many(records)

coin_marketdata_to_mongodb('bitcoin', 2)