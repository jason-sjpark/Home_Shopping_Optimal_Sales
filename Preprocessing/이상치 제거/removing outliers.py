# -*- coding: utf-8 -*-

import pandas as pd

# 3시그마 이용하기 (정규분포라는 가정하에 가능)
def removeOutliers_std(df, column):
    std_price_mean = df[column].mean()
    std_price_std = df[column].std()
    print(std_price_mean)
    print(std_price_std)

    # outliers 확인하기
    std_df_outlier = df[
        (df[column] < std_price_mean - 3 * std_price_std) | (df[column] > std_price_mean + 3 * std_price_std)]
    print("[std_df_outlier]")
    print(std_df_outlier)

    # outliers 확인하기
    std_df_no_outlier = df[
        (df[column] > std_price_mean - 3 * std_price_std) & (df[column] < std_price_mean + 3 * std_price_std)]
    print("[std_df_no_outlier]")
    print(std_df_no_outlier)

    # outliers 지우기
    df = df.drop(std_df_outlier.index, axis=0)

    # 최종확인
    print(df)


# IQR 이용하기 (3시그마보다 더 빡센 기준)
def removeOutliers_IQR(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    IQR_lower_limit = Q1 - 1.5 * IQR
    IQR_upper_limit = Q3 + 1.5 * IQR

    # outliers 확인하기
    IQR_df_outlier = df[(df[column] < IQR_lower_limit) | (df[column] > IQR_upper_limit)]
    print("[IQR_df_outlier]")
    print(IQR_df_outlier)

    # outliers 아닌 것 확인하기
    IQR_df_no_outlier = df[(df[column] > IQR_lower_limit) & (df[column] < IQR_upper_limit)]
    print("[IQR_df_no_outlier]")
    print(IQR_df_no_outlier)

    # outliers 지우기
    df = df.drop(IQR_df_outlier.index, axis=0)

    # 최종확인
    print(df)


# 실적데이터 df으로 불러오기
df = pd.read_csv('실적데이터.csv', encoding='cp949')
column = '판매단가'

# string으로 되어있는 금액
df[column] = df[column].apply(lambda x: x.replace(',', ''))  # 금액에 포함된 , 지우고
df[column] = df[column].astype(float) # float 타입으로 변환

# 3시그마 결과확인
removeOutliers_std(df, column)

# IQR 결과확인
removeOutliers_IQR(df, column)



