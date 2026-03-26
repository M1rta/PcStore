# Proyecto tienda local de componentes de PC

## Estructura
- `backend/` contiene Flask, rutas, modelos y base de datos SQLite.
- `frontend/` contiene HTML, CSS y JS.

## Cómo ejecutar

### 1. Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

El backend quedará en:
`http://127.0.0.1:5000`

### 2. Frontend
Abre `frontend/public/index.html` con Live Server o directamente en el navegador.

## Endpoints principales
- `GET /api/products`
- `GET /api/products/<id>`
- `GET /api/categories`
- `POST /api/orders`
- `GET /api/orders`

## Base de datos
La base se crea sola al arrancar en:
`backend/db/store.db`
