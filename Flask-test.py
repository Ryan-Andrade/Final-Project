from flask import Flask, render_template

# Create an instance of Flask
app = Flask(__name__)

@app.route("/")
def index():
    pagetitle = "HomePage"
    return render_template("index.html",
                            mytitle=pagetitle,
                            mycontent="Hello World")


if __name__ == "__main__":
    app.run(debug = True)