from flask import Blueprint, jsonify
from controllers.order_controller import create_new_order, list_orders, delete_order_api

order_bp = Blueprint('order_bp', __name__)

# Como el blueprint ya tiene url_prefix='/api', aquí NO pones /api
order_bp.route('/orders', methods=['POST'])(create_new_order)
order_bp.route('/orders', methods=['GET'])(list_orders)

@order_bp.route("/orders/<int:order_id>", methods=["DELETE"])
def api_delete_order(order_id):
    result, status_code = delete_order_api(order_id)
    return jsonify(result), status_code
