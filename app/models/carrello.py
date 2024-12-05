from app.extensions import db
from datetime import datetime


class Carrello(db.Model):
    __tablename__ = "carrelli"

    id = db.Column(db.Integer, primary_key=True)
    id_prodotto = db.Column(
        db.Integer, db.ForeignKey("prodotti.id"), nullable=False
    )  # FK con Prodotto
    id_utente = db.Column(
        db.Integer, db.ForeignKey("utenti.id"), nullable=False
    )  # FK con Utente
    quantita = db.Column(db.Integer, nullable=False, default=1)  # Quantità nel carrello

    # Relazioni
    prodotto = db.relationship(
        "Prodotto",
        backref=db.backref("carrello_articoli", cascade="all, delete-orphan"),
    )
    utente = db.relationship(
        "Utente", backref=db.backref("carrello", cascade="all, delete-orphan")
    )

    def save(self):
        """Salva l'oggetto Carrello nel database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Elimina l'oggetto Carrello dal database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def to_dict(self):
        """Restituisce un dizionario rappresentativo dell'oggetto Carrello."""
        return {
            "id": self.id,
            "id_prodotto": self.id_prodotto,
            "id_utente": self.id_utente,
            "quantita": self.quantita,
            "prodotto": self.prodotto.to_dict(),  # Collegamento con Prodotto
        }

    def calcola_totale_parziale(self):
        """Calcola il totale parziale di questo articolo nel carrello."""
        return self.quantita * self.prodotto.prezzo
