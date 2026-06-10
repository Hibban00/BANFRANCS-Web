import sqlite3

conexion = sqlite3.connect("banfrancs.db")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL DEFAULT 'usuario'
)
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")
