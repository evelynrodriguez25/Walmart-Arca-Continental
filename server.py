from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import requests
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

AIRTABLE_TOKEN = os.environ.get('AIRTABLE_TOKEN')
AIRTABLE_BASE  = os.environ.get('AIRTABLE_BASE', 'appy63hUSxVKfo3Ex')
AIRTABLE_TABLE = os.environ.get('AIRTABLE_TABLE', 'tblmf4G0OHyxAOady')
AIRTABLE_URL   = f'https://api.airtable.com/v0/{AIRTABLE_BASE}/{AIRTABLE_TABLE}'

def airtable_headers():
    return {
        'Authorization': f'Bearer {AIRTABLE_TOKEN}',
        'Content-Type': 'application/json'
    }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/pedido', methods=['POST'])
def save_pedido():
    try:
        data      = request.get_json()
        items     = data.get('items', [])
        cliente   = data.get('cliente', 'Sin nombre')
        contacto  = data.get('contacto', '')
        correo    = data.get('correo', '')
        telefono  = data.get('telefono', '')
        cp        = data.get('cp', '')
        direccion = data.get('direccion', '')

        id_pedido = f"PED-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        fecha_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        records = []
        for item in items:
            records.append({
                'fields': {
                    'ID Pedido':  id_pedido,
                    'Fecha':      fecha_now,
                    'Cliente':    cliente,
                    'Contacto':   contacto,
                    'Correo':     correo,
                    'Telefono':   telefono,
                    'CP':         cp,
                    'Direccion':  direccion,
                    'SKU':        item.get('sku', ''),
                    'Producto':   item.get('nombre', ''),
                    'Cantidad':   str(item.get('cantidad', 1))
                }
            })

        # Airtable permite max 10 records por request
        for i in range(0, len(records), 10):
            batch = records[i:i+10]
            resp = requests.post(AIRTABLE_URL, json={'records': batch}, headers=airtable_headers())
            if resp.status_code not in (200, 201):
                return jsonify({'success': False, 'error': resp.text}), 500

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