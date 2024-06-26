from flask import Flask, render_template, request
from flask_cors import CORS
from bd import CustomersManager as bd

app = Flask(__name__)
CORS(app, resources={r"/customers/*": {"origins": "*"}})

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/customers")
def customers():
    return render_template("customers.html")

@app.route("/orders")
def order():
    return render_template("order.html")

@app.post("/login")
def login():
    body = request.json
    print("body", body)
    cone = bd()
    cone.login(body['username'])
    return []

app.run(host="0.0.0.0", port=8000, debug=True)  
