from flask import Blueprint, request, jsonify
from services.grafo_service import GrafoService
from database.connection import get_db_connection

grafos_bp = Blueprint('grafos', __name__)
grafo_service = GrafoService()

# Cargar grafo al iniciar
@grafos_bp.before_app_request
def cargar_grafo():
    if not grafo_service.grafo:
        grafo_service.cargar_desde_bd()

@grafos_bp.route('/palabra/<int:palabra_id>', methods=['GET'])
def obtener_relaciones_palabra(palabra_id):
    """Obtener todas las relaciones de una palabra específica"""
    try:
        # Verificar que la palabra existe
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, palabra FROM palabras WHERE id = ?", (palabra_id,))
        palabra = cursor.fetchone()
        
        if not palabra:
            conn.close()
            return jsonify({"error": "Palabra no encontrada"}), 404
        
        # Obtener relaciones del grafo
        relaciones = grafo_service.obtener_vecinos(palabra_id)
        
        # Obtener detalles de las palabras relacionadas
        relaciones_detalladas = []
        for relacion in relaciones:
            cursor.execute(
                "SELECT id, palabra, lengua, definicion FROM palabras WHERE id = ?", 
                (relacion["palabra_destino_id"],)
            )
            palabra_destino = cursor.fetchone()
            
            if palabra_destino:
                relaciones_detalladas.append({
                    "palabra_destino": dict(palabra_destino),
                    "tipo_relacion": relacion["tipo_relacion"],
                    "peso": relacion["peso"]
                })
        
        conn.close()
        
        return jsonify({
            "palabra_origen": dict(palabra),
            "relaciones": relaciones_detalladas,
            "total_relaciones": len(relaciones_detalladas)
        })
        
    except Exception as e:
        return jsonify({"error": f"Error obteniendo relaciones: {str(e)}"}), 500

@grafos_bp.route('/palabra/<int:palabra_id>/explorar', methods=['GET'])
def explorar_relaciones(palabra_id):
    """Explorar relaciones en profundidad (DFS) o amplitud (BFS)"""
    try:
        algoritmo = request.args.get('algoritmo', 'bfs')  # 'bfs' o 'dfs'
        max_profundidad = request.args.get('max_profundidad', 2, type=int)
        
        if algoritmo == 'dfs':
            resultados = grafo_service.dfs_traversal(palabra_id, max_profundidad)
        else:  # bfs por defecto
            resultados = grafo_service.bfs_traversal(palabra_id, max_profundidad)
        
        # Obtener detalles de las palabras encontradas
        conn = get_db_connection()
        cursor = conn.cursor()
        
        resultados_detallados = []
        for resultado in resultados:
            cursor.execute(
                "SELECT id, palabra, lengua FROM palabras WHERE id = ?", 
                (resultado["palabra_id"],)
            )
            palabra_info = cursor.fetchone()
            
            if palabra_info:
                # Obtener detalles del camino
                camino_detallado = []
                for camino_id in resultado["camino"]:
                    cursor.execute(
                        "SELECT id, palabra FROM palabras WHERE id = ?", 
                        (camino_id,)
                    )
                    camino_palabra = cursor.fetchone()
                    if camino_palabra:
                        camino_detallado.append(dict(camino_palabra))
                
                resultados_detallados.append({
                    "palabra": dict(palabra_info),
                    "profundidad": resultado["profundidad"],
                    "camino": camino_detallado
                })
        
        conn.close()
        
        return jsonify({
            "algoritmo": algoritmo,
            "max_profundidad": max_profundidad,
            "resultados": resultados_detallados,
            "total": len(resultados_detallados)
        })
        
    except Exception as e:
        return jsonify({"error": f"Error explorando relaciones: {str(e)}"}), 500

@grafos_bp.route('/camino', methods=['GET'])
def encontrar_camino():
    """Encontrar camino más corto entre dos palabras"""
    try:
        palabra_origen_id = request.args.get('origen', type=int)
        palabra_destino_id = request.args.get('destino', type=int)
        
        if not palabra_origen_id or not palabra_destino_id:
            return jsonify({"error": "Parámetros 'origen' y 'destino' requeridos"}), 400
        
        camino = grafo_service.obtener_camino_mas_corto(palabra_origen_id, palabra_destino_id)
        
        if not camino:
            return jsonify({"error": "No se encontró camino entre las palabras"}), 404
        
        # Obtener detalles del camino
        conn = get_db_connection()
        cursor = conn.cursor()
        
        camino_detallado = []
        for palabra_id in camino["camino"]:
            cursor.execute(
                "SELECT id, palabra, lengua, definicion FROM palabras WHERE id = ?", 
                (palabra_id,)
            )
            palabra_info = cursor.fetchone()
            if palabra_info:
                camino_detallado.append(dict(palabra_info))
        
        conn.close()
        
        return jsonify({
            "camino": camino_detallado,
            "longitud": camino["longitud"],
            "relaciones": camino["relaciones"]
        })
        
    except Exception as e:
        return jsonify({"error": f"Error encontrando camino: {str(e)}"}), 500

@grafos_bp.route('/relacion', methods=['POST'])
def crear_relacion():
    """Crear una nueva relación semántica entre palabras"""
    try:
        data = request.get_json()
        
        required_fields = ['palabra_origen_id', 'palabra_destino_id', 'tipo_relacion']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo '{field}' es requerido"}), 400
        
        # Validar tipo de relación
        tipos_validos = ['sinonimo', 'cultural', 'contextual', 'gramatical']
        if data['tipo_relacion'] not in tipos_validos:
            return jsonify({"error": f"Tipo de relación debe ser uno de: {', '.join(tipos_validos)}"}), 400
        
        # Validar que las palabras existen
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM palabras WHERE id = ?", (data['palabra_origen_id'],))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Palabra origen no encontrada"}), 404
        
        cursor.execute("SELECT id FROM palabras WHERE id = ?", (data['palabra_destino_id'],))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Palabra destino no encontrada"}), 404
        
        # Insertar en base de datos - CORREGIDO: usar 'relaciones' en lugar de 'relaciones_semanticas'
        peso = data.get('peso', 1.0)
        
        cursor.execute('''
            INSERT OR IGNORE INTO relaciones 
            (palabra_origen_id, palabra_destino_id, tipo_relacion, peso)
            VALUES (?, ?, ?, ?)
        ''', (
            data['palabra_origen_id'],
            data['palabra_destino_id'], 
            data['tipo_relacion'],
            peso
        ))
        
        conn.commit()
        conn.close()
        
        # Actualizar grafo en memoria
        grafo_service.agregar_arista(
            data['palabra_origen_id'],
            data['palabra_destino_id'],
            data['tipo_relacion'],
            peso
        )
        
        return jsonify({
            "mensaje": "Relación creada exitosamente",
            "relacion": {
                "palabra_origen_id": data['palabra_origen_id'],
                "palabra_destino_id": data['palabra_destino_id'],
                "tipo_relacion": data['tipo_relacion'],
                "peso": peso
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Error creando relación: {str(e)}"}), 500

@grafos_bp.route('/estadisticas', methods=['GET'])
def obtener_estadisticas_grafo():
    """Obtener estadísticas del grafo semántico"""
    return jsonify(grafo_service.obtener_estadisticas())

@grafos_bp.route('/top-conectadas', methods=['GET'])
def obtener_palabras_mas_conectadas():
    """Obtener las palabras con más relaciones"""
    try:
        top_n = request.args.get('top', 10, type=int)
        
        palabras_conectadas = grafo_service.palabras_mas_relacionadas(top_n)
        
        # Obtener detalles de las palabras
        conn = get_db_connection()
        cursor = conn.cursor()
        
        resultados = []
        for palabra_id, num_conexiones in palabras_conectadas:
            cursor.execute(
                "SELECT id, palabra, lengua, definicion FROM palabras WHERE id = ?", 
                (palabra_id,)
            )
            palabra_info = cursor.fetchone()
            if palabra_info:
                resultados.append({
                    "palabra": dict(palabra_info),
                    "numero_conexiones": num_conexiones
                })
        
        conn.close()
        
        return jsonify({
            "top_n": top_n,
            "palabras_mas_conectadas": resultados
        })
        
    except Exception as e:
        return jsonify({"error": f"Error obteniendo palabras conectadas: {str(e)}"}), 500