#======================================== IMPORT PACKAGES AND REASON FOR IMPORTS ====================================================================#
import streamlit as st
import pandas as pd
import pymongo

def main():
    # STREAMLIT: Page configuration
    st.set_page_config(
    page_title="morecoins",
    page_icon="✅",
    layout="wide",
    )

    # FUNCTION: Connect to MongoDB
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
        data.append(document["price"])

    df = pd.DataFrame(data, columns=["Bitcoin Price (USD)"])

    st.sidebar.title("more coins")
    st.sidebar.markdown("Welcome!!!")
    st.sidebar.checkbox("Show Analysis", True, key=1)
    select = st.sidebar.selectbox('Select a State',["Bitcoin"])
    st.title("Coin metrics")
    st.markdown("The dashboard will visualize the coin metrics")
    st.markdown("Details")
    st.table(df.head())
    st.line_chart(df)

if __name__ == "__main__":
    main()