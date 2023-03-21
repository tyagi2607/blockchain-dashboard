import pymongo
import requests

client = pymongo.MongoClient("mongodb+srv://apurvtyagi26:Jonty2020@cluster-blockchain-data.a0jvoed.mongodb.net/?retryWrites=true&w=majority")

db = client["bitcoin_database"]
collection = db["bitcoin_prices"]

response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
data = response.json()

collection.insert_one(data)