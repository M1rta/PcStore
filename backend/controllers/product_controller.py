from flask import jsonify, request
from models.product_model import get_all_products, get_product_by_id
from models.category_model import get_all_categories


def list_products():
    category_id = request.args.get('category_id', type=int)
    products = get_all_products(category_id)
    return jsonify({'success': True, 'data': products})


def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404
    return jsonify({'success': True, 'data': product})


def list_categories():
    categories = get_all_categories()
    return jsonify({'success': True, 'data': categories})
