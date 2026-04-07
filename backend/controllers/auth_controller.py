from flask import jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from models.user_model import create_user, get_user_by_email, get_user_by_id


def _serialize_user(user):
    return {
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
    }


def register_user():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get('name', '')).strip()
    email = str(payload.get('email', '')).strip().lower()
    password = str(payload.get('password', ''))

    if len(name) < 2:
        return jsonify({'success': False, 'error': 'Ingresa un nombre válido.'}), 400

    if '@' not in email or '.' not in email:
        return jsonify({'success': False, 'error': 'Ingresa un correo válido.'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'error': 'La contraseña debe tener al menos 6 caracteres.'}), 400

    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({'success': False, 'error': 'Ese correo ya está registrado.'}), 409

    user_id = create_user(name, email, generate_password_hash(password))
    user = get_user_by_id(user_id)
    session['user_id'] = user_id

    return jsonify({
        'success': True,
        'message': 'Cuenta creada correctamente.',
        'user': _serialize_user(user),
    }), 201


def login_user():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get('email', '')).strip().lower()
    password = str(payload.get('password', ''))

    user = get_user_by_email(email)
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'success': False, 'error': 'Correo o contraseña incorrectos.'}), 401

    session['user_id'] = user['id']
    return jsonify({
        'success': True,
        'message': 'Sesión iniciada correctamente.',
        'user': _serialize_user(user),
    })


def get_current_session():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'authenticated': False}), 401

    user = get_user_by_id(user_id)
    if not user:
        session.pop('user_id', None)
        return jsonify({'success': False, 'authenticated': False}), 401

    return jsonify({'success': True, 'authenticated': True, 'user': _serialize_user(user)})


def logout_user():
    session.pop('user_id', None)
    return jsonify({'success': True, 'message': 'Sesión cerrada correctamente.'})
