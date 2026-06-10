import os
from flask import Flask, render_template, request, session, redirect
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "banfrancs.db")
import sqlite3

app = Flask(__name__)
app.secret_key = "banfrancs_secret_key"

@app.route("/")
def inicio():

    registro_error = request.args.get("registro_error")

    return render_template(
        "index.html",
        registro_error=registro_error
    )


@app.route("/colecciones")
def colecciones():
    return render_template("colecciones.html")


@app.route("/productos", methods=["GET", "POST"])
def productos():

    if session.get("rol") != "admin":
        return redirect("/")

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

        conexion = sqlite3.connect(DB_PATH)
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

    conexion = sqlite3.connect(DB_PATH)
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


@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():

    if session.get("rol") != "admin":
        return redirect("/")


    mensaje = ""
    usuario = ""
    password = ""

    if request.method == "POST":

        accion = request.form["accion"]
        usuario = request.form["usuario"]
        password = request.form["password"]

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        if accion == "guardar":

            cursor.execute(
                """
                INSERT INTO usuarios
                (usuario, password, rol)
                VALUES (?, ?, ?)
                """,
                (usuario, password, "usuario"),
            )

            conexion.commit()
            mensaje = "Usuario guardado."

        elif accion == "buscar":

            cursor.execute(
                """
                SELECT password
                FROM usuarios
                WHERE usuario = ?
                """,
                (usuario,),
            )

            resultado = cursor.fetchone()

            if resultado:
                password = resultado[0]
                mensaje = "Usuario encontrado."
            else:
                mensaje = "Usuario no encontrado."

        elif accion == "modificar":

            cursor.execute(
                """
                UPDATE usuarios
                SET password = ?
                WHERE usuario = ?
                """,
                (password, usuario),
            )

            conexion.commit()

            if cursor.rowcount > 0:
                mensaje = "Usuario modificado."
            else:
                mensaje = "Usuario no encontrado."

        elif accion == "eliminar":

            cursor.execute(
                """
                DELETE FROM usuarios
                WHERE usuario = ?
                """,
                (usuario,),
            )

            conexion.commit()

            if cursor.rowcount > 0:

                mensaje = "Usuario eliminado."

                usuario = ""
                password = ""

            else:
                mensaje = "Usuario no encontrado."

        conexion.close()

    return render_template(
        "usuarios.html", mensaje=mensaje, usuario=usuario, password=password
    )

@app.route("/autenticar", methods=["POST"])
def autenticar():

    
    print(request.form)

    usuario = request.form["usuario"]
    password = request.form["password"]

    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT usuario, rol
        FROM usuarios
        WHERE usuario = ?
        AND password = ?
        """,
        (usuario, password),
    )

    resultado = cursor.fetchone()

    conexion.close()

    if resultado:

        session["usuario"] = resultado[0]
        session["rol"] = resultado[1]

    return redirect("/")

@app.route("/registrar", methods=["POST"])
def registrar():

    usuario = request.form["usuario"]
    password = request.form["password"]
    confirmar = request.form["confirmar_password"]

    # Validar contraseñas
    if password != confirmar:
        return redirect("/?registro_error=password")

    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    # Verificar usuario existente
    cursor.execute(
        """
        SELECT usuario
        FROM usuarios
        WHERE usuario = ?
        """,
        (usuario,),
    )

    existe = cursor.fetchone()

    if existe:

        conexion.close()
        return render_template(
            "index.html",
            registro_error="usuario_existe"
        )

    # Registrar usuario
    cursor.execute(
        """
        INSERT INTO usuarios
        (usuario, password, rol)
        VALUES (?, ?, ?)
        """,
        (usuario, password, "usuario"),
    )

    conexion.commit()
    conexion.close()

    return redirect("/")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")    

@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
