import json
from flask import request
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import algorithm
import os

value = os.environ.get("MONGODB_URI")

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/stock_prediction"
# Cloud version
app.config["MONGO_URI"] = value

mongo = PyMongo(app)

# Default Route
@app.route('/')
def index():
    prediction = mongo.db.prediction.find_one()
    return render_template('index.html', prediction=prediction)
 
@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    result = json.loads(output)
    prediction = mongo.db.prediction
    prediction.update_one({}, {'$set': result}, upsert=True) # Store only one result to MongoDB collection

# Route that calls the function to run the model and predict whether the stock will go up or down
@app.route('/ml')
def logistic_regression():
    prediction = mongo.db.prediction
    prediction_data = algorithm.machine_learning()
    prediction.update_one({}, {'$set': prediction_data}, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run()