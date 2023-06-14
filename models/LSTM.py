from math import sqrt
from numpy import concatenate
from matplotlib import pyplot, font_manager
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from matplotlib import rc

# 3. 한글폰트를 설정(한글을 사용한다면 반드시해야 함)
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
# 맥OS인 경우 위 두 줄을 입력하지 말고 아래 코드를 입력하세요
#rc('font', family='AppleGothic')
pyplot.rcParams['axes.unicode_minus'] = False


# convert series to supervised learning(=뒤에 있는값들은 초기값들) n_in은 input_Dim, n_out은 output_dim
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]  # n*m dataframe일때, m리턴함
    df = DataFrame(data)
    cols, names = list(), list()

    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)] #앞의 d에는 j+1들어가고, 뒤의 d에는 i들어감

    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]

    # put it all together
    agg = concat(cols, axis=1)
    print(agg)
    agg.columns = names
    print(agg)

    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True) #숫자 들어있는 것들만 남긴다! 와우
    return agg


# load dataset
dataset = read_csv('ex.csv', header=0, index_col=0, encoding='cp949')
dataset['sex'] = dataset['sex'].fillna(value = 0)
dataset['interest'] = dataset['interest'].fillna(value = 0)

values = dataset.values

# # integer encode direction(values의 4번째 줄 값 wnd_dir이 다 문자라서 정수와 매핑시켜 정수로 변환)
# encoder = LabelEncoder()
# values[:, 4] = encoder.fit_transform(values[:, 4])

# # X_test데이터에만 존재하는 새로 출현한 데이터를 신규 클래스로 추가한다 (중요!!!)
# for label in np.unique(X_test):
#     if label not in encoder.classes_: # unseen label 데이터인 경우( )
#         encoder.classes_ = np.append(encoder.classes_, label) # 미처리 시 ValueError발생
# X_test_encoded = encoder.transform(X_test)

# ensure all data is float
values = values.astype('float32')

# normalize features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values) #0~1사이에 맞춰서 values값을 바꿔줌

# specify the number of lag hours
n_hours = 144
n_features = 10

# frame as supervised learning(n_hours는 input_dim으로 학습할 시간(단위가 시간임), 1은 output_dim으로 pollution데이터만 할거라 1임)
reframed = series_to_supervised(scaled, n_hours, 1)
print(reframed.shape)

# split into train and test sets
values = reframed.values
n_train_hours = 22500 #1년치 데이터만 가져올거임(단위:시간)(원본데이터가 그렇게 돼있음)
train = values[:n_train_hours, :] #위에거 적용!
test = values[n_train_hours:, :]
# split into input and outputs
n_obs = n_hours * n_features
train_X, train_y = train[:, :n_obs], train[:, -n_features]
test_X, test_y = test[:, :n_obs], test[:, -n_features]
print(train_X.shape, len(train_X), train_y.shape)
# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], n_hours, n_features)) #3차원으로 reshape!(size, timestep,feature)
test_X = test_X.reshape((test_X.shape[0], n_hours, n_features)) #여기서train_X.shape[0]는 n_train_hours와 같음
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

# design network
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2]))) #shape[1]=n_hours, shape[2]=n_features, 50=epochs(몇번 반복할건지)
model.add(Dense(1)) #예측하고자 하는 target의 갯수가 1이라서
model.compile(loss='mae', optimizer='adam')         #loss, optimizer
# fit network
history = model.fit(train_X, train_y, epochs=100, batch_size=50, validation_data=(test_X, test_y), verbose=2,            #epochs수, batch_size, verbose 값
                    shuffle=False)
# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.xlabel('epoch')
pyplot.ylabel('loss')
pyplot.legend()
pyplot.show()

# make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], n_hours * n_features)) #다시 원래 모양으로 reshape해주기

# invert scaling for forecast
inv_yhat = concatenate((yhat, test_X[:, -9:]), axis=1) #trian_x로 학습해서 test_x의 추정치 y^을 구한거
inv_yhat = scaler.inverse_transform(inv_yhat) #정규화 해제
inv_yhat = inv_yhat[:, 0] #pollution값만(test_x의 값과 합친거임)

# invert scaling for actual
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, -9:]), axis=1) #test_x의 원래 test_y값
inv_y = scaler.inverse_transform(inv_y) #정규화 해제
inv_y = inv_y[:, 0] #pollution값만

# calculate RMSE
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)
pyplot.plot(inv_yhat, linestyle=':', label='추정치')
pyplot.plot(inv_y, linestyle=':', label='실제값')
pyplot.legend()
pyplot.show()

import numpy as np

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# calculate MAPE
mape = mean_absolute_percentage_error(inv_y, inv_yhat)
print('Test MAPE: %.3f' % mape)