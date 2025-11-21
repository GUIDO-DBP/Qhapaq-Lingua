from database.connection import get_db_connection

def crear_relaciones_ejemplo():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Relaciones de ejemplo entre palabras existentes
    relaciones = [
        # Relaciones para "awayu" (id 25)
        (25, 1, 'sinonimo', 0.8),      # awayu → awa (tejido)
        (25, 3, 'cultural', 0.6),      # awayu → pacha (tierra/mundo)
        
        # Relaciones para "pacha" (id 3)  
        (3, 15, 'sinonimo', 0.9),      # pacha → tierra
        (3, 4, 'contextual', 0.7),     # pacha → uma (agua-tierra)
        
        # Relaciones para "uma" (agua, id 4)
        (4, 25, 'contextual', 0.5),    # uma → awayu (agua-textil)
        (4, 1, 'cultural', 0.6),       # uma → awa (agua-tejido)
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO relaciones 
        (palabra_origen_id, palabra_destino_id, tipo_relacion, peso)
        VALUES (?, ?, ?, ?)
    ''', relaciones)
    
    conn.commit()
    conn.close()
    print(f"✅ {len(relaciones)} relaciones creadas")

if __name__ == '__main__':
    crear_relaciones_ejemplo()