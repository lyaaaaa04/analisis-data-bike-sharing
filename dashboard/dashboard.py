import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="whitegrid")

# LOAD DATA
hour_df = pd.read_csv("hour_clean.csv")
hour_df["date"] = pd.to_datetime(hour_df["date"])

# SIDEBAR
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2972/2972185.png",
    width=120
)
st.sidebar.title("Bike Sharing 🚲")
st.sidebar.caption("Dashboard Analisis Peminjaman Sepeda")

start_date, end_date = st.sidebar.date_input(
    "📆 Rentang Waktu",
    min_value=hour_df["date"].min(),
    max_value=hour_df["date"].max(),
    value=[hour_df["date"].min(), hour_df["date"].max()]
)

filtered_hour = hour_df[
    (hour_df["date"] >= str(start_date)) &
    (hour_df["date"] <= str(end_date))
]

# HEADER
st.title("🚲 Bike Sharing Dashboard")
st.caption("Visualisasi interaktif untuk memahami pola peminjaman sepeda")

# METRICS
col1, col2, col3 = st.columns(3)

col1.metric("Total Peminjaman", f"{filtered_hour['count'].sum()}")
col2.metric("Registered User", f"{filtered_hour['registered'].sum()}")
col3.metric("Casual User", f"{filtered_hour['casual'].sum()}")

# 1. PENGGUNAAN PER JAM
st.subheader("⏰ Peminjaman Berdasarkan Jam")

hourly_usage = filtered_hour.groupby("hour")["count"].sum().reset_index()

fig, ax = plt.subplots(figsize=(12,5))
sns.barplot(data=hourly_usage, x="hour", y="count", color="#90CAF9", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Total Peminjaman")
st.pyplot(fig)

# 2. PENGGUNAAN PER HARI
st.subheader("📅 Peminjaman Berdasarkan Hari")

weekday_usage = (
    filtered_hour
    .groupby("weekday")["count"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12,5))
sns.barplot(data=weekday_usage, x="weekday", y="count", color="#90CAF9", ax=ax)
ax.set_xlabel("Hari")
ax.set_ylabel("Total Peminjaman")
st.pyplot(fig)

# 3. MUSIM
st.subheader("🌤️ Peminjaman Berdasarkan Musim")

season_usage = (
    filtered_hour
    .groupby("season")["count"]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(
    data=season_usage,
    x="season",
    y="count",
    color="#90CAF9",
    ax=ax
)
ax.set_xlabel("Musim")
ax.set_ylabel("Total Peminjaman")
ax.ticklabel_format(style='plain', axis='y')
st.pyplot(fig)

# 4. BULANAN
st.subheader("📈 Tren Peminjaman Bulanan")

monthly_usage = filtered_hour.groupby("month")["count"].sum().reset_index()

fig, ax = plt.subplots(figsize=(12,5))
sns.lineplot(data=monthly_usage, x="month", y="count", marker="o", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Peminjaman")
st.pyplot(fig)

# 5. JENIS PENGGUNA
st.subheader("👥 Registered vs Casual User")

user_type = filtered_hour[["registered", "casual"]].sum()

fig, ax = plt.subplots()
ax.pie(
    user_type,
    labels=user_type.index,
    autopct="%1.1f%%",
    colors=["#90CAF9", "#D3D3D3"],
    startangle=90
)
ax.axis("equal")
st.pyplot(fig)

# 6. PERIODE TERBAIK
st.subheader("💰 Top 5 Periode Paling Menguntungkan")

monthly_yearly = (
    filtered_hour
    .groupby(["year", "month"])["count"]
    .sum()
    .reset_index()
)

best_period = monthly_yearly.sort_values("count", ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(
    data=best_period,
    y="month",
    x="count",
    hue="year",
    palette=["#90CAF9"],
    ax=ax
)
ax.set_xlabel("Total Peminjaman")
ax.set_ylabel("Bulan")
st.pyplot(fig)
