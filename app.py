import json
from flask import request
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import algorithm

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/stock_predictions"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    mongo.db.stock_ticker.insert_one({'ticker': result})
    return result

#@app.route("/ml")
#def machine():
#    ml = mongo.db.ml_vars
#    ml_data = algorithm.run_predictions()
#    ml.update_one({}, {"$set":ml_data}, upsert=True)
#    return redirect('/', code=302)



if __name__ == "__main__":
    app.run(debug = True)