# Final-Project

## Price Gain Prediction
The idea behind this project is to use this dataset of US Mutual Funds/ETF's: https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs
and try to predict which funds will increase in price the next day.

## Current Task
Everyone is creating their own Branches and will be doing some EDA on our files.



## Potential workflow
1. Store the dataset in an S3 bucket
2. Extract the Data into a Pyspark notebook
3. Transform the data using pandas or pyspark
   1. Create buy labels for the data by taking the close price and subtracting the open price and determining which fund made the most money that day.
4. Load the data into PostgreSQL using AWS Relational Database
5. Call the cleaned Data from the database
6. Preprocess the data and prepare it for machine learning
7. Run the data through a Supervised ML model and make a prediction on which stock will have the greatest price increase.
8. Host results using a Tableau dashboard. 
