import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from server.db import (
    init_db, agregar_usuario, obtener_usuario_por_email, obtener_usuario_por_id,
    obtener_productos, obtener_producto_por_id, crear_producto,
    agregar_al_carrito, obtener_carrito, vaciar_carrito, crear_orden, obtener_historial_compras
)

app = Flask(__name__, template_folder='client/templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'NOTMTSCNMQQ')
bcrypt = Bcrypt(app)

# Inicializar Base de Datos al arrancar (solo en entorno local/dev)
init_db()

def login_required(f):
    """Para restringir el acceso si sesion activa"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth'))
        return f(*args, **kwargs)
    return decorated_function

def inject_user_data():
    """Para inyectar datos del usuario en todas las plantillas"""
    if 'user_id' in session:
        return obtener_usuario_por_id(session['user_id'])
    return None

@app.route('/')
def home():
    user = inject_user_data()
    return render_template('index.html', user=user)

@app.route('/about')
def about():
    user = inject_user_data()
    return render_template('about.html', user=user)

@app.route('/contact')
def contact():
    user = inject_user_data()
    return render_template('contact.html', user=user)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    # Si el usuario esta logeado, redirige a Home
    if session.get('logged_in'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'login':
            email = request.form.get('email')
            password = request.form.get('password')
            usuario = obtener_usuario_por_email(email)
            
            if usuario and bcrypt.check_password_hash(usuario['password'], password):
                session['logged_in'] = True
                session['user_id'] = usuario['id']
                session['user_email'] = usuario['email']
                session['user_role'] = usuario['role']
                return redirect(url_for('home'))
            else:
                return render_template('auth.html', error='Contraseña o email incorrectos', active_tab='login')
                
        elif action == 'signup':
            fname = request.form.get('fname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('cpassword')
            role = request.form.get('role', 'client') # Por defecto es cliente
            
            if password != confirm_password:
                return render_template('auth.html', error="Error: Las contraseñas no coinciden.", active_tab='signup')

            password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
            user_id = agregar_usuario(fname, lastname, email, password_hash, role)

            if user_id:
                # Login automático tras registro
                session['logged_in'] = True
                session['user_id'] = user_id
                session['user_email'] = email
                session['user_role'] = role
                return redirect(url_for('home'))
            else: 
                return render_template('auth.html', error="Error al registrar usuario. El email ya existe.", active_tab='signup')
                
    # GET request
    return render_template('auth.html', active_tab='login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/tienda')
def store():
    user = inject_user_data()
    category = request.args.get('category')
    search_query = request.args.get('q')
    productos = obtener_productos(category=category, search_query=search_query)
    return render_template('store.html', user=user, productos=productos, search_query=search_query)

@app.route('/producto/<int:product_id>')
def product_detail(product_id):
    user = inject_user_data()
    producto = obtener_producto_por_id(product_id)
    if not producto:
        return redirect(url_for('store'))
        
    # Guardar en visitados recientemente
    if 'recent' not in session:
        session['recent'] = []
    
    # Evitar duplicados consecutivos y mantener limite de 4
    if product_id in session['recent']:
        session['recent'].remove(product_id)
    session['recent'].insert(0, product_id)
    session['recent'] = session['recent'][:4]
    session.modified = True
        
    return render_template('product_detail.html', user=user, producto=producto)

@app.route('/carrito')
@login_required
def cart():
    user = inject_user_data()
    if user['role'] != 'client':
        return redirect(url_for('home'))
        
    carrito_items = obtener_carrito(user['id'])
    total = sum(item['price'] * item['quantity'] for item in carrito_items) if carrito_items else 0
    return render_template('cart.html', user=user, items=carrito_items, total=total)

@app.route('/carrito/agregar/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    if session.get('user_role') != 'client':
        return redirect(url_for('store'))
        
    cantidad = int(request.form.get('quantity', 1))
    agregar_al_carrito(session['user_id'], product_id, cantidad)
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if session.get('user_role') != 'client':
        return redirect(url_for('home'))
        
    user_id = session['user_id']
    carrito_items = obtener_carrito(user_id)
    
    if not carrito_items:
        return redirect(url_for('cart'))
        
    total = sum(item['price'] * item['quantity'] for item in carrito_items)
    
    # Crear orden y guardar items
    crear_orden(user_id, total, carrito_items)
    vaciar_carrito(user_id)
    
    user = inject_user_data()
    return render_template('checkout.html', user=user, total=total)

@app.route('/publicar', methods=['GET', 'POST'])
@login_required
def publish():
    user = inject_user_data()
    if user['role'] != 'seller':
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url') or 'https://via.placeholder.com/400'
        category = request.form.get('category')
        stock = request.form.get('stock')
        tracklist = request.form.get('tracklist') if category in ['cd', 'vinyl', 'cassette'] else None
        sizes = request.form.get('sizes') if category == 'merch' else None
        
        crear_producto(user['id'], title, description, price, image_url, category, stock, tracklist, sizes)
        return redirect(url_for('store'))
        
    return render_template('publish.html', user=user)

@app.route('/perfil')
@login_required
def profile():
    user = inject_user_data()
    
    historial = []
    if user['role'] == 'client':
        historial = obtener_historial_compras(user['id'])
        
    # Obtener productos recientes
    recent_products = []
    if 'recent' in session:
        for pid in session['recent']:
            p = obtener_producto_por_id(pid)
            if p:
                recent_products.append(p)
                
    return render_template('profile.html', user=user, historial=historial, recent_products=recent_products)

@app.route('/configuracion')
@login_required
def settings():    
    user = inject_user_data()
    return render_template('settings.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)