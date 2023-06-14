import pandas as pd

from datetime import datetime

ts_day_idx = pd.date_range('00:00:00','23:50:00',freq='10T')
series_ts = pd.DataFrame(ts_day_idx, index=range(len(ts_day_idx)))
series_ts.columns = ['시각']
series_ts['시각인덱스'] = series_ts.index
series_ts['시각'] = series_ts['시각'].dt.strftime("%H:%M:%S")

train = pd.read_csv('13_1. 최종train.csv', header=0,encoding='cp949')
train = train.drop(['Unnamed: 0'],axis=1).copy()
train=train.set_index('방송일시')
train.index = pd.to_datetime(train.index)
train['시각'] = train.index.strftime("%H:%M:%S")
# print(train)

total=pd.merge(train,series_ts,on='시각',how='left')
print(total)