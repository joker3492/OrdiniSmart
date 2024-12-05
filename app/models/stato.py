from app.extensions import db


class Stato(db.Model):
    __tablename__ = "stati"

    id = db.Column(db.Integer, primary_key=True)
    descrizione = db.Column(db.String(50), unique=True, nullable=False)

    @staticmethod
    def get_valid_states():
        """Restituisce gli stati validi."""
        return ["Creato", "In Lavorazione", "Evaso", "Annullato"]

    @staticmethod
    def seed():
        """Popola il database con stati predefiniti."""
        stati_predefiniti = Stato.get_valid_states()
        for stato in stati_predefiniti:
            if not Stato.query.filter_by(descrizione=stato).first():
                db.session.add(Stato(descrizione=stato))
        db.session.commit()

    def save(self):
        """Salva lo stato nel database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
