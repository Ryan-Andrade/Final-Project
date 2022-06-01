# Stock Analysis Project

## Overview

We are analyzing stocks and determining whether or not the closing price will be greated than the opening price. We set up a flask app and get the user inputs to determine what stock to analyze, what time period we are training the models on, and for which machine learning algorithm we are using. Our algorithm uses the last day of trading as the test data and returns our prediction and accuracy.

### Tools Used
- IDE Used: VSCode
- Languages Used: Python, Javascript, HTML, CSS
- Libraries Used: Flask, Imbalanced-Learn, MatPlotLib, Numpy, Pandas, PyMongo, SKLearn, yFinance

### Sources
- Stock Data: Yahoo Finance using the yFinance API
- CSS Styling: A theme from https://bootswatch.com
- Trading Widget: TradingView widget from https://www.tradingview.com/widget/advanced-chart/
- Ticker JSON: 
- HTML Dropdown menu: 


# -----------

## Price Direction Prediction
The idea behind this project is to prediction the price direction of 10 energy stocks.  

## Stand UP
What did you do last time?

We created the ML algorithm to predict if a stock will increase or decrease by the close of market 

What are you currently working on/ what progress will we see before next time?
Creating a flask/html page to create an interactive webpage for data visualization

Is there anything blocking your progress?
Current knowledge HTML and Flask (need to review modules for a refresher)

Everyone is creating their own Branches and will be dropping the last column and filtering for the start of 2021. Then creating summary statistics and a visualization to help further understand. 

## Ideas
We should consider encoding the dates as 0-252 (there are 253 trading days in the year).
There may be some similarities on specific days each year that the algorithm may be able to detect patterns within.

Don't round that dataset, leave as floats.

In order to add volume as a learning metric to our algorithm we would need the data listed here: https://firstratedata.com/i/stock/CMS

## Flask Team
-Serving up an html page that connects to our ML Algorithm
-Serving up a welcome


## HTML Team
-Presenting the findings
-Include charts of our predictions of the top ten stocks.
-Have a dropdown menu to select the stock pick
-Show the Open, Low, Close, High, and whatever other categories
-Have a nice fancy way to show the prediction

## ML Team
-Write a preproccesing function to pull, clean, possibly encode, scale, etc. 
-Data Manipulization
-Adding Technical Indicators
-Figuring out what to do with the dates
-Test other algorithms
-Optimizing the predictive capabilities.
