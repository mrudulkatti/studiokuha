from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/services')
def services():
    return render_template('services.html')

@app.route("/home") #coming soon page
def new():
    return render_template("studiokuha.html")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)