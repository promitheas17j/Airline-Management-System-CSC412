from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def login_page():
   return render_template("signin.html")

@app.route('/process-data', methods=["GET", "POST"])
def signin_btn():
    return render_template("not_built_yet.html")

@app.route('/notready')
def not_ready_page():
    return render_template("not_built_yet.html")

if __name__ == "__main__":
    app.run()
