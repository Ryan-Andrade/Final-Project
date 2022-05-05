# Final-Project

## What is most important to you?
### Ryan
    The most important thing to me about the project is that I want to create something business related and professional. I want to recruiters to see this project in my portfolio and understand that I can perform similar analysis for their company's. Ideally I'd like to have some sales metrics and perform an analysis and give recommendations.

### Maksim

## Brainstorming
### Sentiment Analysis
The idea behind this project will be to choose a group of stocks and peform a sentiment analysis by doing a webscrape of the most recent articles and running it through an NLP machine learning algorithm to output whether the stock is a buy or a sell.

### Buy Prediction
The idea behind this project would be to use this dataset of US Funds: https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs
and try to predict which fund will have the greatest increase in price on the next day.
1. Store the dataset in an S3 bucket
2. Extract the Data into a Pyspark notebook
3. Transform the data using pandas or pyspark
   1. Create buy labels for the data by taking the close price and subtracting the open price and determining which fund made the most money that day.
4. Load the data into PostgreSQL using AWS Relational Database
5. Call the cleaned Data from the database
6. Preprocess the data and prepare it for machine learning
7. Run the data through a Supervised ML model and make a prediction on which stock will have the greatest price increase.
8. Host results using a Tableau dashboard. 