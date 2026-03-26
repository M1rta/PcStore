from db.connection import get_connection

def ver_todos_los_pedidos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            o.id AS pedido,
            o.customer_name,
            o.customer_email,
            o.status,
            o.created_at,
            p.name AS producto,
            od.quantity,
            od.unit_price,
            od.subtotal
        FROM orders o
        JOIN order_details od ON o.id = od.order_id
        JOIN products p ON od.product_id = p.id
        ORDER BY o.id DESC
    """)

    resultados = cursor.fetchall()

    pedido_actual = None

    for fila in resultados:
        if pedido_actual != fila["pedido"]:
            pedido_actual = fila["pedido"]
            print("\n" + "=" * 60)
            print(f"Pedido: {fila['pedido']}")
            print(f"Cliente: {fila['customer_name']}")
            print(f"Email: {fila['customer_email']}")
            print(f"Estado: {fila['status']}")
            print(f"Fecha: {fila['created_at']}")
            print("Productos:")

        print(f" - {fila['producto']} | Cantidad: {fila['quantity']} | Precio: ${fila['unit_price']} | Subtotal: ${fila['subtotal']}")

    conn.close()

ver_todos_los_pedidos()