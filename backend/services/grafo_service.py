from collections import deque
import heapq

class GrafoService:
    def __init__(self):
        self.grafo = {}  # {palabra_id: {palabra_vecina_id: {"tipo": tipo, "peso": peso}}}
    
    def agregar_nodo(self, palabra_id):
        """Agregar un nodo al grafo"""
        if palabra_id not in self.grafo:
            self.grafo[palabra_id] = {}
    
    def agregar_arista(self, palabra_origen_id, palabra_destino_id, tipo_relacion, peso=1.0):
        """Agregar una relación entre dos palabras"""
        # Asegurarse de que ambos nodos existan
        self.agregar_nodo(palabra_origen_id)
        self.agregar_nodo(palabra_destino_id)
        
        # Agregar arista en ambas direcciones (grafo no dirigido)
        self.grafo[palabra_origen_id][palabra_destino_id] = {
            "tipo": tipo_relacion,
            "peso": peso
        }
        self.grafo[palabra_destino_id][palabra_origen_id] = {
            "tipo": tipo_relacion, 
            "peso": peso
        }
    
    def obtener_vecinos(self, palabra_id):
        """Obtener todas las palabras relacionadas con una palabra"""
        if palabra_id not in self.grafo:
            return []
        
        return [
            {
                "palabra_destino_id": vecino_id,
                "tipo_relacion": datos["tipo"],
                "peso": datos["peso"]
            }
            for vecino_id, datos in self.grafo[palabra_id].items()
        ]
    
    def dfs_traversal(self, palabra_inicio_id, max_profundidad=3):
        """Recorrido en profundidad - para explorar relaciones profundas"""
        if palabra_inicio_id not in self.grafo:
            return []
        
        visitados = set()
        resultados = []
        
        def dfs_recursivo(palabra_actual_id, profundidad, camino_actual):
            if profundidad > max_profundidad or palabra_actual_id in visitados:
                return
            
            visitados.add(palabra_actual_id)
            camino_actual.append(palabra_actual_id)
            
            if profundidad > 0:  # No incluir el nodo inicial
                resultados.append({
                    "palabra_id": palabra_actual_id,
                    "profundidad": profundidad,
                    "camino": camino_actual.copy()
                })
            
            for vecino_id in self.grafo[palabra_actual_id]:
                dfs_recursivo(vecino_id, profundidad + 1, camino_actual)
            
            camino_actual.pop()
        
        dfs_recursivo(palabra_inicio_id, 0, [])
        return resultados
    
    def bfs_traversal(self, palabra_inicio_id, max_profundidad=2):
        """Recorrido en amplitud - para relaciones cercanas"""
        if palabra_inicio_id not in self.grafo:
            return []
        
        visitados = set()
        cola = deque()
        resultados = []
        
        visitados.add(palabra_inicio_id)
        cola.append((palabra_inicio_id, 0, [palabra_inicio_id]))
        
        while cola:
            palabra_actual_id, profundidad, camino_actual = cola.popleft()
            
            if profundidad > 0 and profundidad <= max_profundidad:
                resultados.append({
                    "palabra_id": palabra_actual_id,
                    "profundidad": profundidad,
                    "camino": camino_actual
                })
            
            if profundidad < max_profundidad:
                for vecino_id in self.grafo[palabra_actual_id]:
                    if vecino_id not in visitados:
                        visitados.add(vecino_id)
                        nuevo_camino = camino_actual + [vecino_id]
                        cola.append((vecino_id, profundidad + 1, nuevo_camino))
        
        return resultados
    
    def obtener_camino_mas_corto(self, palabra_inicio_id, palabra_destino_id):
        """Encontrar el camino más corto entre dos palabras (BFS)"""
        if palabra_inicio_id not in self.grafo or palabra_destino_id not in self.grafo:
            return None
        
        if palabra_inicio_id == palabra_destino_id:
            return {
                "camino": [palabra_inicio_id],
                "longitud": 0,
                "relaciones": []
            }
        
        # BFS para camino más corto
        visitados = set()
        cola = deque()
        padres = {}
        
        visitados.add(palabra_inicio_id)
        cola.append(palabra_inicio_id)
        padres[palabra_inicio_id] = None
        
        while cola:
            actual = cola.popleft()
            
            if actual == palabra_destino_id:
                # Reconstruir camino
                camino = []
                relaciones = []
                nodo = actual
                
                while nodo is not None:
                    camino.append(nodo)
                    if padres[nodo] is not None:
                        relaciones.append({
                            "desde": padres[nodo],
                            "hacia": nodo,
                            "tipo": self.grafo[padres[nodo]][nodo]["tipo"]
                        })
                    nodo = padres[nodo]
                
                camino.reverse()
                relaciones.reverse()
                
                return {
                    "camino": camino,
                    "longitud": len(camino) - 1,
                    "relaciones": relaciones
                }
            
            for vecino in self.grafo[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = actual
                    cola.append(vecino)
        
        return None  # No hay camino
    
    def palabras_mas_relacionadas(self, top_n=10):
        """Encontrar las palabras con más conexiones (para detección de palabras importantes)"""
        conexiones = [
            (palabra_id, len(vecinos)) 
            for palabra_id, vecinos in self.grafo.items()
        ]
        
        # Ordenar por número de conexiones (descendente)
        conexiones.sort(key=lambda x: x[1], reverse=True)
        
        return conexiones[:top_n]
    
    def cargar_desde_bd(self):
        """Cargar relaciones desde la base de datos"""
        from database.connection import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT palabra_origen_id, palabra_destino_id, tipo_relacion, peso 
            FROM relaciones
        ''')
        
        relaciones_cargadas = 0
        for origen_id, destino_id, tipo, peso in cursor.fetchall():
            self.agregar_arista(origen_id, destino_id, tipo, peso)
            relaciones_cargadas += 1
        
        conn.close()
        print(f" Grafo cargado con {relaciones_cargadas} relaciones")
        return relaciones_cargadas
    
    def obtener_estadisticas(self):
        """Obtener estadísticas del grafo"""
        total_nodos = len(self.grafo)
        total_aristas = sum(len(vecinos) for vecinos in self.grafo.values()) // 2  # Dividir por 2 porque es no dirigido
        
        return {
            "total_nodos": total_nodos,
            "total_aristas": total_aristas,
            "densidad": total_aristas / (total_nodos * (total_nodos - 1) / 2) if total_nodos > 1 else 0,
            "nodo_mas_conectado": max([(nodo, len(vecinos)) for nodo, vecinos in self.grafo.items()], key=lambda x: x[1]) if self.grafo else None
        }