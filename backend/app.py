from bd import CustomersManager
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializar el manejador de clientes
customers_manager = CustomersManager()

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        user_data = request.get_json()#metodo de flask para retornar los datos del POST
    
    name = user_data['name']# extrae el valor del nombre de usuario
    response = customers_manager.add_user(name)

    return jsonify(response[0])#estás devolviendo una respuesta en formato JSON al cliente, [0] porque es una tupla y tiene que enviarse solo el primer dato de la tupla

app.run(host="0.0.0.0", port=8000, debug=True) 
