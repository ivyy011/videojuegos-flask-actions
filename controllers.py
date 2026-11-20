from extensions import db
from models import Juego


# Insertar un videojuego
def insertar_juego(nombre, descripcion, precio):
    juego = Juego(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio
    )

    db.session.add(juego)
    db.session.commit()


# Obtener todos los videojuegos
def obtener_juegos():
    return Juego.query.all()


# Obtener un videojuego por su ID
def obtener_juego_por_id(id):
    return db.session.get(Juego, id)


# Actualizar un videojuego
def actualizar_juego(nombre, descripcion, precio, id):
    juego = db.session.get(Juego, id)

    if juego:
        juego.nombre = nombre
        juego.descripcion = descripcion
        juego.precio = precio

        db.session.commit()


# Eliminar un videojuego
def eliminar_juego(id):
    juego = db.session.get(Juego, id)

    if juego:
        db.session.delete(juego)
        db.session.commit()