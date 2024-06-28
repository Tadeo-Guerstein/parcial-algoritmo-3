from bd import CustomersManager
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Inicializar el manejador de clientes
customers_manager = CustomersManager()

@app.route("/login", methods=['POST'])
def login():
    user_data = request.get_json()#metodo de flask para retornar los datos del POST
    
    name = user_data['name']# extrae el valor del nombre de usuario
    response = customers_manager.add_user(name)

    return jsonify(response[0])#estás devolviendo una respuesta en formato JSON al cliente, [0] porque es una tupla y tiene que enviarse solo el primer dato de la tupla

@app.route("/logout/<customerID>", methods=['PUT'])
def logout(customerID):
    response = customers_manager.change_status(customerID)

    return jsonify(response[0])#estás devolviendo una respuesta en formato JSON al cliente, [0] porque es una tupla y tiene que enviarse solo el primer dato de la tupla

@app.route("/customers", methods=['GET'])
def getCustomers():
    response = customers_manager.get_customers()

    return jsonify(response[0])#estás devolviendo una respuesta en formato JSON al cliente, [0] porque es una tupla y tiene que enviarse solo el primer dato de la tupla

@app.route("/order", methods=['POST'])
def addOrder():
    print('request', request)
    order_data = request.get_json()
    customerID = order_data['customerID']
    orderName = order_data['orderName']
    response = customers_manager.add_order(customerID, orderName)

    return jsonify(response[0])#estás devolviendo una respuesta en formato JSON al cliente, [0] porque es una tupla y tiene que enviarse solo el primer dato de la tupla

@app.route("/order/<customerID>", methods=['GET'])
def getOrders(customerID):
    response = customers_manager.get_orders(customerID)

    return jsonify(response[0])

app.run(host="0.0.0.0", port=8000, debug=True) 
