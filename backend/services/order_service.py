from models.product_model import get_product_by_id
from models.order_model import create_order
from db.connection import get_connection

def build_order_items(cart_items):
    normalized_items = []
    total = 0.0

    for item in cart_items:
        product_id = int(item.get('product_id', 0))
        quantity = int(item.get('quantity', 0))
        if product_id <= 0 or quantity <= 0:
            continue

        product = get_product_by_id(product_id)
        if not product:
            continue

        subtotal = round(product['price'] * quantity, 2)
        total += subtotal
        normalized_items.append({
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': product['price'],
            'subtotal': subtotal,
            'name': product['name'],
        })

    return normalized_items, round(total, 2)


def place_order(payload):
    items, total = build_order_items(payload['items'])
    order_id = create_order(
        payload['customer_name'].strip(),
        payload['customer_email'].strip(),
        payload['customer_phone'].strip(),
        total,
        items,
    )
    return order_id, items, total
# backend/services/orders_service.py  (ajusta el nombre si tu archivo se llama distinto)

def delete_order(order_id: int):
    conn = get_connection()
    cur = conn.cursor()

    # primero borrar detalle
    cur.execute("DELETE FROM order_details WHERE order_id = ?", (order_id,))
    # luego borrar pedido
    cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))

    conn.commit()
    conn.close()