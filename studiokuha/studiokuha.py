from flask import Flask , request , render_template, redirect , url_for, session, flash

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("first.html")

@app.route("/home")
def new():
    return render_template("studiokuha.html")

if __name__ == "__main__":
    app.run(debug=True)