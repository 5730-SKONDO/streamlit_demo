import streamlit as st
from streamlit_javascript import st_javascript
import requests

st.title("スマホGPS＋現地時間＋気温デモ（完全版）")

result = st_javascript("""
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            resolve({error: "Geolocation APIが利用できません"});
        } else {
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const now = new Date();
                resolve({
                    lat: lat,
                    lon: lon,
                    time: now.toLocaleString()
                });
            }, function(err){
                resolve({error: err.message + " (code: " + err.code + ")"});
            });
        }
    });
""")

if result:
    if "error" in result:
        st.error(f"位置情報取得エラー: {result['error']}")
    else:
        lat = result["lat"]
        lon = result["lon"]
        now = result["time"]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        temp = data["current_weather"]["temperature"]
        st.metric("現在の気温", f"{temp} ℃")
        st.write(f"取得時刻（現地時間）: {now}")
else:
    st.warning("位置情報が取得できませんでした。")
