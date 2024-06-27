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
                    return {"message": f"Welcome {name}", "customerID": existing_user[0]}, 200
                
                # Insertar nuevo usuario en la base de datos
                cursor.execute("INSERT INTO customers (name, status) VALUES (?, ?)", (name, 1, ))
                self.connection.commit()

                # selecciono ultimo customer que ingrese para saber el id y enviarlo al front
                cursor.execute("SELECT id FROM customers WHERE name=?", (name,)) 
                user = cursor.fetchone()

                return {"message": f"User '{name}' successfully added", "customerID": user[0]}, 201
            
        except bd.Error as e:
            # Manejar errores de la base de datos
            return {"error": str(e)}, 500

