import re


def validate_checkout(data):
    errors = []

    name = str(data.get('customer_name', '')).strip()
    email = str(data.get('customer_email', '')).strip()
    phone = str(data.get('customer_phone', '')).strip()
    items = data.get('items', [])

    if len(name) < 5:
        errors.append('El nombre completo debe tener al menos 5 caracteres.')

    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        errors.append('Correo electrónico inválido.')

    if not re.match(r'^[0-9+\-\s]{8,20}$', phone):
        errors.append('Número de teléfono inválido.')

    if not isinstance(items, list) or len(items) == 0:
        errors.append('El carrito está vacío.')

    return errors
