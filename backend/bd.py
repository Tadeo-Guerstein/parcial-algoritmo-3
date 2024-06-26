import sqlite3 as bd

class CustomersManager: 
  def __init__(self):
    print("BD: Conectado a la bd")
    conexion = bd.connect("BD.db")
    conexion.execute("""
    create table if not exists customers (
      id integer primary key autoincrement not null,
      name text not null,
      status tinyint
    )
    """)
    conexion.execute("""
    create table if not exists orders (
      id integer primary key autoincrement not null, 
      id_customer integer not null, 
      orderDate timestamp not null, 
      orderName text not null,
      foreign key (id_customer) references customers(id)
    )
    """)

    self.connection = conexion

  def login(self, user):
    print('user', user)