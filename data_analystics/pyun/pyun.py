import pandas as pd
import plotly.express as px

# 1. CSV 읽기 (헤더 없이 읽고 첫 행을 컬럼명으로 지정)
df_raw = pd.read_csv('시도별_전거주지별_귀농가구원.csv', encoding='euc-kr', header=None)
df_raw.columns = df_raw.iloc[0]
df_raw = df_raw.drop(0).reset_index(drop=True)

# 2. 귀농인수(명) 데이터만 추출
df = df_raw[df_raw['항목'] == '귀농인수 (명)'].copy()

# 3. '이동후 시도별' → '이동후지역'으로 이름 변경
df = df.rename(columns={'이동후 시도별': '이동후지역'})

# 4. 연도/월 데이터 칼럼만 선택
cols = df.columns.tolist()
date_cols = [c for c in cols if c not in ['이동후지역', '항목']]

# 5. wide → long 변환
df_long = df.melt(id_vars=['이동후지역', '항목'], value_vars=date_cols, 
                  var_name='연월', value_name='값')

# 6. 결측값(X) 처리 후 숫자형으로 변환
df_long['값'] = df_long['값'].replace('X', 0).astype(int)

# 7. 연월 → 년도/월 분리
df_long['년도'] = df_long['연월'].str.extract(r'(\d{4})').astype(int)
df_long['월'] = df_long['연월'].str.extract(r'\.(\d+)')[0].fillna(0).astype(int)

# 8. 경상북도로 귀농한 데이터만 추출
df_경북 = df_long[df_long['이동후지역'] == '경상북도']

# 9. 연도별 귀농 인구 합계
df_경북_연도별 = df_경북.groupby('년도')['값'].sum().reset_index()

# Plotly 시각화
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

fig.show()

df_전남 = df_long[df_long['이동후지역'] == '전라남도']

df_전남_연도별 = df_전남.groupby('년도')['값'].sum().reset_index()

# Plotly 시각화
fig = px.bar(
    df_전남_연도별,
    x='년도',
    y='값',
    text='값',
    labels={'값': '귀농 인구 수 (명)', '년도': '연도'},
    title='연도별 전라남도 귀농 인구 수',
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

fig.show()



df_충남 = df_long[df_long['이동후지역'] == '충청남도']

df_충남_연도별 = df_충남.groupby('년도')['값'].sum().reset_index()

# Plotly 시각화
fig = px.bar(
    df_충남_연도별,
    x='년도',
    y='값',
    text='값',
    labels={'값': '귀농 인구 수 (명)', '년도': '연도'},
    title='연도별 충청남도 귀농 인구 수',
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

fig.show()




##################################################


import pandas as pd
import plotly.express as px

# 1. CSV 읽기 (멀티헤더 2줄)
df2 = pd.read_csv("영천환경체감도_2023.csv", encoding='euc-kr', header=[0,1])

# 2. '전체' 행만 필터링 (특성별(1) 컬럼이 '전체'인 행)
df2 = df2[df2[('특성별(1)', '특성별(1)')] == '전체']

# 3. 인덱스 설정 후 stack해서 긴형식으로 변환
df2_long = df2.set_index([('특성별(1)', '특성별(1)'), ('특성별(2)', '특성별(2)')])\
    .stack(level=[0,1])\
    .reset_index()

df2_long.head()

# 4. 컬럼명 간단하게 바꾸기
df2_long.columns = ['특성', '값', '년도', '평가', '결과']

df2_long

# 환경항목 컬럼에서 괄호 앞까지 텍스트만 추출 (ex: "대기", "수질", "토양", "소음 진동" 등)
df2_long['구분'] = df2_long['평가'].str.extract(r'^(대기|수질|토양|소음\s?진동|녹지환경)')


df_a = df2_long[df2_long['구분'] == '대기'].reset_index()
df_b = df2_long[df2_long['구분'] == '수질'].reset_index()
df_c = df2_long[df2_long['구분'] == '토양'].reset_index()
df_d = df2_long[df2_long['구분'] == '소음 진동'].reset_index()
df_e = df2_long[df2_long['구분'] == '녹지환경'].reset_index()

df_a = df_a.drop(5)
df_b = df_b.drop(5)
df_c = df_c.drop(5)
df_d = df_d.drop(5)
df_e = df_e.drop(5)

df_a['결과'] = pd.to_numeric(df_a['결과'], errors='coerce')
df_b['결과'] = pd.to_numeric(df_b['결과'], errors='coerce')
df_c['결과'] = pd.to_numeric(df_c['결과'], errors='coerce')
df_d['결과'] = pd.to_numeric(df_d['결과'], errors='coerce')
df_e['결과'] = pd.to_numeric(df_e['결과'], errors='coerce')


# 평가 순서 번호 추출 (없으면 0으로)
df_a['평가순번'] = df_a['평가'].str.extract(r'\.(\d+)').fillna(0).astype(int)

# 순번 기준으로 이름 매핑
평가이름 = {
    0: '매우 나쁨',
    1: '약간 나쁨',
    2: '보통',
    3: '약간 좋음',
    4: '매우 좋음'
}

df_a['간단평가'] = df_a['평가순번'].map(평가이름)

# ----------------------------

# 평가 순서 번호 추출 (없으면 0으로)
df_b['평가순번'] = df_b['평가'].str.extract(r'\.(\d+)').fillna(0).astype(int)

# 순번 기준으로 이름 매핑
평가이름 = {
    0: '매우 나쁨',
    1: '약간 나쁨',
    2: '보통',
    3: '약간 좋음',
    4: '매우 좋음'
}

df_b['간단평가'] = df_b['평가순번'].map(평가이름)

# ----------------------------

# 평가 순서 번호 추출 (없으면 0으로)
df_c['평가순번'] = df_c['평가'].str.extract(r'\.(\d+)').fillna(0).astype(int)

# 순번 기준으로 이름 매핑
평가이름 = {
    0: '매우 나쁨',
    1: '약간 나쁨',
    2: '보통',
    3: '약간 좋음',
    4: '매우 좋음'
}

df_c['간단평가'] = df_c['평가순번'].map(평가이름)

# ----------------------------

# 평가 순서 번호 추출 (없으면 0으로)
df_d['평가순번'] = df_d['평가'].str.extract(r'\.(\d+)').fillna(0).astype(int)

# 순번 기준으로 이름 매핑
평가이름 = {
    0: '매우 나쁨',
    1: '약간 나쁨',
    2: '보통',
    3: '약간 좋음',
    4: '매우 좋음'
}

df_d['간단평가'] = df_d['평가순번'].map(평가이름)

# ----------------------------

# 평가 순서 번호 추출 (없으면 0으로)
df_e['평가순번'] = df_e['평가'].str.extract(r'\.(\d+)').fillna(0).astype(int)

# 순번 기준으로 이름 매핑
평가이름 = {
    0: '매우 나쁨',
    1: '약간 나쁨',
    2: '보통',
    3: '약간 좋음',
    4: '매우 좋음'
}

df_e['간단평가'] = df_e['평가순번'].map(평가이름)


import plotly.express as px

# 예: df_a에 '결과' 컬럼이 숫자형이라고 가정
fig = px.bar(
    df_a,
    x='간단평가',
    y='결과',
    text='결과',
    labels={'결과': '응답 비율 (%)', '간단평가': '평가'},
    title='대기 항목에 대한 환경 체감도',
    color='결과',  # '값'처럼 숫자형 컬럼 사용
    color_continuous_scale='Greens'  # 그라데이션 색상맵
)

fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')  # 텍스트 포맷팅
fig.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    yaxis=dict(title='응답 비율 (%)'),
    xaxis=dict(categoryorder='array', categoryarray=['매우 나쁨', '약간 나쁨', '보통', '약간 좋음', '매우 좋음']),
    plot_bgcolor='white',
    coloraxis_colorbar=dict(title='응답 비율')
)

fig.show()


fig = px.bar(
    df_b, 
    x='간단평가', 
    y='결과', 
    title='수질 항목에 대한 환경 체감도',
    labels={'결과': '응답 비율 (%)', '간단평가': '평가'},
    text='결과',
    color='결과',
    color_continuous_scale='Greens'
)

fig.show()

fig = px.bar(
    df_c, 
    x='간단평가', 
    y='결과', 
    title='토양 항목에 대한 환경 체감도',
    labels={'결과': '응답 비율 (%)', '간단평가': '평가'},
    text='결과',
    color='결과',
    color_continuous_scale='Greens'
)

fig.show()

fig = px.bar(
    df_d, 
    x='간단평가', 
    y='결과', 
    title='소음 진동 항목에 대한 환경 체감도',
    labels={'결과': '응답 비율 (%)', '간단평가': '평가'},
    text='결과',
    color='결과',
    color_continuous_scale='Greens'
)

fig.show()

fig = px.bar(
    df_e, 
    x='간단평가', 
    y='결과', 
    title='녹지환경 항목에 대한 환경 체감도',
    labels={'결과': '응답 비율 (%)', '간단평가': '평가'},
    text='결과',
    color='결과',
    color_continuous_scale='Greens'
)

fig.show()

##############################3
#############################################3

import plotly.express as px

# df_all에 필요한 컬럼만 남기기 (예: '간단평가', '결과', '구분')
df_all = pd.concat([df_a, df_b, df_c, df_d, df_e], ignore_index=True)

fig = px.line(
    df_all,
    x='간단평가',
    y='결과',
    color='구분',
    markers=True,
    title='환경 항목별 체감도 비교 (선 그래프)',
    labels={'간단평가': '평가', '결과': '응답 비율 (%)'}
)

fig.update_layout(
    xaxis=dict(categoryorder='array', categoryarray=['매우 나쁨', '약간 나쁨', '보통', '약간 좋음', '매우 좋음']),
    plot_bgcolor='white'
)

fig.show()
