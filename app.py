import os
from flask import Flask, jsonify
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL = "https://mpzufzqoqtazojjupjxf.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Inicialización directa y limpia usando la llave pública
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    supabase = None
    print(f"Error al inicializar Supabase: {e}")

@app.route('/')
def home():
    if not supabase:
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
    if not supabase:
        return jsonify({"error": "Supabase no está conectado en el servidor"}), 500
    
    try:
        response = supabase.table('productos').select("*").eq('id', id_producto).execute()
        
        if response.data:
            return jsonify(response.data[0])
        else:
            return jsonify({"error": f"Producto con ID '{id_producto}' no encontrado en el almacén"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
