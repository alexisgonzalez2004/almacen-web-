import os
import requests
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

SUPABASE_URL = "https://mpzufzqoqtazojjupjxf.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Plantilla HTML visual para celulares con alerta de colores en stock
HTML_PLANTILLA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ficha: {{ p.nombre }}</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
        body { background-color: #121212; color: #e0e0e0; display: flex; justify-content: center; padding: 16px; min-height: 100vh; }
        .card { background: #1e1e1e; border-radius: 16px; width: 100%; max-width: 440px; padding: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border: 1px solid #2d2d2d; align-self: flex-start; }
        .header { text-align: center; border-bottom: 2px solid #D84315; padding-bottom: 12px; margin-bottom: 16px; }
        .header h1 { font-size: 20px; color: #ffffff; margin-bottom: 6px; word-break: break-word; }
        .badge { background: #D84315; color: #ffffff; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 700; display: inline-block; letter-spacing: 0.5px; }
        .img-container { text-align: center; margin-bottom: 16px; background: #262626; border-radius: 10px; padding: 8px; border: 1px solid #333; }
        .img-container img { max-width: 100%; max-height: 200px; border-radius: 8px; object-fit: contain; }
        .stock-box { background: #1a1a1a; border-left: 4px solid {{ color_stock }}; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #2a2a2a; }
        .stock-title { font-size: 11px; color: #b0bec5; text-transform: uppercase; font-weight: bold; }
        .stock-sub { font-size: 12px; color: #90a4ae; margin-top: 2px; }
        .stock-value { font-size: 22px; font-weight: bold; color: {{ color_stock }}; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }
        .item { background: #282828; padding: 10px 12px; border-radius: 8px; border: 1px solid #333; }
        .item-full { grid-column: span 2; }
        .label { font-size: 10px; color: #9e9e9e; text-transform: uppercase; font-weight: 600; margin-bottom: 3px; letter-spacing: 0.5px; }
        .value { font-size: 14px; font-weight: 500; color: #ffffff; word-break: break-word; }
        .footer { text-align: center; font-size: 11px; color: #666; margin-top: 8px; border-top: 1px solid #282828; padding-top: 12px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h1>{{ p.get('nombre', 'Sin Nombre') }}</h1>
            <span class="badge">ID: {{ p.get('id', '-') }}</span>
        </div>

        {% if p.get('imagen') %}
        <div class="img-container">
            <img src="{{ p.imagen }}" alt="Imagen del producto">
        </div>
        {% endif %}

        <div class="stock-box">
            <div>
                <div class="stock-title">Stock Disponible</div>
                <div class="stock-sub">Mín: {{ p.get('stock_minimo', 'N/A') }} | Reorden: {{ p.get('punto_reorden', 'N/A') }}</div>
            </div>
            <div class="stock-value">{{ p.get('stock', 0) }} pcs</div>
        </div>

        <div class="grid">
            <div class="item">
                <div class="label">N° Manufactura</div>
                <div class="value">{{ p.get('num_manufactura', '-') }}</div>
            </div>
            <div class="item">
                <div class="label">Categoría</div>
                <div class="value">{{ p.get('categoria', '-') }}</div>
            </div>
            <div class="item">
                <div class="label">Proveedor</div>
                <div class="value">{{ p.get('proveedor', '-') }}</div>
            </div>
            <div class="item">
                <div class="label">Reservado</div>
                <div class="value">{{ p.get('reservado', '-') }}</div>
            </div>
            <div class="item item-full">
                <div class="label">Descripción</div>
                <div class="value" style="font-weight: normal; color: #d6d6d6;">{{ p.get('descripcion', 'Sin descripción.') }}</div>
            </div>
        </div>

        <div class="footer">
            Sistema de Control de Almacén HNI
        </div>
    </div>
</body>
</html>
"""

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
        return "<h3>Error: SUPABASE_KEY no está configurada</h3>", 500
    
    try:
        url = f"{SUPABASE_URL}/rest/v1/productos?id=eq.{id_producto}&select=*"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                p = data[0]
                
                # Conversión segura a enteros para la comparación
                try:
                    stock = int(p.get('stock', 0))
                except (ValueError, TypeError):
                    stock = 0
                    
                try:
                    stock_minimo = int(p.get('stock_minimo', 0))
                except (ValueError, TypeError):
                    stock_minimo = -1
                    
                try:
                    punto_reorden = int(p.get('punto_reorden', 0))
                except (ValueError, TypeError):
                    punto_reorden = -1

                # Lógica de colores según tus reglas:
                if stock_minimo != -1 and stock <= stock_minimo:
                    color_stock = "#ff5252"  # Rojo (Crítico: igual o menor al stock mínimo)
                elif punto_reorden != -1 and stock <= punto_reorden:
                    color_stock = "#ffd700"  # Amarillo (Advertencia: menor o igual a reorden)
                else:
                    color_stock = "#00e676"  # Verde (Stock adecuado)

                return render_template_string(HTML_PLANTILLA, p=p, color_stock=color_stock)
            else:
                return f"<h3 style='color:white; background:#121212; padding:20px;'>Producto con ID '{id_producto}' no encontrado</h3>", 404
        else:
            return f"<h3>Error en consulta: {response.text}</h3>", response.status_code
            
    except Exception as e:
        return f"<h3>Error del servidor: {str(e)}</h3>", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
