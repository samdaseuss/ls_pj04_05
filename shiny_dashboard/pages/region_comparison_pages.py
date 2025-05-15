# shiny_dashboard/pages/region_comparison_page.py
from shiny import ui, render, reactive
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from shiny_dashboard.data.region_comparison_data import get_data
from shiny_dashboard.styles.styles import get_custom_css


dummy_data = get_data()
custom_css = get_custom_css()


def region_comparison_ui():
    """지역 비교 페이지 UI 컴포넌트"""
    return ui.page_fluid(
        ui.head_content(
            ui.tags.style(custom_css)
        ),
        
        ui.div(
            {"class": "header-section"},
            ui.row(
                ui.column(12, 
                    ui.h1("경북 지역 귀농 혜택 비교", style="text-align: center; font-size: 36px;"),
                    ui.p("지역별 귀농 지원 정책 및 혜택을 비교하여 최적의 정착지를 선택하세요.", style="text-align: center; font-size: 18px;")
                )
            )
        ),
        
        ui.h2("지역별 종합 혜택 비교", class_="section-title"),
        
        # 지역별 카드 비교 (구독형 플랜 스타일)
        ui.row(
            ui.column(4,
                ui.div(
                    {"class": "region-card third-choice"},
                    ui.card(
                        ui.card_header("의성군", style="text-align: center; font-size: 24px;"),
                        ui.div(
                            {"class": "stats-box"},
                            ui.p("종합 평가 점수"),
                            ui.div({"class": "score-display"}, f"{dummy_data['policy_scores']['의성군']['종합평가']}/10")
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★"), "정착지원금: ", 
                            dummy_data['policies']['의성군']['정착지원금']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★"), "주택지원: ", 
                            dummy_data['policies']['의성군']['주택지원']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★"), "농지지원: ", 
                            dummy_data['policies']['의성군']['농지지원']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★"), "교육지원: ", 
                            dummy_data['policies']['의성군']['교육지원']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★"), "농기계지원: ", 
                            dummy_data['policies']['의성군']['농기계지원']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★"), "판로지원: ", 
                            dummy_data['policies']['의성군']['판로지원']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★"), "컨설팅: ", 
                            dummy_data['policies']['의성군']['컨설팅']
                        ),
                        ui.div(
                            {"class": "stats-box"},
                            f"성공 사례: {dummy_data['success_cases']['의성군']}건"
                        ),
                        style="background: transparent; border: none; color: inherit;"
                    )
                )
            ),
            
            # 영천시 카드 (최고 선택)
            ui.column(4,
                ui.div(
                    {"class": "region-card best-choice"},
                    ui.div({"class": "ribbon"}, "최고의 선택"),
                    ui.card(
                        ui.card_header("영천시", style="text-align: center; font-size: 28px; font-weight: bold;"),
                        ui.div(
                            {"class": "stats-box"},
                            ui.p("종합 평가 점수"),
                            ui.div({"class": "score-display"}, f"{dummy_data['policy_scores']['영천시']['종합평가']}/10"),
                            ui.p("경북 지역 최고 평가!")
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★★"), "정착지원금: ", 
                            ui.tags.strong(dummy_data['policies']['영천시']['정착지원금'])
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★★"), "주택지원: ", 
                            ui.tags.strong(dummy_data['policies']['영천시']['주택지원'])
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★★"), "농지지원: ", 
                            ui.tags.strong(dummy_data['policies']['영천시']['농지지원'])
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★★"), "교육지원: ", 
                            ui.tags.strong(dummy_data['policies']['영천시']['교육지원'])
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★★"), "농기계지원: ", 
                            ui.tags.strong(dummy_data['policies']['영천시']['농기계지원'])
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★★"), "추가혜택: ", 
                            ui.tags.strong(f"담당부서: {dummy_data['extra_info']['영천시']['담당부서']}")
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★★"), "농가계 혜택: ", 
                            ui.tags.strong(dummy_data['benefits']['영천시']['농가계 입대료'])
                        ),
                        ui.div(
                            {"class": "stats-box"},
                            f"성공 사례: ",
                            ui.tags.strong(f"{dummy_data['success_cases']['영천시']}건"),
                            ui.p("경북 지역 최다!")
                        ),
                        style="background: transparent; border: none; color: inherit;"
                    )
                )
            ),
            
            # 상주시 카드
            ui.column(4,
                ui.div(
                    {"class": "region-card second-choice"},
                    ui.card(
                        ui.card_header("상주시", style="text-align: center; font-size: 24px;"),
                        ui.div(
                            {"class": "stats-box"},
                            ui.p("종합 평가 점수"),
                            ui.div({"class": "score-display"}, f"{dummy_data['policy_scores']['상주시']['종합평가']}/10")
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★"), "정착지원금: ", 
                            dummy_data['policies']['상주시']['정착지원금']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★"), "주택지원: ", 
                            dummy_data['policies']['상주시']['주택지원']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★"), "농지지원: ", 
                            dummy_data['policies']['상주시']['농지지원']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★"), "교육지원: ", 
                            dummy_data['policies']['상주시']['교육지원']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★"), "농기계지원: ", 
                            dummy_data['policies']['상주시']['농기계지원']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★"), "판로지원: ", 
                            dummy_data['policies']['상주시']['판로지원']
                        ),
                        ui.div(
                            {"class": "feature-item"},
                            ui.tags.span({"class": "feature-star"}, "★★"), "컨설팅: ", 
                            dummy_data['policies']['상주시']['컨설팅']
                        ),
                        ui.div(
                            {"class": "stats-box"},
                            f"성공 사례: {dummy_data['success_cases']['상주시']}건"
                        ),
                        style="background: transparent; border: none; color: inherit;"
                    )
                )
            )
        ),
        
        ui.h2("영천시 귀농지원 대상 자격 요건", class_="section-title"),
        
        ui.row(
            ui.column(12,
                ui.div(
                    {"class": "chart-container"},
                    ui.h3("영천시 귀농정착 지원금 대상", style="color: #4CAF50; font-weight: bold;"),
                    ui.p(dummy_data['target_info']['영천시']['귀농정착 지원금'], style="line-height: 1.6;"),
                    ui.hr(),
                    ui.h3("영천시 귀농 농업창업 자금 융자 대상", style="color: #4CAF50; font-weight: bold;"),
                    ui.p(dummy_data['target_info']['영천시']['귀농 농업창업 자금 융자'], style="line-height: 1.6;"),
                    ui.hr(),
                    ui.h3("영천시 신규농업인 현장실습 교육 대상", style="color: #4CAF50; font-weight: bold;"),
                    ui.p(dummy_data['target_info']['영천시']['신규농업인 현장실습 교육'], style="line-height: 1.6;"),
                    ui.p(dummy_data['extra_info']['영천시']['연수생 교육'], style="font-style: italic; color: #666;")
                )
            )
        ),
        
        ui.h2("지원 정책 항목별 평가", class_="section-title"),

        # 지원 정책 레이더 차트 (Plotly 출력으로 변경)
        ui.row(
            ui.column(12,
                ui.div(
                    {"class": "chart-container"},
                    ui.output_ui("radar_chart")
                )
            )
        ),
        
        ui.h2("연간 귀농인 추이", class_="section-title"),
        
        # 연간 귀농인 추이 그래프
        ui.row(
            ui.column(12,
                ui.div(
                    {"class": "chart-container"},
                    ui.output_ui("yearly_trend")
                )
            )
        ),
        
        ui.h2("작물별 평균 소득 비교", class_="section-title"),
        
        # 작물별 소득 비교 그래프
        ui.row(
            ui.column(12,
                ui.div(
                    {"class": "chart-container"},
                    ui.output_ui("crop_income")
                )
            )
        ),
        
        # 바닥글
        ui.row(
            ui.column(12,
                ui.div(
                    ui.p("※ 본 데이터는 2024년 5월 기준으로 작성되었으며, 정확한 정보는 각 지자체 홈페이지를 참고하시기 바랍니다.", 
                         style="text-align: center; margin-top: 30px; color: #666;"),
                    ui.p(f"문의처: {dummy_data['extra_info']['영천시']['담당부서']}", 
                         style="text-align: center; margin-top: 10px; color: #666;"),
                    style="margin-top: 50px; padding: 20px; border-top: 1px solid #ddd;"
                )
            )
        )
    )

def region_comparison_server(input, output, session):
    """지역 비교 페이지 서버 로직"""
    
    # 지원 정책 레이더 차트 (Plotly로 변경)
    @render.ui
    def radar_chart():
        # 데이터 준비
        categories = list(dummy_data['policy_scores']['영천시'].keys())
        categories = [cat for cat in categories if cat != '종합평가']  # 종합평가 제외
        
        # 각 지역별 점수
        yeongcheon_scores = [dummy_data['policy_scores']['영천시'][cat] for cat in categories]
        uiseong_scores = [dummy_data['policy_scores']['의성군'][cat] for cat in categories]
        sangju_scores = [dummy_data['policy_scores']['상주시'][cat] for cat in categories]
        
        # 첫 번째 카테고리를 마지막에 다시 추가하여 닫힌 다각형 생성
        categories.append(categories[0])
        yeongcheon_scores.append(yeongcheon_scores[0])
        uiseong_scores.append(uiseong_scores[0])
        sangju_scores.append(sangju_scores[0])
        
        # Plotly 레이더 차트 생성
        fig = go.Figure()
        
        # 영천시 데이터 추가
        fig.add_trace(go.Scatterpolar(
            r=yeongcheon_scores,
            theta=categories,
            fill='toself',
            name='영천시',
            line=dict(color='#4CAF50', width=3),
            fillcolor='rgba(76, 175, 80, 0.3)'
        ))
        
        # 의성군 데이터 추가
        fig.add_trace(go.Scatterpolar(
            r=uiseong_scores,
            theta=categories,
            fill='toself',
            name='의성군',
            line=dict(color='#9C27B0', width=2),
            fillcolor='rgba(156, 39, 176, 0.1)'
        ))
        
        # 상주시 데이터 추가
        fig.add_trace(go.Scatterpolar(
            r=sangju_scores,
            theta=categories,
            fill='toself',
            name='상주시',
            line=dict(color='#2196F3', width=2),
            fillcolor='rgba(33, 150, 243, 0.1)'
        ))
        
        # 레이아웃 설정
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5
            ),
            title=dict(
                text='지역별 지원 정책 평가 점수',
                font=dict(size=18)
            ),
            height=600,
            margin=dict(t=100)
        )
        
        # Plotly 그래프를 HTML로 변환하여 UI 요소로 반환
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))
    
    # 연간 귀농인 추이 그래프 - Plotly로 개선
    @render.ui
    def yearly_trend():
        # 데이터 준비
        years = dummy_data['yearly_migrants']['연도']
        yeongcheon = dummy_data['yearly_migrants']['영천시']
        uiseong = dummy_data['yearly_migrants']['의성군']
        sangju = dummy_data['yearly_migrants']['상주시']
        
        # Plotly 그래프 생성
        fig = go.Figure()
        
        # 영천시 데이터 추가
        fig.add_trace(go.Scatter(
            x=years,
            y=yeongcheon,
            mode='lines+markers+text',
            name='영천시',
            line=dict(color='#4CAF50', width=3),
            marker=dict(size=10),
            text=yeongcheon,
            textposition='top center',
            textfont=dict(color='#4CAF50', size=14, family='Arial Bold')
        ))
        
        # 의성군 데이터 추가
        fig.add_trace(go.Scatter(
            x=years,
            y=uiseong,
            mode='lines+markers+text',
            name='의성군',
            line=dict(color='#9C27B0', width=2),
            marker=dict(symbol='square', size=8),
            text=uiseong,
            textposition='top center',
            textfont=dict(color='#9C27B0', size=12)
        ))
        
        # 상주시 데이터 추가
        fig.add_trace(go.Scatter(
            x=years,
            y=sangju,
            mode='lines+markers+text',
            name='상주시',
            line=dict(color='#2196F3', width=2),
            marker=dict(symbol='triangle-up', size=8),
            text=sangju,
            textposition='top center',
            textfont=dict(color='#2196F3', size=12)
        ))
        
        # 레이아웃 설정
        fig.update_layout(
            title='연도별 귀농인 추이 (2020-2024)',
            xaxis_title='연도',
            yaxis_title='귀농인 수 (명)',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5
            ),
            height=500,
            template='plotly_white',
            xaxis=dict(
                tickmode='array',
                tickvals=years
            )
        )
        
        # Plotly 그래프를 HTML로 변환하여 UI 요소로 반환
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))
    
    # 작물별 소득 비교 그래프 - 이미 Plotly 사용 중이므로 유지하되 HTML로 변환
    @render.ui
    def crop_income():
        # 데이터 프레임 생성
        df = pd.DataFrame({
            '작물': dummy_data['crop_income']['작물'],
            '영천시': dummy_data['crop_income']['영천시'],
            '의성군': dummy_data['crop_income']['의성군'],
            '상주시': dummy_data['crop_income']['상주시']
        })
        
        # 데이터 재구성 (롱 포맷)
        df_long = pd.melt(df, id_vars=['작물'], value_vars=['영천시', '의성군', '상주시'],
                          var_name='지역', value_name='소득(만원/년)')
        
        # Plotly Express 그래프 생성
        fig = px.bar(df_long, x='작물', y='소득(만원/년)', color='지역', barmode='group',
                     color_discrete_map={'영천시': '#4CAF50', '의성군': '#9C27B0', '상주시': '#2196F3'},
                     title='작물별 평균 연간 소득 비교 (만원)')
        
        fig.update_layout(
            xaxis_title='작물',
            yaxis_title='연평균 소득 (만원)',
            legend_title='지역',
            font=dict(size=12),
            height=500
        )
        
        # y축에 그리드 추가
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        
        # Plotly 그래프를 HTML로 변환하여 UI 요소로 반환
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))