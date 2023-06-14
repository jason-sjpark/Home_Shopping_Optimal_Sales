import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv("./원본/실적데이터.csv", sep=",", encoding='cp949')
train, test = train_test_split(df, test_size=0.4)
