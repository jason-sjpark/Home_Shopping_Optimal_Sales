# -*- coding: utf-8 -*-

import pandas as pd

train = pd.read_csv('train.csv', encoding='UTF-8')
print(train)

####################################################################
# 상품군 숫자형으로 변환 (가나다 순)
train['상품군'] = train['상품군'].map( {'가구': 0, '가전': 1, '건강기능': 2, '농수축': 3, '생활용품': 4, '속옷': 5, '의류': 6, '이미용': 7, '잡화': 8, '주방': 9, '침구': 10} ).astype(int)
print(train)

####################################################################
# 노출시간 범주형으로 변환
train['노출(분)'] = train['노출(분)'].fillna(0) # 결측치 0으로 채워주기
for i in range(train.shape[0]):
    if (train.iloc[i]['노출(분)'] <= 10):
        train.loc[i, '노출(분)'] = 10
    elif (train.iloc[i]['노출(분)'] <= 20):
        train.loc[i, '노출(분)'] = 20
    elif (train.iloc[i]['노출(분)'] <= 30):
        train.loc[i, '노출(분)'] = 30
    elif (train.iloc[i]['노출(분)'] > 30):
        train.loc[i, '노출(분)'] = 40
print(train)
# 위의 코드 문제 생기면
# train.loc[ train['노출(분)'] < 10, '노출(분)'] = 0
# train.loc[(train['노출(분)'] >= 10), '노출(분)'] = 1
# train.loc[(train['노출(분)'] >= 20), '노출(분)'] = 2
# train.loc[(train['노출(분)'] >= 30), '노출(분)'] = 3

####################################################################
# 판매단가 범주형으로 변환
train['판매단가'] = train['판매단가'].apply(lambda x: x.replace(',', '')) # 가격에 포함된 , 지우고
train['판매단가'] = pd.to_numeric(train['판매단가']) # int형으로 변환
for i in range(train.shape[0]):
    if (train.iloc[i]['판매단가'] <= 122000):
        train.loc[i, '판매단가'] = 0
    elif (train.iloc[i]['판매단가'] <= 280000):
        train.loc[i, '판매단가'] = 1
    elif (train.iloc[i]['판매단가'] <= 649000):
        train.loc[i, '판매단가'] = 2
    elif (train.iloc[i]['판매단가'] <= 1239000):
        train.loc[i, '판매단가'] = 3
    elif (train.iloc[i]['판매단가'] <= 1899000):
        train.loc[i, '판매단가'] = 4
    elif (train.iloc[i]['판매단가'] <= 2690000):
        train.loc[i, '판매단가'] = 5
    elif (train.iloc[i]['판매단가'] > 2690000):
        train.loc[i, '판매단가'] = 6
print(train)
# 위의 코드 문제 생기면
# train.loc[ train['판매단가'] < 122000, '판매단가'] = 0
# train.loc[(train['판매단가'] >= 122000), '판매단가'] = 1
# train.loc[(train['판매단가'] >= 280000), '판매단가'] = 2
# train.loc[(train['판매단가'] >= 649000), '판매단가'] = 3
# train.loc[(train['판매단가'] >= 1239000), '판매단가'] = 4
# train.loc[(train['판매단가'] >= 1899000), '판매단가'] = 5
# train.loc[(train['판매단가'] >= 2690000), '판매단가'] = 6

print("변환이 모두 완료되었습니다~~!")