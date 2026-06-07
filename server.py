from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import csv
from datetime import datetime
 
app = Flask(__name__, static_folder='.')
CORS(app)
 
BASE_DIR    = os.path.dirname(__file__)
PEDIDOS_CSV = os.path.join(BASE_DIR, 'pedidos_nuevos.csv')
 
CSV_HEADERS = [
    'id_pedido', 'fecha', 'status',
    'cliente', 'nombre_contacto', 'correo', 'telefono',
    'sku', 'nombre_producto', 'cantidad',
    'direccion', 'cp',
]
 
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
 
@app.route('/api/pedido', methods=['POST'])
def save_pedido():
    try:
        data     = request.get_json()
        items    = data.get('items', [])
        cliente  = data.get('cliente', 'Sin nombre')
        contacto = data.get('contacto', '')
        correo   = data.get('correo', '')
        telefono = data.get('telefono', '')
        cp       = data.get('cp', '')
        direccion= data.get('direccion', '')
 
        id_pedido = f"PED-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        fecha_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 
        file_exists = os.path.exists(PEDIDOS_CSV)
        with open(PEDIDOS_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(CSV_HEADERS)
            for item in items:
                writer.writerow([
                    id_pedido, fecha_now, 'Registrado',
                    cliente, contacto, correo, telefono,
                    item.get('sku', ''),
                    item.get('nombre', ''),
                    item.get('cantidad', 1),
                    direccion, cp,
                ])
 
        return jsonify({'success': True, 'id_pedido': id_pedido, 'total_items': len(items)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
 
if __name__ == '__main__':
    print("=" * 55)
    print("  Portal de Pedidos — Arca Continental")
    print("  Servidor: http://localhost:5000")
    print("=" * 55)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)