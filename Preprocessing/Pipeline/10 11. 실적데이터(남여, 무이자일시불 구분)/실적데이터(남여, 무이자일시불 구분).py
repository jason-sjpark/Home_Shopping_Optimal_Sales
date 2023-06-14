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
raw_sold = pd.read_csv("실적데이터(휴일,공휴일 추가).csv", encoding='cp949')
sold_data=raw_sold.drop(['Unnamed: 0'],axis=1).copy()
# print(sold_data['상품명'])

# 의류군만 남여 붙여주기 (남자=0, 여자=1)
sold_data.loc[(sold_data['상품명'].str.contains('남성'))&(sold_data['상품군']=='의류'), "남여"] = 0
sold_data.loc[(sold_data['상품명'].str.contains('여성'))&(sold_data['상품군']=='의류'), "남여"] = 1
# sold_data.fillna("NaN")
# print(sold_data)

# 무이자/일시불 붙여주기 (무이자=0, 일시불=1)
sold_data.loc[sold_data['상품명'].str.contains('무이자'), "무이자/일시불"] = 0
sold_data.loc[sold_data['상품명'].str.contains('일시불'), "무이자/일시불"] = 1
#csv로 내보내기
sold_data.to_csv('실적데이터(남여, 무이자일시불 구분).csv',encoding='ms949')