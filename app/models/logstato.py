from app.extensions import db
from datetime import datetime
from app.models.stato import Stato


class LogStato(db.Model):
    __tablename__ = "log_stati"

    id = db.Column(db.Integer, primary_key=True)
    id_ordine = db.Column(
        db.Integer, db.ForeignKey("ordini.id"), nullable=False
    )  # Relazione con Ordine
    id_stato = db.Column(
        db.Integer, db.ForeignKey("stati.id"), nullable=False
    )  # Relazione con Stato
    data_modifica = db.Column(db.DateTime, default=datetime.utcnow)

    # Relazioni
    ordine = db.relationship(
        "Ordine", backref=db.backref("log_stati", cascade="all, delete-orphan")
    )
    stato = db.relationship(
        "Stato", backref=db.backref("log_stati", cascade="all, delete-orphan")
    )

    def save(self):
        """Salva il LogStato nel database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Eliminazione non permessa."""
        raise NotImplementedError("L'eliminazione dei log di stato non è permessa")

    def to_dict(self):
        """Serializza l'oggetto in un dizionario."""
        return {
            "id": self.id,
            "id_ordine": self.id_ordine,
            "id_stato": self.id_stato,
            "stato": self.stato.descrizione,
            "data_modifica": self.data_modifica.isoformat(),
        }
