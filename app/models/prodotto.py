from app.extensions import db
from datetime import datetime


class Prodotto(db.Model):
    __tablename__ = "prodotti"

    id = db.Column(db.Integer, primary_key=True)
    id_categoria = db.Column(
        db.Integer, db.ForeignKey("categorie.id"), nullable=False
    )  # FK con Categoria
    id_admin = db.Column(
        db.Integer, db.ForeignKey("utenti.id"), nullable=False
    )  # FK con Utente (admin che gestisce il prodotto)
    nome = db.Column(db.String(100), nullable=False)
    url_foto = db.Column(
        db.String(255), nullable=True
    )  # URL per l'immagine del prodotto
    prezzo = db.Column(db.Float, nullable=False, default=0.0)
    quantita = db.Column(db.Integer, nullable=False, default=0)

    # Relazioni
    categoria = db.relationship(
        "Categoria", backref=db.backref("prodotti", cascade="all, delete-orphan")
    )
    admin = db.relationship(
        "Utente", backref=db.backref("prodotti", cascade="all, delete-orphan")
    )

    __table_args__ = (
        db.UniqueConstraint("nome", "id_admin", name="unique_nome_per_admin"),
    )

    def save(self):
        """Salva il prodotto nel database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Elimina il prodotto dal database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def to_dict(self):
        """Restituisce un dizionario rappresentativo dell'oggetto Prodotto."""
        return {
            "id": self.id,
            "id_categoria": self.id_categoria,
            "id_admin": self.id_admin,
            "nome": self.nome,
            "url_foto": self.url_foto,
            "prezzo": self.prezzo,
            "quantita": self.quantita,
        }
