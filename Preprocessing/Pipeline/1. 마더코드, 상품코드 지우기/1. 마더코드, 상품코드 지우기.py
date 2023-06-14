import pandas as pd

df= pd.read_csv('./원본/실적데이터.csv', encoding='UTF-8')

del df['마더코드']
del df['상품코드']

df.to_csv('./Preprocessing/1. 코드지우기.csv',encoding='UTF-8')