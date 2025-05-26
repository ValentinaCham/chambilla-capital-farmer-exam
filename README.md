# Sistema de Cotizaciones - Capital & Farmer

## Instalación
1. Clone el repositorio
2. pip install -r requirements.txt
3. python app.py
4. Para visualización de respuesta de caso: python apigeminitest.py

## Uso
- Acceder a http://localhost:5000
- Completar formulario de cotización
- Registro: Registro con un Nombre, correo electrónico y contraseña
- Login: Ingreso por medio de Correo y Contraseña
- Index: Registro de Cotizaciones

## generativeai

Se hizo la descarga de la librería, pero el peso hizo que no estuviera lista para testing y por ello se tiene el archivo extra de apigeminitest.py con una implementación.

## CONSIDERACIONES

El .env debe de contener:

API_KEY_GEMINI = [Generar Gemini API KEY]
SECRET_KEY = [Colocar cualqueir cosa]

## APIs utilizadas
- Se hizo uso de la API Key de GEmini y se trato de hacer una impooolementacion con google generative ai para hacer una ejecuión interna.

## Funcionalidades bonus
- Se hicieron validaciones con la pagian de error y el inicio de session por medio del guardado de credenciales de forma interna.
