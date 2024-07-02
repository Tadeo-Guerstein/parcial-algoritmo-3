from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.types import Integer, VARCHAR, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

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

class DbManager: 
    def __init__(self) -> None:
        engine = create_engine('sqlite:///BD.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)
    
    def add_user(self, name):
        try:
            # Verificar si el usuario ya existe en la base de datos
            existing_user = self.session.query(Customer).filter_by(name = name).first()
            
            if existing_user:
                # si existe el usuario tiene que dar ok de una y enviar el customerID
                # TODO probar solo con el "existing_user"
                customerToUpdate = self.session.query(Customer).filter_by(id = existing_user.id).first()
                customerToUpdate.status = 1
                self.session.commit()
                return {"message": f"Welcome {name}", "customerID": existing_user.id}, 200

            # Insertar nuevo usuario en la base de datos
            newCustomer = Customer(name = name, status = 1)
            self.session.add(newCustomer)
            self.session.commit()

            return {"message": f"User '{name}' successfully added", "customerID": newCustomer.id}, 200

        except SQLAlchemyError as e:
        # Manejar errores de la base de datos
            return {"error": str(e)}, 500
        
    def change_status(self, customerID):
        try:
            existing_user = self.session.query(Customer).filter_by(id=customerID).first()
    
            if not existing_user:
                return {"error": f"It doesn't exist a customer with that ID"}, 406
    
            existing_user.status = 0
            self.session.commit()
    
            return {"message": f"ok"}, 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
        
     # Método dentro de la clase CustomersManager
    def get_customers(self):
        try:
            customers = self.session.query(Customer).all()
            data = []
            for customer in customers:
                last_order = self.session.query(Order).filter_by(id_customer=customer.id).order_by(Order.orderDate.desc()).first()
                user = {
                    "id": customer.id,
                    "nombre": customer.name,
                    "isLogged": True if customer.status == 1 else False,
                    "groups": last_order.orderName if last_order else None
                }
                data.append(user)
            return {"message": "ok", "data": data}, 200
            
        except SQLAlchemyError as e:
            # Manejar errores de la base de datos
            return {"error": str(e)}, 500
    
    def add_order(self, customerID, orderName):
        try:
            existing_user = self.session.query(Customer).filter_by(id=customerID).first()
    
            if not existing_user:
                return {"error": f"It doesn't exist a customer with that ID"}, 406
            
            new_order = Order(id_customer=customerID, orderName=orderName, orderDate=datetime.now())
            self.session.add(new_order)
            self.session.commit()
    
            return {"message": f"Order '{orderName}' successfully added"}, 200
            
        except SQLAlchemyError as e:
            # Manejar errores de la base de datos
            return {"error": str(e)}, 500
    
    def get_orders(self, customerID):
        try:
            orders = self.session.query(Order,Customer).join(Customer).filter(Order.id_customer == customerID).all()
            data = [{"id": order[0].id, "orderDate": order[0].orderDate, "orderName": order[0].orderName, "customer": order[1].name} for order in orders]
            return {"message": "ok", "data": data}, 200
            
        except SQLAlchemyError as e:
            # Manejar errores de la base de datos
            return {"error": str(e)}, 500
