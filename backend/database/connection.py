import sqlite3
import os
from config import config

def get_db_connection():
    """Obtener conexión a la base de datos"""
    conn = sqlite3.connect(config['default'].DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializar base de datos con todas las tablas necesarias"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla de palabras (cumple con documento)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS palabras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra TEXT UNIQUE NOT NULL,
        lengua TEXT NOT NULL CHECK (lengua IN ('quechua', 'aymara')),
        definicion TEXT NOT NULL,
        contexto_cultural TEXT,
        frecuencia_uso INTEGER DEFAULT 0,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla de relaciones semánticas (para grafos)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS relaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra_origen_id INTEGER NOT NULL,
        palabra_destino_id INTEGER NOT NULL,
        tipo_relacion TEXT NOT NULL CHECK (tipo_relacion IN ('sinonimo', 'cultural', 'contextual', 'gramatical')),
        peso REAL DEFAULT 1.0 CHECK (peso >= 0 AND peso <= 1),
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (palabra_origen_id) REFERENCES palabras (id) ON DELETE CASCADE,
        FOREIGN KEY (palabra_destino_id) REFERENCES palabras (id) ON DELETE CASCADE,
        UNIQUE(palabra_origen_id, palabra_destino_id, tipo_relacion)
    )
    ''')
    
    # Tabla para estadísticas (detección de palabras en riesgo)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estadisticas_uso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra_id INTEGER NOT NULL,
        fecha DATE DEFAULT CURRENT_DATE,
        busquedas INTEGER DEFAULT 0,
        reproducciones_audio INTEGER DEFAULT 0,
        FOREIGN KEY (palabra_id) REFERENCES palabras (id) ON DELETE CASCADE,
        UNIQUE(palabra_id, fecha)
    )
    ''')
    
    # NUEVA: Tabla de alertas del sistema
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        mensaje TEXT NOT NULL,
        nivel TEXT DEFAULT 'media',
        palabra_id INTEGER,
        leida BOOLEAN DEFAULT FALSE,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (palabra_id) REFERENCES palabras (id)
    )
    ''')
    
    # NUEVAS ALERTAS MÁS SIGNIFICATIVAS PARA USUARIOS
    alertas_ejemplo = [
        # Alertas de palabras en riesgo (¡ESTAS SON LAS IMPORTANTES!)
        ('palabra_riesgo', 'Palabra "uma" (agua) muestra uso decreciente en comunidades jóvenes', 'alta', 4),
        ('palabra_riesgo', '"pacha" (tierra/mundo) requiere documentación urgente de variantes dialectales', 'alta', 3),
        ('palabra_riesgo', 'Término "awayu" (textil) necesita registro de técnicas tradicionales', 'media', 25),
        
        # Alertas de uso frecuente (interesantes para educadores)
        ('uso_frecuente', '"ayni" (reciprocidad) es el término más consultado - ideal para materiales educativos', 'baja', 1),
        ('uso_frecuente', '"suma" (armonía) genera alto interés en investigaciones académicas', 'baja', 4),
    
        # Alertas de relaciones descubiertas (valor cultural)
        ('relacion_semantica', 'Conexión cultural descubierta: "ayni" (reciprocidad) ↔ "suma" (armonía)', 'media', 1),
        ('relacion_semantica', 'Relación semántica: "pacha" (tierra) conecta con conceptos de cosmovisión andina', 'media', 3),
    ]
    
    # INSERTAR LAS NUEVAS ALERTAS (FALTABA ESTA PARTE)
    cursor.executemany('''
        INSERT OR IGNORE INTO alertas (tipo, mensaje, nivel, palabra_id)
        VALUES (?, ?, ?, ?)
    ''', alertas_ejemplo)
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente con alertas significativas")