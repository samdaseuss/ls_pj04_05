# 전국 귀농귀촌 인구통계 시각화
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일
df1 = pd.read_csv("../../data/ikhyeon.csv",encoding='cp949')

df1.info()

df2 = df1[df1['행정구역별'] == '전국']
df2

year_columns = ['2018', '2019', '2020', '2021', '2022', '2023']

df_selected = df2[year_columns]
df_selected
row_data = df_selected.iloc[[1]]
row_data

# 시각화(전국 귀농 인구 추이)
import matplotlib.pyplot as plt

# 데이터프레임 형태로 데이터 구성
data = {
    '2018': [12055],
    '2019': [11504],
    '2020': [12570],
    '2021': [14461],
    '2022': [12660],
    '2023': [10540]
}

df3 = pd.DataFrame(data)

# x축: 연도 (컬럼명 리스트)
x = list(df3.columns)

# y축: 2행 값 (index 0으로 접근)
y = df3.iloc[0].values

# 그래프 시각화
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.cm as cm

# ✅ 한글 폰트 설정
mpl.rc('font', family='Malgun Gothic')
mpl.rcParams['axes.unicode_minus'] = False

# 데이터
x = np.arange(6)
years = [2018, 2019, 2020, 2021, 2022, 2023]
y = [12055, 11504, 12570, 14461, 12660, 10540]

# ✅ 값 기준 채도 조절 (vmin 임의로 살짝 높여줌)
norm = plt.Normalize(vmin=min(y) * 0.95, vmax=max(y))  # 하한선을 살짝 위로
colors = cm.Greens(norm(y))

# ✅ 시각화
plt.figure(figsize=(10, 6))

# 막대그래프 (테두리 포함, 채도 정상화)
plt.bar(x, y, width=0.6, color=colors, edgecolor='black', alpha=0.8, label='귀농인수 (막대)')

# 선그래프 (겹치기)
plt.plot(x, y, marker='o', linestyle='-', linewidth=2, color='blue', label='귀농인수 (선)')

# x축 라벨
plt.xticks(x, years)

# 제목, 라벨, 범례
plt.title('연도별 귀농인수 추이 (막대+선)', fontsize=14)
plt.xlabel('연도')
plt.ylabel('귀농인수 (명)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()


df1

target_regions = ['부산광역시', '대구광역시', '인천광역시', '경기도', 
                  '충청북도', '충청남도', '강원도', '경상북도', '경상남도','전라북도','전라남도','제주특별자치도']
dfQ = df1[df1['행정구역별'].isin(target_regions)]
dfQ

df_guinong2 = dfQ[dfQ['항목'] == '귀농인수 (명)']

year_columns2 = ['2018', '2019', '2020', '2021', '2022', '2023']

df_selected2 = df_guinong2[['행정구역별', '항목'] + year_columns2]

df_selected2

# 시각화

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# ✅ 한글 폰트 설정 (윈도우 기준)
mpl.rc('font', family='Malgun Gothic')
mpl.rcParams['axes.unicode_minus'] = False

# 데이터프레임 구성
data2 = {
    '행정구역별': ['부산광역시', '대구광역시', '인천광역시', '경기도', '강원도', '충청북도', '충청남도', 
                 '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도'],
    '2018': [25, 59, 134, 987, 1055, 925, 1328, 1335, 2039, 2196, 1518, 281],
    '2019': [18, 76, 146, 999, 948, 847, 1268, 1327, 2020, 2156, 1323, 238],
    '2020': [35, 58, 122, 1118, 947, 938, 1502, 1511, 2358, 2252, 1349, 231],
    '2021': [26, 71, 171, 1288, 1022, 1086, 1821, 1524, 2579, 2726, 1699, 250],
    '2022': [24, 62, 118, 1207, 954, 962, 1595, 1237, 1987, 2579, 1530, 249],
    '2023': [36, 163, 88, 1033, 720, 730, 1333, 1099, 1803, 1950, 1220, 243]
}

# top5 지역만 시각화화
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# ✅ 한글 폰트 설정 (윈도우 기준)
mpl.rc('font', family='Malgun Gothic')
mpl.rcParams['axes.unicode_minus'] = False

# 데이터프레임
data2 = {
    '행정구역별': ['부산광역시', '대구광역시', '인천광역시', '경기도', '강원도', '충청북도', '충청남도', 
                 '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도'],
    '2018': [25, 59, 134, 987, 1055, 925, 1328, 1335, 2039, 2196, 1518, 281],
    '2019': [18, 76, 146, 999, 948, 847, 1268, 1327, 2020, 2156, 1323, 238],
    '2020': [35, 58, 122, 1118, 947, 938, 1502, 1511, 2358, 2252, 1349, 231],
    '2021': [26, 71, 171, 1288, 1022, 1086, 1821, 1524, 2579, 2726, 1699, 250],
    '2022': [24, 62, 118, 1207, 954, 962, 1595, 1237, 1987, 2579, 1530, 249],
    '2023': [36, 163, 88, 1033, 720, 730, 1333, 1099, 1803, 1950, 1220, 243]
}

df47 = pd.DataFrame(data2)

# ✅ 원하는 지역만 필터링
target_regions = ['충청남도', '전라북도', '전라남도', '경상북도', '경상남도']
df_target = df47[df47['행정구역별'].isin(target_regions)]

# 막대그래프 파라미터 설정
years47 = ['2018', '2019', '2020', '2021', '2022', '2023']
x = np.arange(len(df_target['행정구역별']))  # 지역별 위치 (x축)
bar_width = 0.12  # 막대 너비 (6개 그룹이니까 좁게)

# 시각화 시작
plt.figure(figsize=(14, 6))

# 연도별 막대 쌓기
for i, year in enumerate(years47):
    plt.bar(x + i * bar_width, df_target[year], width=bar_width, label=year)

# x축 설정 (지역 이름 가운데 정렬)
plt.xticks(x + bar_width * (len(years47)-1) / 2, df_target['행정구역별'], rotation=45)

# 제목 및 라벨
plt.title('도별 연도별 귀농인수 (충남, 전북, 전남, 경북, 경남)', fontsize=14)
plt.xlabel('행정구역별')
plt.ylabel('귀농인수 (명)')
plt.legend(title='연도', loc='upper right')
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()


df_selected2
# '2023' 컬럼 문자열로 선택
df_2023 = df_selected2[['행정구역별', '항목', '2023']]

# 결과 출력
print(df_2023)

df_2023.to_csv('df_2023.csv', index=False, encoding='utf-8-sig')

import pandas as pd
import folium
import json

df1 = pd.read_csv("../../data/ikhyeon.csv",encoding='cp949')
import json
import folium

# 1. 귀농인구수 데이터 불러오기
df_2023 = pd.read_csv('./df_2023.csv')

# 2. GeoJSON (시도 경계 데이터) 불러오기
with open('TL_SCCO_CTPRVN.json', encoding='utf-8') as f:
    geo_data = json.load(f)

# 3. folium 지도 객체 생성 (중심좌표 설정)
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 4. Choropleth (귀농인구수 기준 색상 채우기)
folium.Choropleth(
    geo_data=geo_data,
    data=df_2023,
    columns=['행정구역별', '2023'],
    key_on='feature.properties.CTP_KOR_NM',  # GeoJSON 속성 이름 (시도명)
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='2023년 귀농인구수'
).add_to(m)

# 5. 지도 저장 및 보기
m.save('귀농인구수_choropleth.html')




import json
import folium
import pandas as pd

# 1. 데이터 불러오기
df_2023 = pd.read_csv('./df_2023.csv')

# 2. GeoJSON 불러오기
with open('TL_SCCO_CTPRVN.json', encoding='utf-8') as f:
    geo_data = json.load(f)

# 3. 남한 시도 필터링 (세종특별자치시 제거)
south_korea_regions = [
    "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시",
    "대전광역시", "울산광역시", "경기도", "강원도", "강원특별자치도",
    "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도"
]

geo_data['features'] = [
    feature for feature in geo_data['features']
    if feature['properties']['CTP_KOR_NM'] in south_korea_regions
]

# 4. 라벨 위치 수동 지정
label_positions = {
    "서울특별시": [37.65, 126.95],
    "경기도": [37.3, 127.4],
    "인천광역시": [37.45, 126.6],
    "충청남도": [36.4, 126.8],
    "충청북도": [36.9, 127.8],
    "대전광역시": [36.3, 127.4],
    "전라남도": [34.8, 126.7],
    "전라북도": [35.7, 127.2],
    "경상남도": [35.2, 128.2],
    "경상북도": [36.3, 128.8],
    "강원도": [37.5, 128.2],
    "강원특별자치도": [37.5, 128.2],
    "제주특별자치도": [33.4, 126.5]
}

# 5. 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7, tiles='cartodbpositron')

# 6. Choropleth (기본 범례 제거)
folium.Choropleth(
    geo_data=geo_data,
    data=df_2023,
    columns=['행정구역별', '2023'],
    key_on='feature.properties.CTP_KOR_NM',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

# 7. 라벨 (도 이름)
for feature in geo_data['features']:
    name = feature['properties']['CTP_KOR_NM']
    
    if name in label_positions:
        lat, lon = label_positions[name]
    else:
        coordinates = feature['geometry']['coordinates']
        if feature['geometry']['type'] == 'MultiPolygon':
            poly = coordinates[0][0]
        else:
            poly = coordinates[0]
        lon = sum([point[0] for point in poly]) / len(poly)
        lat = sum([point[1] for point in poly]) / len(poly)

    folium.Marker(
        [lat, lon],
        icon=folium.DivIcon(
            html=f"""
            <div style="
                font-size: 8px;
                font-weight: bold;
                text-align: center;
                white-space: nowrap;
                transform: translate(-50%, -50%);
                line-height: 1;
            ">
                {name}
            </div>
            """
        )
    ).add_to(m)

# 8. 커스텀 범례 (얇고 잘리지 않게)
legend_html = '''
<div style="
    position: fixed;
    top: 100px; right: 10px;
    width: 110px;
    z-index:9999;
    font-size:11px;
    background-color:white;
    padding:6px 8px;
    border:1px solid grey;
    box-shadow: 1px 1px 4px rgba(0,0,0,0.2);
    line-height: 1.4;">
    <b style="font-size:12px;">귀농 인구수</b><br>
    <i style="background: #edf8b1; width: 14px; height: 14px; display: inline-block; margin-right: 6px;"></i>0 - 674<br>
    <i style="background: #7fcdbb; width: 14px; height: 14px; display: inline-block; margin-right: 6px;"></i>675 - 993<br>
    <i style="background: #41b6c4; width: 14px; height: 14px; display: inline-block; margin-right: 6px;"></i>994 - 1312<br>
    <i style="background: #2c7fb8; width: 14px; height: 14px; display: inline-block; margin-right: 6px;"></i>1313 - 1631<br>
    <i style="background: #253494; width: 14px; height: 14px; display: inline-block; margin-right: 6px;"></i>1632 - 1950
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# 9. 지도 범위 조정
m.fit_bounds([[33, 124], [39, 132]])

# 10. 저장
m.save('귀농인구수_choropleth_최종작업.html')

######################################################################

# # CSV 파일
# dfg = pd.read_csv("./gungsang.csv",encoding='cp949')


# # 2. 필요한 컬럼만 추출
# df_2023_gwinong = dfg[['시군명', '2023년(귀농)']]

# # 3. 결과 출력
# print(df_2023_gwinong.head())
# df_2023_gwinong['2023년(귀농)'] = df_2023_gwinong['2023년(귀농)'].fillna(df_2023_gwinong['2023년(귀농)'].mean())


# df_2023_gwinong.to_csv('dfg_2023_귀농데이터2.csv', index=False, encoding='utf-8-sig')


# import pandas as pd
# import folium
# import json

# # 1. 데이터 불러오기
# df_2023_gwinong = pd.read_csv('dfg_2023_귀농데이터2.csv', encoding='utf-8-sig')  # 또는 cp949
# with open('sig.geojson', encoding='utf-8') as f:
#     geo_data = json.load(f)

# # 2. folium 지도 생성
# m2 = folium.Map(location=[36.0, 128.5], zoom_start=9, tiles='cartodbpositron')

# # 3. Choropleth 시각화
# folium.Choropleth(
#     geo_data=geo_data,
#     data=df_2023_gwinong,
#     columns=['시군명', '2023년(귀농)'],
#     key_on='feature.properties.sggnm',  # GeoJSON 속성명
#     fill_color='YlGnBu',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='2023년 귀농 인구수 (경상북도)'
# ).add_to(m2)

# # 4. 저장
# m2.save('경상북도_귀농_지도.html')