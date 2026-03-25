import streamlit as st
import streamlit.components.v1 as components

st.title("スマホGPSデモ（ステップ）")

gps_js = """
<script>
navigator.geolocation.getCurrentPosition(function(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    const now = new Date();
    document.body.innerHTML = `<p id='gps'>緯度:${lat}, 経度:${lon}, 現地時間:${now.toLocaleString()}</p>`;
});
</script>
"""

components.html(gps_js, height=150)

