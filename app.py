
import os
from urllib.parse import quote_plus

from flask import Flask, render_template, request, redirect
from extensions import db
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required

# Crear aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

# Configuración de MySQL
password = os.environ["MYSQL_PASSWORD"]

# Seleccionar base de datos normal o de pruebas
nombre_bd = (
    "juegos_test"
    if os.environ.get("FLASK_TESTING") == "1"
    else "juegos"
)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://root:{quote_plus(password)}@localhost/{nombre_bd}"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db.init_app(app)

# Importar el modelo de videojuegos
from models import Juego, User

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

from auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

# Importar controladores
import controllers

# Registrar API REST
from api.routes import api
api.init_app(app)

# Mostrar formulario para agregar videojuegos
@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")


# Guardar un nuevo videojuego
@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]

    controllers.insertar_juego(nombre, descripcion, precio)

    return redirect("/juegos")


# Mostrar todos los videojuegos
@app.route("/")
@app.route("/juegos")
@login_required
def juegos():
    lista_juegos = controllers.obtener_juegos()
    return render_template("juegos.html", juegos=lista_juegos)


# Eliminar videojuego
@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    id = int(request.form["id"])

    controllers.eliminar_juego(id)

    return redirect("/juegos")


# Mostrar formulario para editar videojuego
@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controllers.obtener_juego_por_id(id)

    return render_template("editar_juego.html", juego=juego)


# Actualizar videojuego
@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = int(request.form["id"])
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]

    controllers.actualizar_juego(nombre, descripcion, precio, id)

    return redirect("/juegos")


# Ejecutar aplicación
if __name__ == "__main__":
    app.run(debug=True, port=8000)
