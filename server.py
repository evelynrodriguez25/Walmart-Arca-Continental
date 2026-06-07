from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

def get_db():
    import psycopg2
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

def init_db():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id_pedido TEXT,
                fecha TEXT,
                status TEXT,
                cliente TEXT,
                nombre_contacto TEXT,
                correo TEXT,
                telefono TEXT,
                sku TEXT,
                nombre_producto TEXT,
                cantidad INTEGER,
                direccion TEXT,
                cp TEXT
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error init_db: {e}")

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

        conn = get_db()
        cur  = conn.cursor()
        for item in items:
            cur.execute('''
                INSERT INTO pedidos VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''', (
                id_pedido, fecha_now, 'Registrado',
                cliente, contacto, correo, telefono,
                item.get('sku', ''), item.get('nombre', ''), item.get('cantidad', 1),
                direccion, cp
            ))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'success': True, 'id_pedido': id_pedido, 'total_items': len(items)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    print("=" * 55)
    print("  Portal de Pedidos — Arca Continental")
    print("  Servidor: http://localhost:5000")
    print("=" * 55)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)
