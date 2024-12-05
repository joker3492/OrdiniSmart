from app.models.carrello import Carrello
from app.models.ordine import Ordine
from app.models.ordinedettaglio import OrdineDettaglio
from app.services.carrello_service import (
    calcola_totale_carrello,
    svuota_carrello,
    verifica_disponibilita_carrello,
)
from app.services.prodotto_service import processa_articolo
from app.services.log_stato_service import crea_log, recupera_stato
from app.extensions import db


def conferma_carrello(user_id):
    """
    Conferma il carrello, crea un ordine e genera i dettagli ordine con stato 'Creato'.
    """
    try:
        # Verifica disponibilità prodotti nel carrello
        verifica_disponibilita_carrello(user_id)

        # Crea ordine con stato iniziale
        ordine = Ordine(id_utente=user_id, totale=0)
        ordine.save()  # Salva l'ordine nel database
        crea_log(ordine.id, "Creato")  # Stato iniziale

        # Recupera articoli del carrello
        carrello_items = Carrello.query.filter_by(id_utente=user_id).all()

        if not carrello_items:
            raise ValueError("Il carrello è vuoto. Impossibile creare un ordine.")

        dettagli_ordine = []

        # Aggiungi dettagli ordine e scala quantità prodotti
        for item in carrello_items:
            try:
                prodotto = processa_articolo(
                    item.id_prodotto, item.quantita
                )  # Scala quantità prodotto
                dettaglio = OrdineDettaglio(
                    id_ordine=ordine.id,
                    id_prodotto=item.id_prodotto,
                    id_utente=user_id,
                    quantita=item.quantita,
                    prezzo_unitario=prodotto.prezzo,
                    id_stato=recupera_stato("Creato").id,  # Stato iniziale
                )
                dettaglio.save()  # Salva ogni dettaglio
                db.session.commit()
                dettagli_ordine.append(dettaglio)
            except Exception as e:
                raise ValueError(
                    f"Errore nel salvataggio del dettaglio ordine per {item.id_prodotto}: {str(e)}"
                )

        # Calcola e aggiorna il totale dell'ordine
        ordine.totale = sum(
            dettaglio.calcola_totale_dettaglio() for dettaglio in dettagli_ordine
        )
        ordine.save()

        # Svuota il carrello
        svuota_carrello(user_id)

        return ordine
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante la conferma del carrello: {str(e)}")


def aggiorna_stato_ordine(id_ordine):
    """
    Aggiorna lo stato dell'ordine in base ai suoi dettagli:
    - "In lavorazione" se almeno un dettaglio è evaso.
    - "Chiuso" se tutti i dettagli sono evasi.
    """
    ordine = Ordine.query.get(id_ordine)
    if not ordine:
        raise ValueError(f"Ordine con ID {id_ordine} non trovato.")

    dettagli = ordine.ordine_dettagli
    stati_dettagli = [dettaglio.stato.descrizione for dettaglio in dettagli]

    if all(stato == "Evaso" for stato in stati_dettagli):
        nuovo_stato = "Chiuso"
    elif any(stato == "Evaso" for stato in stati_dettagli):
        nuovo_stato = "In lavorazione"
    else:
        nuovo_stato = "Creato"  # Default o stato iniziale.

    stato_corrente = ordine.log_stati[-1].stato.descrizione
    if stato_corrente != nuovo_stato:
        crea_log(ordine.id, nuovo_stato)  # Crea un log solo se cambia stato


def elimina_ordine(id_ordine):
    """
    Elimina un ordine solo se non è stato evaso o annullato.
    """
    ordine = Ordine.query.get(id_ordine)
    if not ordine:
        raise ValueError("Ordine non trovato.")

    # Verifica lo stato corrente
    stato_corrente = ordine.log_stati[-1].stato.descrizione  # Ultimo log di stato
    if stato_corrente in ["Evaso", "Annullato"]:
        raise ValueError("Non è possibile eliminare un ordine nello stato attuale.")

    ordine.delete()  # Usa il metodo `delete` del modello

    return {"message": "Ordine eliminato con successo."}


def visualizza_ordini(id_utente):
    """Visualizza tutti gli ordini di un utente."""
    ordini = Ordine.query.filter_by(id_utente=id_utente).all()
    return [ordine.to_dict() for ordine in ordini]
