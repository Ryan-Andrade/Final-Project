# Dependencies
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
from datetime import timedelta
from pymongo import MongoClient
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import RandomOverSampler
from imblearn.metrics import classification_report_imbalanced
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
    ticker = mongo_connection()
    yesterday = dt.datetime.date(dt.datetime.now() - timedelta(days= 1)).isoformat()
    data = yf.download(ticker, '2021-01-01', yesterday, interval='1d')
    data.drop(['Adj Close', 'Volume'], axis=1, inplace=True)    
    data['Day Result'] = np.where(data['Close'] > data['Open'], 1, 0)
    df = pd.DataFrame(data)
    df.drop(columns='Close', inplace=True)
    return df

def preprocessing():
    df = download_data()
    # Encode the data
    df['Open'] = le.fit_transform(df['Open'])
    df['High'] = le.fit_transform(df['High'])
    df['Low'] = le.fit_transform(df['Low'])
    # Split data into training and testing sets
    X = df.drop(['Day Result'], axis=1)
    y = df['Day Result'].values
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
    ticker = mongo_connection()
    today = dt.datetime.date(dt.datetime.now()).isoformat()
    test_data = yf.download(ticker, start= today)
    cleaned_test_data = test_data.drop(['Volume', 'Close', 'Adj Close'], axis=1)
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