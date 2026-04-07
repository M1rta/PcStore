from models.product_model import get_product_by_id
from models.order_model import create_order, delete_order_by_user

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


def place_order(user_id, payload):
    items, total = build_order_items(payload['items'])
    order_id = create_order(
        user_id,
        payload['customer_name'].strip(),
        payload['customer_email'].strip(),
        payload['customer_phone'].strip(),
        total,
        items,
    )
    return order_id, items, total

def delete_order(order_id: int, user_id: int):
    return delete_order_by_user(order_id, user_id)
