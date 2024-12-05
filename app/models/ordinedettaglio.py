from app.extensions import db


class OrdineDettaglio(db.Model):
    __tablename__ = "ordine_dettagli"

    id = db.Column(db.Integer, primary_key=True)
    id_ordine = db.Column(
        db.Integer, db.ForeignKey("ordini.id", ondelete="CASCADE"), nullable=False
    )  # FK con Ordine
    id_prodotto = db.Column(
        db.Integer, db.ForeignKey("prodotti.id", ondelete="CASCADE"), nullable=False
    )  # FK con Prodotto
    id_utente = db.Column(
        db.Integer, db.ForeignKey("utenti.id", ondelete="CASCADE"), nullable=False
    )  # FK con Utente
    id_stato = db.Column(
        db.Integer, db.ForeignKey("stati.id", ondelete="CASCADE"), nullable=False
    )  # FK con Stato
    quantita = db.Column(db.Integer, nullable=False, default=1)  # Quantità acquistata
    prezzo_unitario = db.Column(
        db.Float, nullable=False
    )  # Prezzo al momento dell'acquisto

    # Relazioni
    ordine = db.relationship(
        "Ordine",
        backref=db.backref("ordine_dettagli", lazy=True, cascade="all, delete-orphan"),
    )
    prodotto = db.relationship(
        "Prodotto",
        backref=db.backref("ordine_dettagli", lazy=True, cascade="all, delete-orphan"),
    )
    utente = db.relationship(
        "Utente",
        backref=db.backref("ordine_dettagli", lazy=True, cascade="all, delete-orphan"),
    )
    stato = db.relationship(
        "Stato",
        backref=db.backref("ordine_dettagli", lazy=True, cascade="all, delete-orphan"),
    )

    def calcola_totale_dettaglio(self):
        """Calcola il totale per questo dettaglio (quantità * prezzo unitario)."""
        return self.quantita * self.prezzo_unitario

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            print(f"Salvato correttamente: {self.to_dict()}")
        except Exception as e:
            print(f"Errore durante il salvataggio: {e}")
            db.session.rollback()
            raise

    def delete(self):
        """Elimina l'oggetto OrdineDettaglio dal database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def to_dict(self):
        """Restituisce un dizionario rappresentativo dell'oggetto OrdineDettaglio."""
        return {
            "id": self.id,
            "id_ordine": self.id_ordine,
            "id_prodotto": self.id_prodotto,
            "id_utente": self.id_utente,
            "id_stato": self.id_stato,
            "quantita": self.quantita,
            "prezzo_unitario": self.prezzo_unitario,
            "prodotto": self.prodotto.to_dict() if self.prodotto else None,
            "stato": self.stato.descrizione if self.stato else None,
        }
