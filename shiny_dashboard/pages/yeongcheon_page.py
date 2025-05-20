# pages/yeongcheon_page.py
from shiny import ui, render
import pandas as pd
import folium
import plotly.express as px
import sys
import os
from shiny_dashboard.styles.styles import get_custom_css

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.migration_data import (
    migration_data,
    region_coordinates,
    yeongcheon_coordinates
)

data_types = {
    "yeongcheon_migrants": "귀촌인 전체",
    "yeongcheon_household_heads": "귀촌가구주",
    "yeongcheon_family_members": "동반가구원"
}

def yeongcheon_dashboard():
    return ui.page_fluid(
        ui.head_content(ui.tags.style(get_custom_css())),

        ui.div(
            {"class":"header-section"},
            ui.row(
                ui.column(12,
                    ui.h1("영천시 귀농/귀촌 현황 대시보드", style="text-align: center; font-size: 36px; margin-bottom: 20px;"),
                    ui.p("영천시 귀농 인구 수 비교", style="text-align: center; font-size: 18px;")
                )
            )
        ),

        ui.row(
            ui.column(4,
                ui.value_box(
                    "최다 귀촌 지역",
                    ui.output_text("top_region"),
                    theme="bg-gradient-blue-purple"
                )),
                ui.column(4,
                    ui.value_box(
                        "영천시 총 귀촌인",
                        ui.output_text("total_migrants"),
                        theme="bg-gradient-orange-red"
                    )
                ),
                ui.column(4,
                    ui.value_box(
                        "대구 비율",
                        ui.output_text("daegu_ratio"),
                        theme="bg-gradient-green-yellow"
                    )
                )
            ),

        ui.row(
            ui.column(3,
                ui.div(
                    {"class": "sidebar-container"},
                    ui.card(
                        ui.card_header("귀촌인 통계"),
                        ui.output_text("summary_stats"),
                    ),
                    ui.card(
                        ui.card_header("대시보드 설정"),
                        ui.input_select(
                            "data_type",
                            "데이터 유형 선택:",
                            data_types
                        ),
                        ui.input_slider(
                            "marker_size",
                            "마커 크기 조정:",
                            min=0.5,
                            max=3.0,
                            value=1.0,
                            step=0.1
                        ),
                        ui.input_checkbox(
                            "show_labels",
                            "지역 라벨 표시",
                            True
                        ),
                        ui.hr(),
                        ui.p("이 대시보드는 경북 영천시 귀촌인의 이전 거주지 현황을 시각화합니다."),
                        ui.p(f"마지막 업데이트: {pd.Timestamp.now().strftime('%Y-%m-%d')}"),
                    ),
                )
            ),
            
            ui.column(9,
                ui.card(
                    ui.card_header("대한민국 지도 - 영천시 귀촌인 출신지"),
                    ui.output_ui("map_output"),
                ),
                
                ui.p("영천 지역의 귀농/귀촌 인구 현황 및 출신지 분석", style="text-align: center; font-size: 18px; margin-top: 20px; margin-bottom: 20px;"),
                
                ui.card(
                    ui.card_header("지역별 귀촌인 현황"),
                    ui.output_ui("bar_chart"),
                ),
            )
        ),
        
        ui.h2("영천시 귀농 연도별 현황 (Top3 지역)", class_="section-title", style="margin-top: 30px;"),
        ui.row(
            ui.column(4,
                ui.div(
                    {"class": "chart-container"},
                    ui.output_ui("yeongcheon_chart_1")
                )
            ),
            ui.column(4,
                ui.div(
                    {"class": "chart-container"},
                    ui.output_ui("yeongcheon_chart_2")
                )
            ),
            ui.column(4,
                ui.div(
                    {"class": "chart-container"},
                    ui.output_ui("yeongcheon_chart_3")
                )
            )
        ),
    )

def yeongcheon_dashboard_server(input, output, session):
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "시도별_전거주지별_귀농가구원.csv")
        df_raw = pd.read_csv(data_path, encoding='euc-kr', header=None)
        df_raw.columns = df_raw.iloc[0]
        df_raw = df_raw.drop(0).reset_index(drop=True)

        df = df_raw[df_raw['항목'] == '귀농인수 (명)'].copy()
        df = df.rename(columns={'이동후 시도별': '이동후지역'})

        cols = df.columns.tolist()
        date_cols = [c for c in cols if c not in ['이동후지역', '항목']]

        df_long = df.melt(
            id_vars=['이동후지역', '항목'], 
            value_vars=date_cols, 
            var_name='연월', value_name='값')

        df_long['값'] = df_long['값'].replace('X', 0).astype(int)

        df_long['년도'] = df_long['연월'].str.extract(r'(\d{4})').astype(int)
        df_long['월'] = df_long['연월'].str.extract(r'\.(\d+)')[0].fillna(0).astype(int)
    except Exception as e:
        print(f"데이터 로드 실패: {e}")
        years = list(range(2018, 2025))
        regions = ['경상북도', '충청남도', '전라남도']
        data = []
        for region in regions:
            for year in years:
                data.append({'이동후지역': region, '항목': '귀농인수 (명)', 
                             '년도': year, '값': 100 + year - 2018 + (50 if region == '경상북도' else 30 if region == '충청남도' else 20)})
        df_long = pd.DataFrame(data)
    
    @render.text
    def summary_stats():
        data_type = input.data_type()
        data = migration_data[data_type]
        regions = migration_data["regions"]
        
        total = sum(data)
        max_idx = data.index(max(data))
        max_region = regions[max_idx]
        
        stats = f"총 인원: {total}명\n"
        stats += f"최다 지역: {max_region} ({data[max_idx]}명, {data[max_idx]/total*100:.1f}%)\n"
        
        sorted_idx = sorted(range(len(data)), key=lambda i: data[i], reverse=True)
        stats += "\n상위 3개 지역:\n"
        for i in range(3):
            idx = sorted_idx[i]
            stats += f"{i+1}. {regions[idx]}: {data[idx]}명 ({data[idx]/total*100:.1f}%)\n"
            
        return stats
    
    @render.text
    def top_region():
        data_type = input.data_type()
        data = migration_data[data_type]
        regions = migration_data["regions"]
        max_idx = data.index(max(data))
        return f"{regions[max_idx]}"
    
    @render.text
    def top_count():
        data_type = input.data_type()
        data = migration_data[data_type]
        total = sum(data)
        max_val = max(data)
        return f"{max_val}명 ({max_val/total*100:.1f}%)"
    
    @render.text
    def total_migrants():
        data_type = input.data_type()
        data = migration_data[data_type]
        return f"{sum(data)}명"
    
    @render.text
    def daegu_ratio():
        data_type = input.data_type()
        data = migration_data[data_type]
        regions = migration_data["regions"]
        daegu_idx = regions.index("대구")
        daegu_val = data[daegu_idx]
        total = sum(data)
        return f"{daegu_val}명 ({daegu_val/total*100:.1f}%)"
    
    @render.ui
    def map_output():
        data_type = input.data_type()
        selected_data = migration_data[data_type]
        regions = migration_data["regions"]
        
        m = folium.Map(
            location=[36.5, 127.8], 
            zoom_start=7,
            tiles='CartoDB positron'
        )
        
        folium.Marker(
            yeongcheon_coordinates,
            popup="<b>영천시</b>",
            tooltip="영천시",
            icon=folium.Icon(color='red', icon='home', prefix='fa')
        ).add_to(m)
        
        for i, region in enumerate(regions):
            if selected_data[i] > 0:
                size = selected_data[i] / max(selected_data) * 30 * input.marker_size()
                
                percentage = selected_data[i] / sum(selected_data) * 100
                
                if selected_data[i] == max(selected_data):
                    color = 'darkred'
                elif selected_data[i] > sum(selected_data) / len(regions) * 2:
                    color = 'red'
                elif selected_data[i] > sum(selected_data) / len(regions):
                    color = 'orange'
                else:
                    color = 'blue'
                
                folium.CircleMarker(
                    location=region_coordinates[region],
                    radius=size,
                    popup=f"<b>{region}</b><br>{selected_data[i]}명 ({percentage:.1f}%)",
                    tooltip=f"{region}: {selected_data[i]}명",
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.6
                ).add_to(m)
                
                if input.show_labels():
                    folium.map.Marker(
                        region_coordinates[region],
                        icon=folium.DivIcon(
                            icon_size=(0, 0),
                            icon_anchor=(0, 0),
                            html=f'<div style="font-size: 10pt; font-weight: bold;">{region}</div>'
                        )
                    ).add_to(m)
            
        for i, region in enumerate(regions):
            if selected_data[i] > 0:
                weight = selected_data[i] / max(selected_data) * 10
                if weight < 1:
                    weight = 1
                
                if selected_data[i] == max(selected_data):
                    color = 'darkred'
                elif selected_data[i] > sum(selected_data) / len(regions) * 2:
                    color = 'red'
                elif selected_data[i] > sum(selected_data) / len(regions):
                    color = 'orange'
                else:
                    color = 'blue'
                
                folium.PolyLine(
                    locations=[region_coordinates[region], yeongcheon_coordinates],
                    color=color,
                    weight=weight,
                    opacity=0.6,
                    dash_array='5, 5',
                    tooltip=f"{region} → 영천시: {selected_data[i]}명"
                ).add_to(m)
        
        map_html = m._repr_html_()
        
        return ui.HTML(map_html)
    
    @render.ui
    def bar_chart():
        data_type = input.data_type()
        selected_data = migration_data[data_type]
        regions = migration_data["regions"]
        
        sorted_indices = sorted(range(len(selected_data)), key=lambda i: selected_data[i], reverse=True)
        sorted_regions = [regions[i] for i in sorted_indices]
        sorted_data = [selected_data[i] for i in sorted_indices]
        
        top_n = 10
        if len(sorted_data) > top_n:
            sorted_regions = sorted_regions[:top_n]
            sorted_data = sorted_data[:top_n]
        
        df = pd.DataFrame({
            '지역': sorted_regions,
            '인원수': sorted_data
        })
        
        title_type = data_types[data_type]
        fig = px.bar(
            df, 
            x='지역', 
            y='인원수',
            title=f'지역별 영천시 {title_type} 현황 (상위 {len(sorted_data)}개 지역)',
            color='지역',
            color_discrete_sequence=px.colors.qualitative.Bold,
            text='인원수'
        )
        
        fig.update_layout(
            xaxis_title='출신 지역',
            yaxis_title='인원수 (명)',
            xaxis_tickangle=-45,
            height=500,
            margin=dict(l=50, r=50, t=80, b=100),
            showlegend=False
        )
        
        fig.update_traces(
            texttemplate='%{text}명',
            textposition='outside'
        )
        
        plot_html = fig.to_html(include_plotlyjs='cdn')

        return ui.HTML(plot_html)
    
    @render.ui
    def yeongcheon_chart_1():
        df_경북 = df_long[df_long['이동후지역'] == '경상북도']
        df_경북_연도별 = df_경북.groupby('년도')['값'].sum().reset_index()

        fig = px.bar(
            df_경북_연도별,
            x='년도',
            y='값',
            text='값',
            labels={'값': '귀농 인구 수 (명)', '년도': '연도'},
            title='연도별 경상북도 귀농 인구 수',
            color='값',
            color_continuous_scale='Greens'
        )

        fig.update_traces(texttemplate='%{text:,}명', textposition='outside')
        fig.update_layout(
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            yaxis=dict(title='귀농 인구 수'),
            xaxis=dict(dtick=1),
            plot_bgcolor='white'
        )

        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))
    
    @render.ui
    def yeongcheon_chart_2():
        df_충남 = df_long[df_long['이동후지역'] == '충청남도']
        df_충남_연도별 = df_충남.groupby('년도')['값'].sum().reset_index()

        fig = px.bar(
            df_충남_연도별,
            x='년도',
            y='값',
            text='값',
            labels={'값': '귀농 인구 수 (명)', '년도': '연도'},
            title='연도별 충청남도 귀농 인구 수',
            color='값',
            color_continuous_scale='Blues'
        )

        fig.update_traces(texttemplate='%{text:,}명', textposition='outside')
        fig.update_layout(
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            yaxis=dict(title='귀농 인구 수'),
            xaxis=dict(dtick=1),
            plot_bgcolor='white'
        )
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))
    
    @render.ui
    def yeongcheon_chart_3():
        df_전남 = df_long[df_long['이동후지역'] == '전라남도']
        df_전남_연도별 = df_전남.groupby('년도')['값'].sum().reset_index()

        fig = px.bar(
            df_전남_연도별,
            x='년도',
            y='값',
            text='값',
            labels={'값': '귀농 인구 수 (명)', '년도': '연도'},
            title='연도별 전라남도 귀농 인구 수',
            color='값',
            color_continuous_scale='Oranges'
        )

        fig.update_traces(texttemplate='%{text:,}명', textposition='outside')
        fig.update_layout(
            uniformtext_minsize=8,
            uniformtext_mode='hide',
            yaxis=dict(title='귀농 인구 수'),
            xaxis=dict(dtick=1),
            plot_bgcolor='white'
        )

        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))