import os
import gdown
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Spotify Audio Feature Dashboard",
    page_icon="🎧",
    layout="wide"
)

# -------------------------------------------------
# Title
# -------------------------------------------------

st.title("🎧 Spotify Audio Feature Analysis Dashboard")
st.markdown("Interactive exploration of Spotify audio features and song popularity.")

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

@st.cache_data
def load_data():

    url = "https://github.com/yash-khandelwal-dev/spotify-audio-analysis/releases/download/Dataset/spotify.csv"

    df = pd.read_csv(url)

    df.columns = df.columns.str.strip().str.lower()

    return df


df = load_data()

df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")
df["tempo"] = pd.to_numeric(df["tempo"], errors="coerce")

# -------------------------------------------------
# Dataset Metrics
# -------------------------------------------------

st.subheader("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Songs", len(df))
col2.metric("Average Popularity", round(df['popularity'].mean(), 2))
col3.metric("Average Tempo (BPM)", round(df['tempo'].mean(), 2))

st.markdown("---")

# -------------------------------------------------
# Sidebar Controls
# -------------------------------------------------

st.sidebar.title("⚙️ Visualization Controls")

features = [
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo"
]

x_feature = st.sidebar.selectbox("Select X-axis Feature", features)

y_feature = st.sidebar.selectbox(
    "Select Y-axis Feature",
    ["popularity"] + features
)

# -------------------------------------------------
# Scatter Plot
# -------------------------------------------------

st.subheader("📈 Feature Relationship Explorer")

fig1, ax1 = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=df.sample(10000),
    x=x_feature,
    y=y_feature,
    alpha=0.4,
    ax=ax1
)

ax1.set_title(f"{x_feature.capitalize()} vs {y_feature.capitalize()}")

st.pyplot(fig1)

st.markdown("---")

# -------------------------------------------------
# Feature Distribution
# -------------------------------------------------

st.subheader("📊 Feature Distribution")

selected_feature = st.selectbox(
    "Choose Feature",
    features
)

fig2, ax2 = plt.subplots(figsize=(8,5))

sns.histplot(df[selected_feature], kde=True, ax=ax2)

ax2.set_title(f"Distribution of {selected_feature.capitalize()}")

st.pyplot(fig2)

st.markdown("---")

# -------------------------------------------------
# Correlation Heatmap
# -------------------------------------------------

st.subheader("Feature Correlation Heatmap")

fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(df.corr(numeric_only=True), cmap="coolwarm", ax=ax)

st.pyplot(fig)

st.markdown("---")

st.subheader("Popularity Distribution")

fig, ax = plt.subplots()
sns.histplot(df["popularity"], bins=30, kde=True, ax=ax)

st.pyplot(fig)

# -------------------------------------------------
# Dataset Preview
# -------------------------------------------------

st.subheader("📋 Dataset Preview")

st.dataframe(df.head(100))

st.subheader("Key Insights")

st.markdown("""
• Songs with higher **danceability** tend to have slightly higher popularity.

• **Energy and loudness** show strong correlation.

• Most songs cluster around **tempo 100–150 BPM**.

• Popular songs generally have **moderate danceability and energy**.
""")