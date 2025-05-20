import pandas as pd
import plotly.express as px
import folium

# # 데이터 불러오기
# df3 = pd.read_csv("yc_busevent.csv")
# df3.head()

# df3['bus stop_name'].value_counts()

# df3 = df3.drop_duplicates(subset='bus stop_name')


# # 중심 위치 지정 (영천시 중심 좌표, 대략)
# map_center = [36.0, 128.9]

# # 지도 생성
# m = folium.Map(location=map_center, zoom_start=13)

# # 정류장마다 마커 추가
# for i, row in df3.iterrows():
#     folium.Marker(
#         location=[row['bus stop_gps y'], row['bus stop_gps x']],
#         popup=row['bus stop_name'],
#         icon=folium.Icon(color='green', icon='bus', prefix='fa')
#     ).add_to(m)

# m

#####################################
####################################3


# 데이터 불러오기
df4 = pd.read_csv("영천시_의료기관.csv", encoding='cp949')
df4.head()


# 중심 위치 지정 (영천시 중심 좌표, 대략)
map_center = [35.9736, 128.9408]

# 지도 생성
m = folium.Map(location=map_center, zoom_start=13)

for i, row in df4.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['의료기관명'],
        icon=folium.Icon(color='blue', icon='hospital', prefix='fa')
    ).add_to(m)

m

#####################################
####################################3

df5 = pd.read_csv("경상북도 영천시_도시공원.csv", encoding='cp949')
df5.head()

# 중심 위치 지정 (영천시 중심 좌표, 대략)
map_center = [35.9736, 128.9408]

# 지도 생성
m = folium.Map(location=map_center, zoom_start=13)

for i, row in df5.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['명칭'],
        icon=folium.Icon(color='blue', icon='park', prefix='fa')
    ).add_to(m)

m



# from geopy.geocoders import Nominatim
# import pandas as pd
# import time

# # 지오코더 초기화
# geolocator = Nominatim(user_agent="yc-map")

# # 주소 → 위도·경도 함수
# def geocode(address):
#     try:
#         location = geolocator.geocode("영천시 " + address)
#         if location:
#             return pd.Series([location.latitude, location.longitude])
#     except:
#         return pd.Series([None, None])

# # 예제: 지번 주소만 있는 df
# df5[['위도', '경도']] = df5['지번'].apply(geocode)

# # 잠깐 쉬어가면서 (API 과부하 방지)
# time.sleep(1)


# 최종 지도 시각화 코드

import pandas as pd
import folium
from folium.plugins import GroupedLayerControl

# 데이터 불러오기
df4 = pd.read_csv("영천시_의료기관.csv", encoding='cp949')
df5 = pd.read_csv("경상북도 영천시_도시공원.csv", encoding='cp949')

# 중심 좌표
map_center = [35.9736, 128.9408]
m = folium.Map(location=map_center, zoom_start=13)

# ✅ 의료기관 Layer (같은 그룹으로 묶기)
hospital_layer = folium.FeatureGroup(name='의료기관')
for _, row in df4.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['의료기관명'],
        icon=folium.Icon(color='blue', icon='hospital', prefix='fa')
    ).add_to(hospital_layer)

# ✅ 공원 Layer
park_layer = folium.FeatureGroup(name='공원')
for _, row in df5.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['명칭'],
        icon=folium.Icon(color='green', icon='tree', prefix='fa')
    ).add_to(park_layer)

# ✅ 지도 타일 추가
folium.TileLayer('OpenStreetMap', name='지도').add_to(m)

# ✅ Layer 추가
hospital_layer.add_to(m)
park_layer.add_to(m)

# ✅ Grouped Layer Control: 두 레이어를 같은 그룹에 넣으면 라디오 버튼처럼 작동
GroupedLayerControl(
    groups={
        "시설 종류": [hospital_layer, park_layer]  # 그룹 이름: 포함 레이어 목록
    },
    collapsed=False
).add_to(m)

# 출력
m
