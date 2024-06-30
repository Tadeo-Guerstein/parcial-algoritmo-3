import sqlite3 as bd

class CustomersManager: 
    def __init__(self):
        print("BD: Conectado a la bd")
        self.connection = bd.connect("BD.db", check_same_thread=False)#usa distintos hilos para hacer distintas peticiones
        self.connection.execute("""
            create table if not exists customers (
                id integer primary key autoincrement not null,
                name text not null,
                status tinyint
            )
        """)
        self.connection.execute("""
            create table if not exists orders (
                id integer primary key autoincrement not null, 
                id_customer integer not null, 
                orderDate timestamp not null, 
                orderName text not null,
                foreign key (id_customer) references customers(id)
            )
        """)
    
    def add_user(self, name):
        try:
                cursor = self.connection.cursor()
                # Verificar si el usuario ya existe en la base de datos
                cursor.execute("SELECT * FROM customers WHERE name=?", (name,))
                existing_user = cursor.fetchone()

                if existing_user:
                    # si existe el usuario tiene que dar ok de una y enviar el customerID
                    cursor.execute("UPDATE customers SET status = 1 WHERE id = ?", (existing_user[0],))
                    self.connection.commit()
                    return {"message": f"Welcome {name}", "customerID": existing_user[0]}, 200
                
                # Insertar nuevo usuario en la base de datos
                cursor.execute("INSERT INTO customers (name, status) VALUES (?, ?)", (name, 1, ))
                self.connection.commit()

                # selecciono ultimo customer que ingrese para saber el id y enviarlo al front
                cursor.execute("SELECT id FROM customers WHERE name=?", (name,)) 
                user = cursor.fetchone()

                return {"message": f"User '{name}' successfully added", "customerID": user[0]}, 200
            
        except bd.Error as e:
            # Manejar errores de la base de datos
            return {"error": str(e)}, 500
        
    def change_status(self, customerID):
        try:
                cursor = self.connection.cursor()
                # Verificar si el usuario ya existe en la base de datos
                cursor.execute("SELECT * FROM customers WHERE id=?", (customerID,))
                existing_user = cursor.fetchone()

                if not existing_user:
                    # si existe el usuario tiene que dar ok de una y enviar el customerID
                    return {"error": f"It doesn't exist a customer with that ID"}, 406
                
                # Insertar nuevo usuario en la base de datos
                cursor.execute("UPDATE customers SET status = 0 WHERE id = ?", (customerID,))
                self.connection.commit()

                return {"message": f"ok"}, 200
        except bd.Error as e:
            # Manejar errores de la base de datos
            return {"error": str(e)}, 500
        
    # Método dentro de la clase CustomersManager
    def get_customers(self):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT customers.id, customers.name, customers.status, orders.orderName
        FROM customers
        INNER JOIN orders ON customers.id = orders.id_customer
        WHERE orders.orderDate = (
            SELECT MAX(orderDate)
            FROM orders
            WHERE id_customer = customers.id
        )  
        """,)
        #el where filtra las órdenes de la fecha maxima de cada cliente donde coincida el cliente con su orden(id_customer)
       
        data = cursor.fetchall()
        customers = [{"id": id, "nombre": name, "isLogged": status, "groups": orderName} for id, name, status, orderName in data]
        print(customers)
        return {"message": "ok", "data": customers}, 200
    
    def add_order(self, customerID, orderName):
        try:
                cursor = self.connection.cursor()
                # Verificar si el usuario ya existe en la base de datos
                cursor.execute("SELECT * FROM customers WHERE id=?", (customerID,))
                existing_user = cursor.fetchone()

                if not existing_user:
                    # si existe el usuario tiene que dar ok de una y enviar el customerID
                    return {"error": f"It doesn't exist a customer with that ID"}, 406
                
                # Insertar nuevo usuario en la base de datos
                cursor.execute("INSERT INTO orders (id_customer, orderDate, orderName) VALUES (?, datetime('now'), ?)", (customerID, orderName, ))
                self.connection.commit()

                return {"message": f"Order '{orderName}' successfully added"}, 200
            
        except bd.Error as e:
            # Manejar errores de la base de datos
            return {"error": str(e)}, 500
        
    def get_orders(self, customerID):
        try:
                cursor = self.connection.cursor()
                cursor.execute("""
                    SELECT orders.id, orders.orderName, orders.orderDate, customers.name AS customer 
                    FROM orders
                    INNER JOIN customers ON customers.id = ?
                    WHERE orders.id_customer = ?
                """, (customerID, customerID, ))
                data = cursor.fetchall()

                orders = [{"id": id,  "orderDate": orderDate, "orderName": orderName, "customer": customer } for id, orderName, orderDate, customer in data]

                return {"message": "ok", "data": orders}, 200
            
        except bd.Error as e:
            # Manejar errores de la base de datos
            return {"error": str(e)}, 500