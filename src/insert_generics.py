import psycopg2
import sys

db_url = 'postgresql://postgres:rBnkurpLkOpxyFnfILEgIOFWDIaeFcyE@roundhouse.proxy.rlwy.net:11950/PCDB'

sql_commands = """
INSERT INTO items (name, description, image, price, clasification, category, status_item)
VALUES 
    ('Sudadera (Personalizado)', 'Artículo genérico para pedidos de Sudaderas personalizadas', 'https://via.placeholder.com/150', 750.0, 4, 1, 1),
    ('Suéter (Personalizado)', 'Artículo genérico para pedidos de Suéteres personalizados', 'https://via.placeholder.com/150', 650.0, 4, 1, 1),
    ('Camiseta (Personalizado)', 'Artículo genérico para pedidos de Camisetas personalizadas', 'https://via.placeholder.com/150', 350.0, 1, 1, 1)
RETURNING id_item, name;
"""

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute(sql_commands)
    rows = cur.fetchall()
    conn.commit()
    for r in rows:
        print(f"Inserted: {r}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
