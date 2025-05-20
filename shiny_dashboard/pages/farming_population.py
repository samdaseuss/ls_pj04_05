from shiny import ui, render, App
import pandas as pd
from shiny_dashboard.styles.styles import get_custom_css
import plotly.express as px
import plotly.graph_objects as go
import folium
import json
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np
import os
from pathlib import Path


def get_base_dir():
    current_dir = Path(os.getcwd())
    
    while current_dir.name != 'ls_pj04_5' and current_dir.parent != current_dir:
        current_dir = current_dir.parent
    
    if current_dir.parent == current_dir:
        print("경고: 프로젝트 루트 디렉토리를 찾지 못했습니다. 현재 디렉토리를 사용합니다.")
        current_dir = Path(os.getcwd())
    
    return current_dir

BASE_DIR = get_base_dir()
DATA_DIR = BASE_DIR / "data_analystics" / "pyun"
RAW_DATA_DIR = BASE_DIR / "shiny_dashboard" / "data" / "raw"
FARMING_DATA_PATH = DATA_DIR / "시도별_전거주지별_귀농가구원.csv"
NATIONAL_DATA_PATH = RAW_DATA_DIR / "전국" / "df_2023.csv"
GEOJSON_PATH = RAW_DATA_DIR / "전국" / "TL_SCCO_CTPRVN.json"
MEDICAL_DATA_PATH = RAW_DATA_DIR / "영천" / "인프라" / "영천시_의료기관.csv"
PARK_DATA_PATH = RAW_DATA_DIR / "영천" / "인프라" / "경상북도 영천시_도시공원.csv"

def load_farming_data():
    try:
        df_raw = pd.read_csv(FARMING_DATA_PATH, encoding='euc-kr', header=None)
        df_raw.columns = df_raw.iloc[0]
        df_raw = df_raw.drop(0).reset_index(drop=True)
        df = df_raw[df_raw['항목'] == '귀농인수 (명)'].copy()

        # '이동후 시도별' → '이동후지역'으로 이름 변경
        df = df.rename(columns={'이동후 시도별': '이동후지역'})

        # 연도/월 데이터 칼럼만 선택
        cols = df.columns.tolist()
        date_cols = [c for c in cols if c not in ['이동후지역', '항목']]

        # wide → long 변환
        df_long = df.melt(
            id_vars=['이동후지역', '항목'], value_vars=date_cols, var_name='연월', value_name='값')

        # 결측값(X) 처리 후 숫자형으로 변환
        df_long['값'] = df_long['값'].replace('X', 0).astype(int)

        # 연월 → 년도/월 분리
        df_long['년도'] = df_long['연월'].str.extract(r'(\d{4})').astype(int)
        df_long['월'] = (
            df_long['연월']
            .str.extract(r'\.(\d+)')[0]
            .fillna('0')  # 문자열 '0'로 채움
            .astype('Int64')  # nullable 정수형으로 변환
        )
        
        return df_long
    
    except Exception as e:
        print(f"데이터 로딩 오류: {str(e)}")
        return pd.DataFrame({
            '이동후지역': ['경상북도', '충청남도', '전라남도'] * 20,
            '항목': ['귀농인수 (명)'] * 60,
            '연월': ['2018.1', '2019.1', '2020.1', '2021.1', '2022.1', '2023.1'] * 10,
            '값': np.random.randint(500, 2000, 60),
            '년도': [2018, 2019, 2020, 2021, 2022, 2023] * 10,
            '월': [1] * 60
        })

def create_region_bar_chart(df_long, region_name, color_scale='Greens'):
    """연도별 귀농 인구 막대 그래프"""
    try:
        df_region = df_long[df_long['이동후지역'] == region_name]
        df_region_yearly = df_region.groupby('년도')['값'].sum().reset_index()

        fig = px.bar(
            df_region_yearly,
            x='년도',
            y='값',
            text='값',
            labels={'값': '귀농 인구 수 (명)', '년도': '연도'},
            title=f'연도별 {region_name} 귀농 인구 수',
            color='값',
            color_continuous_scale=color_scale
        )
        
        fig.update_traces(texttemplate='%{text:,}명', textposition='outside')
        fig.update_layout(
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            yaxis=dict(title='귀농 인구 수'),
            xaxis=dict(dtick=1),
            plot_bgcolor='white'
        )

        return fig
    
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"그래프 로딩 오류: {str(e)}",
            showarrow=False,
            font=dict(size=14, color="red")
        )
        return fig


def farming_population_dashboard():
    return ui.page_fluid(
        ui.head_content(ui.tags.style(get_custom_css())),
        ui.div(
            {"class":"header-section"},
            ui.row(
                ui.column(12,
                    ui.h1("전국 귀농 시각화 지도", style="text-align: center; font-size: 36px;"),
                    ui.p("전국 귀농 인구수 비교", style="text-align: center; font-size: 18px;")
                )
            )
        ),

        ui.h2("연도별 전국 귀농 인구 추이"),
        ui.row(
            ui.column(12,  # 전체 너비 사용
                ui.card(
                    ui.card_header("전국 연도별 귀농 현황"),
                    ui.div(
                        {"class": "chart-container", "style": "height: 550px; width: 100%; padding: 15px;"},
                        ui.output_ui("annual_returning_farmers_chart")
                    )
                )
            )
        ),

        ui.h2("전국 귀농 인구 추이"),
        ui.row(
            ui.column(6,
                ui.card(
                    ui.card_header("대한민국 귀농 현황 - 전국 지도"),
                    ui.output_ui("ko_map_output"),
                ),
            ),
            ui.column(6, 
                ui.card(
                    ui.card_header("전국 귀농 인구 테이블"),
                    ui.output_ui("view_table_ko_map")
                )
            ),
        ),
        
        ui.h2("귀농인수 Top 3(충청남도, 경상북도, 전라북도)", class_="section-title"),
        ui.row(
            ui.column(4,
                ui.div(
                    {"class": "chart-container"},
                    ui.output_ui("yeongcheon_chart_11")
                )
            ),
            ui.column(4,
                ui.div(
                    {"class": "chart-container"},
                    ui.output_ui("yeongcheon_chart_21")
                )
            ),
            ui.column(4,
                ui.div(
                    {"class": "chart-container"},
                    ui.output_ui("yeongcheon_chart_31")
                )
            )
        ),

        ui.navset_tab(
            ui.nav_panel("의료기관",
                ui.h2("귀농에 영향을 주는 의료기관 인프라 분석", class_="section-title"),
                ui.row(
                    ui.column(12,
                        ui.div(
                            {"class": "chart-container"},
                            ui.output_ui("yeongcheon_medical")
                        )
                    ),
                )
            ),
            ui.nav_panel("도시공원",
                ui.h2("귀농에 영향을 주는 도시공원 인프라 분석", class_="section-title"),
                ui.row(
                    ui.column(12,
                        ui.div(
                            {"class": "chart-container"},
                            ui.output_ui("yeongcheon_park")
                        )
                    )
                )    
            ),
            ui.nav_panel("데이터 테이블",
                ui.h2("귀농 원시 데이터", class_="section-title"),
                ui.row(
                    ui.column(12,
                        ui.div(
                            {"class": "table-container"},
                            ui.output_table("farming_data_table")
                        )
                    ),
                )
            ),
            id="tabset"
        )
    )


def farming_population_dashboard_server(input, output, session):
    df_long = load_farming_data()

    @render.ui
    def annual_returning_farmers_chart():
        try:
            years = ['2018', '2019', '2020', '2021', '2022', '2023']
            values = [12055, 11504, 12570, 14461, 12660, 10540]
            df_national = pd.DataFrame({'연도': years, '귀농인수': values})
            
            colorscale = 'Greens'
            
            fig = go.Figure()
            
            # 막대 그래프 추가
            fig.add_trace(go.Bar(
                x=df_national['연도'], 
                y=df_national['귀농인수'],
                name='귀농인수 (막대)', 
                marker=dict(
                    color=values,
                    colorscale=colorscale,
                    colorbar=dict(title="귀농인수"),
                    line=dict(color='black', width=1)
                ),
                opacity=0.8
            ))
            
            # 선 그래프 추가
            fig.add_trace(go.Scatter(
                x=df_national['연도'], 
                y=df_national['귀농인수'], 
                name='귀농인수 (선)', 
                mode='lines+markers',
                line=dict(color='blue', width=2),
                marker=dict(size=8)
            ))
            
            # 레이아웃 설정
            fig.update_layout(
                title='연도별 귀농인수 추이 (막대 + 선)',
                title_font_size=18,
                xaxis_title='연도',
                yaxis_title='귀농인수 (명)',
                template='plotly_white',
                height=500,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )

            fig.update_traces(
                texttemplate='%{y:,}', 
                textposition='outside',
                selector=dict(type='bar')
            )
            
            fig.update_yaxes(
                showgrid=True, 
                gridwidth=1, 
                gridcolor='rgba(0,0,0,0.1)',
                griddash='dash'
            )
            
            return ui.HTML(fig.to_html(include_plotlyjs="require", full_html=False))
        
        except Exception as e:
            return ui.div(
                ui.h3("그래프 로딩 오류", style="color:red;"),
                ui.p(f"오류 메시지: {str(e)}")
            )
    
    @render.ui
    def yeongcheon_chart_11():
        fig = create_region_bar_chart(df_long, '경상북도')
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))
    
    @render.ui
    def yeongcheon_chart_21():
        fig = create_region_bar_chart(df_long, '충청남도')
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))
    
    @render.ui
    def yeongcheon_chart_31():
        fig = create_region_bar_chart(df_long, '전라남도')
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))

    @render.ui
    def yeongcheon_medical():
        try:
            medical_info = pd.read_csv(MEDICAL_DATA_PATH, encoding='cp949')
            map_center = [35.9736, 128.9408]
            m = folium.Map(location=map_center, zoom_start=13)
            for i, row in medical_info.iterrows():
                folium.Marker(
                    location=[row['위도'], row['경도']],
                    popup=row['의료기관명'],
                    icon=folium.Icon(color='blue', icon='hospital', prefix='fa')
                ).add_to(m)
            map_html = m._repr_html_()
            return ui.HTML(map_html)
        except Exception as e:
            return ui.div(
                ui.h3("지도 로딩 오류"),
                ui.p(f"오류 메시지: {str(e)}")
            )
    
    @render.table
    def farming_data_table():
        try:
            df_summary = df_long.groupby('이동후지역')['값'].sum().reset_index()
            df_summary = df_summary.sort_values('값', ascending=False)
            df_summary.columns = ['시도', '총 귀농인수']
            return df_summary
        except Exception as e:
            # 오류 발생 시 샘플 데이터 반환
            sample_data = pd.DataFrame({
                '시도': ['경상북도', '전라남도', '충청남도', '경기도', '강원도'],
                '총 귀농인수': [1950, 1803, 1333, 1033, 720]
            })
            return sample_data
    
    @render.ui
    def yeongcheon_park():
        try:
            park_info = pd.read_csv(PARK_DATA_PATH, encoding='cp949')
            map_center = [35.9736, 128.9408]
            m = folium.Map(location=map_center, zoom_start=13)
            for i, row in park_info.iterrows():
                folium.Marker(
                    location=[row['위도'], row['경도']],
                    popup=row['명칭'],
                    icon=folium.Icon(color='blue', icon='tree', prefix='fa')
                ).add_to(m)
            
            map_html = m._repr_html_()
            return ui.HTML(map_html)
        except Exception as e:
            return ui.div(
                ui.h3("지도 로딩 오류"),
                ui.p(f"오류 메시지: {str(e)}")
            )
    
    @render.ui
    def ko_map_output():
        try:
            df_2023 = pd.read_csv(NATIONAL_DATA_PATH)

            with open(GEOJSON_PATH, encoding='utf-8') as f:
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

            m = folium.Map(location=[36.5, 127.8], zoom_start=7, tiles='cartodbpositron')

            folium.Choropleth(
                geo_data=geo_data,
                data=df_2023,
                columns=['행정구역별', '2023'],
                key_on='feature.properties.CTP_KOR_NM',
                fill_color='YlGnBu',
                fill_opacity=0.7,
                line_opacity=0.2
            ).add_to(m)
            
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

            m.fit_bounds([[33, 124], [39, 132]])
            map_html = m._repr_html_()
            return ui.HTML(map_html)
        except Exception as e:
            return ui.div(
                ui.h3("지도 로딩 오류"),
                ui.p(f"오류 메시지: {str(e)}")
            )
    
    @render.ui
    def view_table_ko_map():
        try:
            df_2023 = pd.read_csv(NATIONAL_DATA_PATH)

            if "항목" in df_2023.columns:
                new_df_2023 = df_2023.drop(columns=["항목"])
            else:
                new_df_2023 = df_2023

            행정구역 = new_df_2023["행정구역별"].tolist()
            귀농인_수 = new_df_2023["2023"].tolist()

            fig = go.Figure(data=[go.Table(
                header=dict(
                    values=['<b>행정구역</b>', '<b>귀농인 수(명)</b>'],
                    fill_color='lightpink',
                    align='center'
                ),
                cells=dict(
                    values=[행정구역, 귀농인_수],
                    fill_color='white',
                    align='center'
                )
            )])

            return ui.HTML(fig.to_html(include_plotlyjs="cdn"))
        
        except Exception as e:
            print(f"테이블 데이터 로딩 오류: {str(e)}")
            
            sample_data = pd.DataFrame({
                '행정구역별': ['경상북도', '전라남도', '충청남도', '경기도', '강원도'],
                '2023': [1950, 1803, 1333, 1033, 720]
            })
            
            행정구역 = sample_data["행정구역별"].tolist()
            귀농인_수 = sample_data["2023"].tolist()
            
            sample_fig = go.Figure(data=[go.Table(
                header=dict(
                    values=['<b>행정구역</b>', '<b>귀농인 수(명)</b>'],
                    fill_color='lightpink',
                    align='center'
                ),
                cells=dict(
                    values=[행정구역, 귀농인_수],
                    fill_color='white',
                    align='center'
                )
            )])
            
            sample_fig.update_layout(
                title="샘플 데이터 (원본 데이터 로딩 실패)"
            )
            
            return ui.HTML(sample_fig.to_html(include_plotlyjs="cdn"))