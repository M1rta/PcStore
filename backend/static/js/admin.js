const API_URL = '/api';

function updateUserUI(user) {
  const welcomeUser = document.getElementById('welcomeUser');
  if (welcomeUser) {
    welcomeUser.textContent = `Hola, ${user.name}`;
  }
}

async function requireSession() {
  const response = await fetch(`${API_URL}/auth/session`, {
    credentials: 'include',
  });

  if (!response.ok) {
    localStorage.removeItem('pc_store_user');
    window.location.href = '/login';
    throw new Error('Usuario no autenticado');
  }

  const result = await response.json();
  localStorage.setItem('pc_store_user', JSON.stringify(result.user));
  updateUserUI(result.user);
}

async function logout() {
  await fetch(`${API_URL}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  localStorage.removeItem('pc_store_user');
  window.location.href = '/login';
}

async function deleteOrder(orderId) {
  const confirmDelete = confirm(`Eliminar el pedido #${orderId}? Esta accion no se puede deshacer.`);
  if (!confirmDelete) return;

  try {
    const response = await fetch(`${API_URL}/orders/${orderId}`, {
      method: 'DELETE',
      credentials: 'include',
    });

    const result = await response.json().catch(() => ({}));
    if (!response.ok) {
      alert(result.message || 'No se pudo eliminar el pedido.');
      return;
    }

    alert('Pedido eliminado correctamente.');
    loadOrders();
  } catch (error) {
    console.error(error);
    alert('Error de conexion con el servidor.');
  }
}

async function loadOrders() {
  const response = await fetch(`${API_URL}/orders`, {
    credentials: 'include',
  });
  const result = await response.json();
  const container = document.getElementById('ordersContainer');

  if (!response.ok) {
    container.innerHTML = '<div class="empty">No se pudieron cargar tus pedidos.</div>';
    return;
  }

  if (!result.data.length) {
    container.innerHTML = '<div class="empty">Todavia no has realizado pedidos.</div>';
    return;
  }

  container.innerHTML = result.data.map((order) => `
    <article class="order-card">
      <h3>Pedido #${order.id}</h3>
      <p><strong>Cliente:</strong> ${order.customer_name}</p>
      <p><strong>Correo:</strong> ${order.customer_email}</p>
      <p><strong>Telefono:</strong> ${order.customer_phone}</p>
      <p><strong>Estado:</strong> ${order.status}</p>
      <p><strong>Fecha:</strong> ${order.created_at}</p>
      <p><strong>Total:</strong> $${Number(order.total).toFixed(2)}</p>

      <div>
        <strong>Productos:</strong>
        <ul>
          ${order.items.map((item) => `<li>${item.product_name} x${item.quantity} - $${Number(item.subtotal).toFixed(2)}</li>`).join('')}
        </ul>
      </div>

      <button class="btn-delete" onclick="deleteOrder(${order.id})">
        Eliminar
      </button>
    </article>
  `).join('');
}

window.deleteOrder = deleteOrder;

(async function init() {
  await requireSession();
  document.getElementById('logoutBtn')?.addEventListener('click', logout);
  loadOrders();
})();
