import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import random

st.set_page_config(page_title="Mission Green 🌍", layout="wide")
st.title("🌍 Mission Green – World Map Simulation")

# -----------------------------
# Session state
# -----------------------------
if 'score' not in st.session_state:
    st.session_state.score = 0

if 'completed_cities' not in st.session_state:
    st.session_state.completed_cities = []

# -----------------------------
# ตัวอย่างข้อมูลเมืองจริง
# -----------------------------
cities = pd.DataFrame({
    'city': ['Bangkok','New York','London','Tokyo','Sydney','Paris','Delhi','Cairo','Rio de Janeiro','Cape Town'],
    'lat': [13.7563,40.7128,51.5074,35.6895,-33.8688,48.8566,28.6139,30.0444,-22.9068,-33.9249],
    'lon': [100.5018,-74.0060,-0.1278,139.6917,151.2093,2.3522,77.2090,31.2357,-43.1729,18.4241],
    'co2_emission': [10.5,15.0,6.0,9.0,4.5,5.5,8.0,3.0,2.5,1.5], # metric tons per capita (ตัวอย่าง)
    'population': [8.3,8.4,9.0,14.0,5.3,2.1,21.0,9.5,6.7,4.0]
})

# -----------------------------
# เลือกเมืองทำภารกิจ
# -----------------------------
st.sidebar.header("📍 เลือกเมือง")
available_cities = cities[~cities['city'].isin(st.session_state.completed_cities)]
selected_city = st.sidebar.selectbox("เมืองที่ต้องการช่วย", available_cities['city'])

city_data = cities[cities['city']==selected_city].iloc[0]

# -----------------------------
# ภารกิจสิ่งแวดล้อม
# -----------------------------
st.subheader(f"🌱 ภารกิจใน {selected_city}")
st.write(f"- ประชากร: {city_data['population']} ล้านคน")
st.write(f"- ปริมาณ CO₂ ต่อคน: {city_data['co2_emission']} ตัน/ปี")

tree_action = st.slider("ปลูกต้นไม้ (จำนวนต้นไม้)", 1, 1000, 100)
co2_action = st.slider("ลด CO₂ (หน่วยตัน)", 1, 50, 10)

if st.button("ทำภารกิจ"):
    # คะแนนจากกิจกรรม: แบบจำลองง่าย
    score_gain = int(tree_action*0.02 + co2_action*random.uniform(1,3))
    st.session_state.score += score_gain
    st.session_state.completed_cities.append(selected_city)
    st.success(f"คุณทำภารกิจใน {selected_city} สำเร็จ! ได้คะแนน {score_gain}")
    st.experimental_rerun()

# -----------------------------
# แผนที่โลก
# -----------------------------
# สร้างสีตามคะแนนสะสม
cities['color'] = cities['city'].apply(lambda x: [0,200,0] if x in st.session_state.completed_cities else [255,100,100])

map_layer = pdk.Layer(
    'ScatterplotLayer',
    cities,
    get_position=['lon','lat'],
    get_fill_color='color',
    get_radius=100000,
    pickable=True
)

view_state = pdk.ViewState(latitude=20, longitude=0, zoom=1, pitch=30)

st.pydeck_chart(pdk.Deck(layers=[map_layer], initial_view_state=view_state))

# -----------------------------
# คะแนนรวม
# -----------------------------
st.sidebar.header("🏆 คะแนนสะสม")
st.sidebar.metric("คะแนนรวม", st.session_state.score)
