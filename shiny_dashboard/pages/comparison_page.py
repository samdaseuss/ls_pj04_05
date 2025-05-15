# pages/comparison_page.py
from shiny import ui, render
import pandas as pd
import folium
import plotly.express as px
from shiny_dashboard.data.migration_data import (
    migration_data,
    region_coordinates,
    yeongcheon_coordinates
)

data_types = {
    "yeongcheon_migrants": "귀촌인 전체",
    "yeongcheon_household_heads": "귀촌가구주",
    "yeongcheon_family_members": "동반가구원"
}

# A 페이지 UI 정의
def page_a_ui():
    return ui.page_fluid(
        ui.h1("영천시 귀촌인 현황 대시보드"),
        ui.row(
            # 사이드바 (3열)
            ui.column(3,
                ui.card(
                    ui.card_header("대시보드 정보"),
                    ui.p("이 대시보드는 경북 영천시 귀촌인의 이전 거주지 현황을 시각화합니다."),
                    ui.p(f"마지막 업데이트: {pd.Timestamp.now().strftime('%Y-%m-%d')}"),
                    ui.hr(),
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
                ),
                
                ui.card(
                    ui.card_header("귀촌인 통계"),
                    ui.output_text("summary_stats"),
                ),
            ),
            
            # 메인 컨텐츠 (9열)
            ui.column(9,
                ui.card(
                    ui.card_header("대한민국 지도 - 영천시 귀촌인 출신지"),
                    ui.output_ui("map_output"),
                ),
                
                ui.layout_column_wrap(
                    ui.value_box(
                        "최다 귀촌 지역",
                        ui.output_text("top_region"),
                        showcase=ui.output_text("top_count"),
                        theme="bg-gradient-blue-purple"
                    ),
                    ui.value_box(
                        "영천시 총 귀촌인",
                        ui.output_text("total_migrants"),
                        theme="bg-gradient-orange-red"
                    ),
                    ui.value_box(
                        "대구 비율",
                        ui.output_text("daegu_ratio"),
                        theme="bg-gradient-green-yellow"
                    ),
                    width="32%"
                ),
                
                ui.card(
                    ui.card_header("지역별 귀촌인 현황"),
                    ui.output_ui("bar_chart"),
                ),
            )
        )
    )

# A 페이지 서버 함수
def page_a_server(input, output, session):
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
        
        # 상위 3개 지역 표시
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
        
        # 지도 생성
        m = folium.Map(
            location=[36.5, 127.8], 
            zoom_start=7,
            tiles='CartoDB positron'
        )
        
        # 영천시 위치 마커 추가
        folium.Marker(
            yeongcheon_coordinates,
            popup="<b>영천시</b>",
            tooltip="영천시",
            icon=folium.Icon(color='red', icon='home', prefix='fa')
        ).add_to(m)
        
        # 지역별 마커 추가
        for i, region in enumerate(regions):
            if selected_data[i] > 0:  # 데이터가 있는 경우만 표시
                # 마커 크기 계산
                size = selected_data[i] / max(selected_data) * 30 * input.marker_size()
                
                # 비율 계산
                percentage = selected_data[i] / sum(selected_data) * 100
                
                # 마커 색상 결정 (값에 따라)
                if selected_data[i] == max(selected_data):
                    color = 'darkred'
                elif selected_data[i] > sum(selected_data) / len(regions) * 2:
                    color = 'red'
                elif selected_data[i] > sum(selected_data) / len(regions):
                    color = 'orange'
                else:
                    color = 'blue'
                
                # 마커 생성
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
                
                # 라벨 추가 (선택 시)
                if input.show_labels():
                    folium.map.Marker(
                        region_coordinates[region],
                        icon=folium.DivIcon(
                            icon_size=(0, 0),
                            icon_anchor=(0, 0),
                            html=f'<div style="font-size: 10pt; font-weight: bold;">{region}</div>'
                        )
                    ).add_to(m)
            
        # 영천시에서 각 지역으로 선 그리기
        for i, region in enumerate(regions):
            if selected_data[i] > 0:
                # 선 두께 계산
                weight = selected_data[i] / max(selected_data) * 10
                if weight < 1:
                    weight = 1
                
                # 선 색상 결정
                if selected_data[i] == max(selected_data):
                    color = 'darkred'
                elif selected_data[i] > sum(selected_data) / len(regions) * 2:
                    color = 'red'
                elif selected_data[i] > sum(selected_data) / len(regions):
                    color = 'orange'
                else:
                    color = 'blue'
                
                # 영천시에서 각 지역으로 화살표 그리기
                folium.PolyLine(
                    locations=[region_coordinates[region], yeongcheon_coordinates],
                    color=color,
                    weight=weight,
                    opacity=0.6,
                    dash_array='5, 5',
                    tooltip=f"{region} → 영천시: {selected_data[i]}명"
                ).add_to(m)
        
        # 지도를 HTML로 변환
        map_html = m._repr_html_()
        
        # HTML을 UI 요소로 반환
        return ui.HTML(map_html)
    
    @render.ui
    def bar_chart():
        data_type = input.data_type()
        selected_data = migration_data[data_type]
        regions = migration_data["regions"]
        
        # 데이터 정렬 및 준비
        sorted_indices = sorted(range(len(selected_data)), key=lambda i: selected_data[i], reverse=True)
        sorted_regions = [regions[i] for i in sorted_indices]
        sorted_data = [selected_data[i] for i in sorted_indices]
        
        # 상위 10개 지역만 표시
        top_n = 10
        if len(sorted_data) > top_n:
            sorted_regions = sorted_regions[:top_n]
            sorted_data = sorted_data[:top_n]
        
        # 데이터프레임 생성
        df = pd.DataFrame({
            '지역': sorted_regions,
            '인원수': sorted_data
        })
        
        # Plotly Express로 차트 생성
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
            showlegend=False  # 범례 숨기기
        )
        
        fig.update_traces(
            texttemplate='%{text}명',
            textposition='outside'
        )
        
        # HTML로 변환하여 반환
        plot_html = fig.to_html(include_plotlyjs='cdn')
        return ui.HTML(plot_html)