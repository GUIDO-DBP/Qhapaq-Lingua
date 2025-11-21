import os
import pandas as pd
import sys

# Agregar el backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def extraer_datos_simple():
    """Extraer datos de forma simple y confiable"""
    
    print(" INICIANDO EXTRACCIÓN DE DICCIONARIOS...")
    
    # Lista para guardar todas las palabras
    todas_palabras = []
    
    # === PALABRAS QUECHUA DE EJEMPLO (base inicial) ===
    palabras_quechua = [
        ("ayni", "quechua", "Trabajo comunitario recíproco", "Concepto fundamental de reciprocidad andina"),
        ("pacha", "quechua", "Tierra mundo tiempo", "Concepto cosmológico integral"),
        ("munay", "quechua", "Amor fuerza del corazón", "Energía del corazón en cosmovisión andina"),
        ("yachay", "quechua", "Saber conocimiento", "Sabiduría ancestral y aprendizaje"),
        ("llankay", "quechua", "Trabajo", "Valor del trabajo comunitario y productivo"),
        ("inti", "quechua", "Sol", "Deidad solar en cosmovisión inca"),
        ("killa", "quechua", "Luna", "Deidad lunar y ciclos agrícolas"),
        ("wawa", "quechua", "Bebé niño", "Futuro de la comunidad y descendencia"),
        ("chakra", "quechua", "Tierra de cultivo", "Relación sagrada con la agricultura"),
        ("kawsay", "quechua", "Vida existencia", "Energía vital y fuerza cósmica"),
    ]
    
    # === PALABRAS AYMARA DE EJEMPLO (base inicial) ===
    palabras_aymara = [
        ("suma", "aymara", "Bueno agradable", "Calificativo positivo en la vida comunitaria"),
        ("jach'a", "aymara", "Grande", "Referente a tamaño importancia y respeto"),
        ("uma", "aymara", "Agua", "Elemento vital en cosmovisión andina"),
        ("ampara", "aymara", "Proteger", "Cuidado comunitario y preservación"),
        ("jayma", "aymara", "Compartir", "Tradición de reciprocidad alimentaria"),
        ("khuska", "aymara", "Juntos", "Fuerza de la comunidad y unidad"),
        ("qhana", "aymara", "Claro luminoso", "Sabiduría entendimiento y claridad"),
        ("tayka", "aymara", "Madre", "Origen y protección maternal"),
        ("awki", "aymara", "Padre", "Origen y guía paternal"),
        ("jaqi", "aymara", "Persona ser humano", "Individuo en contexto comunitario"),
    ]
    
    # Agregar todas las palabras
    for palabra, lengua, definicion, contexto in palabras_quechua + palabras_aymara:
        todas_palabras.append({
            'palabra': palabra,
            'lengua': lengua,
            'definicion': definicion,
            'contexto_cultural': contexto
        })
    
    print(f" CREADAS {len(todas_palabras)} PALABRAS BASE")
    
    # === INTENTAR EXTRAER DEL PDF SI EXISTE ===
    try:
        import pdfplumber
        
        pdf_quechua = 'data/diccionarios/diccionario_quechua_real.pdf'
        pdf_aymara = 'data/diccionarios/diccionario_aymara_real.pdf'
        
        # Extraer del PDF Quechua si existe
        if os.path.exists(pdf_quechua):
            print(" EXTRAYENDO DEL PDF QUECHUA...")
            with pdfplumber.open(pdf_quechua) as pdf:
                for i, page in enumerate(pdf.pages[:10]):  # Solo primeras 10 páginas
                    texto = page.extract_text()
                    if texto:
                        lineas = texto.split('\n')
                        for linea in lineas:
                            linea = linea.strip()
                            if len(linea) > 10 and len(linea) < 100:  # Líneas de diccionario
                                # Buscar patrones simples
                                if ' - ' in linea:
                                    partes = linea.split(' - ', 1)
                                    if len(partes) == 2 and len(partes[0].strip()) > 2:
                                        palabra = partes[0].strip().lower()
                                        definicion = partes[1].strip()
                                        todas_palabras.append({
                                            'palabra': palabra,
                                            'lengua': 'quechua',
                                            'definicion': definicion[:150],
                                            'contexto_cultural': 'Extraído de diccionario oficial'
                                        })
        
        # Extraer del PDF Aymara si existe  
        if os.path.exists(pdf_aymara):
            print(" EXTRAYENDO DEL PDF AYMARA...")
            with pdfplumber.open(pdf_aymara) as pdf:
                for i, page in enumerate(pdf.pages[:10]):  # Solo primeras 10 páginas
                    texto = page.extract_text()
                    if texto:
                        lineas = texto.split('\n')
                        for linea in lineas:
                            linea = linea.strip()
                            if len(linea) > 10 and len(linea) < 100:
                                if ' - ' in linea:
                                    partes = linea.split(' - ', 1)
                                    if len(partes) == 2 and len(partes[0].strip()) > 2:
                                        palabra = partes[0].strip().lower()
                                        definicion = partes[1].strip()
                                        todas_palabras.append({
                                            'palabra': palabra,
                                            'lengua': 'aymara', 
                                            'definicion': definicion[:150],
                                            'contexto_cultural': 'Extraído de diccionario académico'
                                        })
        
    except Exception as e:
        print(f" Extracción PDF falló, usando datos base: {e}")
    
    print(f" TOTAL PALABRAS ENCONTRADAS: {len(todas_palabras)}")
    return todas_palabras

def cargar_a_bd(palabras):
    """Cargar palabras a la base de datos"""
    from database.connection import get_db_connection
    from services.trie_service import TrieService
    
    conn = get_db_connection()
    cursor = conn.cursor()
    trie = TrieService()
    
    palabras_nuevas = 0
    
    for palabra_data in palabras:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO palabras (palabra, lengua, definicion, contexto_cultural)
                VALUES (?, ?, ?, ?)
            ''', (
                palabra_data['palabra'],
                palabra_data['lengua'], 
                palabra_data['definicion'],
                palabra_data['contexto_cultural']
            ))
            
            if cursor.rowcount > 0:
                palabra_id = cursor.lastrowid
                trie.insertar(palabra_data['palabra'], palabra_id)
                palabras_nuevas += 1
                
        except Exception as e:
            continue
    
    conn.commit()
    conn.close()
    
    return palabras_nuevas

if __name__ == '__main__':
    print(" INICIANDO CARGA MASIVA DE DATOS REALES...")
    
    # 1. Extraer datos
    palabras = extraer_datos_simple()
    
    # 2. Cargar a base de datos
    nuevas = cargar_a_bd(palabras)
    
    print(f"\n CARGA COMPLETADA!")
    print(f"    Palabras procesadas: {len(palabras)}")
    print(f"    Nuevas palabras agregadas: {nuevas}")
    print(f"    Sistema actualizado exitosamente")