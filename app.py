from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/colecciones")
def colecciones():
    return render_template("colecciones.html")


@app.route("/productos", methods=["GET", "POST"])
def productos():

    mensaje = ""
    codigo = ""
    nombre = ""
    precio = ""

    productos = []

    if request.method == "POST":

        accion = request.form["accion"]
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        precio = request.form["precio"]

        conexion = sqlite3.connect("banfrancs.db")
        cursor = conexion.cursor()

        if accion == "guardar":

            cursor.execute(
                """
                INSERT INTO productos
                (codigo, nombre, precio)
                VALUES (?, ?, ?)
                """,
                (codigo, nombre, precio),
            )

            conexion.commit()
            mensaje = "Producto guardado."

        elif accion == "buscar":

            cursor.execute(
                """
                SELECT nombre, precio
                FROM productos
                WHERE codigo = ?
                """,
                (codigo,),
            )

            resultado = cursor.fetchone()

            if resultado:
                nombre = resultado[0]
                precio = resultado[1]
                mensaje = "Producto encontrado."
            else:
                mensaje = "Producto no encontrado."

        elif accion == "modificar":

            cursor.execute(
                """
                UPDATE productos
                SET nombre = ?, precio = ?
                WHERE codigo = ?
                """,
                (nombre, precio, codigo),
            )

            conexion.commit()

            if cursor.rowcount > 0:
                mensaje = "Producto modificado."
            else:
                mensaje = "Producto no encontrado."

        elif accion == "eliminar":

            cursor.execute(
                """
                DELETE FROM productos
                WHERE codigo = ?
                """,
                (codigo,),
            )

            conexion.commit()

            if cursor.rowcount > 0:
                mensaje = "Producto eliminado."

                codigo = ""
                nombre = ""
                precio = ""
            else:
                mensaje = "Producto no encontrado."

        conexion.close()

    conexion = sqlite3.connect("banfrancs.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT codigo, nombre, precio
    FROM productos
    """)

    productos = cursor.fetchall()

    conexion.close()

    return render_template(
        "productos.html",
        mensaje=mensaje,
        codigo=codigo,
        nombre=nombre,
        precio=precio,
        productos=productos,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
