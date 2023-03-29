import streamlit as st
import pandas as pd
import pymongo

def main():
    print(st.secrets.db_username)

    # Connect to MongoDB
    @st.cache_resource
    def init_connection():
        # Construct connection string
        connection_string = "mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority".format(
            username=st.secrets.db_username,
            password=st.secrets.db_password,
            cluster=st.secrets.cluster_name
        )
        return pymongo.MongoClient(connection_string)

    client = init_connection()
    # Select database and collection
    db = client["bitcoin_database"]
    collection = db["bitcoin_market"]


    #def init_connection():
    #    return pymongo.MongoClient("mongodb+srv://st.secrets.db_username:st.secrets.db_password@st.secrets.cluster_name.a0jvoed.mongodb.net/st.secrets.db_name?retryWrites=true&w=majority")

    # client = init_connection()


    data = []
    for document in collection.find():
        data.append(document["bpi"]["USD"]["rate_float"])

    df = pd.DataFrame(data, columns=["Bitcoin Price (USD)"])
    st.table(df)
    st.line_chart(df)

if __name__ == "__main__":
    main()