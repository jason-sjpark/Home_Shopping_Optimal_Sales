import csv

import pandas as pd
# import matplotlib
# from matplotlib import pyplot as plt
# from matplotlib import font_manager
# from matplotlib import rc

# # 3. 한글폰트를 설정(한글을 사용한다면 반드시해야 함)
# font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
# rc('font', family=font_name)
# # 맥OS인 경우 위 두 줄을 입력하지 말고 아래 코드를 입력하세요
# #rc('font', family='AppleGothic')
# plt.rcParams['axes.unicode_minus'] = False


# 컬럼 정리
raw_rating = pd.read_csv("시청률.csv", encoding='cp949')
raw_rating.columns=raw_rating.loc[0]
rating_data = raw_rating.drop(0).copy()

# 맨 마지막줄 잘라내기
row_tail=rating_data.tail(1)
rating_data = rating_data.drop(rating_data.tail(1).index)


#
#'시간대'행을 datetime으로 바꿔주기
rating_data=rating_data.set_index('시간대')
rating_data.index=pd.to_datetime(rating_data.index)


# 다 숫자로 바꿔주기
rating_data = rating_data.apply(pd.to_numeric)
#

#'시간대'행 20분 단위로 그루핑 해주기
grouped_data=rating_data.resample('20min').sum()

# 인덱스 해제해주기
grouped_data=grouped_data.reset_index()
grouped_data['시간대']=grouped_data['시간대'].dt.time


#위에서 잘라놓은 맨 마지막줄 붙여주기
data=grouped_data.append(row_tail,ignore_index=True)
print(data)

#csv로 내보내기
data.to_csv('시청률 묶기.csv',encoding='ms949')




