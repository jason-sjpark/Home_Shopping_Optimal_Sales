# -*- coding: utf-8 -*-

import pandas as pd

# 실적데이터 train으로 불러오기
train = pd.read_csv('실적데이터.csv', encoding='cp949')
# 기상데이터 weather으로 불러오기
weather = pd.read_csv('일별_기상데이터.csv', encoding='cp949')

# 잘 불러와졌는지 확인 ><
print(train)
print(weather)

# train의 방송일시 컬럼 자료형 날짜형으로 변환
train['방송일시'] = pd.to_datetime(train['방송일시'], format='%Y-%m-%d %H:%M:%S', errors='raise')
# weather의 날짜 컬럼 자료형 날짜형으로 변환
weather['날짜'] = pd.to_datetime(weather['날짜'], format='%Y-%m-%d %H:%M:%S', errors='raise')

# train에 평균기온, 강수량 컬럼 추가 (기본값 0.0, double형)
train['최저기온'] = 0.0
train['최고기온'] = 0.0
train['평균기온'] = 0.0
train['강수량'] = 0.0
train['미세먼지농도'] = 0.0

# 방송일시의 일에 맞는 기상데이터 넣어주기
for i in range(train.shape[0]):
    for j in range(weather.shape[0]):
        if (train.iloc[i]['방송일시'].date() == weather.iloc[j]['날짜'].date()):
            train.loc[i, '최저기온'] = weather.loc[j, '최저기온']
            train.loc[i, '최고기온'] = weather.loc[j, '최고기온']
            train.loc[i, '평균기온'] = weather.loc[j, '평균기온']
            train.loc[i, '강수량'] = weather.loc[j, '강수량']
            train.loc[i, '미세먼지농도'] = weather.loc[j, '미세먼지농도']
            break

# 잘 들어갔는지 확인
print(train)