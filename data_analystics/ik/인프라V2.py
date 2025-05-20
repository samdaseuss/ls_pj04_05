
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