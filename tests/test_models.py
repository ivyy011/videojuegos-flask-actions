
import os
import unittest
from decimal import Decimal

# Activar base de datos de pruebas
os.environ["FLASK_TESTING"] = "1"

from app import app
from extensions import db
from models import Juego


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True

        self.ctx = self.app.app_context()
        self.ctx.push()

        # Verificar que usamos juegos_test
        if db.engine.url.database != "juegos_test":
            self.ctx.pop()
            raise RuntimeError(
                "ERROR: No estamos usando juegos_test"
            )

        db.create_all()

        # Limpiar registros anteriores
        db.session.query(Juego).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def test_juego_creation(self):
        juego = Juego(
            nombre="Test",
            descripcion="Desc",
            precio=Decimal("9.99")
        )

        db.session.add(juego)
        db.session.commit()

        self.assertEqual(Juego.query.count(), 1)


if __name__ == "__main__":
    unittest.main()
