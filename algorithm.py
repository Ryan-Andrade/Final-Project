# Dependencies
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
from pymongo import MongoClient
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import RandomOverSampler
from imblearn.metrics import classification_report_imbalanced

client = MongoClient("mongodb://localhost:27017/")
db = client.stock_prediction
collection = db.prediction
document = collection.find_one()
ticker = document['ticker']

def preprocessing():
    data = yf.download(ticker, '2021-01-01', dt.datetime.date(dt.datetime.now()).isoformat(), interval='1d')
    data.drop(['Adj Close', 'Volume'], axis=1, inplace=True)    
    data['Day Result'] = np.where(data['Close'] > data['Open'], 1, 0)
    df = pd.DataFrame(data)
    df.drop(columns='Close', inplace=True)
    # Encode the data
    le = LabelEncoder()
    df['Open'] = le.fit_transform(df['Open'])
    df['High'] = le.fit_transform(df['High'])
    df['Low'] = le.fit_transform(df['Low'])
    # Split data into training and testing sets
    X = df.drop(['Day Result'], axis=1)
    y = df['Day Result'].values
    # Build the logistic regression model
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    # Scale and normalize the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit_transform(X_test)
    # Naive Random Oversampling
    ros = RandomOverSampler(random_state=0)
    X_res, y_res = ros.fit_resample(X_train_scaled, y_train)
    # Train the logistic regression model using resampled data
    logreg = LogisticRegression(solver='lbfgs', random_state=1)
    logreg.fit(X_res, y_res)
    y_pred = logreg.predict(X_test_scaled)
    accuracy_score = balanced_accuracy_score(y_test, y_pred)
    return accuracy_score