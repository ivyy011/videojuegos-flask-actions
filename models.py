from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from sqlalchemy.dialects.mysql import BIGINT

class Juego(db.Model):
    __tablename__ = 'juegos'

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Numeric(9, 2), nullable=False)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is write-only')

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)
