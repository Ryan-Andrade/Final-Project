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
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN
from imblearn.ensemble import BalancedRandomForestClassifier
from imblearn.ensemble import EasyEnsembleClassifier
le = LabelEncoder()
scaler = StandardScaler()

def mongo_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.stock_prediction
    collection = db.prediction
    document = collection.find_one()
    ticker = document['ticker']
    algorithm = document['algorithm']
    period = document['period']
    return ticker, algorithm, period

def download_data():
    ticker, algorithm, period = mongo_connection()
    ticker = yf.Ticker(ticker)
    data = ticker.history(period=period)
    data = pd.DataFrame(data)
    data = data[:-1]
    data['Day Result'] = np.where(data['Close'] > data['Open'], 1, 0)
    data.drop(['Volume', 'Close'], axis=1, inplace=True)    
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
    return X_train_scaled, X_test_scaled, X_train, y_train, y_test, X, y

def Naive_Random_Oversampling(test):
    X_train_scaled, X_test_scaled, X_train, y_train, y_test, X, y = preprocessing()
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

def SMOTE_Oversampling(test):
    X_train_scaled, X_test_scaled, X_train, y_train, y_test, X, y = preprocessing()
    # Resample the training data with SMOTE
    X_res, y_res = SMOTE(random_state=1, sampling_strategy='auto').fit_resample(X_train, y_train)
    # Train the logistic regression model using resampled data
    logreg = LogisticRegression(solver='lbfgs', random_state=1)
    logreg.fit(X_res, y_res)
    y_pred = logreg.predict(X_test_scaled)
    accuracy_score = balanced_accuracy_score(y_test, y_pred)
    prediction = logreg.predict(test)
    return prediction, accuracy_score

def Cluster_Centroids_Undersampling(test):
    X_train_scaled, X_test_scaled, X_train, y_train, y_test, X, y = preprocessing()
    rus = RandomUnderSampler(random_state=1)
    X_res, y_res = rus.fit_resample(X_train, y_train)
    # Train the logistic regression model using resampled data
    logreg = LogisticRegression(solver='lbfgs', random_state=1)
    logreg.fit(X_res, y_res)
    y_pred = logreg.predict(X_test_scaled)
    accuracy_score = balanced_accuracy_score(y_test, y_pred)
    prediction = logreg.predict(test)
    return prediction, accuracy_score

def SMOTE_ENN(test):
    X_train_scaled, X_test_scaled, X_train, y_train, y_test, X, y = preprocessing()
    smote_enn = SMOTEENN(random_state=1)
    X_res, y_res = smote_enn.fit_resample(X, y)
    # Train the logistic regression model using resampled data
    logreg = LogisticRegression(solver='lbfgs', random_state=1)
    logreg.fit(X_res, y_res)
    y_pred = logreg.predict(X_test_scaled)
    accuracy_score = balanced_accuracy_score(y_test, y_pred)
    prediction = logreg.predict(test)
    return prediction, accuracy_score

def Balanced_Random_Forest_Classifier(test):
    X_train_scaled, X_test_scaled, X_train, y_train, y_test, X, y = preprocessing()
    rf_model = BalancedRandomForestClassifier(n_estimators=100, random_state=1) 
    rf_model = rf_model.fit(X_train_scaled, y_train)
    predictions = rf_model.predict(X_test_scaled)
    accuracy_score = balanced_accuracy_score(y_test, predictions)
    prediction = rf_model.predict(test)
    return prediction, accuracy_score

def Easy_Ensemble_Adaboost_Classifier(test):
    X_train_scaled, X_test_scaled, X_train, y_train, y_test, X, y = preprocessing()
    rf_model = EasyEnsembleClassifier(n_estimators=100, random_state=1) 
    rf_model = rf_model.fit(X_train_scaled, y_train)
    predictions = rf_model.predict(X_test_scaled)
    accuracy_score = balanced_accuracy_score(y_test, predictions)
    prediction = rf_model.predict(test)
    return prediction, accuracy_score

def test_data():
    ticker, algorithm, period = mongo_connection()
    ticker = yf.Ticker(ticker)
    test_data = ticker.history(period='1d')
    cleaned_test_data = test_data.drop(['Volume', 'Close'], axis=1)
    cleaned_test_data['Open'] = le.fit_transform(cleaned_test_data['Open'])
    cleaned_test_data['High'] = le.fit_transform(cleaned_test_data['High'])
    cleaned_test_data['Low'] = le.fit_transform(cleaned_test_data['Low'])
    cleaned_scaled_test_data = scaler.fit_transform(cleaned_test_data)
    return cleaned_scaled_test_data

def machine_learning():
    test = test_data()
    ticker, algorithm, period = mongo_connection()
    if algorithm == 'naive':
        prediction, accuracy_score = Naive_Random_Oversampling(test)
    elif algorithm == 'smote':
        prediction, accuracy_score = SMOTE_Oversampling(test)
    elif algorithm == 'under':
        prediction, accuracy_score = Cluster_Centroids_Undersampling(test)
    elif algorithm == 'smoteenn':
        prediction, accuracy_score = SMOTE_ENN(test)
    elif algorithm == 'balanced':
        prediction, accuracy_score = Balanced_Random_Forest_Classifier(test)
    elif algorithm == 'easy':
        prediction, accuracy_score = Easy_Ensemble_Adaboost_Classifier(test) 
    accuracy_score = accuracy_score * 100
    accuracy_score = "{:.2f}%".format(accuracy_score) 
    loss = 'Closing price < Opening price'
    gain = 'Closing price > Opening price'
    direction = loss if prediction == 0 else gain
    data = {"accuracy_score":accuracy_score, "ticker": ticker, "prediction": direction}
    return data