import sqlite3

conexion = sqlite3.connect("banfrancs.db")
cursor = conexion.cursor()

productos = [
    ("P001", "Polo Negro", 49.90),
    ("P002", "Polo Blanco", 44.90),
    ("P003", "Polo Azul", 54.90),

    ("P004", "Polo Negro Oversize", 39.90),
    ("P005", "Polo Blanco Oversize", 39.90),
    ("P006", "Polo Azul Oversize", 42.90),

    ("P007", "Polo Negro Clasico", 29.90),
    ("P008", "Polo Blanco Clasico", 29.90),
    ("P009", "Polo Azul Clasico", 31.90),

    ("P010", "Polo Gris Clasico", 31.90),
    ("P011", "Polo Beige Clasico", 31.90),
    ("P012", "Polo Verde Olivo", 34.90),

    ("P013", "Polo Negro Premium", 44.90),
    ("P014", "Polo Blanco Premium", 44.90),
    ("P015", "Polo Azul Premium", 46.90),

    ("P016", "Polo Gris Premium", 46.90),
    ("P017", "Polo Beige Premium", 46.90),
    ("P018", "Polo Verde Premium", 48.90),

    ("P019", "Polo Black Edition", 52.90),
    ("P020", "Polo White Edition", 52.90),
    ("P021", "Polo Blue Edition", 54.90),

    ("P022", "Polo Gold Edition", 59.90),
    ("P023", "Polo Signature BANFRANCS", 64.90),
]

cursor.executemany(
    """
    INSERT INTO productos
    (codigo, nombre, precio)
    VALUES (?, ?, ?)
    """,
    productos
)

conexion.commit()
conexion.close()

print("23 productos insertados correctamente.")