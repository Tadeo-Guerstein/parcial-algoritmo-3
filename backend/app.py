from bd import CustomersManager as bd
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/customers/*": {"origins": "*"}})

@app.post("/login")
def login():
    body = request.json
    print("body", body)
    cone = bd()
    cone.login(body['username'])
    return []

app.run(host="0.0.0.0", port=8000, debug=True) 
