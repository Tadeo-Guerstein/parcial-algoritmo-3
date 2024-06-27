from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from bd import CustomersManager

app = Flask(__name__)
CORS(app, resources={r"/customers/*": {"origins": "*"}})

# Inicializar el manejador de clientes
customers_manager = CustomersManager()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        user_data = request.get_json()#metodo de flask para retornar los datos del POST
    
    name = user_data['name']# extrae el valor del nombre de usuario
    response = customers_manager.add_user(name)
    return jsonify(response)#estás devolviendo una respuesta en formato JSON al cliente

@app.route("/customers")
def customers():
    return render_template("customers.html")

@app.route("/orders")
def order():
    return render_template("order.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
