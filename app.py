from flask import Flask, render_template_string

app = Flask(__name__)
BanFrancs_html = """

<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <title>BANFRANCS</title>

    <!-- BOOTSTRAP -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />

    <!-- ICONOS -->
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    />

    <style>
      body {
        background-color: #f5f5f5;
        font-family: Arial, Helvetica, sans-serif;
      }

      /* NAVBAR */
      .navbar {
        background-color: #111;
        padding: 15px;
      }

      .navbar-brand {
        font-size: 32px;
        font-weight: bold;
        letter-spacing: 2px;
      }

      .navbar-brand span {
        font-size: 28px;
        letter-spacing: 3px;
      }

      .nav-link {
        color: white !important;
        margin-left: 15px;
        transition: 0.3s;
      }

      .nav-link:hover {
        color: #d4af37 !important;
      }

      /* BUSCADOR */
      .form-control {
        border-radius: 20px;
      }

      .btn-search {
        border-radius: 20px;
        background-color: #d4af37;
        border: none;
        color: black;
        font-weight: bold;
      }

      /* ICONOS NAVBAR */
      .iconos i {
        color: white;
        font-size: 22px;
        margin-left: 20px;
        cursor: pointer;
        transition: 0.3s;
      }

      .iconos i:hover {
        color: #d4af37;
      }

      .carrito {
        position: relative;
      }

      .badge-carrito {
        position: absolute;
        top: -10px;
        right: -10px;
        background: red;
        color: white;
        border-radius: 50%;
        font-size: 12px;
        width: 18px;
        height: 18px;
        display: flex;
        justify-content: center;
        align-items: center;
      }

      /* CARRUSEL */
      .carousel-container {
        width: 92%;
        margin: auto;
        margin-top: 30px;
      }

      .carousel-item {
        padding: 10px;
      }

      .carousel-item img {
        height: 420px;
        object-fit: cover;
        object-position: top;
        border-radius: 15px;
      }

      .texto-carousel {
        background: linear-gradient(135deg, #111, #2d2d2d);
        color: white;
        height: 420px;
        border-radius: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 50px;
      }

      .texto-carousel h1 {
        font-size: 55px;
        font-weight: bold;
      }

      .texto-carousel p {
        font-size: 22px;
        margin-top: 15px;
      }

      .btn-premium {
        background-color: #d4af37;
        color: black;
        border: none;
        font-weight: bold;
        width: 220px;
        padding: 12px;
        margin-top: 20px;
        transition: 0.3s;
      }

      .btn-premium:hover {
        background-color: white;
      }

      /* TITULO */
      .titulo {
        text-align: center;
        margin-top: 70px;
        margin-bottom: 50px;
        font-size: 40px;
        font-weight: bold;
        color: #111;
      }

      /* CARDS */
      .card {
        border: none;
        border-radius: 15px;
        overflow: hidden;
        transition: 0.4s;
      }

      .card:hover {
        transform: translateY(-10px);
      }

      .card img {
        height: 320px;
        object-fit: contain;
        background: white;
      }

      .card-body {
        padding: 25px;
      }

      .precio {
        color: #198754;
        font-size: 24px;
        font-weight: bold;
      }

      .btn-dark {
        width: 100%;
        border-radius: 8px;
      }

      /* BENEFICIOS */
      .beneficios {
        background-color: white;
        margin-top: 70px;
        padding: 50px;
      }

      .beneficio-box {
        text-align: center;
        padding: 20px;
      }

      .beneficio-box i {
        font-size: 45px;
        color: #d4af37;
        margin-bottom: 15px;
      }

      /* FOOTER */
      footer {
        background-color: #111;
        color: white;
        margin-top: 70px;
        padding: 40px;
      }

      .redes i {
        font-size: 24px;
        margin: 10px;
        cursor: pointer;
        transition: 0.3s;
      }

      .redes i:hover {
        color: #d4af37;
      }
    </style>
  </head>

  <body>
    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark">
      <div class="container">
        <!-- LOGO -->
        <a class="navbar-brand d-flex align-items-center" href="#">
          <img
            src="https://raw.githubusercontent.com/Hibban00/BANFRANCS-Web/refs/heads/main/static/LOGO%20NAVBAR.png"
            width="60"
            class="me-2"
          />

          <span class="text-white"> BANFRANCS </span>
        </a>

        <!-- BOTON HAMBURGUESA -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#menu"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- CONTENIDO DEL MENU -->
        <div class="collapse navbar-collapse" id="menu">
          <!-- OPCIONES -->
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" href="#"> Inicio </a>
            </li>

            <!-- DROPDOWN PRODUCTOS -->
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
              >
                Productos
              </a>

              <ul class="dropdown-menu">
                <li>
                  <a class="dropdown-item" href="#"> Polos Negros </a>
                </li>

                <li>
                  <a class="dropdown-item" href="#"> Polos Blancos </a>
                </li>

                <li>
                  <a class="dropdown-item" href="#"> Polos Oversize </a>
                </li>

                <li>
                  <a class="dropdown-item" href="#"> Nueva Temporada </a>
                </li>
              </ul>
            </li>

            <!-- COLECCION NORMAL -->
            <li class="nav-item">
              <a class="nav-link" href="#"> Colección </a>
            </li>

            <li class="nav-item">
              <a class="nav-link" href="#"> Contacto </a>
            </li>
          </ul>

          <!-- BUSCADOR -->
          <form class="d-flex ms-4 mt-3 mt-lg-0">
            <input
              class="form-control me-2"
              type="search"
              placeholder="Buscar"
            />

            <button class="btn btn-search">Buscar</button>
          </form>

          <!-- ICONOS -->
          <div class="iconos d-flex align-items-center ms-4 mt-3 mt-lg-0">
            <!-- USUARIO -->
            <i class="fa-solid fa-user"></i>

            <!-- FAVORITOS -->
            <i class="fa-solid fa-heart"></i>

            <!-- CARRITO -->
            <div class="carrito">
              <i class="fa-solid fa-cart-shopping"></i>

              <span class="badge-carrito"> 0 </span>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- CARRUSEL -->
    <div class="carousel-container">
      <div
        id="slider"
        class="carousel slide"
        data-bs-ride="carousel"
        data-bs-interval="3500"
      >
        <div class="carousel-inner">
          <!-- SLIDE 1 -->
          <div class="carousel-item active">
            <div class="row">
              <div class="col-md-6">
                <img
                  src="https://raw.githubusercontent.com/Hibban00/BANFRANCS-Web/refs/heads/main/static/POLO%20BLANCO%20CARRUSEL%20BASE.png"
                  class="d-block w-100"
                />
              </div>

              <div class="col-md-6">
                <div class="texto-carousel">
                  <h1>Viste con Seguridad</h1>

                  <p>Diseños modernos para hombres con estilo.</p>

                  <button class="btn-premium">Explorar Colección</button>
                </div>
              </div>
            </div>
          </div>

          <!-- SLIDE 2 -->
          <div class="carousel-item">
            <div class="row">
              <div class="col-md-6">
                <img
                  src="https://raw.githubusercontent.com/Hibban00/BANFRANCS-Web/refs/heads/main/static/POLO%20NEGRO%20CARRUSEL%20BASE.png"
                  class="d-block w-100"
                />
              </div>

              <div class="col-md-6">
                <div class="texto-carousel">
                  <h1>Moda Premium</h1>

                  <p>Calidad, comodidad y elegancia.</p>

                  <button class="btn-premium">Comprar Ahora</button>
                </div>
              </div>
            </div>
          </div>

          <!-- SLIDE 3 -->
          <div class="carousel-item">
            <div class="row">
              <div class="col-md-6">
                <img
                  src="https://raw.githubusercontent.com/Hibban00/BANFRANCS-Web/refs/heads/main/static/POLO%20AZUL%20CARRUSEL%20BASE.png"
                  class="d-block w-100"
                />
              </div>

              <div class="col-md-6">
                <div class="texto-carousel">
                  <h1>Nueva Temporada</h1>

                  <p>Encuentra polos exclusivos y modernos.</p>

                  <button class="btn-premium">Ver Productos</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- CONTROLES -->
        <button
          class="carousel-control-prev"
          type="button"
          data-bs-target="#slider"
          data-bs-slide="prev"
        >
          <span class="carousel-control-prev-icon bg-dark rounded-circle p-3">
          </span>
        </button>

        <button
          class="carousel-control-next"
          type="button"
          data-bs-target="#slider"
          data-bs-slide="next"
        >
          <span class="carousel-control-next-icon bg-dark rounded-circle p-3">
          </span>
        </button>
      </div>
    </div>

    <!-- PRODUCTOS -->
    <div class="container">
      <h2 class="titulo">Productos Destacados</h2>

      <div class="row">
        <div class="col-md-4 mb-4">
          <div class="card shadow">
            <img
              src="https://raw.githubusercontent.com/Hibban00/BANFRANCS-Web/refs/heads/main/static/PARA%20VENTA%20NEGRO.png"
              class="card-img-top"
            />

            <div class="card-body text-center">
              <h4>Polo Negro</h4>

              <p class="precio">S/ 49.90</p>

              <button class="btn btn-dark">Comprar</button>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="card shadow">
            <img
              src="https://raw.githubusercontent.com/Hibban00/BANFRANCS-Web/refs/heads/main/static/PARA%20VENTA%20BLANCO.png"
              class="card-img-top"
            />

            <div class="card-body text-center">
              <h4>Polo Blanco</h4>

              <p class="precio">S/ 44.90</p>

              <button class="btn btn-dark">Comprar</button>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="card shadow">
            <img
              src="https://raw.githubusercontent.com/Hibban00/BANFRANCS-Web/refs/heads/main/static/PARA%20VENTA%20AZUL.png"
              class="card-img-top"
            />

            <div class="card-body text-center">
              <h4>Polo Azul</h4>

              <p class="precio">S/ 54.90</p>

              <button class="btn btn-dark">Comprar</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- BENEFICIOS -->
    <section class="beneficios">
      <div class="container">
        <div class="row">
          <div class="col-md-4">
            <div class="beneficio-box">
              <i class="fa-solid fa-truck"></i>

              <h4>Envíos Rápidos</h4>

              <p>Entregas seguras a todo el país.</p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="beneficio-box">
              <i class="fa-solid fa-shirt"></i>

              <h4>Calidad Premium</h4>

              <p>Polos modernos y cómodos.</p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="beneficio-box">
              <i class="fa-solid fa-lock"></i>

              <h4>Compra Segura</h4>

              <p>Protección en todas tus compras.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer>
      <div class="container text-center">
        <h3>BANFRANCS</h3>

        <p>Moda masculina moderna y elegante.</p>

        <div class="redes">
          <i class="fa-brands fa-facebook"></i>

          <i class="fa-brands fa-instagram"></i>

          <i class="fa-brands fa-whatsapp"></i>
        </div>

        <p class="mt-3">BANFRANCS © 2026 | Todos los derechos reservados</p>
      </div>
    </footer>

    <!-- JS BOOTSTRAP -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>

"""


@app.route("/")
def inicio():
    return render_template_string(BanFrancs_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
