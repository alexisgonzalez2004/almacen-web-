import os
from flask import Flask, jsonify
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

app = Flask(__name__)

SUPABASE_URL = "https://mpzufzqoqtazojjupjxf.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
DUMMY_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.s43d3p-a-333"

def get_supabase_client():
    try:
        if SUPABASE_KEY.startswith("sb_"):
            return create_client(
                SUPABASE_URL,
                DUMMY_JWT,
                options=ClientOptions(
                    headers={
                        "apiKey": SUPABASE_KEY,
                        "Authorization": f"Bearer {SUPABASE_KEY}"
                    }
                )
            )
        else:
            return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error al conectar: {e}")
        return None

@app.route('/')
def home():
    client = get_supabase_client()
    if not client:
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
    client = get_supabase_client()
    if not client:
        return jsonify({"error": "Supabase no está conectado en el servidor"}), 500
    
    try:
        response = client.table('productos').select("*").eq('id', id_producto).execute()
        
        if response.data:
            return jsonify(response.data[0])
        else:
            return jsonify({"error": f"Producto con ID '{id_producto}' no encontrado en el almacén"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
