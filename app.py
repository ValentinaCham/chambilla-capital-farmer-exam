from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    nombre = request.form['nombre']
    correo = request.form['correo']
    servicio = request.form['servicio']
    descripcion = request.form['descripcion']
    return f"Cotización generada para {nombre} ({servicio})"

if __name__ == '__main__':
    app.run(debug=True)