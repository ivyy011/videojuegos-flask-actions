
from decimal import Decimal, InvalidOperation

from flask import request
from flask_restful import Api, Resource
from extensions import db
from models import Juego

class ApiPersonalizada(Api):
    def handle_error(self, e):
        from werkzeug.exceptions import HTTPException

        if isinstance(e, HTTPException):
            return self.app.handle_http_exception(e)

        return super().handle_error(e)


api = ApiPersonalizada()


# Convertir un videojuego a JSON
def juego_a_json(juego):
    return {
        "id": juego.id,
        "nombre": juego.nombre,
        "descripcion": juego.descripcion,
        "precio": float(juego.precio)
    }


# Validar los datos recibidos
def validar_juego(datos):
    if not isinstance(datos, dict):
        return None, "Debes enviar un objeto JSON"

    campos = ["nombre", "descripcion", "precio"]

    for campo in campos:
        if campo not in datos:
            return None, f"Falta el campo: {campo}"

    nombre = datos["nombre"]
    descripcion = datos["descripcion"]

    if not isinstance(nombre, str) or not nombre.strip():
        return None, "El nombre no es valido"

    if not isinstance(descripcion, str) or not descripcion.strip():
        return None, "La descripcion no es valida"

    if len(nombre) > 255 or len(descripcion) > 255:
        return None, "El texto supera los 255 caracteres"

    try:
        if isinstance(datos["precio"], bool):
            raise ValueError()

        precio = Decimal(str(datos["precio"]))

        if not precio.is_finite():
            raise ValueError()

        if precio < 0 or precio > Decimal("9999999.99"):
            raise ValueError()

        if precio.as_tuple().exponent < -2:
            raise ValueError()

    except (InvalidOperation, ValueError, TypeError):
        return None, "El precio debe ser un numero valido"

    return {
        "nombre": nombre.strip(),
        "descripcion": descripcion.strip(),
        "precio": precio
    }, None


# ==========================================
# ENDPOINT: /api/juegos
# ==========================================
# GET: Obtiene todos los videojuegos.
# Respuesta exitosa: 200 OK.
#
# POST: Registra un videojuego nuevo.
# Datos requeridos: nombre, descripcion, precio.
# Respuesta exitosa: 201 Created.
# Error: 400 Bad Request si faltan datos
# o los valores son invalidos.
# ==========================================
class JuegoList(Resource):

    def get(self):
        juegos = db.session.execute(
            db.select(Juego).order_by(Juego.id)
        ).scalars().all()

        return [juego_a_json(juego) for juego in juegos], 200

    def post(self):
        datos = request.get_json(silent=True)
        valores, error = validar_juego(datos)

        if error:
            return {"error": error}, 400

        nuevo_juego = Juego(**valores)

        db.session.add(nuevo_juego)
        db.session.commit()

        return juego_a_json(nuevo_juego), 201


# ==========================================
# ENDPOINT: /api/juegos/<int:id>
# ==========================================
# GET: Consulta un videojuego por su ID.
# Respuesta exitosa: 200 OK.
# Error: 404 si el juego no existe.
#
# PUT: Actualiza los datos de un videojuego.
# Datos requeridos: nombre, descripcion, precio.
# Respuesta exitosa: 200 OK.
# Errores: 400 por datos invalidos,
# 404 si el juego no existe.
#
# DELETE: Elimina un videojuego por su ID.
# Respuesta exitosa: 204 No Content.
# Error: 404 si el juego no existe.
# ==========================================
class JuegoResource(Resource):

    def get(self, id):
        juego = db.session.get(Juego, id)

        if juego is None:
            return {"error": "Juego no encontrado"}, 404

        return juego_a_json(juego), 200

    def put(self, id):
        juego = db.session.get(Juego, id)

        if juego is None:
            return {"error": "Juego no encontrado"}, 404

        datos = request.get_json(silent=True)
        valores, error = validar_juego(datos)

        if error:
            return {"error": error}, 400

        juego.nombre = valores["nombre"]
        juego.descripcion = valores["descripcion"]
        juego.precio = valores["precio"]

        db.session.commit()

        return juego_a_json(juego), 200

    def delete(self, id):
        juego = db.session.get(Juego, id)

        if juego is None:
            return {"error": "Juego no encontrado"}, 404

        db.session.delete(juego)
        db.session.commit()

        return "", 204


# Registrar las rutas
api.add_resource(JuegoList, "/api/juegos")
api.add_resource(JuegoResource, "/api/juegos/<int:id>")
