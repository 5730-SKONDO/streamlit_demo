import streamlit as st
import requests
from datetime import datetime, timezone

st.title("気温デモ（ステップ）")

# UTC時刻
now_utc = datetime.now(timezone.utc)

# ダミー座標（東京）
lat = 35.68
lon = 139.76

# API（UTC指定）
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=UTC"

response = requests.get(url)
data = response.json()

temp = data["current_weather"]["temperature"]
api_time = data["current_weather"]["time"]

# 表示
st.metric("気温", f"{temp} ℃")
st.write("取得時刻（UTC）:", now_utc.strftime("%Y-%m-%d %H:%M:%S"))
st.write("気温データ時刻（UTC）:", api_time)
