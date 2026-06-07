const express = require('express');
const path    = require('path');
 
const app  = express();
const PORT = process.env.PORT || 3000;
 
const AIRTABLE_TOKEN    = 'patGsjHZd5fEzHvLa.c1c664582c4573a9772d6a89ceafbfbd3c16e93df3ce40d0a7c954ed9e70f534';
const AIRTABLE_BASE_ID  = 'appy63hUSxVKfo3Ex';
const AIRTABLE_TABLE_ID = 'tblmf4G0OHyxAOady';
 
app.use(express.json());
app.use(express.static(__dirname));
 
// POST /api/pedido  →  guarda el pedido en Airtable
app.post('/api/pedido', async (req, res) => {
  const { cliente, contacto, correo, telefono, cp, direccion, items } = req.body;
 
  if (!items || !items.length) {
    return res.status(400).json({ success: false, error: 'Sin productos' });
  }
 
  const idPedido = 'PED-' + Date.now();
  const fecha    = new Date().toLocaleString('es-MX');
 
  // Una fila por producto
  const records = items.map((item, idx) => ({
    fields: {
      'ID Pedido':  idPedido,
      'Fecha':      fecha,
      'Cliente':    cliente    || '',
      'Contacto':   contacto   || '',
      'Correo':     correo     || '',
      'Telefono':   telefono   || '',
      'CP':         cp         || '',
      'Direccion':  direccion  || '',
      'ID Linea':   String(idx + 1),
      'SKU':        String(item.sku   || ''),
      'Producto':   item.nombre       || '',
      'Cantidad':   String(item.cantidad || 0)
    }
  }));
 
  try {
    const response = await fetch(https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/${AIRTABLE_TABLE_ID}, {
      method: 'POST',
      headers: {
        'Authorization': Bearer ${AIRTABLE_TOKEN},
        'Content-Type':  'application/json'
      },
      body: JSON.stringify({ records })
    });
 
    const result = await response.json();
    if (!response.ok) throw new Error(result.error?.message || 'Error Airtable');
 
    console.log(✅ Pedido ${idPedido} guardado (${items.length} productos));
    res.json({ success: true, id_pedido: idPedido });
  } catch (e) {
    console.error('Error Airtable:', e.message);
    res.status(500).json({ success: false, error: e.message });
  }
});
 
app.listen(PORT, () => {
  console.log(🚀 Servidor corriendo en http://localhost:${PORT});
});
