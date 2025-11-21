import sqlite3
from datetime import datetime, timedelta
from database.connection import get_db_connection

class AlertaService:
    """Servicio para detectar palabras en riesgo de desaparición"""
    
    def __init__(self):
        self.umbral_riesgo = 0.1  # Umbral para considerar en riesgo (10%)
        self.dias_analisis = 30   # Período de análisis en días
    
    def registrar_busqueda(self, palabra_id):
        """Registrar que una palabra fue buscada"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            fecha_hoy = datetime.now().date()
            
            # Verificar si ya existe registro para hoy
            cursor.execute('''
                SELECT id FROM estadisticas_uso 
                WHERE palabra_id = ? AND fecha = ?
            ''', (palabra_id, fecha_hoy))
            
            existe = cursor.fetchone()
            
            if existe:
                # Incrementar búsquedas
                cursor.execute('''
                    UPDATE estadisticas_uso 
                    SET busquedas = busquedas + 1 
                    WHERE palabra_id = ? AND fecha = ?
                ''', (palabra_id, fecha_hoy))
            else:
                # Crear nuevo registro
                cursor.execute('''
                    INSERT INTO estadisticas_uso (palabra_id, fecha, busquedas)
                    VALUES (?, ?, 1)
                ''', (palabra_id, fecha_hoy))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Error registrando búsqueda: {e}")
    
    def calcular_estadisticas_uso(self):
        """Calcular estadísticas de uso para todas las palabras"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener fecha límite (últimos N días)
        fecha_limite = (datetime.now() - timedelta(days=self.dias_analisis)).date()
        
        # Estadísticas por palabra
        cursor.execute('''
            SELECT 
                p.id,
                p.palabra,
                p.lengua,
                COALESCE(SUM(e.busquedas), 0) as total_busquedas,
                COUNT(DISTINCT e.fecha) as dias_con_uso,
                MAX(e.fecha) as ultima_busqueda
            FROM palabras p
            LEFT JOIN estadisticas_uso e ON p.id = e.palabra_id AND e.fecha >= ?
            GROUP BY p.id, p.palabra, p.lengua
            ORDER BY total_busquedas DESC
        ''', (fecha_limite,))
        
        estadisticas = []
        for row in cursor.fetchall():
            estadisticas.append({
                'palabra_id': row['id'],
                'palabra': row['palabra'],
                'lengua': row['lengua'],
                'total_busquedas': row['total_busquedas'],
                'dias_con_uso': row['dias_con_uso'],
                'ultima_busqueda': row['ultima_busqueda'],
                'frecuencia_promedio': row['total_busquedas'] / self.dias_analisis if self.dias_analisis > 0 else 0
            })
        
        conn.close()
        return estadisticas
    
    def detectar_palabras_riesgo(self, top_n=10):
        """
        Detectar palabras en riesgo basado en:
        - Baja frecuencia de uso
        - Mucho tiempo sin ser consultadas
        - Pocos días de actividad
        """
        estadisticas = self.calcular_estadisticas_uso()
        
        if not estadisticas:
            return []
        
        # Calcular métricas de riesgo
        max_busquedas = max(stat['total_busquedas'] for stat in estadisticas)
        palabras_riesgo = []
        
        for stat in estadisticas:
            if max_busquedas == 0:  # Evitar división por cero
                score_riesgo = 1.0
            else:
                # Score basado en múltiples factores
                factor_frecuencia = 1 - (stat['total_busquedas'] / max_busquedas)
                
                # Factor de antigüedad (si no se usa hace mucho)
                factor_antiguedad = 0
                if stat['ultima_busqueda']:
                    dias_desde_uso = (datetime.now().date() - datetime.strptime(stat['ultima_busqueda'], '%Y-%m-%d').date()).days
                    factor_antiguedad = min(dias_desde_uso / self.dias_analisis, 1.0)
                
                # Factor de consistencia (pocos días de uso)
                factor_consistencia = 1 - (stat['dias_con_uso'] / self.dias_analisis)
                
                # Score final de riesgo (0-1, donde 1 es máximo riesgo)
                score_riesgo = (
                    factor_frecuencia * 0.5 +      # 50% frecuencia
                    factor_antiguedad * 0.3 +      # 30% antigüedad  
                    factor_consistencia * 0.2      # 20% consistencia
                )
            
            # Solo incluir si supera el umbral de riesgo
            if score_riesgo >= self.umbral_riesgo:
                palabras_riesgo.append({
                    **stat,
                    'score_riesgo': round(score_riesgo, 3),
                    'nivel_riesgo': self._clasificar_riesgo(score_riesgo)
                })
        
        # Ordenar por score de riesgo (descendente)
        palabras_riesgo.sort(key=lambda x: x['score_riesgo'], reverse=True)
        return palabras_riesgo[:top_n]
    
    def _clasificar_riesgo(self, score):
        """Clasificar el nivel de riesgo"""
        if score >= 0.8:
            return "CRÍTICO"
        elif score >= 0.6:
            return "ALTO" 
        elif score >= 0.4:
            return "MEDIO"
        elif score >= 0.2:
            return "BAJO"
        else:
            return "MINIMO"
    
    def obtener_estadisticas_generales(self):
        """Obtener estadísticas generales del sistema"""
        estadisticas = self.calcular_estadisticas_uso()
        
        if not estadisticas:
            return {}
        
        total_palabras = len(estadisticas)
        palabras_con_uso = sum(1 for s in estadisticas if s['total_busquedas'] > 0)
        total_busquedas = sum(s['total_busquedas'] for s in estadisticas)
        
        palabras_riesgo = self.detectar_palabras_riesgo()
        
        return {
            'total_palabras': total_palabras,
            'palabras_con_uso': palabras_con_uso,
            'porcentaje_uso': round((palabras_con_uso / total_palabras) * 100, 1),
            'total_busquedas': total_busquedas,
            'palabras_en_riesgo': len(palabras_riesgo),
            'porcentaje_riesgo': round((len(palabras_riesgo) / total_palabras) * 100, 1),
            'periodo_analisis_dias': self.dias_analisis
        }