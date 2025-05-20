import folium
import pandas as pd
import json
from pathlib import Path

def create_korea_farming_map(national_data_path, geojson_path):
    try:
        df_2023 = pd.read_csv(national_data_path)

        with open(geojson_path, encoding='utf-8') as f:
            geo_data = json.load(f)

        south_korea_regions = [
            "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시",
            "대전광역시", "울산광역시", "경기도", "강원도", "강원특별자치도",
            "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도"
        ]

        geo_data['features'] = [
            feature for feature in geo_data['features']
            if feature['properties']['CTP_KOR_NM'] in south_korea_regions
        ]

        # 라벨 위치 수동 지정
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

        # 지도 생성
        m = folium.Map(location=[36.5, 127.8], zoom_start=7, tiles='cartodbpositron')

        # Choropleth
        folium.Choropleth(
            geo_data=geo_data,
            data=df_2023,
            columns=['행정구역별', '2023'],
            key_on='feature.properties.CTP_KOR_NM',
            fill_color='YlGnBu',
            fill_opacity=0.7,
            line_opacity=0.2
        ).add_to(m)

        # 라벨 (도 이름)
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

        # 범례 추가
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

        # 지도 범위 조정
        m.fit_bounds([[33, 124], [39, 132]])
        
        # HTML로 변환
        return m._repr_html_()
    
    except Exception as e:
        raise Exception(f"지도 생성 중 오류가 발생했습니다: {str(e)}")

def create_local_facility_map(facility_data_path, center=None, zoom_level=13, facility_type='hospital'):
    """시설(의료기관, 공원 등) 지도를 생성합니다.
    
    Args:
        facility_data_path: 시설 데이터 파일 경로
        center: 지도 중심 좌표 [위도, 경도]
        zoom_level: 줌 레벨
        facility_type: 시설 유형 ('hospital' 또는 'park')
        
    Returns:
        str: HTML 형식의 지도
    """
    try:
        # 데이터 로드
        facility_info = pd.read_csv(facility_data_path, encoding='cp949')
        
        # 기본 중심 좌표 설정
        if center is None:
            center = [35.9736, 128.9408]  # 영천시 기본 좌표
        
        # 지도 생성
        m = folium.Map(location=center, zoom_start=zoom_level)
        
        # 아이콘 유형 설정
        if facility_type == 'hospital':
            icon_color = 'blue'
            icon_name = 'hospital'
            popup_field = '의료기관명'
        elif facility_type == 'park':
            icon_color = 'green'
            icon_name = 'tree'
            popup_field = '명칭'
        else:
            icon_color = 'blue'
            icon_name = 'info'
            popup_field = '명칭'
        
        # 마커 추가
        for _, row in facility_info.iterrows():
            try:
                popup_text = row[popup_field] if popup_field in row else "정보 없음"
                folium.Marker(
                    location=[row['위도'], row['경도']],
                    popup=popup_text,
                    icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa')
                ).add_to(m)
            except KeyError:
                # 필드 이름이 다를 경우 대체
                lat_field = '위도' if '위도' in row else 'latitude' if 'latitude' in row else 'lat'
                lon_field = '경도' if '경도' in row else 'longitude' if 'longitude' in row else 'lon'
                folium.Marker(
                    location=[row[lat_field], row[lon_field]],
                    popup="정보 없음",
                    icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa')
                ).add_to(m)
        
        return m._repr_html_()
    
    except Exception as e:
        raise Exception(f"지도 생성 중 오류가 발생했습니다: {str(e)}")