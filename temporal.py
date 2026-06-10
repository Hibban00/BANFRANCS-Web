import sqlite3

conexion = sqlite3.connect("banfrancs.db")
cursor = conexion.cursor()

cursor.execute("""
INSERT INTO usuarios
(usuario, password, rol)
VALUES (?, ?, ?)
""", ("Hibban00", "fl@re5oo", "admin"))

conexion.commit()
conexion.close()

print("Administrador creado")