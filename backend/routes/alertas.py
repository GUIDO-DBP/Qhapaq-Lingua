from flask import Blueprint, request, jsonify
from services.alerta_service import AlertaService
from database.connection import get_db_connection

alertas_bp = Blueprint('alertas', __name__)
alerta_service = AlertaService()

# ========== ENDPOINTS NUEVOS PARA EL FRONTEND ==========

@alertas_bp.route('/', methods=['GET'])
def obtener_alertas():
    """Obtener todas las alertas (para el frontend)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, tipo, mensaje, nivel, palabra_id, leida, fecha_creacion
            FROM alertas 
            ORDER BY fecha_creacion DESC
        ''')
        
        alertas = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(alerta) for alerta in alertas])
        
    except Exception as e:
        return jsonify({'error': f'Error obteniendo alertas: {str(e)}'}), 500

@alertas_bp.route('/crear', methods=['POST'])
def crear_alerta():
    """Crear nueva alerta (para el frontend)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Datos JSON requeridos'}), 400
        
        required_fields = ['tipo', 'mensaje']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo "{field}" es requerido'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alertas (tipo, mensaje, nivel, palabra_id, leida)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['tipo'],
            data['mensaje'],
            data.get('nivel', 'media'),
            data.get('palabra_id'),
            data.get('leida', False)
        ))
        
        alerta_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'mensaje': 'Alerta creada exitosamente',
            'id': alerta_id,
            'tipo': data['tipo']
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error creando alerta: {str(e)}'}), 500

@alertas_bp.route('/<int:alerta_id>/leer', methods=['PUT'])
def marcar_alerta_leida(alerta_id):
    """Marcar alerta como leída (para el frontend)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alertas SET leida = TRUE 
            WHERE id = ?
        ''', (alerta_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Alerta no encontrada'}), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'mensaje': f'Alerta {alerta_id} marcada como leída',
            'id': alerta_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Error marcando alerta como leída: {str(e)}'}), 500

# ========== ENDPOINTS EXISTENTES (MANTENER) ==========

@alertas_bp.route('/palabras-riesgo', methods=['GET'])
def obtener_palabras_riesgo():
    """Obtener lista de palabras en riesgo de desaparición"""
    try:
        top_n = request.args.get('top', 10, type=int)
        
        palabras_riesgo = alerta_service.detectar_palabras_riesgo(top_n)
        
        return jsonify({
            'palabras_en_riesgo': palabras_riesgo,
            'total': len(palabras_riesgo),
            'periodo_analisis_dias': alerta_service.dias_analisis,
            'umbral_riesgo': alerta_service.umbral_riesgo
        })
        
    except Exception as e:
        return jsonify({'error': f'Error obteniendo palabras en riesgo: {str(e)}'}), 500

@alertas_bp.route('/estadisticas', methods=['GET'])
def obtener_estadisticas_generales():
    """Obtener estadísticas generales del sistema"""
    try:
        estadisticas = alerta_service.obtener_estadisticas_generales()
        
        return jsonify(estadisticas)
        
    except Exception as e:
        return jsonify({'error': f'Error obteniendo estadísticas: {str(e)}'}), 500

@alertas_bp.route('/registrar-busqueda/<int:palabra_id>', methods=['POST'])
def registrar_busqueda(palabra_id):
    """Registrar que una palabra fue buscada (para estadísticas)"""
    try:
        alerta_service.registrar_busqueda(palabra_id)
        
        return jsonify({
            'mensaje': f'Búsqueda registrada para palabra ID {palabra_id}',
            'palabra_id': palabra_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Error registrando búsqueda: {str(e)}'}), 500