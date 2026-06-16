import sqlite3

conexion = sqlite3.connect("banfrancs.db")
cursor = conexion.cursor()

cursor.execute("""
SELECT usuario, password, rol
FROM usuarios
""")

for fila in cursor.fetchall():
    print(fila)

conexion.close()