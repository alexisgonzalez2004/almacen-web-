import os
from flask import Flask, jsonify
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://tu-proyecto.supabase.co")
# Obtenemos la clave de Render (sb_secret_...)
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Creamos un JWT mínimo sintácticamente válido únicamente para superar 
# la validación local de supabase-py al inicializar el objeto
DUMMY_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.s43d3p-a-333"

# Si SUPABASE_KEY empieza por "sb_", usamos la clave real dentro de los headers HTTP
if SUPABASE_KEY.startswith("sb_"):
    supabase: Client = create_client(
        SUPABASE_URL,
        DUMMY_JWT,  # Pasa la validación sintáctica local
        options=ClientOptions(
            headers={
                "apiKey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            }
        )
    )
else:
    # Si usaste una clave tradicional (eyJ...), la usa directamente
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Servidor activo en Render"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
