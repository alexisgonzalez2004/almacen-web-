import os
from flask import Flask, jsonify
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

app = Flask(__name__)

SUPABASE_URL = "https://mpzufzqoqtazojjupjxf.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Usamos un JWT falso meramente para superar la validación sintáctica interna de supabase-py
DUMMY_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.s43d3p-a-333"

# Inicialización segura inyectando la Secret Key real dentro de los headers de la API
try:
    if SUPABASE_KEY.startswith("sb_"):
        supabase: Client = create_client(
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
