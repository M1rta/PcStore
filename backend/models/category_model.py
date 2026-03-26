from db.connection import get_connection


def get_all_categories():
    conn = get_connection()
    rows = conn.execute('SELECT id, name FROM categories ORDER BY name').fetchall()
    conn.close()
    return [dict(row) for row in rows]
