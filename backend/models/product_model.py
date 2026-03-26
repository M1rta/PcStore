from db.connection import get_connection


def get_all_products(category_id=None):
    conn = get_connection()
    query = '''
        SELECT p.id, p.name, p.description, p.price, p.stock, p.image, p.category_id, c.name AS category
        FROM products p
        INNER JOIN categories c ON p.category_id = c.id
    '''
    params = []

    if category_id:
        query += ' WHERE p.category_id = ?'
        params.append(category_id)

    query += ' ORDER BY c.name ASC, p.name ASC'
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_product_by_id(product_id):
    conn = get_connection()
    row = conn.execute(
        '''
        SELECT p.id, p.name, p.description, p.price, p.stock, p.image, p.category_id, c.name AS category
        FROM products p
        INNER JOIN categories c ON p.category_id = c.id
        WHERE p.id = ?
        ''',
        (product_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None
