from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

DATABASE = 'database.db'

def init_db():
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            fecha_registro TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Tablas aseguradas (cotizaciones y usuarios).")


@app.route('/')
def index():
    if not session.get('usuario_id'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/consulta', methods=['GET', 'POST'])
def analizar_caso():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        tipo_servicio = request.form['tipo_servicio']
        
        resultado = analizar_con_ia(descripcion, tipo_servicio)
        
        return render_template('response.html', resultado=resultado)
    else:
        return render_template('case.html')

def analizar_con_ia(descripcion, tipo_servicio):
    prompt = f"""
    Analiza este caso legal: {descripcion}
    Tipo de servicio: {tipo_servicio}
    
    Evalúa:
    1. Complejidad (Baja/Media/Alta)
    2. Ajuste de precio recomendado (0%, 25%, 50%)
    3. Servicios adicionales necesarios
    4. Genera propuesta profesional para cliente
    """
    # Aquí iría la llamada real a Gemini o la API que uses
    # Simulación de respuesta:
    return {
        'complejidad': 'Media',
        'ajuste_precio': 25,
        'servicios_adicionales': ['Revisión de contratos'],
        'propuesta_texto': 'Estimado cliente, recomendamos proceder con...'
    }

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if password != password_confirm:
            return render_template('register.html')

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM usuarios WHERE email = ?', (correo,))
        if cursor.fetchone():
            conn.close()
            return render_template('El correo ya está registrado.')

        password_hash = generate_password_hash(password)
        fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
            INSERT INTO usuarios (nombre, email, password, fecha_registro)
            VALUES (?, ?, ?, ?)
        ''', (nombre, correo, password_hash, fecha_registro))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, password FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['usuario_id'] = user[0]
            session['nombre_usuario'] = user[1]
            # return f"Bienvenido, {user[1]}. Sesión iniciada."
            return redirect(url_for('index'))
        else:
            return render_template('error.html', mensaje='Usuario o contraseña incorrectos.')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

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
