from app.models.carrello import Carrello
from app.models.ordine import Ordine
from app.models.ordinedettaglio import OrdineDettaglio
from app.models.logstato import LogStato
from app.models.stato import Stato
from app.extensions import db
from datetime import datetime
from app.services.carrello_service import verifica_disponibilita_carrello
from app.services.log_stato_service import crea_log_iniziale
from app.services.prodotto_service import scala_quantita_prodotto


def crea_ordine(user_id):
    """Crea un nuovo ordine per un utente e assegna il log di stato iniziale."""
    ordine = Ordine(id_utente=user_id)
    try:
        db.session.add(ordine)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante la creazione dell'ordine: {e}")

    # Crea il log di stato iniziale usando il servizio
    try:
        crea_log_iniziale(ordine.id)  # Chiama il servizio per creare il log iniziale
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante la creazione del log di stato iniziale: {e}")

    return ordine


def aggiungi_dettaglio_ordine(id_ordine, id_prodotto, quantita):
    """Aggiunge un dettaglio a un ordine esistente."""
    dettaglio = OrdineDettaglio(
        id_ordine=id_ordine, id_prodotto=id_prodotto, quantita=quantita
    )
    dettaglio.save()

    # Aggiorna il totale dell'ordine
    ordine = Ordine.query.get(id_ordine)
    ordine.totale = calcola_totale_ordine(id_ordine)
    ordine.save()
    return dettaglio


def calcola_totale_ordine(id_ordine):
    """Calcola il totale di un ordine sommando i dettagli."""
    dettagli = OrdineDettaglio.query.filter_by(id_ordine=id_ordine).all()
    totale = sum(
        dettaglio.quantita * dettaglio.prodotto.prezzo for dettaglio in dettagli
    )
    return totale


def elimina_ordine(id_ordine):
    """Elimina un ordine solo se non è stato evaso o annullato."""
    ordine = Ordine.query.get(id_ordine)
    if not ordine:
        raise ValueError("Ordine non trovato.")

    log_stato_corrente = ordine.log_stati[-1]  # Ottieni lo stato corrente
    if log_stato_corrente.stato.descrizione in ["Evaso", "Annullato"]:
        raise ValueError("Non è possibile eliminare un ordine nello stato attuale.")

    ordine.delete()
    return True


def visualizza_ordini(id_utente):
    """Visualizza tutti gli ordini di un utente."""
    ordini = Ordine.query.filter_by(id_utente=id_utente).all()
    return [ordine.to_dict() for ordine in ordini]


def crea_ordine_da_carrello(user_id):
    """
    Converte il carrello in un ordine, verifica la disponibilità
    dei prodotti e scala le quantità.
    """
    # Verifica disponibilità prodotti nel carrello
    verifica_disponibilita_carrello(user_id)

    # Crea un nuovo ordine
    ordine = Ordine(id_utente=user_id, totale=0)
    try:
        db.session.add(ordine)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante la creazione dell'ordine: {str(e)}")

    totale_ordine = 0
    carrello_items = Carrello.query.filter_by(id_utente=user_id).all()

    for item in carrello_items:
        # Scala la quantità del prodotto
        scala_quantita_prodotto(item.id_prodotto, item.quantita)

        # Crea il dettaglio dell'ordine
        dettaglio = OrdineDettaglio(
            id_ordine=ordine.id,
            id_prodotto=item.id_prodotto,
            id_utente=user_id,
            quantita=item.quantita,
            prezzo_unitario=item.prodotto.prezzo,
        )
        totale_ordine += dettaglio.calcola_totale_dettaglio()
        try:
            db.session.add(dettaglio)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(
                f"Errore durante il salvataggio del dettaglio ordine: {str(e)}"
            )

    # Aggiorna il totale dell'ordine
    ordine.totale = totale_ordine
    try:
        ordine.save()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante l'aggiornamento del totale ordine: {str(e)}")

    # Svuota il carrello
    try:
        for item in carrello_items:
            db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante lo svuotamento del carrello: {str(e)}")

    return ordine
