#!/bin/bash

echo "📦 Instalando dependencias de Python..."
pip install -r requirements.txt

echo "🗃️ Inicializando base de datos..."
python -c "
from database.connection import init_db
init_db()
print('✅ Base de datos inicializada')
"

echo "🚀 Backend listo para Render.com"