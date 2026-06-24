import os
from flask import Flask, render_template, request, session, redirect, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "banfrancs.db")
import sqlite3

app = Flask(__name__)
app.secret_key = "banfrancs_secret_key"

def block_quicksort(productos, criterio):

    if len(productos) <= 1:
        return productos

    if criterio == "precio_asc":
        clave = lambda x: float(x[2])

    elif criterio == "precio_desc":
        clave = lambda x: -float(x[2])

    elif criterio == "nombre_asc":
        clave = lambda x: x[1].lower()

    else:
        return productos

    pivote = clave(productos[len(productos) // 2])

    menores = []
    iguales = []
    mayores = []

    # Procesamiento por bloques
    tam_bloque = 4

    for i in range(0, len(productos), tam_bloque):

        bloque = productos[i:i + tam_bloque]

        for producto in bloque:

            valor = clave(producto)

            if valor < pivote:
                menores.append(producto)

            elif valor > pivote:
                mayores.append(producto)

            else:
                iguales.append(producto)

    return (
        block_quicksort(menores, criterio)
        + iguales
        + block_quicksort(mayores, criterio)
    )

class NodoPatricia:

    def __init__(self):
        self.hijos = {}
        self.palabras = []


class PatriciaTrie:

    def __init__(self):
        self.raiz = NodoPatricia()

    def insertar(self, palabra):

        nodo = self.raiz

        for letra in palabra.lower():

            if letra not in nodo.hijos:
                nodo.hijos[letra] = NodoPatricia()

            nodo = nodo.hijos[letra]

        nodo.palabras.append(palabra)

    def buscar_prefijo(self, prefijo):

        nodo = self.raiz

        for letra in prefijo.lower():

            if letra not in nodo.hijos:
                return []

            nodo = nodo.hijos[letra]

        resultados = []

        self._recolectar(nodo, resultados)

        return resultados

    def _recolectar(self, nodo, resultados):

        resultados.extend(nodo.palabras)

        for hijo in nodo.hijos.values():
            self._recolectar(hijo, resultados)                              



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

    criterio_orden = "default"

    seccion = request.args.get("seccion")

    if request.method == "POST":

        accion_producto = request.form.get("accion_producto")
        accion_usuario = request.form.get("accion_usuario")

        if accion_producto:
            print("CRUD PRODUCTOS")
            codigo = request.form.get("codigo") or ""
            nombre = request.form.get("nombre") or ""
            precio = request.form.get("precio") or ""

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

                resultado = None

                tipo_busqueda = ""

                # SOLO CÓDIGO
                if codigo.strip() and not nombre.strip():

                    tipo_busqueda = "codigo"

                    cursor.execute(
                        """
                        SELECT nombre, precio
                        FROM productos
                        WHERE codigo = ?
                        """,
                        (codigo,),
                    )

                    resultado = cursor.fetchone()

                # SOLO NOMBRE
                elif nombre.strip() and not codigo.strip():

                    tipo_busqueda = "nombre"

                    cursor.execute(
                        """
                        SELECT codigo, precio
                        FROM productos
                        WHERE nombre = ?
                        """,
                        (nombre,),
                    )

                    resultado = cursor.fetchone()

                    if resultado:
                        codigo = resultado[0]
                        precio = resultado[1]

                # CÓDIGO Y NOMBRE
                elif codigo.strip() and nombre.strip():

                    tipo_busqueda = "ambos"

                    cursor.execute(
                        """
                        SELECT nombre, precio
                        FROM productos
                        WHERE codigo = ?
                        AND nombre = ?
                        """,
                        (codigo, nombre),
                    )

                    resultado = cursor.fetchone()

                else:

                    mensaje = "Ingrese un código o nombre."

                if resultado:

                    # Caso SOLO CÓDIGO
                    if tipo_busqueda == "codigo":

                        nombre = resultado[0]
                        precio = resultado[1]

                    # Caso CÓDIGO + NOMBRE
                    elif tipo_busqueda == "ambos":

                        nombre = resultado[0]
                        precio = resultado[1]

                    mensaje = "Producto encontrado."

                elif mensaje == "":
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
           
            elif accion_producto == "ordenar":

                criterio_orden = request.form.get("criterio_orden")

                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT codigo, nombre, precio
                    FROM productos
                """)

                productos = cursor.fetchall()

                conexion.close()

                if criterio_orden != "default":
                    productos = block_quicksort(productos, criterio_orden)

                if criterio_orden == "precio_asc":
                    mensaje = "Productos ordenados por precio ascendente."

                elif criterio_orden == "precio_desc":
                    mensaje = "Productos ordenados por precio descendente."

                elif criterio_orden == "nombre_asc":
                    mensaje = "Productos ordenados por nombre."

                else:
                    mensaje = "Orden original restaurado."


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

    if not productos:
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
        criterio_orden=criterio_orden,
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

@app.route("/sugerencias_productos")
def sugerencias_productos():

    texto = request.args.get("texto", "").strip()

    if not texto:
        return jsonify([])

    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT nombre
        FROM productos
    """)

    productos = cursor.fetchall()

    conexion.close()

    trie = PatriciaTrie()

    for producto in productos:
        trie.insertar(producto[0])

    sugerencias = trie.buscar_prefijo(texto)

    return jsonify(sugerencias[:5])

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
