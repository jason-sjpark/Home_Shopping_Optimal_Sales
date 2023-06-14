# -*- coding: utf-8 -*-

import pandas as pd

# 실적데이터 train으로 불러오기
train = pd.read_csv('실적데이터.csv', encoding='cp949')
# 소비자물가지수 CPI로 불러오기
CPI = pd.read_csv('월별_소비자물가지수.csv', encoding='cp949')

# 잘 불러와졌는지 확인 ><
print(train)
print(CPI)

# train의 방송일시 컬럼 자료형 날짜형으로 변환
train['방송일시'] = pd.to_datetime(train['방송일시'], format='%Y-%m-%d %H:%M:%S', errors='raise')

# train에 소비자물가지수 컬럼 추가 (기본값 0.0, double형)
train['소비자물가지수'] = 0.0

# 방송일시의 월에 맞는 소비자물가지수 넣어주기
for i in range(train.shape[0]):
    for j in range(1, 13):
        if (train.iloc[i]['방송일시'].month == j):
            train.loc[i, '소비자물가지수'] = CPI['소비자물가지수'][j-1]
            break

# 잘 들어갔는지 확인
print(train)