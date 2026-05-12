import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="News Dashboard", layout="wide")

engine=create_engine("postgresql+pg8000://postgres:abhisheksunil@news-db.c70wyi68w8wm.ap-south-1.rds.amazonaws.com:5432/postgres") #mysql+pymysql/(postgressql)://username:password@host/database

if st.button("🔄 Refresh"):
    st.rerun()

df = pd.read_sql('SELECT * FROM news ORDER BY id desc',engine)

st.title('📊 News Sentiment Dashboard')

# Metrics
total = len(df)
positive = (df["sentiment"] > 0).sum()
negative = (df["sentiment"] < 0).sum()
neutral = total - positive - negative

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total News", total)
c2.metric("Positive", positive)
c3.metric("Negative", negative)
c4.metric("Neutral", neutral)

st.dataframe(df)

st.write("### Sentiment Summary")

st.write(df["sentiment"].describe())

st.line_chart(df["sentiment"])
