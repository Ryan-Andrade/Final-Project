from flask import Flask

# Create an instance of Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug = True)