import mysql.connector
from mysql.connector import errorcode
import os

# Configuración de la conexión MySQL
db_config = {
    'user': 'root',
    'password': 'toor',
    'host': 'localhost',
    'database': 'prueba'
}

def init_db():
    try:
        cnx = mysql.connector.connect(user=db_config['user'], password=db_config['password'], host=db_config['host'])
        cursor = cnx.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS prueba")
        cursor.close()
        cnx.close()
        
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        # Modificar tabla de usuarios si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fname VARCHAR(255) NOT NULL,
                lastname VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('client', 'seller', 'admin') DEFAULT 'client'
            )
        """)
        
        # Tabla de productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                seller_id INT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                image_url VARCHAR(500),
                category ENUM('cd', 'vinyl', 'cassette', 'merch') DEFAULT 'cd',
                stock INT DEFAULT 0,
                tracklist TEXT,
                sizes VARCHAR(255),
                FOREIGN KEY (seller_id) REFERENCES users(id)
            )
        """)
        
        # Tabla de carrito
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                product_id INT,
                quantity INT DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        
        # Tabla de ordenes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                total_price DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Tabla de order_items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                product_id INT,
                quantity INT,
                price DECIMAL(10, 2),
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        cnx.commit()
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print("Error inicializando DB:", err)

def agregar_usuario(fname, lastname, email, password_hash, role='client'):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        insertar_usuario = "INSERT INTO users (fname, lastname, email, password, role) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insertar_usuario, (fname, lastname, email, password_hash, role))
        cnx.commit()
        last_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return last_id
    except mysql.connector.Error as err:
        print("Error al agregar usuario:", err)
        return None

def obtener_usuario_por_email(email):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        cnx.close()
        return usuario
    except mysql.connector.Error as err:
        print("Error al obtener usuario por email:", err)
        return None

def obtener_usuario_por_id(user_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
        cnx.close()
        return usuario
    except mysql.connector.Error as err:
        print("Error al obtener usuario por ID:", err)
        return None

def obtener_productos(category=None, search_query=None):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = %s"
            params.append(category)
            
        if search_query:
            query += " AND (title LIKE %s OR description LIKE %s OR tracklist LIKE %s)"
            search_pattern = f"%{search_query}%"
            params.extend([search_pattern, search_pattern, search_pattern])
            
        cursor.execute(query, tuple(params))
        productos = cursor.fetchall()
        cursor.close()
        cnx.close()
        return productos
    except mysql.connector.Error as err:
        print("Error al obtener productos:", err)
        return []

def obtener_producto_por_id(product_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        producto = cursor.fetchone()
        cursor.close()
        cnx.close()
        return producto
    except mysql.connector.Error as err:
        print("Error al obtener producto:", err)
        return None

def crear_producto(seller_id, title, description, price, image_url, category, stock, tracklist=None, sizes=None):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = "INSERT INTO products (seller_id, title, description, price, image_url, category, stock, tracklist, sizes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (seller_id, title, description, price, image_url, category, stock, tracklist, sizes))
        cnx.commit()
        last_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return last_id
    except mysql.connector.Error as err:
        print("Error al crear producto:", err)
        return None

def agregar_al_carrito(user_id, product_id, quantity=1):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        # Verificar si ya existe en el carrito
        cursor.execute("SELECT id, quantity FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        item = cursor.fetchone()
        if item:
            new_qty = item[1] + quantity
            cursor.execute("UPDATE cart SET quantity = %s WHERE id = %s", (new_qty, item[0]))
        else:
            cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)", (user_id, product_id, quantity))
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except mysql.connector.Error as err:
        print("Error al agregar al carrito:", err)
        return False

def obtener_carrito(user_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT c.id as cart_id, c.quantity, p.* 
            FROM cart c 
            JOIN products p ON c.product_id = p.id 
            WHERE c.user_id = %s
        """
        cursor.execute(query, (user_id,))
        carrito = cursor.fetchall()
        cursor.close()
        cnx.close()
        return carrito
    except mysql.connector.Error as err:
        print("Error al obtener carrito:", err)
        return []

def vaciar_carrito(user_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except mysql.connector.Error as err:
        print("Error al vaciar carrito:", err)
        return False

def crear_orden(user_id, total, items):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        # Crear la orden
        cursor.execute("INSERT INTO orders (user_id, total_price) VALUES (%s, %s)", (user_id, total))
        order_id = cursor.lastrowid
        # Insertar los items
        for item in items:
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)", 
                           (order_id, item['id'], item['quantity'], item['price']))
        cnx.commit()
        cursor.close()
        cnx.close()
        return order_id
    except mysql.connector.Error as err:
        print("Error al crear orden:", err)
        return None

def obtener_historial_compras(user_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT o.id as order_id, o.total_price, o.created_at, 
                   oi.quantity, oi.price as item_price, p.title, p.image_url
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            WHERE o.user_id = %s
            ORDER BY o.created_at DESC
        """
        cursor.execute(query, (user_id,))
        historial = cursor.fetchall()
        cursor.close()
        cnx.close()
        
        # Agrupar por orden
        ordenes = {}
        for row in historial:
            oid = row['order_id']
            if oid not in ordenes:
                ordenes[oid] = {
                    'order_id': oid,
                    'total_price': row['total_price'],
                    'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M'),
                    'items': []
                }
            ordenes[oid]['items'].append(row)
            
        return list(ordenes.values())
    except mysql.connector.Error as err:
        print("Error al obtener historial:", err)
        return []