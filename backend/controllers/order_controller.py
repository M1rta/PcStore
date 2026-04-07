from flask import jsonify, request, session
from models.order_model import get_orders_by_user
from services.order_service import place_order, build_order_items , delete_order 
from utils.validators import validate_checkout


def create_new_order():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'errors': ['Debes iniciar sesión para hacer un pedido.']}), 401

    payload = request.get_json(silent=True) or {}
    errors = validate_checkout(payload)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    items, total = build_order_items(payload['items'])
    if not items:
        return jsonify({'success': False, 'errors': ['No se pudieron procesar los productos del carrito.']}), 400

    order_id, saved_items, saved_total = place_order(user_id, payload)
    return jsonify({
        'success': True,
        'message': 'Pedido realizado correctamente.',
        'order_id': order_id,
        'total': saved_total,
        'items': saved_items,
    }), 201


def list_orders():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'errors': ['Debes iniciar sesión para ver tus pedidos.']}), 401

    orders = get_orders_by_user(user_id)
    return jsonify({'success': True, 'data': orders})



def delete_order_api(order_id):
    user_id = session.get('user_id')
    if not user_id:
        return {"ok": False, "message": "Debes iniciar sesión"}, 401

    deleted = delete_order(int(order_id), int(user_id))
    if not deleted:
        return {"ok": False, "message": "Pedido no encontrado para este usuario"}, 404

    return {"ok": True, "message": "Pedido eliminado"}, 200
