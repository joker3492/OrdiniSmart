from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Utente(db.Model):
    __tablename__ = "utenti"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    data_registrazione = db.Column(db.DateTime, default=datetime.utcnow)
    data_modifica = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """Hash della password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica della password"""
        return check_password_hash(self.password_hash, password)

    def save(self):
        """Salva l'utente nel database"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Cancella l'utente dal database"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "data_registrazione": self.data_registrazione.isoformat(),
            "data_modifica": (
                self.data_modifica.isoformat() if self.data_modifica else None
            ),
            "is_admin": self.is_admin,
        }
