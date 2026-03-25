import streamlit as st
import requests
import streamlit.components.v1 as components

st.title("スマホGPS＋現地時間＋気温デモ（完全版）")

# JSでGPSと現地時間取得 → Pythonに返す
gps_js = """
<script>
navigator.geolocation.getCurrentPosition(function(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    const now = new Date();
    // Pythonに返す
    const result = {lat: lat, lon: lon, time: now.toLocaleString()};
    window.parent.postMessage(result, "*");
    // 画面にも表示
    document.getElementById('display').innerHTML = `
        <p style="color:white; font-size:16px; line-height:1.5;">
            緯度: ${lat} <br>
            経度: ${lon} <br>
            現地時間: ${now.toLocaleString()}
        </p>
    `;
});
</script>
<div id="display"></div>
"""

# Componentsで戻り値を受け取る
gps_data = components.html(gps_js, height=150, scrolling=False)

# Python側で取得できたらAPI呼び出し
if gps_data:
    lat = gps_data.get("lat")
    lon = gps_data.get("lon")
    now = gps_data.get("time")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    temp = data["current_weather"]["temperature"]
    
    st.metric("現在の気温", f"{temp} ℃")
    st.write(f"取得時刻（現地時間）: {now}")
