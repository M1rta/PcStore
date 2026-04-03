const API_URL = 'http://localhost:5000/api';

async function deleteOrder(orderId) {
  const confirmDelete = confirm(`¿Eliminar el pedido #${orderId}? Esta acción no se puede deshacer.`);
  if (!confirmDelete) return;

  try {
    const res = await fetch(`${API_URL}/orders/${orderId}`, { method: 'DELETE' });

    const text = await res.text();
    console.log("DELETE status:", res.status);
    console.log("DELETE response:", text);

    if (!res.ok) {
      alert(`Error ${res.status}: ${text}`);
      return;
    }

    alert("✅ Pedido eliminado");
    loadOrders();
  } catch (err) {
    console.error(err);
    alert("Error de conexión (revisa CORS o que el backend esté corriendo)");
  }
}

async function loadOrders() {
  const response = await fetch(`${API_URL}/orders`);
  const result = await response.json();
  const container = document.getElementById('ordersContainer');

  if (!result.data.length) {
    container.innerHTML = '<div class="empty">No hay pedidos registrados.</div>';
    return;
  }

  container.innerHTML = result.data.map(order => `
    <article class="order-card">
      <h3>Pedido #${order.id}</h3>
      <p><strong>Cliente:</strong> ${order.customer_name}</p>
      <p><strong>Correo:</strong> ${order.customer_email}</p>
      <p><strong>Teléfono:</strong> ${order.customer_phone}</p>
      <p><strong>Estado:</strong> ${order.status}</p>
      <p><strong>Fecha:</strong> ${order.created_at}</p>
      <p><strong>Total:</strong> $${Number(order.total).toFixed(2)}</p>

      <div>
        <strong>Productos:</strong>
        <ul>
          ${order.items.map(item => `<li>${item.product_name} x${item.quantity} - $${Number(item.subtotal).toFixed(2)}</li>`).join('')}
        </ul>
      </div>

      <button class="btn-delete" onclick="deleteOrder(${order.id})">
        Eliminar
      </button>
    </article>
  `).join('');
}

loadOrders();