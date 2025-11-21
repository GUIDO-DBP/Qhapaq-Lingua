class KNNService:
    """KNN MEJORADO con múltiples factores de similitud"""
    
    def __init__(self):
        self.palabras_cache = {}
    
    def cargar_palabras(self):
        """Cargar palabras desde BD para KNN"""
        from database.connection import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, palabra, lengua, definicion, contexto_cultural FROM palabras")
        
        for row in cursor.fetchall():
            self.palabras_cache[row['id']] = {
                'palabra': row['palabra'],
                'lengua': row['lengua'],
                'definicion': row['definicion'],
                'contexto': row['contexto_cultural'] or ''
            }
        
        conn.close()
        print(f" KNN MEJORADO cargado con {len(self.palabras_cache)} palabras")
    
    def distancia_levenshtein(self, s1, s2):
        """Calcular distancia de Levenshtein entre dos strings"""
        if len(s1) < len(s2):
            return self.distancia_levenshtein(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous[j + 1] + 1
                deletions = current[j] + 1
                substitutions = previous[j] + (c1 != c2)
                current.append(min(insertions, deletions, substitutions))
            previous = current
        
        return previous[-1]
    
    def similitud_texto(self, texto1, texto2):
        """Similitud basada en texto de palabra"""
        distancia = self.distancia_levenshtein(texto1.lower(), texto2.lower())
        return 1 / (1 + distancia)
    
    def similitud_lengua(self, lengua1, lengua2):
        """Similitud basada en mismo lenguaje"""
        return 1.0 if lengua1 == lengua2 else 0.3
    
    def similitud_contexto(self, contexto1, contexto2):
        """Similitud basada en palabras comunes en el contexto"""
        if not contexto1 or not contexto2:
            return 0.1
        
        palabras1 = set(contexto1.lower().split())
        palabras2 = set(contexto2.lower().split())
        
        if not palabras1 or not palabras2:
            return 0.1
        
        interseccion = palabras1.intersection(palabras2)
        union = palabras1.union(palabras2)
        
        return len(interseccion) / len(union) if union else 0.1
    
    def encontrar_similares_mejorado(self, palabra_id, k=5):
        """
        KNN MEJORADO con múltiples factores:
        - Similitud de texto (40%)
        - Mismo lenguaje (30%) 
        - Contexto cultural (30%)
        """
        if palabra_id not in self.palabras_cache:
            return []
        
        palabra_objetivo = self.palabras_cache[palabra_id]
        similitudes = []
        
        for otro_id, otro_data in self.palabras_cache.items():
            if otro_id == palabra_id:
                continue
            
            # Calcular diferentes tipos de similitud
            sim_texto = self.similitud_texto(
                palabra_objetivo['palabra'], 
                otro_data['palabra']
            )
            
            sim_lengua = self.similitud_lengua(
                palabra_objetivo['lengua'],
                otro_data['lengua']
            )
            
            sim_contexto = self.similitud_contexto(
                palabra_objetivo['contexto'],
                otro_data['contexto']
            )
            
            # Combinar con pesos
            score_final = (
                sim_texto * 0.4 +      # 40% texto
                sim_lengua * 0.3 +     # 30% lenguaje
                sim_contexto * 0.3     # 30% contexto
            )
            
            similitudes.append((otro_id, score_final, otro_data['palabra']))
        
        # Ordenar por similitud y tomar top K
        similitudes.sort(key=lambda x: x[1], reverse=True)
        return similitudes[:k]
    
    def encontrar_similares(self, palabra_id, k=5):
        """Método principal - usa la versión mejorada"""
        return self.encontrar_similares_mejorado(palabra_id, k)