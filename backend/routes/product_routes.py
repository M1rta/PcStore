from flask import Blueprint
from controllers.product_controller import list_products, product_detail, list_categories

product_bp = Blueprint('product_bp', __name__)

product_bp.route('/products', methods=['GET'])(list_products)
product_bp.route('/products/<int:product_id>', methods=['GET'])(product_detail)
product_bp.route('/categories', methods=['GET'])(list_categories)
