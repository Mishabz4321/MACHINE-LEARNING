
import numpy as np
from datetime import datetime
import smtplib
from selenium import webdriver
import os

#For Prediction
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn.model_selection import cross_validate
#For Stock Data
from iexfinance.stocks import get_historical_data
from iexfinance import stocks
#getting stocks
# n--->no.of stocks we want to retrieve
def getStocks(n):
    # Navigating to the Yahoo stock screener
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    url = 'https://finance.yahoo.com/screener/predefined/aggressive_small_caps?offset=0&count=202'
    driver.get(url)
    # Creating a stock list and iterating through the ticker names on the stock screener list
    stock_list= []
    n += 1
    for i in range(1,n):
         ticker= driver.find_element_by_xpath(
             '//*[@id = "scr-res-table"]/div[1]/table/tbody/tr[' + str(i) + ']/td[1]/a')
    stock_list.append(ticker.text)
    driver.quit()
    # Using the stock list to predict the future price of the stock a specificed amount of days
    number = 0
    for i in stock_list:
        print("Number: " + str(number))
        try:
            predictData(i, 5)
        except:
            print("Stock: " + i + " was not predicted")
        number += 1

def predictData(stock, days):
    print(stock)

    start = datetime(2017, 1, 1)
    end = datetime.now()

    #Outputting the Historical data into a .csv for later use
    df = get_historical_data(stock, start=start, end=end, output_format='pandas')
    if os.path.exists('./Exports'):
        csv_name = ('Exports/' + stock + '_Export.csv')
    else:
        os.mkdir("Exports")
        csv_name = ('Exports/' + stock + '_Export.csv')
    df.to_csv(csv_name)
    df['prediction'] = df['close'].shift(-1)
    df.dropna(inplace=True)

    forecast_time = int(days)

    #Predicting the Stock price in the future
    X = np.array(df.drop(['prediction'], 1))
    Y = np.array(df['prediction'])
    X = preprocessing.scale(X)
    X_prediction = X[-forecast_time:]
    X_train, Y_train, Y_test = cross_validate.train_test_split(
        X, Y, test_size=0.5)

    #Performing the Regression on the training data
    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    prediction = (clf.predict(X_prediction))

    last_row = df.tail(1)
    print(last_row['close'])
if __name__ == '__main__':
    getStocks(100)