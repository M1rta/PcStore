from db.connection import get_connection


def create_order(user_id, customer_name, customer_email, customer_phone, total, items):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO orders (user_id, customer_name, customer_email, customer_phone, total) VALUES (?, ?, ?, ?, ?)',
        (user_id, customer_name, customer_email, customer_phone, total),
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


def get_orders_by_user(user_id):
    conn = get_connection()
    orders = conn.execute(
        '''
        SELECT id, user_id, customer_name, customer_email, customer_phone, status, created_at, total
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
        '''
        ,
        (user_id,),
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


def delete_order_by_user(order_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        'SELECT id FROM orders WHERE id = ? AND user_id = ?',
        (order_id, user_id),
    ).fetchone()
    if not row:
        conn.close()
        return False

    cursor.execute('DELETE FROM order_details WHERE order_id = ?', (order_id,))
    cursor.execute('DELETE FROM orders WHERE id = ? AND user_id = ?', (order_id, user_id))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted > 0
