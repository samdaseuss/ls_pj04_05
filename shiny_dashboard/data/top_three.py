# shiny_dashboard/data/top_three.py
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import os


current_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(current_dir, "raw", "경상북도_귀농 및 귀촌 가구원 수 현황_20231231.csv")
regions = ['영천', '의성', '상주']

df = pd.read_csv(file_path, encoding="cp949")

years = []
region_data = {region: [] for region in regions}

for column in df.columns:
    # 귀농 가구원 수 컬럼만 찾기
    if "귀농 가구원 수" in column:
        # 연도 추출
        year_match = re.search(r'(\d{4})년', column)
        if year_match:
            year = year_match.group(1)
            years.append(year)
            
            # 각 지역별 데이터 추출
            for region in regions:
                # 지역명과 일치하는 행 찾기
                region_row = df[df['구분'] == region]
                if not region_row.empty:
                    # 해당 연도의 귀농 가구원 수 추출
                    region_data[region].append(region_row[column].values[0])


for region in regions:
    print(f"{region} 귀농 가구원 수:", region_data[region])


# ===== 그래프 그래기 ======
fig = go.Figure()

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

for i, region in enumerate(regions):
    fig.add_trace(
        go.Scatter(
            x=years, 
            y=region_data[region],
            mode='lines+markers',
            name=f'{region}',
            line=dict(color=colors[i], width=2),
            marker=dict(size=8)
        )
    )


fig.update_layout(
    title='경상북도 주요 지역별 귀농 가구원 수 추이 (2013-2023)',
    xaxis_title='연도',
    yaxis_title='귀농 가구원 수',
    legend_title='지역',
    template='plotly_white',
    height=600,
    width=1000,
    hovermode='x unified'
)


fig.update_xaxes(
    tickvals=years,
    ticktext=years
)

output_path = os.path.join(current_dir, "top_three_farming_population.html")

try:
    fig.write_html(output_path)
    print(f"\n그래프가 {output_path}에 저장되었습니다.")
except Exception as e:
    print(f"파일 저장 중 오류 발생: {e}")
    # 디렉토리 확인
    print(f"현재 디렉토리: {current_dir}")
    print(f"디렉토리 쓰기 권한: {os.access(current_dir, os.W_OK)}")


fig.show()