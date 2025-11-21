from flask import Blueprint, request, jsonify
import sqlite3
from services.trie_service import TrieService
from database.connection import get_db_connection

# Crear Blueprint y servicio TRIE
palabras_bp = Blueprint('palabras', __name__)
trie_service = TrieService()

# Cargar TRIE al iniciar (esto se mejorará después)
@palabras_bp.before_app_request
def cargar_trie():
    if trie_service.total_palabras == 0:
        trie_service.cargar_desde_bd()

@palabras_bp.route('/buscar', methods=['GET'])
def buscar_palabras():
    """
    Endpoint para búsqueda con autocompletado usando TRIE
    Si no hay término, devuelve todas las palabras (para admin)
    """
    try:
        prefijo = request.args.get('termino', '').strip()
        limite = request.args.get('limit', 100, type=int)
        
        if limite > 200:
            limite = 200
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if not prefijo:
            # SIN TÉRMINO: Devolver todas las palabras ORDENADAS POR ID
            cursor.execute('''
                SELECT id, palabra, lengua, definicion, contexto_cultural 
                FROM palabras 
                ORDER BY id ASC
                LIMIT ?
            ''', (limite,))
            
            palabras = cursor.fetchall()
            
            resultados_detallados = [
                {
                    'id': p['id'],
                    'palabra': p['palabra'],
                    'idioma': p['lengua'],
                    'significado': p['definicion'],
                    'contexto_uso': p['contexto_cultural']
                }
                for p in palabras
            ]
            
        else:
            # CON TÉRMINO: Búsqueda normal con TRIE
            palabra_ids = trie_service.buscar_por_prefijo(prefijo, limite)
            
            resultados_detallados = []
            if palabra_ids:
                # CORRECCIÓN: Verificar que palabra_ids no esté vacío y sean números válidos
                valid_ids = [str(pid) for pid in palabra_ids if isinstance(pid, (int, float)) and pid > 0]
                
                if valid_ids:
                    placeholders = ','.join(['?'] * len(valid_ids))
                    query = f'''
                        SELECT id, palabra, lengua, definicion, contexto_cultural 
                        FROM palabras 
                        WHERE id IN ({placeholders})
                        ORDER BY id ASC
                    '''
                    cursor.execute(query, valid_ids)
                    palabras = cursor.fetchall()
                    
                    resultados_detallados = [
                        {
                            'id': p['id'],
                            'palabra': p['palabra'],
                            'idioma': p['lengua'],
                            'significado': p['definicion'],
                            'contexto_uso': p['contexto_cultural']
                        }
                        for p in palabras
                    ]
        
        # Registrar búsquedas para estadísticas
        from services.alerta_service import AlertaService
        alerta_service = AlertaService()
        for resultado in resultados_detallados:
            alerta_service.registrar_busqueda(resultado['id'])
        
        conn.close()
        
        return jsonify({
            'prefijo': prefijo,
            'resultados': resultados_detallados,
            'total': len(resultados_detallados),
            'limite': limite
        })
        
    except Exception as e:
        return jsonify({'error': f'Error en búsqueda: {str(e)}'}), 500

@palabras_bp.route('/', methods=['POST'])
def crear_palabra():
    """
    Endpoint para crear nueva palabra
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Datos JSON requeridos'}), 400
        
        required_fields = ['palabra', 'lengua', 'definicion']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo "{field}" es requerido'}), 400
        
        # Validar lengua
        if data['lengua'] not in ['quechua', 'aymara']:
            return jsonify({'error': 'Lengua debe ser "quechua" o "aymara"'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO palabras (palabra, lengua, definicion, contexto_cultural)
                VALUES (?, ?, ?, ?)
            ''', (
                data['palabra'].strip(),
                data['lengua'],
                data['definicion'].strip(),
                data.get('contexto_cultural', '').strip()
            ))
            
            palabra_id = cursor.lastrowid
            conn.commit()
            
            # Actualizar TRIE en memoria
            trie_service.insertar(data['palabra'], palabra_id)
            
            return jsonify({
                'mensaje': 'Palabra creada exitosamente',
                'id': palabra_id,
                'palabra': data['palabra'],
                'lengua': data['lengua']
            }), 201
            
        except sqlite3.IntegrityError:
            return jsonify({'error': 'La palabra ya existe en la base de datos'}), 400
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Error creando palabra: {str(e)}'}), 500

@palabras_bp.route('/<int:palabra_id>', methods=['GET'])
def obtener_palabra(palabra_id):
    """
    Obtener detalles completos de una palabra por ID
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, palabra, lengua, definicion, contexto_cultural, 
                   fecha_creacion, frecuencia_uso
            FROM palabras 
            WHERE id = ?
        ''', (palabra_id,))
        
        palabra = cursor.fetchone()
        
        # Registrar que se consultó esta palabra
        if palabra:
            from services.alerta_service import AlertaService
            alerta_service = AlertaService()
            alerta_service.registrar_busqueda(palabra_id)
        
        conn.close()
        
        if not palabra:
            return jsonify({'error': 'Palabra no encontrada'}), 404
        
        # Mapear campos para que coincidan con el frontend
        palabra_mapeada = {
            'id': palabra['id'],
            'palabra': palabra['palabra'],
            'idioma': palabra['lengua'],
            'significado': palabra['definicion'],
            'contexto_uso': palabra['contexto_cultural'],
            'fecha_creacion': palabra['fecha_creacion'],
            'frecuencia_uso': palabra['frecuencia_uso']
        }
        return jsonify(palabra_mapeada)
        
    except Exception as e:
        return jsonify({'error': f'Error obteniendo palabra: {str(e)}'}), 500

@palabras_bp.route('/estadisticas/trie', methods=['GET'])
def obtener_estadisticas_trie():
    """
    Obtener estadísticas del TRIE (para demostración)
    """
    return jsonify(trie_service.obtener_estadisticas())

@palabras_bp.route('/<int:palabra_id>/similares', methods=['GET'])
def obtener_palabras_similares(palabra_id):
    """
    Endpoint para obtener palabras similares usando KNN
    Ejemplo: /api/palabras/1/similares
    """
    try:
        from services.knn_service import KNNService
        
        knn = KNNService()
        knn.cargar_palabras()
        
        similares = knn.encontrar_similares(palabra_id, k=5)
        
        # Obtener detalles de las palabras similares
        conn = get_db_connection()
        cursor = conn.cursor()
        
        resultados = []
        for sim_id, score, palabra_texto in similares:
            cursor.execute(
                "SELECT id, palabra, lengua, definicion FROM palabras WHERE id = ?", 
                (sim_id,)
            )
            palabra_info = cursor.fetchone()
            if palabra_info:
                # Mapear campos para el frontend
                palabra_mapeada = {
                    'id': palabra_info['id'],
                    'palabra': palabra_info['palabra'],
                    'idioma': palabra_info['lengua'],
                    'significado': palabra_info['definicion']
                }
                resultados.append({
                    'palabra': palabra_mapeada,
                    'score_similitud': round(score, 3)
                })
        
        # Registrar que se consultó esta palabra
        from services.alerta_service import AlertaService
        alerta_service = AlertaService()
        alerta_service.registrar_busqueda(palabra_id)
        
        conn.close()
        
        return jsonify({
            'palabra_original_id': palabra_id,
            'similares': resultados,
            'total': len(resultados),
            'algoritmo': 'KNN MEJORADO (texto + lengua + contexto)'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error en KNN: {str(e)}'}), 500