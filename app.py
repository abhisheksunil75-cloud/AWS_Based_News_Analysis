#Import necessary libraries for data manipulation, web dashboard, and database connection
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import os

#Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

db_password = os.getenv("DB_PASSWORDSTREAM")

# Configure the main settings for the Streamlit web page
st.set_page_config(page_title="News Dashboard", layout="wide")

#Create the SQLAlchemy engine to connect to the database
engine=create_engine(f"postgresql+pg8000://postgres:{db_password}@news-db.c70wyi68w8wm.ap-south-1.rds.amazonaws.com:5432/postgres") #mysql+pymysql/(postgressql)://username:password@host/database

# Create a refresh button that forces the Streamlit app to rerun and fetch new data
if st.button("🔄 Refresh"):
    st.rerun()
    
# Query the database to get all news articles, ordered by newest first, and load into a DataFrame
df = pd.read_sql('SELECT * FROM news ORDER BY id desc', engine)

# Displays title of the dashboard
st.title('📊 News Sentiment Dashboard')

# Calculate metrics for the summary cards based on the numeric sentiment score
total = len(df)
positive = (df["sentiment"] > 0).sum()
negative = (df["sentiment"] < 0).sum()
neutral = total - positive - negative

# Create 4 columns across the screen and display the calculated metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total News", total)
c2.metric("Positive", positive)
c3.metric("Negative", negative)
c4.metric("Neutral", neutral)

#Function to convert numeric scores into text labels
def get_label(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    return "Neutral"
    
#To create a new 'sentiment_label' column in the DataFrame
df['sentiment_label'] = df['sentiment'].apply(get_label)

#To apply CSS background colors based on the text label
def color_sentiment(val):
    if val == 'Positive':
        return 'background-color: lightgreen; color: black;'
    elif val == 'Negative':
        return 'background-color: lightcoral; color: black;'
    elif val == 'Neutral':
        return 'background-color: lightgray; color: black;'
    return ''

#Apply the color styling function  to sentiment_label colomn
styled_df = df.style.map(color_sentiment, subset=['sentiment_label'])

# Display a subheader and render the interactive, color-coded DataFrame
st.write("### Live Articles")
st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Display a subheader and the statistical breakdown of the sentiment scores
st.write("### Sentiment Summary")
st.write(df["sentiment"].describe())

# To visualize line chart
st.line_chart(df["sentiment"])
