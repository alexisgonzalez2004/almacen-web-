import os
from flask import Flask, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# URL limpia de tu proyecto en Supabase
SUPABASE_URL = "https://mpzufzqoqtazojjupjxf.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Inicialización directa compatible con las llaves nuevas
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Servidor activo en Render y conectado a Supabase"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
