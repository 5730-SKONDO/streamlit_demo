import streamlit as st
import requests
import streamlit.components.v1 as components

st.title("スマホGPS＋現地時間＋気温デモ")

# JSでスマホのGPSと現地時間を取得し、session_stateに渡す
gps_js = """
<script>
navigator.geolocation.getCurrentPosition(function(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    const now = new Date();
    
    // hidden inputに値をセットしてPythonに渡す
    const coords_input = document.getElementById('coords_input');
    coords_input.value = `${lat},${lon}`;
    coords_input.dispatchEvent(new Event('change'));

    // 表示用
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
<input type="hidden" id="coords_input">
"""

components.html(gps_js, height=150)

# Python側でsession_stateから緯度経度を取得
if 'coords' not in st.session_state:
    st.session_state['coords'] = None

# hidden input連携用（ユーザーに見せない）
coords_input = st.text_input("", key="coords", value=st.session_state['coords'], label_visibility="collapsed")
if coords_input:
    st.session_state['coords'] = coords_input

# 緯度経度が入ったらAPI呼び出し
if st.session_state['coords']:
    lat, lon = map(float, st.session_state['coords'].split(","))
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    temp = data["current_weather"]["temperature"]
    
    st.metric("現在の気温", f"{temp} ℃")

