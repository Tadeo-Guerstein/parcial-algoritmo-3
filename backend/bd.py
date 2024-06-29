from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, VARCHAR, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine('sqlite:///BD.db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50))
    status = Column(Boolean)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    id_customer = Column(Integer, ForeignKey("customers.id"))
    orderName = Column(VARCHAR(256))
    orderDate = Column(TIMESTAMP)

class CustomersManager: 
    def add_user(self, name):
        try:
            # Verificar si el usuario ya existe en la base de datos
            existing_user = session.query(Customer).filter_by(name = name).first()
            
            if existing_user:
                # si existe el usuario tiene que dar ok de una y enviar el customerID
                # TODO probar solo con el "existing_user"
                customerToUpdate = session.query(Customer).filter_by(id = existing_user.id).first()
                customerToUpdate.status = 1
                session.commit()
                return {"message": f"Welcome {name}", "customerID": existing_user.id}, 200

            # Insertar nuevo usuario en la base de datos
            newCustomer = Customer(name = name, status = 1)
            session.add(newCustomer)
            session.commit()

            return {"message": f"User '{name}' successfully added", "customerID": newCustomer.id}, 200

        except SQLAlchemyError as e:
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
    
Base.metadata.create_all(engine)