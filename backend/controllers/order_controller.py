from flask import jsonify, request , redirect
from models.order_model import get_all_orders
from services.order_service import place_order, build_order_items , delete_order 
from utils.validators import validate_checkout


def create_new_order():
    payload = request.get_json(silent=True) or {}
    errors = validate_checkout(payload)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    items, total = build_order_items(payload['items'])
    if not items:
        return jsonify({'success': False, 'errors': ['No se pudieron procesar los productos del carrito.']}), 400

    order_id, saved_items, saved_total = place_order(payload)
    return jsonify({
        'success': True,
        'message': 'Pedido realizado correctamente.',
        'order_id': order_id,
        'total': saved_total,
        'items': saved_items,
    }), 201


def list_orders():
    orders = get_all_orders()
    return jsonify({'success': True, 'data': orders})



def delete_order_api(order_id):
    delete_order(int(order_id))
    return {"ok": True, "message": "Pedido eliminado"}