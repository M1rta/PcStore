from db.connection import get_connection


def create_order(customer_name, customer_email, customer_phone, total, items):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO orders (customer_name, customer_email, customer_phone, total) VALUES (?, ?, ?, ?)',
        (customer_name, customer_email, customer_phone, total),
    )
    order_id = cursor.lastrowid

    for item in items:
        cursor.execute(
            '''
            INSERT INTO order_details (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (order_id, item['product_id'], item['quantity'], item['unit_price'], item['subtotal']),
        )

    conn.commit()
    conn.close()
    return order_id


def get_all_orders():
    conn = get_connection()
    orders = conn.execute(
        '''
        SELECT id, customer_name, customer_email, customer_phone, status, created_at, total
        FROM orders
        ORDER BY id DESC
        '''
    ).fetchall()

    result = []
    for order in orders:
        details = conn.execute(
            '''
            SELECT od.quantity, od.unit_price, od.subtotal, p.name AS product_name
            FROM order_details od
            INNER JOIN products p ON od.product_id = p.id
            WHERE od.order_id = ?
            ''',
            (order['id'],),
        ).fetchall()
        order_data = dict(order)
        order_data['items'] = [dict(detail) for detail in details]
        result.append(order_data)

    conn.close()
    return result
