import os
from flask import Flask, jsonify
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

app = Flask(__name__)

# Configuración de credenciales desde las Variables de Entorno de Render
# NOTA: Reemplaza la URL de abajo si no la agregaste en las variables de Render
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://tu-proyecto.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inicialización de Supabase compatible con las claves de formato sb_secret_
if SUPABASE_KEY:
    supabase: Client = create_client(
        SUPABASE_URL,
        SUPABASE_KEY,
        options=ClientOptions(
            headers={"apiKey": SUPABASE_KEY}
        )
    )
else:
    supabase = None

@app.route('/')
def home():
    if not supabase:
        return jsonify({
            "status": "error",
            "message": "Falta configurar la variable SUPABASE_KEY en Render."
        }), 500

    return jsonify({
        "status": "online",
        "message": "Servidor corriendo y conectado a Supabase exitosamente."
    })

if __name__ == '__main__':
    # Puerto dinámico para Render o local (puerto 5000)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
