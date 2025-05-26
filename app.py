from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DATABASE = 'database.db'

def init_db():
    if not os.path.exists(DATABASE):
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
        print("Base de datos y tabla 'cotizaciones' creada correctamente.")
    else:
        print("Base de datos ya existente.")

@app.route('/')
def index():
    return render_template('index.html')

def get_next_cotizacion_number():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM cotizaciones')
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"COT-2025-{str(count).zfill(4)}"

def get_precio(servicio):
    precios = {
        'Constitución de empresa': 1500,
        'Defensa laboral': 2000,
        'Consultoría tributaria': 800
    }
    return precios.get(servicio, 0)

@app.route('/generar', methods=['POST'])
def generar():
    nombre = request.form['nombre']
    correo = request.form['correo']
    servicio = request.form['servicio']
    descripcion = request.form['descripcion']

    numero_cotizacion = get_next_cotizacion_number()
    precio = get_precio(servicio)
    fecha_creacion = datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cotizaciones (
            numero_cotizacion, nombre_cliente, correo, tipo_servicio, descripcion, precio, fecha_creacion
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (numero_cotizacion, nombre, correo, servicio, descripcion, precio, fecha_creacion))
    conn.commit()
    conn.close()

    cotizacion = {
        'numero_cotizacion': numero_cotizacion,
        'nombre_cliente': nombre,
        'correo': correo,
        'tipo_servicio': servicio,
        'descripcion': descripcion,
        'precio': precio,
        'fecha_creacion': fecha_creacion
    }

    print(f"Generada cotización (JSON): {cotizacion}")

    return jsonify(cotizacion)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
