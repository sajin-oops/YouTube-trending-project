import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to PostgreSQL
@st.cache_resource
def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

conn = get_connection()

# Title
st.title("🎬 YouTube Trending Dashboard")
st.markdown("Top trending videos in India — powered by a real data warehouse!")

# Load fact table
df = pd.read_sql("SELECT * FROM staging_marts.fact_trending", conn)

# KPI metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Videos", len(df))
col2.metric("Total Views", f"{df['view_count'].sum():,}")
col3.metric("Total Likes", f"{df['like_count'].sum():,}")

st.divider()

# Top 10 videos by views
st.subheader("🏆 Top 10 Videos by Views")
top10 = df.nlargest(10, 'view_count')[['title', 'view_count']]
fig1 = px.bar(top10, x='view_count', y='title', orientation='h',
              color='view_count', color_continuous_scale='reds')
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# Top 10 channels by views
st.subheader("📺 Top 10 Channels by Views")
channels = pd.read_sql("""
    SELECT f.channel_id, c.channel_title,
           SUM(f.view_count) as total_views
    FROM staging_marts.fact_trending f
    JOIN staging_marts.dim_channel c ON f.channel_id = c.channel_id
    GROUP BY f.channel_id, c.channel_title
    ORDER BY total_views DESC
    LIMIT 10
""", conn)
fig2 = px.bar(channels, x='total_views', y='channel_title', orientation='h',
              color='total_views', color_continuous_scale='blues')
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Views vs Likes scatter
st.subheader("❤️ Views vs Likes")
fig3 = px.scatter(df, x='view_count', y='like_count',
                  hover_data=['title'], color='view_count',
                  color_continuous_scale='greens')
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Raw data table
st.subheader("📊 Raw Data")
st.dataframe(df[['title', 'channel_id', 'view_count', 
                  'like_count', 'comment_count']].sort_values(
                  'view_count', ascending=False))

