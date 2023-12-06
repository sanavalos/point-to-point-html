
from flask import Flask, request, jsonify, render_template

from flask_cors import CORS

import mysql.connector

from werkzeug.utils import secure_filename

#--------------------------------------------------------------------

app = Flask(__name__)
CORS(app)

class Products:
    
    def __init__(self, host, user, password, database):

        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            id INT,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            price INT NOT NULL,
            sale_price INT DEFAULT NULL)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pointers (
            name VARCHAR(255) NOT NULL,
            latitude VARCHAR(255) NOT NULL,
            longitude VARCHAR(255) NOT NULL)''')
        
        self.conn.commit()

        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def add_product(self, id, name, description, price, sale_price = None):

        self.cursor.execute(f"SELECT * FROM products WHERE id = {id}")
        equipo_existe = self.cursor.fetchone()
        if equipo_existe:
            return False

        sql = f"INSERT INTO products \
               (id, name, description, price, sale_price) \
               VALUES \
               ({id}, '{name}', '{description}', {price}, '{sale_price}')"
        self.cursor.execute(sql)
        self.conn.commit()
        return True
    
    def query_product(self, id):
       
        self.cursor.execute(f"SELECT * FROM products WHERE id = {id}")
        return self.cursor.fetchone()
    
    def modify_product(self, id, new_name, new_description, new_price, new_sale_price):

        sql = "UPDATE products SET name = %s, description = %s, price = %s, sale_price = %s WHERE id = %s"
        valores = (new_name, new_description, new_price, new_sale_price, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0 
    
    def list_products(self):
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        return products
    
    def delete_product(self, id):
        self.cursor.execute(f"DELETE FROM products WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0 

    def show_product(self, id):
        product = self.query_product(id)
        if product:
            print("-" * 40)
            print(f"Código.....: {product['id']}")
            print(f"Nombre.....: {product['name']}")
            print(f"Descripción: {product['description']}")
            print(f"Tipo.......: {product['price']}")
            print(f"Categoria..: {product['sale_price']}")
            print("-" * 40)
        else:
            print("Equipo no encontrado.")

#####################
products = Products(host='localhost', user='root', password='', database='miapp')

@app.route("/products", methods=["GET"])
def list_products():
    all_products = products.list_products()
    return jsonify(all_products)


@app.route("/products/<int:id>", methods=["GET"])
def show_product(id):
    product = products.query_product(id)
    if product:
        return jsonify(product), 201
    else:
        return "Equipo no encontrado.", 404

@app.route("/products", methods=["POST"])
def add_product():
    id = request.form['id']
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    sale_price = request.form['sale_price']

    product = products.query_product(id)
    if not product: 
        if products.add_product(id, name, description, price, sale_price):
            return jsonify({"mensaje": "Equipo agregado correctamente."}), 201
        else:
            return jsonify({"mensaje": "Error al agregar el product."}), 500

    else:
        return jsonify({"mensaje": "Equipo ya existe."}), 400

@app.route("/products/<int:id>", methods=["PUT"])
def modify_product(id):
    new_name = request.form.get("name")
    new_description = request.form.get("description")
    new_price = request.form.get("price")
    new_sale_price = request.form.get("sale_price")
    
    if products.modify_product(id, new_name, new_description, new_price, new_sale_price):
        return jsonify({"mensaje": "Equipo modificado"}), 200
    else:
        return jsonify({"mensaje": "Equipo no encontrado"}), 403

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = products.query_product(id)
    if product: 
        if products.delete_product(id):
            return jsonify({"mensaje": "Equipo eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el product"}), 500
    else:
        return jsonify({"mensaje": "Equipo no encontrado"}), 404
    

#############

if __name__ == "__main__":
    app.run(debug=True)

