from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/home")
def new():
    return render_template("studiokuha.html")

if __name__ == "__main__":
    app.run(debug=True, port=80, threaded=True)