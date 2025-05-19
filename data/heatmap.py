import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 1. 데이터 불러오기
df = pd.read_csv("C:/Users/USER/Desktop/lsbigdata-gen4/data_zip/ames.csv")

# 2. 변수 리스트 정의
cond_cols = ["BsmtCond", "ExterCond", "GarageCond"]

# 3. 등급 매핑
cond_map = {"Ex": 1, "Gd": 2, "TA": 3, "Fa": 4, "Po": 5}

# 4. Cond 관련 변수: 수치 매핑 후 dropna()
for col in cond_cols:
    df[col + "_num"] = df[col].map(cond_map)

cond_corr_cols = [col + "_num" for col in cond_cols] + ["OverallCond"]
cond_corr_df = df[cond_corr_cols].dropna()
cond_corr = cond_corr_df.corr()

# 5. 시각화: OverallCond 히트맵
plt.figure(figsize=(6, 5))
sns.heatmap(cond_corr, annot=True, cmap="coolwarm", fmt=".2f", square=True)
plt.title("Correlation: OverallCond & Related Variables")
plt.tight_layout()
plt.show()





