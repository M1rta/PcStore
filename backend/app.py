from flask import Flask, jsonify
from flask_cors import CORS
from db.init_db import initialize_database
from routes.product_routes import product_bp
from routes.order_routes import order_bp

app = Flask(__name__)
CORS(app)

initialize_database()

app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(order_bp, url_prefix='/api')


@app.get('/')
def home():
    return jsonify({
        'success': True,
        'message': 'Backend de tienda PC funcionando correctamente.'
    })


if __name__ == '__main__':
    app.run(debug=True)
