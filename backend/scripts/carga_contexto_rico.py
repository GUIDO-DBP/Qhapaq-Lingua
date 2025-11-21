import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def cargar_dataset_mejorado():
    """Cargar dataset MEJORADO con palabras CLAVE y relaciones"""
    
    # PALABRAS CLAVE SELECCIONADAS MANUALMENTE con contexto cultural RICO
    palabras_mejoradas = [
        # === CONCEPTOS CULTURALES FUNDAMENTALES ===
        ("ayni", "quechua", "Trabajo comunitario recíproco", 
         "Sistema de ayuda mutua que fortalece los lazos comunitarios en los Andes. Base de la organización social andina."),
        
        ("pacha", "quechua", "Tierra mundo tiempo cosmos", 
         "Concepto integral que une espacio-tiempo, fundamental en la cosmovisión andina. Representa la totalidad del universo."),
        
        ("munay", "quechua", "Amor fuerza voluntad energía del corazón", 
         "Una de las tres energías fundamentales en la cosmovisión andina. Representa la fuerza del amor y la voluntad."),
        
        ("suma", "aymara", "Bueno bello armónico equilibrado", 
         "Concepto de bienestar integral que incluye belleza, bondad y equilibrio en la vida comunitaria."),
        
        ("jach'a", "aymara", "Grande importante respetado", 
         "No solo se refiere al tamaño físico, sino a la importancia y respeto en la comunidad."),

        # === SISTEMAS DE CONOCIMIENTO ===
        ("yachay", "quechua", "Saber conocimiento sabiduría", 
         "Conocimiento ancestral transmitido generacionalmente. Incluye sabiduría práctica y espiritual."),
        
        ("yatiri", "aymara", "Sabio guía espiritual", 
         "Persona que posee conocimiento ancestral y sirve como guía espiritual de la comunidad."),
        
        ("hamutay", "quechua", "Pensar reflexionar meditar", 
         "Proceso de pensamiento profundo y reflexión contemplativa valorado en la cultura andina."),

        # === RELACIONES COMUNITARIAS ===
        ("khuska", "aymara", "Juntos unidos comunidad", 
         "Fuerza que surge de la unión comunitaria. Valor fundamental del trabajo colectivo."),
        
        ("jayma", "aymara", "Compartir reciprocidad alimentaria", 
         "Tradición de compartir alimentos que fortalece los lazos familiares y comunitarios."),
        
        ("yananti", "quechua", "Ayudar colaborar cooperar", 
         "Espíritu de ayuda mutua que complementa el ayni en las relaciones comunitarias."),

        # === ELEMENTOS COSMOLÓGICOS ===
        ("inti", "quechua", "Sol deidad solar", 
         "Deidad principal en la cosmovisión inca, fuente de vida y energía."),
        
        ("killa", "quechua", "Luna deidad lunar", 
         "Deidad femenina relacionada con los ciclos agrícolas y la fertilidad."),
        
        ("uma", "aymara", "Agua vida purificación", 
         "Elemento sagrado de purificación y fuente de vida en la cosmovisión andina."),

        # === SISTEMAS DE REGISTRO ===
        ("khipu", "quechua", "Nudo registro contabilidad", 
         "Sistema de registro inca usando nudos en cuerdas. Incluía datos numéricos y narrativos."),
        
        ("kené", "quechua", "Diseño geométrico arte", 
         "Patrones geométricos en textiles que representan la cosmovisión y identidad cultural."),

        # === CONCEPTOS ECOLÓGICOS ===
        ("chakra", "quechua", "Tierra cultivable agricultura", 
         "No solo terreno de cultivo, sino relación sagrada con la Pachamama."),
        
        ("allpa", "aymara", "Tierra suelo fértil", 
         "Madre tierra como ser vivo con el que se mantiene una relación recíproca."),

        # === SABIDURÍA ANCESTRAL ===
        ("awki", "quechua", "Abuelo anciano sabio", 
         "Portador de sabiduría ancestral y memoria histórica de la comunidad."),
        
        ("awicha", "aymara", "Abuela sabiduría femenina", 
         "Guardiana de conocimientos tradicionales y sabiduría femenina ancestral."),

        # === PRÁCTICAS RITUALES ===
        ("sami", "quechua", "Suerte energía positiva bendición", 
         "Energía cósmica positiva que fluye cuando hay equilibrio y reciprocidad."),
        
        ("ch'amakani", "aymara", "Guía espiritual ritual", 
         "Persona que conduce ceremonias y rituales para mantener el equilibrio comunitario."),

        # === ALIMENTOS SAGRADOS ===
        ("papa", "quechua", "Papa alimento sagrado", 
         "No solo alimento básico, sino don sagrado de la Pachamama con profund significado cultural."),
        
        ("quínua", "aymara", "Quinua grano sagrado", 
         "Grano ancestral considerado sagrado, base de la alimentación y cultura andina."),

        # === EXPRESIONES CULTURALES ===
        ("awayu", "aymara", "Manta tejida identidad", 
         "Textil que representa identidad cultural, historia familiar y cosmovisión."),
        
        ("thaxsi", "aymara", "Tejido arte textil", 
         "Arte del tejido como expresión cultural y transmisión de conocimientos ancestrales."),

        # === CONCEPTOS TEMPORALES ===
        ("ñaupa", "quechua", "Antes pasado tradición", 
         "Tiempo ancestral que contiene la sabiduría y tradiciones de los antepasados."),
        
        ("kunan", "quechua", "Ahora presente actual", 
         "Tiempo presente donde se actualizan y revitalizan las tradiciones ancestrales."),

        # === 25 PALABRAS MÁS PARA LLEGAR A 50 MEJORADAS ===
        ("phawa", "quechua", "Soñar visión profecía", "Los sueños como medio de comunicación espiritual y fuente de visiones."),
        ("tikray", "quechua", "Transformar cambiar renovar", "Concepto de cambio cíclico y renovación en la naturaleza."),
        ("kawsay", "quechua", "Vivir existir energía vital", "Fuerza vital que anima todos los seres en la cosmovisión andina."),
        ("llankay", "quechua", "Trabajar crear producir", "Trabajo como acto creativo y de servicio a la comunidad."),
        ("muna", "quechua", "Amar querer desear", "Fuerza del deseo y el amor que motiva la acción."),
        ("rikchay", "quechua", "Reconocer recordar identificar", "Memoria colectiva y reconocimiento de la identidad."),
        ("puri", "quechua", "Caminar viajar buscar", "Camino físico y espiritual de búsqueda de conocimiento."),
        ("qaway", "quechua", "Mirar observar contemplar", "Observación profunda como forma de conocimiento."),
        ("uyariy", "quechua", "Escuchar atender comprender", "Escucha activa valorada como forma de aprendizaje."),
        ("parlay", "quechua", "Hablar comunicar expresar", "Palabra como vehículo de tradición oral y sabiduría."),
        ("chuyma", "aymara", "Corazón sentimiento emoción", "Centro emocional y moral de la persona."),
        ("ajayu", "aymara", "Alma espíritu esencia", "Principio espiritual individual en la cosmovisión aymara."),
        ("amaya", "aymara", "Alma colectiva comunidad", "Espíritu colectivo que une a la comunidad."),
        ("laru", "aymara", "Camino destino trayectoria", "Trayectoria vital individual dentro del contexto comunitario."),
        ("thakhi", "aymara", "Sendero tradición camino", "Camino tradicional que sigue la sabiduría ancestral."),
        ("uta", "aymara", "Casa hogar familia", "Espacio sagrado del núcleo familiar y la vida doméstica."),
        ("marka", "aymara", "Pueblo comunidad territorio", "Unidad social básica con territorio e identidad propia."),
        ("jilata", "aymara", "Hermano solidaridad fraternidad", "Relación de hermandad que trasciende los lazos sanguíneos."),
        ("kullaka", "aymara", "Hermana sororidad apoyo", "Relación de sororidad y apoyo mutuo entre mujeres."),
        ("wawa", "aymara", "Hijo niño futuro", "Representación del futuro y continuidad de la comunidad."),
        ("manq'a", "aymara", "Comida alimento nutrición", "Alimento como don sagrado y fuente de vida."),
        ("sarxa", "aymara", "Bailar danza celebración", "Expresión corporal de la identidad y celebración comunitaria."),
        ("jarxata", "aymara", "Cantar música tradición", "Expresión musical que transmite historia y valores."),
        ("phaxsi", "aymara", "Luna ciclo femenino", "Ciclo lunar relacionado con lo femenino y la fertilidad."),
        ("willka", "aymara", "Sol energía masculina", "Energía solar relacionada con lo masculino y la vitalidad."),
    ]
    
    from database.connection import get_db_connection
    from services.trie_service import TrieService
    
    conn = get_db_connection()
    cursor = conn.cursor()
    trie = TrieService()
    
    nuevas = 0
    for palabra, lengua, definicion, contexto in palabras_mejoradas:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO palabras (palabra, lengua, definicion, contexto_cultural)
                VALUES (?, ?, ?, ?)
            ''', (palabra, lengua, definicion, contexto))
            
            if cursor.rowcount > 0:
                palabra_id = cursor.lastrowid
                trie.insertar(palabra, palabra_id)
                nuevas += 1
        except Exception as e:
            continue
    
    conn.commit()
    conn.close()
    return nuevas

def crear_relaciones_ricas():
    """Crear relaciones semánticas ENRIQUECIDAS entre conceptos clave"""
    
    from database.connection import get_db_connection
    from services.grafo_service import GrafoService
    
    conn = get_db_connection()
    cursor = conn.cursor()
    grafo = GrafoService()
    
    # RELACIONES SEMÁNTICAS ENRIQUECIDAS
    relaciones = [
        # CONCEPTOS FUNDAMENTALES INTERRELACIONADOS
        ("ayni", "yananti", "complementariedad", 0.9),
        ("ayni", "khuska", "reciprocidad", 0.8),
        ("pacha", "allpa", "cosmovision", 0.9),
        ("pacha", "kawsay", "vitalidad", 0.8),
        
        # SISTEMAS DE CONOCIMIENTO
        ("yachay", "yatiri", "sabiduria", 0.9),
        ("yachay", "hamutay", "reflexion", 0.8),
        ("yatiri", "ch'amakani", "liderazgo", 0.7),
        
        # ELEMENTOS COSMOLÓGICOS
        ("inti", "killa", "complementariedad", 0.9),
        ("inti", "willka", "solar", 0.8),
        ("killa", "phaxsi", "lunar", 0.8),
        
        # SABIDURÍA ANCESTRAL
        ("awki", "awicha", "sabiduria", 0.9),
        ("awki", "yachay", "conocimiento", 0.8),
        ("awicha", "yatiri", "guia", 0.7),
        
        # PRÁCTICAS CULTURALES
        ("awayu", "thaxsi", "textil", 0.9),
        ("khipu", "kené", "registro", 0.7),
        ("sami", "phawa", "energia", 0.6),
    ]
    
    relaciones_creadas = 0
    
    for palabra1, palabra2, tipo, peso in relaciones:
        try:
            # Buscar IDs
            cursor.execute("SELECT id FROM palabras WHERE palabra = ?", (palabra1,))
            id1 = cursor.fetchone()
            cursor.execute("SELECT id FROM palabras WHERE palabra = ?", (palabra2,))
            id2 = cursor.fetchone()
            
            if id1 and id2:
                cursor.execute('''
                    INSERT OR IGNORE INTO relaciones_semanticas 
                    (palabra_origen_id, palabra_destino_id, tipo_relacion, peso)
                    VALUES (?, ?, ?, ?)
                ''', (id1['id'], id2['id'], tipo, peso))
                
                grafo.agregar_arista(id1['id'], id2['id'], tipo, peso)
                relaciones_creadas += 1
        except:
            continue
    
    conn.commit()
    conn.close()
    return relaciones_creadas

if __name__ == '__main__':
    print("🚀 CARGANDO DATASET MEJORADO CON CONTEXTO CULTURAL RICO...")
    
    # 1. Cargar palabras mejoradas
    nuevas_palabras = cargar_dataset_mejorado()
    
    # 2. Crear relaciones enriquecidas
    nuevas_relaciones = crear_relaciones_ricas()
    
    print(f"🎉 OPCIÓN C COMPLETADA!")
    print(f"    Nuevas palabras MEJORADAS: {nuevas_palabras}")
    print(f"    Relaciones ENRIQUECIDAS: {nuevas_relaciones}")
    print(f"    Total estimado: {134 + nuevas_palabras} palabras")
    print(f"    ¡Sistema con datos CULTURALMENTE RICOS!")