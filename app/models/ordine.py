from app.extensions import db
from datetime import datetime


class Ordine(db.Model):
    __tablename__ = "ordini"

    id = db.Column(db.Integer, primary_key=True)
    id_utente = db.Column(
        db.Integer, db.ForeignKey("utenti.id"), nullable=False
    )  # FK con Utente
    data_creazione = db.Column(db.DateTime, default=datetime.utcnow)
    totale = db.Column(db.Float, default=0.0)

    # Relazione
    utente = db.relationship(
        "Utente", backref=db.backref("ordini", cascade="all, delete-orphan")
    )

    def save(self):
        """Salva l'ordine nel database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Elimina l'ordine dal database, se permesso."""

        log_stato_corrente = self.log_stati[-1]  # Ottieni lo stato corrente
        if log_stato_corrente.stato.descrizione in ["Evaso", "Annullato"]:
            raise ValueError("Non è possibile eliminare un ordine nello stato attuale.")
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def to_dict(self):
        """Restituisce un dizionario rappresentativo dell'oggetto Ordine."""
        return {
            "id": self.id,
            "id_utente": self.id_utente,
            "data_creazione": self.data_creazione.isoformat(),
            "totale": self.totale,
            "dettagli": [
                dettaglio.to_dict() for dettaglio in self.ordine_dettagli
            ],  # Include i dettagli
        }
