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

    return render_template("index.html", registro_error=registro_error)


@app.route("/colecciones")
def colecciones():
    return render_template("colecciones.html")


@app.route("/admindedatos", methods=["GET", "POST"])
def admindedatos():

    if session.get("rol") != "admin":
        return redirect("/")

    mensaje = ""

    codigo = ""
    nombre = ""
    precio = ""

    usuario = ""
    password = ""
    rol = "usuario"

    productos = []

    total_productos = 0
    precio_promedio = 0
    total_usuarios = 0
    total_admins = 0
    total_normales = 0

    productos_top = []

    rango1 = 0
    rango2 = 0
    rango3 = 0

    seccion = request.args.get("seccion")

    if request.method == "POST":

        accion_producto = request.form.get("accion_producto")
        accion_usuario = request.form.get("accion_usuario")

        if accion_producto:
            print("CRUD PRODUCTOS")
            codigo = request.form.get("codigo")
            nombre = request.form.get("nombre")
            precio = request.form.get("precio")

            print(codigo)
            print(nombre)
            print(precio)

            if accion_producto == "guardar":
                precio_valido = True

                try:
                    precio_num = float(precio)

                    if precio_num <= 0:
                        mensaje = "El precio debe ser mayor a cero."
                        precio_valido = False

                except ValueError:
                    mensaje = "Ingrese un precio válido."
                    precio_valido = False

                if not codigo.strip():
                    mensaje = "El código es obligatorio."

                elif not nombre.strip():
                    mensaje = "El nombre es obligatorio."

                elif not precio.strip():
                    mensaje = "El precio es obligatorio."

                elif not precio_valido:
                    pass

                else:
                    conexion = sqlite3.connect(DB_PATH)
                    cursor = conexion.cursor()

                    cursor.execute(
                        """
                        SELECT codigo
                        FROM productos
                        WHERE codigo = ?
                        """,
                        (codigo,),
                    )

                    existe = cursor.fetchone()

                    if existe:

                        mensaje = "El código ya existe."

                    else:

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

                    conexion.close()

            elif accion_producto == "buscar":

                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()

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

                conexion.close()
            elif accion_producto == "modificar":

                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()

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

                conexion.close()

            elif accion_producto == "eliminar":

                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()

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

            elif accion_producto == "dashboard":
                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM productos
                """)

                total_productos = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT AVG(precio)
                    FROM productos
                """)

                promedio = cursor.fetchone()[0]

                if promedio:
                    precio_promedio = round(promedio, 2)
                else:
                    precio_promedio = 0

                mensaje = "dashboard"

                conexion.close()

        if accion_usuario:

            print("CRUD USUARIOS")

            usuario = request.form.get("usuario")
            password = request.form.get("password")
            rol = request.form.get("rol")

            print(usuario)
            print(password)

            if accion_usuario == "guardar":
                if not usuario.strip():
                    mensaje = "El usuario es obligatorio."

                elif not password.strip():
                    mensaje = "La contraseña es obligatoria."

                elif len(password) < 4:
                    mensaje = "La contraseña debe tener al menos 4 caracteres."

                else:

                    conexion = sqlite3.connect(DB_PATH)
                    cursor = conexion.cursor()

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

                        mensaje = "El usuario ya existe."

                    else:

                        cursor.execute(
                            """
                            INSERT INTO usuarios
                            (usuario, password, rol)
                            VALUES (?, ?, ?)
                            """,
                            (usuario, password, rol),
                        )

                        conexion.commit()

                        mensaje = "Usuario guardado."

                    conexion.close()

            elif accion_usuario == "buscar":

                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()

                cursor.execute(
                    """
                    SELECT password, rol
                    FROM usuarios
                    WHERE usuario = ?
                    """,
                    (usuario,),
                )

                resultado = cursor.fetchone()

                if resultado:

                    password = resultado[0]
                    rol = resultado[1]

                    mensaje = "Usuario encontrado."

                else:

                    mensaje = "Usuario no encontrado."

                conexion.close()

            elif accion_usuario == "modificar":

                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()

                cursor.execute(
                    """
                    UPDATE usuarios
                    SET password = ?, rol = ?
                    WHERE usuario = ?
                    """,
                    (password, rol, usuario),
                )

                conexion.commit()

                if cursor.rowcount > 0:

                    mensaje = "Usuario modificado."

                else:

                    mensaje = "Usuario no encontrado."

                conexion.close()

            elif accion_usuario == "eliminar":

                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()

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

            elif accion_usuario == "resumen":

                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM usuarios
                """)

                total_usuarios = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM usuarios
                    WHERE rol = 'admin'
                """)

                total_admins = cursor.fetchone()[0]

                total_normales = total_usuarios - total_admins

                mensaje = "resumen_usuarios"

                conexion.close()

        print("Producto:", accion_producto)
        print("Usuario:", accion_usuario)

    if seccion == "dashboard":

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Productos
        cursor.execute("""
            SELECT COUNT(*)
            FROM productos
        """)

        total_productos = cursor.fetchone()[0]

        # Usuarios
        cursor.execute("""
            SELECT COUNT(*)
            FROM usuarios
        """)

        total_usuarios = cursor.fetchone()[0]

        # Administradores
        cursor.execute("""
            SELECT COUNT(*)
            FROM usuarios
            WHERE rol = 'admin'
        """)

        total_admins = cursor.fetchone()[0]

        # Usuarios normales
        total_normales = total_usuarios - total_admins

        # Top 5 productos más caros
        cursor.execute("""
            SELECT nombre, precio, codigo
            FROM productos
            ORDER BY precio DESC
            LIMIT 5
        """)

        productos_top = cursor.fetchall()

        # Rangos de precio
        cursor.execute("""
            SELECT COUNT(*)
            FROM productos
            WHERE precio <= 35
        """)

        rango1 = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM productos
            WHERE precio > 35
            AND precio <= 50
        """)

        rango2 = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM productos
            WHERE precio > 50
        """)

        rango3 = cursor.fetchone()[0]

        conexion.close()

    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT codigo, nombre, precio
    FROM productos
    """)

    productos = cursor.fetchall()

    cursor.execute("""
    SELECT usuario, rol
    FROM usuarios
    """)

    usuarios = cursor.fetchall()    

    conexion.close()

    return render_template(
        "admindedatos.html",
        seccion=seccion,
        mensaje=mensaje,
        codigo=codigo,
        nombre=nombre,
        precio=precio,
        productos=productos,
        usuarios=usuarios,
        usuario=usuario,
        password=password,
        total_productos=total_productos,
        precio_promedio=precio_promedio,
        total_usuarios=total_usuarios,
        total_admins=total_admins,
        total_normales=total_normales,
        rol=rol,
        productos_top=productos_top,

        rango1=rango1,
        rango2=rango2,
        rango3=rango3,
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
        return render_template("index.html", registro_error="usuario_existe")

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
