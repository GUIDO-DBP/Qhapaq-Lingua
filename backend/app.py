from flask import Flask, jsonify
from flask_cors import CORS  # ← AGREGAR ESTA IMPORTACIÓN
from config import config
from database.connection import init_db
from routes.palabras import palabras_bp
from routes.grafos import grafos_bp
from routes.alertas import alertas_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['default'])
    
    # HABILITAR CORS TEMPORALMENTE - El proxy tiene problemas de redirección
    CORS(app, origins=["http://localhost:5173"])  # ← AGREGAR ESTA LÍNEA
    
    # Inicializar base de datos
    print(" Inicializando base de datos...")
    init_db()
    
    # Registrar blueprints (rutas API)
    app.register_blueprint(palabras_bp, url_prefix='/api/palabras')
    app.register_blueprint(grafos_bp, url_prefix='/api/grafos')
    app.register_blueprint(alertas_bp, url_prefix='/api/alertas')
    
    # Ruta de verificación de salud
    @app.route('/')
    def home():
        return jsonify({
            'mensaje': ' Qhapaq Lingua API - Backend funcionando',
            'version': '1.0',
            'desarrollador': 'Guido - Backend',
            'estado': 'COMPLETO - Listo para concurso ',
            'algoritmos_implementados': [
                'TRIE balanceado (autocompletado O(L))',
                'Grafos semánticos (DFS, BFS, caminos cortos)',
                'KNN mejorado (similitud texto + lengua + contexto)',
                'Sistema de alertas (detección palabras en riesgo)'
            ],
            'endpoints_principales': {
                'buscar_palabras': 'GET /api/palabras/buscar?termino=prefijo',
                'crear_palabra': 'POST /api/palabras/',
                'obtener_palabra': 'GET /api/palabras/<id>',
                'palabras_similares': 'GET /api/palabras/<id>/similares',
                'grafos_palabra': 'GET /api/grafos/palabra/<id>',
                'explorar_relaciones': 'GET /api/grafos/palabra/<id>/explorar?algoritmo=bfs|dfs',
                'camino_mas_corto': 'GET /api/grafos/camino?origen=X&destino=Y',
                'crear_relacion': 'POST /api/grafos/relacion',
                'estadisticas_grafo': 'GET /api/grafos/estadisticas',
                'palabras_riesgo': 'GET /api/alertas/palabras-riesgo',
                'estadisticas_sistema': 'GET /api/alertas/estadisticas',
                'registrar_busqueda': 'POST /api/alertas/registrar-busqueda/<id>',
                'obtener_alertas': 'GET /api/alertas/',
                'crear_alerta': 'POST /api/alertas/crear',
                'marcar_alerta_leida': 'PUT /api/alertas/<id>/leer'
            }
        })
    
    # Manejo de errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    print(" Servidor Flask inicializado correctamente")
    print(" Servidor corriendo en: http://127.0.0.1:5000")
    print(" Documentación API disponible en la ruta principal")
    print(" BACKEND COMPLETO - Listo para el concurso!")
    app.run(debug=True, host='0.0.0.0', port=5000)