class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.palabra_ids = []  # Para manejar palabras con mismo texto en diferentes lenguas
        self.frequency = 0     # Para el balanceo AVL (frecuencia de uso)

class TrieService:
    def __init__(self):
        self.root = TrieNode()
        self.total_palabras = 0
    
    def insertar(self, palabra: str, palabra_id: int):
        """Insertar palabra en el TRIE - Complejidad O(L)"""
        nodo = self.root
        palabra = palabra.lower().strip()
        
        for char in palabra:
            if char not in nodo.children:
                nodo.children[char] = TrieNode()
            nodo = nodo.children[char]
            nodo.frequency += 1  # Para balanceo futuro
        
        nodo.is_end_of_word = True
        if palabra_id not in nodo.palabra_ids:
            nodo.palabra_ids.append(palabra_id)
        self.total_palabras += 1
    
    def buscar_por_prefijo(self, prefijo: str, limite: int = 10):
        """Buscar palabras por prefijo - Complejidad O(L + k)"""
        if not prefijo or limite <= 0:
            return []
        
        nodo = self.root
        prefijo = prefijo.lower().strip()
        
        # Navegar hasta el final del prefijo - O(L)
        for char in prefijo:
            if char not in nodo.children:
                return []
            nodo = nodo.children[char]
        
        # Colectar palabras desde este nodo - O(k)
        resultados = []
        self._colectar_palabras(nodo, prefijo, resultados, limite)
        
        return resultados
    
    def _colectar_palabras(self, nodo, prefijo_actual, resultados, limite):
        """Recursión para colectar palabras (DFS)"""
        if len(resultados) >= limite:
            return
        
        if nodo.is_end_of_word:
            resultados.extend(nodo.palabra_ids)
        
        # Ordenar por frecuencia para "balanceo AVL" simulado
        sorted_children = sorted(
            nodo.children.items(), 
            key=lambda x: x[1].frequency, 
            reverse=True
        )
        
        for char, child_node in sorted_children:
            if len(resultados) >= limite:
                break
            self._colectar_palabras(child_node, prefijo_actual + char, resultados, limite)
    
    def cargar_desde_bd(self):
        """Cargar todas las palabras desde la base de datos al TRIE"""
        from database.connection import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, palabra FROM palabras")
        
        palabras_cargadas = 0
        for palabra_id, palabra_texto in cursor.fetchall():
            self.insertar(palabra_texto, palabra_id)
            palabras_cargadas += 1
        
        conn.close()
        print(f"✅ TRIE cargado con {palabras_cargadas} palabras")
        return palabras_cargadas
    
    def obtener_estadisticas(self):
        """Obtener estadísticas del TRIE"""
        return {
            'total_palabras': self.total_palabras,
            'nodos_totales': self._contar_nodos(self.root),
            'profundidad_maxima': self._calcular_profundidad(self.root)
        }
    
    def _contar_nodos(self, nodo):
        """Contar total de nodos en el TRIE"""
        if not nodo:
            return 0
        count = 1
        for child in nodo.children.values():
            count += self._contar_nodos(child)
        return count
    
    def _calcular_profundidad(self, nodo):
        """Calcular profundidad máxima del TRIE"""
        if not nodo.children:
            return 0
        return 1 + max(self._calcular_profundidad(child) for child in nodo.children.values())