# Dependencies
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
from pymongo import MongoClient
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
from imblearn.over_sampling import RandomOverSampler
le = LabelEncoder()
scaler = StandardScaler()

def mongo_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.stock_prediction
    collection = db.prediction
    document = collection.find_one()
    ticker = document['ticker']
    return ticker

def download_data():
    ticker = yf.Ticker(mongo_connection())
    data = ticker.history(period='2y')
    data = pd.DataFrame(data)
    data = data[:-1]
    data['Day Result'] = np.where(data['Close'] > data['Open'], 1, 0)
    data.drop(['Volume', 'Close', 'Dividends', 'Stock Splits'], axis=1, inplace=True)    
    return data

def preprocessing():
    data = download_data()
    # Encode the data
    data['Open'] = le.fit_transform(data['Open'])
    data['High'] = le.fit_transform(data['High'])
    data['Low'] = le.fit_transform(data['Low'])
    # Split data into training and testing sets
    X = data.drop(['Day Result'], axis=1)
    y = data['Day Result'].values
    # Build the logistic regression model
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    # Scale and normalize the data
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit_transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test

def Naive_Random_Oversampling(test):
    X_train_scaled, X_test_scaled, y_train, y_test = preprocessing()
    # Naive Random Oversampling
    ros = RandomOverSampler(random_state=0)
    X_res, y_res = ros.fit_resample(X_train_scaled, y_train)
    # Train the logistic regression model using resampled data
    logreg = LogisticRegression(solver='lbfgs', random_state=1)
    logreg.fit(X_res, y_res)
    y_pred = logreg.predict(X_test_scaled)
    accuracy_score = balanced_accuracy_score(y_test, y_pred)
    prediction = logreg.predict(test)
    return prediction, accuracy_score

def test_data():
    ticker = yf.Ticker(mongo_connection())
    test_data = ticker.history(period='1d')
    cleaned_test_data = test_data.drop(['Volume', 'Close', 'Dividends', 'Stock Splits'], axis=1)
    cleaned_test_data['Open'] = le.fit_transform(cleaned_test_data['Open'])
    cleaned_test_data['High'] = le.fit_transform(cleaned_test_data['High'])
    cleaned_test_data['Low'] = le.fit_transform(cleaned_test_data['Low'])
    cleaned_scaled_test_data = scaler.fit_transform(cleaned_test_data)
    return cleaned_scaled_test_data

def machine_learning():
    ticker = mongo_connection()
    test = test_data()
    prediction, accuracy_score = Naive_Random_Oversampling(test)
    loss = 'The closing price will be less than the opening price'
    gain = 'The closing price will be greater than the opening price'
    direction = loss if prediction == 0 else gain
    data = {"accuracy_score":accuracy_score, "ticker": ticker, "prediction": direction}
    return data
