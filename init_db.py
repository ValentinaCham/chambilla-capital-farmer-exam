import sqlite3

DATABASE = 'database.db'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cotizaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_cotizacion TEXT UNIQUE,
        nombre_cliente TEXT,
        correo TEXT,
        tipo_servicio TEXT,
        descripcion TEXT,
        precio REAL,
        fecha_creacion TEXT
    )
''')

conn.commit()
conn.close()

print("Tabla 'cotizaciones' creada correctamente.")
