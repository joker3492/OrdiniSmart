from app.models.carrello import Carrello
from app.models.prodotto import Prodotto
from app.extensions import db
from app.services.prodotto_service import verifica_disponibilita_prodotto


def aggiungi_al_carrello(user_id, prodotto_id, quantita):
    """
    Aggiunge o aggiorna un prodotto nel carrello di un utente standard.
    """
    prodotto = Prodotto.query.get(prodotto_id)
    if not prodotto:
        raise ValueError("Prodotto non trovato.")
    if prodotto.quantita < quantita:
        raise ValueError("Quantità del prodotto insufficiente.")

    articolo = Carrello.query.filter_by(
        id_utente=user_id, id_prodotto=prodotto_id
    ).first()
    if articolo:
        articolo.quantita += quantita
    else:
        articolo = Carrello(
            id_utente=user_id, id_prodotto=prodotto_id, quantita=quantita
        )

    try:
        articolo.save()
        return articolo.to_dict()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante l'aggiunta al carrello: {str(e)}")


def verifica_disponibilita_carrello(user_id):
    """
    Verifica la disponibilità di tutti i prodotti nel carrello di un utente.
    """
    carrello_items = Carrello.query.filter_by(id_utente=user_id).all()
    if not carrello_items:
        raise ValueError("Il carrello è vuoto.")

    for item in carrello_items:
        try:
            verifica_disponibilita_prodotto(item.id_prodotto, item.quantita)
        except Exception as e:
            raise ValueError(
                f"Errore nel verificare disponibilità per {item.id_prodotto}: {str(e)}"
            )


def calcola_totale_carrello(user_id):
    """
    Calcola il totale del carrello di un utente.
    """
    carrello_items = Carrello.query.filter_by(id_utente=user_id).all()
    return sum(item.quantita * item.prodotto.prezzo for item in carrello_items)


def svuota_carrello(user_id):
    """
    Svuota il carrello di un utente standard.
    """
    try:
        Carrello.query.filter_by(id_utente=user_id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante lo svuotamento del carrello: {str(e)}")


def rimuovi_dal_carrello(user_id, prodotto_id):
    """
    Rimuove un prodotto dal carrello di un utente.
    """
    articolo = Carrello.query.filter_by(
        id_utente=user_id, id_prodotto=prodotto_id
    ).first()
    if not articolo:
        raise ValueError("Articolo non trovato nel carrello.")

    try:
        articolo.delete()
        return {"message": "Articolo rimosso dal carrello con successo."}
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante la rimozione dal carrello: {str(e)}")


def visualizza_carrello(user_id):
    """
    Visualizza tutti gli articoli nel carrello di un utente.
    """
    try:
        articoli = Carrello.query.filter_by(id_utente=user_id).all()
        if not articoli:
            raise ValueError("Il carrello è vuoto.")

        # Restituisci i dettagli del carrello come una lista di dizionari
        return [articolo.to_dict() for articolo in articoli]
    except Exception as e:
        raise ValueError(f"Errore durante il recupero del carrello: {str(e)}")
