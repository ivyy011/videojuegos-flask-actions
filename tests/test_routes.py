import os
import unittest

os.environ["FLASK_TESTING"] = "1"

from app import app
from extensions import db


class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True

        self.ctx = self.app.app_context()
        self.ctx.push()

        if db.engine.url.database != "juegos_test":
            self.ctx.pop()
            raise RuntimeError("La base de datos no es juegos_test")

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def test_inicio_requiere_login(self):
        respuesta = self.client.get("/")

        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("/auth/login", respuesta.headers["Location"])

    def test_juegos_requiere_login(self):
        respuesta = self.client.get("/juegos")

        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("/auth/login", respuesta.headers["Location"])


if __name__ == "__main__":
    unittest.main()