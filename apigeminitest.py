# legal_analysis_gemini.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

# Configurar Gemini
API_KEY_GEMINI = os.getenv('API_KEY_GEMINI')
genai.configure(api_key=API_KEY_GEMINI)

# Configuración del modelo
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def analizar_con_ia(descripcion, tipo_servicio):
    prompt = f"""
    Eres un experto analista legal. Analiza este caso con precisión y profesionalismo.
    
    Caso legal: {descripcion}
    Tipo de servicio: {tipo_servicio}
    
    Proporciona un análisis estructurado con:
    1. Complejidad (Baja/Media/Alta) - Considera factores legales, documentación requerida y tiempo estimado
    2. Ajuste de precio recomendado (0%, 25%, 50%) - Basado en complejidad y horas estimadas
    3. Servicios adicionales necesarios - Lista de posibles servicios complementarios
    4. Propuesta profesional - Texto bien redactado para enviar al cliente
    
    Devuelve el análisis en formato JSON con las claves: complejidad, ajuste_precio, servicios_adicionales, propuesta_texto
    """
    
    try:
        response = model.generate_content(prompt)
        
        # Procesar la respuesta para extraer el JSON
        # Gemini puede devolver texto plano que parece JSON, necesitamos extraerlo
        response_text = response.text
        
        # Buscar el JSON en la respuesta (puede venir con marcas ```json)
        if '```json' in response_text:
            json_str = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            json_str = response_text.split('```')[1].split('```')[0].strip()
        else:
            json_str = response_text.strip()
        
        # Convertir a diccionario (aquí deberías implementar un manejo de errores más robusto)
        import json
        analysis_result = json.loads(json_str)
        
        return analysis_result
    
    except Exception as e:
        print(f"Error al analizar con Gemini: {str(e)}")
        return {
            'complejidad': 'Media',
            'ajuste_precio': 25,
            'servicios_adicionales': ['Revisión de contratos'],
            'propuesta_texto': 'Texto profesional generado por IA...'
        }

# Ejemplo de uso
if __name__ == "__main__":
    ejemplo_descripcion = "Cliente necesita ayuda con despido injustificado, tiene pruebas documentales pero la empresa alega faltas disciplinarias."
    ejemplo_tipo = "Laboral"
    
    resultado = analizar_con_ia(ejemplo_descripcion, ejemplo_tipo)
    print("Resultado del análisis:")
    print(f"Complejidad: {resultado['complejidad']}")
    print(f"Ajuste de precio: {resultado['ajuste_precio']}%")
    print(f"Servicios adicionales: {', '.join(resultado['servicios_adicionales'])}")
    print("\nPropuesta:")
    print(resultado['propuesta_texto'])