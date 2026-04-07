import os

from flask import Flask, redirect, render_template, session, url_for
from flask_cors import CORS
from db.connection import initialize_database 
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'techhardware-dev-secret')
CORS(app, supports_credentials=True)
app.config['DB_INITIALIZED'] = False



app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(order_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')

@app.before_request
def ensure_database():
    if not app.config['DB_INITIALIZED']:
        initialize_database()
        app.config['DB_INITIALIZED'] = True


@app.get('/')
def home():
    if session.get('user_id'):
        return redirect(url_for('catalog_page'))
    return redirect(url_for('login_page'))


@app.get('/login')
def login_page():
    return render_template('login.html')


@app.get('/register')
def register_page():
    return render_template('register.html')


@app.get('/index')
def catalog_page():
    return render_template('index.html')


@app.get('/cart')
def cart_page():
    return render_template('cart.html')


@app.get('/checkout')
def checkout_page():
    return render_template('checkout.html')


@app.get('/orders')
def orders_page():
    return render_template('admin-orders.html')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
