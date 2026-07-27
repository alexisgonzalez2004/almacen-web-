import os
from flask import Flask, render_template_string
from supabase import create_client, Client

app = Flask(__name__)

# Credenciales de Supabase
SUPABASE_URL = "https://mpzufzqoqtazojjupjxf.supabase.co"
SUPABASE_KEY = "sb_publishable_2aykMEmM9VWpvLpnTej3FQ_o1IG0QGF" # Asegúrate de que esté tu llave completa

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Plantilla de la Ficha Técnica para el móvil
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ficha de Producto - HNI</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #1a1a1a; color: white; margin: 0; padding: 20px; }
        .card { background-color: #2b2b2b; padding: 20px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h1 { color: #D84315; font-size: 22px; border-bottom: 2px solid #D84315; padding-bottom: 10px; }
        .item { margin-bottom: 12px; }
        .label { font-weight: bold; color: #bbb; display: block; font-size: 13px; }
        .value { font-size: 16px; margin-top: 2px; }
        .badge { background-color: #D84315; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1>📦 {{ p.nombre }}</h1>
        <div class="item"><span class="label">ID / Código:</span><span class="value">{{ p.id }}</span></div>
        <div class="item"><span class="label">N° Manufactura:</span><span class="value">{{ p.num_manufactura or 'N/A' }}</span></div>
        <div class="item"><span class="label">Categoría:</span><span class="value">{{ p.categoria or 'General' }}</span></div>
        <div class="item"><span class="label">Proveedor:</span><span class="value">{{ p.proveedor or 'N/A' }}</span></div>
        <div class="item"><span class="label">Stock Físico Disponible:</span><span class="value badge">{{ p.stock }}</span></div>
        <div class="item"><span class="label">Descripción:</span><span class="value">{{ p.descripcion or 'Sin descripción' }}</span></div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return "Servidor Web del Almacén HNI en línea ✅"

@app.route('/p/<id_producto>')
def ver_producto(id_producto):
    try:
        res = supabase.table("productos").select("*").eq("id", str(id_producto)).execute()
        if not res.data:
            return "<h1>Producto no encontrado</h1><p>El código escaneado no existe en la base de datos.</p>", 404
        
        producto = res.data[0]
        return render_template_string(HTML_TEMPLATE, p=producto)
    except Exception as e:
        return f"Error en el servidor: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
