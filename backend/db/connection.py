import sqlite3
import os

# Definimos la ruta de la base de datos para que siempre se cree en la carpeta 'db'
DB_PATH = os.path.join(os.path.dirname(__file__), 'store.db')

def get_connection():
    """Establece y retorna la conexión a la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# ESQUEMA Y DATOS INICIALES
# ==========================================
SCHEMA_SQL = '''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    image TEXT,
    product_url TEXT, 
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS order_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
'''

CATEGORIES = [
    'Procesadores',
    'Tarjetas Gráficas',
    'Memorias RAM',
    'Almacenamiento',
    'Motherboards',
]

# ¡URLs AGREGADAS COMO PENÚLTIMO DATO EN CADA TUPLA!
PRODUCTS = [
    ('AMD Ryzen 5 5600G', 'Procesador de 6 núcleos ideal para gaming y productividad.', 129.99, 10, 'https://i1.wp.com/i.ibb.co/CH8rZbj/AMD-RYZEN-5-4500-WITH-WRAITH-STEALTH-CO-3-RD-3-6-GHZ.jpg?w=10000&resize=10000,10000&ssl=1', 'https://www.amd.com/es/products/processors/desktops/ryzen/5000-series/amd-ryzen-5-5600g.html', 1),
    ('Intel Core i5-12400F', 'CPU con excelente rendimiento para equipos de gama media.', 159.99, 8, 'https://cyberteamcr.com/wp-content/uploads/2024/02/9ee77decfc77911a19e68a2c83f01ff2-1.webp', 'https://www.intel.la/content/www/xl/es/products/sku/134587/intel-core-i512400f-processor-18m-cache-up-to-4-40-ghz/specifications.html', 1),
    ('NVIDIA RTX 4060', 'Tarjeta gráfica moderna para juegos en 1080p y 1440p.', 349.99, 5, 'https://img.pacifiko.com/PROD/resize/1/1000x1000/NmMwMTEwZD.jpg', 'https://www.nvidia.com/es-la/geforce/graphics-cards/40-series/rtx-4060-4060ti/', 2),
    ('AMD Radeon RX 7600', 'GPU equilibrada para jugadores y creadores.', 299.99, 4, 'https://extremetechcr.com/wp-content/uploads/2024/11/28259.jpg', 'https://www.amd.com/es/products/graphics/desktops/radeon/7000-series/amd-radeon-rx-7600.html', 2),
    ('Corsair Vengeance 16GB DDR4', 'Memoria RAM 2x8GB de alto rendimiento.', 54.99, 15, 'https://c1.neweggimages.com/ProductImageCompressAll1280/20-236-701-V02.jpg', 'https://www.corsair.com/', 3),
    ('Kingston Fury 32GB DDR4', 'Memoria RAM 2x16GB para multitarea y edición.', 94.99, 12, 'https://www.intelec.co.cr/wp-content/uploads/2024/03/KF436C18BB2A.jpg', 'https://www.kingston.com/', 3),
    ('SSD NVMe 1TB WD Black', 'Unidad SSD rápida para sistema y juegos.', 89.99, 11, 'https://diamondsystemar.vtexassets.com/arquivos/ids/163426/hd-ssd-1tb-wd-black-sn850x-m2-nvme-gen4-7300mbs-0.jpg?v=638847311493300000', 'https://www.westerndigital.com/', 4),
    ('HDD Seagate 2TB', 'Disco duro para almacenamiento masivo.', 64.99, 9, 'https://extremetechcr.com/wp-content/uploads/2024/11/25505.jpg', 'https://www.seagate.com/', 4),
    ('ASUS B550M-A', 'Motherboard AM4 con gran compatibilidad.', 119.99, 6, 'https://extremetechcr.com/wp-content/uploads/2024/11/22314.jpg', 'https://www.asus.com/', 5),
    ('MSI PRO B760M', 'Tarjeta madre moderna para Intel de 12va y 13va gen.', 139.99, 7, 'https://extremetechcr.com/wp-content/uploads/2024/11/28121.jpg', 'https://www.msi.com/', 5)
]

def initialize_database():
    """Crea las tablas y pobla los datos iniciales si no existen."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)

    cursor.execute('SELECT COUNT(*) AS total FROM categories')
    if cursor.fetchone()['total'] == 0:
        cursor.executemany('INSERT INTO categories (name) VALUES (?)', [(name,) for name in CATEGORIES])

    cursor.execute('SELECT COUNT(*) AS total FROM products')
    if cursor.fetchone()['total'] == 0:
        # ¡ACTUALIZADO: 7 columnas y 7 signos de interrogación!
        cursor.executemany(
            'INSERT INTO products (name, description, price, stock, image, product_url, category_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            PRODUCTS,
        )

    conn.commit()
    conn.close()
    print("Base de datos se genero correctamente.")

# Esto te permite correr el archivo directamente desde la terminal
if __name__ == '__main__':
    initialize_database()