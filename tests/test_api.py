import os
import unittest
from decimal import Decimal

os.environ["FLASK_TESTING"] = "1"

from app import app
from extensions import db
from models import Juego


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True

        self.ctx = self.app.app_context()
        self.ctx.push()

        if db.engine.url.database != "juegos_test":
            self.ctx.pop()
            raise RuntimeError(
                "ERROR: No estamos usando juegos_test"
            )

        self.client = self.app.test_client()

        db.create_all()

        # Limpiar los juegos de prueba
        db.session.query(Juego).delete()
        db.session.commit()

        juego = Juego(
            nombre="Juego API",
            descripcion="Prueba de API",
            precio=Decimal("19.99")
        )

        db.session.add(juego)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        self.ctx.pop()

    def test_get_juegos(self):
        respuesta = self.client.get("/api/juegos")

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.get_json()

        self.assertIsInstance(datos, list)
        self.assertEqual(len(datos), 1)
        self.assertEqual(datos[0]["nombre"], "Juego API")


if __name__ == "__main__":
    unittest.main()