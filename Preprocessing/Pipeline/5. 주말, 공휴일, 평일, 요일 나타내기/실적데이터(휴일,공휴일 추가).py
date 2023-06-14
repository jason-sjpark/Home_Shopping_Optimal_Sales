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
raw_sold = pd.read_csv("실적데이터.csv", encoding='cp949')
raw_sold.columns=raw_sold.loc[0]
sold_data=raw_sold.drop(0).copy()


# 인덱스 정렬
col = []
for num, temp in enumerate(sold_data['노출(분)']):
    if pd.isna(temp) :
        col.append(col[num-1])
    else :
        col.append(temp)
sold_data['노출(분)']=col

# 무형의 것들은 제거
sold_data=sold_data.dropna()

# 요일 붙여주기
sold_data['방송일시']=pd.to_datetime(sold_data['방송일시'])
sold_data['요일']=sold_data['방송일시'].dt.day_name()

# 요일 바탕으로 휴일 붙여주기
sold_data['휴일'] = ["Yes" if (s=='Saturday')|(s=='Sunday') else "No" for s in sold_data['요일']]
# print(sold_data['방송일시'])

# 공휴일 붙여주기
holidays = ['2019-01-01','2019-02-04','2019-02-05','2019-02-06','2019-03-01','2019-05-06','2019-05-12','2019-06-06','2019-08-15','2019-09-12','2019-09-13','2019-09-14','2019-10-03','2019-10-09','2019-12-25','2020-01-01']
# print(holidays)

#비교 위해 방송일시 date만 남겨서 문자열로 바꾸기
date=sold_data['방송일시'].dt.strftime("%Y-%m-%d")

#holidays랑 비교해서 공휴일 인지 아닌지 리스트로 내보내기
is_hol=[]
for i in date:
    if i in holidays:
        is_hol.append('Yes')
    else:
        is_hol.append('No')

#is_hol을 sold_data에 붙여주기
sold_data['공휴일']=is_hol
print(sold_data)

#csv로 내보내기
sold_data.to_csv('실적데이터(휴일,공휴일 추가).csv',encoding='ms949')

