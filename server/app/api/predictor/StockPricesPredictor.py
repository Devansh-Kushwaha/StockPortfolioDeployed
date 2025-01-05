import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import datetime as dt
from keras.models import load_model

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

def model_predictor(company='META', start='2012-01-01', end='2020-01-01', prediction_days=60):
    
    # with open('api/predictor/temp.txt','a') as file:
    #     file.write(f'Company: {company}\n')
    # return

    data = yf.download(company, start=start, end=end)

    scaler=MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

    prediction_days=60

    x_train=[]
    y_train=[]

    for x in range (prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x,0])
        
    x_train, y_train= np.array(x_train), np.array(y_train)
    x_train=np.reshape(x_train, (x_train.shape[0], x_train.shape[1],1))


    model=Sequential()

    model.add(LSTM( units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(Dropout(0.2))

    model.add(LSTM( units=50, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM( units=50))
    model.add(Dropout(0.2))

    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train,y_train, epochs=25, batch_size=32)
    
    model.save(f'api/predictor/${company}_prediction.h5')

    # '''Testing the model'''

    # test_start=dt.datetime(2020,1,1)
    # test_end=dt.datetime.now()
    # test_data = yf.download(company, start=test_start, end=test_end)
    # actual_prices=test_data['Close'].values

    # total_dataset = pd.concat((data['Close'], test_data['Close']))

    # model_inputs = total_dataset[len(total_dataset)-len(test_data)-prediction_days:].values
    # model_inputs=model_inputs.reshape(-1,1)
    # model_inputs=scaler.transform(model_inputs)

    # x_test=[]
    # for x in range(prediction_days, len(model_inputs)):
    #     x_test.append(model_inputs[x-prediction_days:x, 0])

    # x_test=np.array(x_test)
    # x_test=np.reshape (x_test, (x_test.shape[0], x_test.shape[1],1))

    # predicted_prices = model.predict(x_test)
    # predicted_prices=scaler.inverse_transform(predicted_prices)

    # plt.plot(actual_prices, color="blue", label="Actual Price")
    # plt.plot(predicted_prices, color="red", label="Predicted Price")

    # plt.xlabel('Time')
    # plt.ylabel('Price')
    # plt.legend()
    # plt.show()
    
def predict_stock_price(company, prediction_days=60):
    try:
        model = load_model(f'api/predictor/${company}_prediction.h5')
        
        end = dt.datetime.now()
        start = end - dt.timedelta(days=prediction_days + 50)
        data = yf.download(company, start=start, end=end)

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
    
    
    
        model_inputs = scaled_data[len(scaled_data)-60:].reshape(1, prediction_days, 1)

        
        predicted_prices = model.predict(model_inputs)
        predicted_price = scaler.inverse_transform(predicted_prices)
        print(predicted_price[0][0])
        return predicted_price[0][0]
    except:
        # model_predictor(company)
        # return predict_stock_price(company, prediction_days=60)
        return None