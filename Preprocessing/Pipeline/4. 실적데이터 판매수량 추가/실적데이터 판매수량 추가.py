
import pandas as pd
import numpy as np

df= pd.read_csv(r'2-1. 실적데이터 무형 지우기.csv',thousands=',')

df["판매수량"]=np.ceil(df[" 취급액 "]/df["판매단가"]).astype(int)

df.to_csv('실적데이터 판매수량 추가.csv')




