import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.connection import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) as total FROM palabras")
total = cursor.fetchone()['total']

cursor.execute("SELECT lengua, COUNT(*) as cantidad FROM palabras GROUP BY lengua")
por_lengua = cursor.fetchall()

conn.close()

print(f" ESTADÍSTICAS ACTUALES:")
print(f"   TOTAL PALABRAS: {total}")
for row in por_lengua:
    print(f"   {row['lengua']}: {row['cantidad']} palabras")