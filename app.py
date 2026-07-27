import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

SUPABASE_URL = "https://mpzufzqoqtazojjupjxf.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

@app.route('/')
def home():
    if not SUPABASE_KEY:
        return jsonify({
            "status": "error",
            "message": "Revisa que la SUPABASE_KEY en Render esté configurada correctamente."
        }), 500

    return jsonify({
        "status": "online",
        "message": "Servidor activo en Render y conectado a Supabase exitosamente."
    })

@app.route('/p/<id_producto>')
def ver_producto(id_producto):
    if not SUPABASE_KEY:
        return jsonify({"error": "SUPABASE_KEY no está configurada"}), 500
    
    try:
        # Petición HTTP directa a la REST API de Supabase sin filtros de librerías intermedias
        url = f"{SUPABASE_URL}/rest/v1/productos?id=eq.{id_producto}&select=*"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return jsonify(data[0])
            else:
                return jsonify({"error": f"Producto con ID '{id_producto}' no encontrado en el almacén"}), 404
        else:
            return jsonify({"error": response.text}), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
