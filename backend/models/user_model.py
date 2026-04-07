from db.connection import get_connection


def create_user(name, email, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        (name, email, password_hash),
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_user_by_email(email):
    conn = get_connection()
    row = conn.execute(
        'SELECT id, name, email, password_hash, created_at FROM users WHERE email = ?',
        (email,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    conn = get_connection()
    row = conn.execute(
        'SELECT id, name, email, created_at FROM users WHERE id = ?',
        (user_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None
