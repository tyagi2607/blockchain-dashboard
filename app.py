#======================================== IMPORT PACKAGES AND REASON FOR IMPORTS ====================================================================#
import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px

def show_overview(client, coin):
    # Show the content for the Overview page
    # Select database and collection
    db = client["bitcoin_database"]
    collection = db["bitcoin_market"]


    data = []
    for document in collection.find():
        data.append(document["price"])

    df = pd.DataFrame(data, columns=["Bitcoin Price (USD)"])

    st.title(coin)
    st.markdown(coin)

    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Price $",
        value=30,
        delta=30 - 10,
    )

    kpi2.metric(
        label="Market cap $",
        value=int(200),
        delta=-200 + 10 ,
    )

    kpi3.metric(
        label="Volumne ＄",
        value=f"$ {round(20,2)} ",
        delta=-round(30 / 1400) * 100,
    )

    st.markdown("Details")

    cht1, cht2 = st.columns(2)
    
    cht1.table(df.head(10))

    cht2.markdown("Line chart")
    cht2.line_chart(df, y="Bitcoin Price (USD)", use_container_width=False)
    
    
    # Display the coin overview
    st.subheader(coin)
    st.write("Current Price: $")
    st.write("Market Cap: $")
    st.write("Volume: $")
    # Add card visual, table, or any other desired components

def show_profile():
    # Show the content for the Profile page
    st.title("Profile")
    # Add card visual, table, or any other desired components

def show_charts():
    # Show the content for the Charts page
    st.title("Charts")
    # Add card visual, table, or any other desired components

def show_metrics():
    # Show the content for the Metrics page
    st.title("Metrics")
    # Add card visual, table, or any other desired components

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

    #def init_connection():
    #    return pymongo.MongoClient("mongodb+srv://st.secrets.db_username:st.secrets.db_password@st.secrets.cluster_name.a0jvoed.mongodb.net/st.secrets.db_name?retryWrites=true&w=majority")

    # client = init_connection()

    st.title("Coin metrics")
    st.markdown("The dashboard will visualize the coin metrics")
    st.markdown("Details")

    st.sidebar.title("more coins")
    st.sidebar.markdown("Welcome!!!")
    st.sidebar.checkbox("Show Analysis", True, key=2)

    # Create a sidebar for coin selection and page navigation
    coin = st.sidebar.selectbox("Select Coin", ["Bitcoin", "Ethereum", "Litecoin"])

    # Create radio buttons for selecting the page
    page = st.sidebar.radio("Page", ["Overview", "Profile", "Charts", "Metrics"])



    # Based on the selected page, show the corresponding content
    if page == "Overview":
        show_overview(client, coin)
    elif page == "Profile":
        show_profile()
    elif page == "Charts":
        show_charts()
    elif page == "Metrics":
        show_metrics()

if __name__ == "__main__":
    main()