from app.extensions import db


class Categoria(db.Model):
    __tablename__ = "categorie"

    id = db.Column(db.Integer, primary_key=True)
    descrizione = db.Column(db.String(100), unique=True, nullable=False)

    def save(self):
        """Salva la categoria nel database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError("Categoria già esistente.")

    def delete(self):
        """Elimina la categoria dal database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def to_dict(self):
        """Restituisce un dizionario rappresentativo dell'oggetto Categoria."""
        return {
            "id": self.id,
            "descrizione": self.descrizione,
        }
