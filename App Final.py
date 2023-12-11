
from flask import Flask, request, jsonify

from flask_cors import CORS

import mysql.connector

from werkzeug.utils import secure_filename

import os
import time

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
            imagen_url VARCHAR(255),
            sale_price INT DEFAULT NULL)''')
        
        self.conn.commit()

        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def add_product(self, id, name, description, price, imagen, sale_price = None):

        self.cursor.execute(f"SELECT * FROM products WHERE id = {id}")
        product_exists = self.cursor.fetchone()
        if product_exists:
            return False

        sql = "INSERT INTO products (id, name, description, price, imagen_url, sale_price) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (id, name, description, price, imagen, sale_price)
        self.cursor.execute(sql, values)
        self.conn.commit()
        return True
    
    def query_product(self, id):
        self.cursor.execute(f"SELECT * FROM products WHERE id = {id}")
        return self.cursor.fetchone()
    
    def modify_product(self, id, new_name, new_description, new_price, nueva_imagen, new_sale_price):
        sql = "UPDATE products SET name = %s, description = %s, price = %s, imagen_url= %s, sale_price = %s WHERE id = %s"
        valores = (new_name, new_description, new_price, nueva_imagen, new_sale_price, id)
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
            print(f"ID.....: {product['id']}")
            print(f"Name.....: {product['name']}")
            print(f"Description: {product['description']}")
            print(f"Price.......: {product['price']}")
            print(f"Imagen.....: {product['imagen_url']}")
            print(f"Sale price..: {product['sale_price']}")
            print("-" * 40)
        else:
            print("Product not found.")

#####################
products = Products(host='pointoapp.mysql.pythonanywhere-services.com', user='pointoapp', password='tidedet237@jalunaki.com', database='pointoapp$miapp')

RUTA_DESTINO = '/home/pointoapp/mysite/static/imagenes'

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
        return "Product not found.", 404

@app.route("/products", methods=["POST"])
def add_product():
    id = request.form['id']
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    imagen = request.files['imagen']
    sale_price = request.form['sale_price']
    name_imagen = ""

    product = products.query_product(id)
    if not product: 
        name_imagen = secure_filename(imagen.filename)
        name_base, extension = os.path.splitext(name_imagen)
        name_imagen = f"{name_base}_{int(time.time())}{extension}"

        if products.add_product(id, name, description, price, name_imagen, sale_price):
            imagen.save(os.path.join(RUTA_DESTINO, name_imagen))
            return jsonify({"mensaje": "Product added successfully.", "imagen": name_imagen}), 201
        else:
            return jsonify({"mensaje": "Error while trying to add product."}), 500

    else:
        return jsonify({"mensaje": "Product already exists."}), 400

@app.route("/products/<int:id>", methods=["PUT"])
def modify_product(id):
    new_name = request.form.get("name")
    new_description = request.form.get("description")
    new_price = request.form.get("price")
    imagen = request.files['imagen'] if 'imagen' in request.files else None
    new_sale_price = request.form.get("sale_price")
    product = product = products.query_product(id)
    name_imagen = request.form.get("imagen") if not 'imagen' in request.files else None
    if product:
        old_imagen = product["imagen_url"]
        rout_imagen = os.path.join(RUTA_DESTINO, old_imagen)
        if imagen:
            name_imagen = secure_filename(imagen.filename) 
            name_base, extension = os.path.splitext(name_imagen)
            name_imagen = f"{name_base}_{int(time.time())}{extension}"
            if old_imagen == name_imagen:
                name_imagen = old_imagen
            else:
                if os.path.exists(rout_imagen):
                    os.remove(rout_imagen)
        if products.modify_product(id, new_name, new_description, new_price, name_imagen, new_sale_price):
            if imagen:
               imagen.save(os.path.join(RUTA_DESTINO, name_imagen))
            return jsonify({"mensaje": "Product edited successfully."}), 200
        else:
            return jsonify({"mensaje": "Product not found."}), 403
    else:
        return jsonify({"mensaje": "Product not found."}), 403

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = products.query_product(id)

    if product: 
        old_image = product["imagen_url"]
        rout_imagen = os.path.join(RUTA_DESTINO, old_image)

        if os.path.exists(rout_imagen):
            os.remove(rout_imagen)
        if products.delete_product(id):
            return jsonify({"mensaje": "Product deleted successfully."}), 200
        else:
            return jsonify({"mensaje": "Error while trying to deleted product."}), 500
    else:
        return jsonify({"mensaje": "Product not found."}), 404
    

#############

if __name__ == "__main__":
    app.run(debug=True)

