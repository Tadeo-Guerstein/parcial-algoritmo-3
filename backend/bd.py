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
        
    def get_customers(self):
        try:
                cursor = self.connection.cursor()
                # Verificar si el usuario ya existe en la base de datos
                cursor.execute("SELECT * FROM customers")
                data = cursor.fetchall()
                print('data', data)

                users = [{"id": id, "nombre": nombre, "isLogged": True if status == 1 else (False)  } for id, nombre, status in data]

                return {"message": "ok", "data": users}, 200
            
        except bd.Error as e:
            # Manejar errores de la base de datos
            return {"error": str(e)}, 500

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
                # Verificar si el usuario ya existe en la base de datos
                cursor.execute("SELECT * FROM orders WHERE id_customer=?", (customerID,))
                data = cursor.fetchall()

                orders = [{"id": id, "id_customer": id_customer, "orderDate": orderDate, "orderName": orderName } for id, id_customer, orderDate, orderName in data]

                return {"message": "ok", "data": orders}, 200
            
        except bd.Error as e:
            # Manejar errores de la base de datos
            return {"error": str(e)}, 500