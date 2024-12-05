from datetime import datetime
from app.models.ordine import Ordine
from app.models.ordinedettaglio import OrdineDettaglio
from app.models.prodotto import Prodotto
from app.models.logstato import LogStato
from app.models.stato import Stato
from app.extensions import db
from app.services.auth_service import verifica_admin
from app.services.prodotto_service import processa_articolo
from app.services.log_stato_service import crea_log, recupera_stato


def crea_dettaglio_ordine(id_ordine, id_prodotto, id_utente, quantita, prezzo_unitario):
    """
    Crea un dettaglio ordine e lo salva nel database.
    """
    stato = recupera_stato("Creato")  # Stato iniziale per ogni dettaglio ordine
    dettaglio = OrdineDettaglio(
        id_ordine=id_ordine,
        id_prodotto=id_prodotto,
        id_utente=id_utente,
        quantita=quantita,
        prezzo_unitario=prezzo_unitario,
        id_stato=stato.id,
    )
    try:
        dettaglio.save()
        return dettaglio
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante la creazione del dettaglio ordine: {str(e)}")


def crea_ordine_da_carrello(user_id):
    """
    Converte gli articoli del carrello in un ordine e crea i dettagli ordine.
    """
    from app.models.carrello import Carrello
    from app.models.ordine import Ordine
    from app.services.carrello_service import (
        verifica_disponibilita_carrello,
        svuota_carrello,
    )

    # Verifica disponibilità prodotti nel carrello
    verifica_disponibilita_carrello(user_id)

    # Crea l'ordine
    ordine = Ordine(id_utente=user_id, totale=0)
    try:
        ordine.save()
    except Exception as e:
        raise ValueError(f"Errore durante la creazione dell'ordine: {str(e)}")

    # Recupera gli articoli del carrello
    carrello_items = Carrello.query.filter_by(id_utente=user_id).all()
    totale_ordine = 0

    for item in carrello_items:
        processa_articolo(item.id_prodotto, item.quantita)  # Scala quantità prodotto
        dettaglio = crea_dettaglio_ordine(
            id_ordine=ordine.id,
            id_prodotto=item.id_prodotto,
            id_utente=user_id,
            quantita=item.quantita,
            prezzo_unitario=item.prodotto.prezzo,
        )
        totale_ordine += dettaglio.calcola_totale_dettaglio()

    # Aggiorna il totale dell'ordine
    ordine.totale = totale_ordine
    try:
        ordine.save()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante l'aggiornamento del totale ordine: {str(e)}")

    # Svuota il carrello
    svuota_carrello(user_id)

    return ordine


def visualizza_dettagli_ordine(id_ordine):
    """
    Visualizza i dettagli di un ordine specifico.
    """
    dettagli = OrdineDettaglio.query.filter_by(id_ordine=id_ordine).all()
    if not dettagli:
        raise ValueError(f"Nessun dettaglio trovato per l'ordine con ID {id_ordine}")
    return [dettaglio.to_dict() for dettaglio in dettagli]


def aggiorna_stato_dettaglio(id_dettaglio, nuovo_stato_descrizione):
    """
    Aggiorna lo stato di un dettaglio ordine e propaga lo stato all'ordine.
    """
    try:
        # Recupera il dettaglio ordine
        dettaglio = OrdineDettaglio.query.get_or_404(
            id_dettaglio, description="Dettaglio non trovato"
        )
        print(f"Dettaglio trovato: {dettaglio.to_dict()}")

        # Recupera il nuovo stato
        nuovo_stato = recupera_stato(nuovo_stato_descrizione)
        print(f"Nuovo stato recuperato: {nuovo_stato.descrizione}")

        # Aggiorna lo stato del dettaglio
        dettaglio.id_stato = nuovo_stato.id
        dettaglio.save()
        print(f"Stato dettaglio aggiornato con successo.")

        # Propaga lo stato all'ordine
        _propaga_stato_all_ordine(dettaglio.id_ordine)
        print(f"Propagazione dello stato completata.")
    except Exception as e:
        print(f"Errore durante l'aggiornamento dello stato dettaglio: {str(e)}")
        raise


def _propaga_stato_all_ordine(id_ordine):
    """
    Aggiorna lo stato dell'ordine in base agli stati dei suoi dettagli e crea un log.
    """
    try:
        # Recupera l'ordine
        ordine = Ordine.query.get_or_404(id_ordine, description="Ordine non trovato")

        # Recupera gli stati di tutti i dettagli ordine
        stati_dettagli = {
            dettaglio.stato.descrizione for dettaglio in ordine.ordine_dettagli
        }

        # Determina il nuovo stato dell'ordine
        if stati_dettagli == {"Evaso"}:  # Tutti i dettagli sono "Evaso"
            nuovo_stato = "Evaso"
        elif (
            "In Lavorazione" in stati_dettagli
        ):  # Almeno un dettaglio è "In Lavorazione"
            nuovo_stato = "In Lavorazione"
        else:
            print(f"Nessuna modifica necessaria allo stato dell'ordine {id_ordine}.")
            return

        # Recupera lo stato corrente dell'ordine (dal log più recente)
        stato_corrente = (
            ordine.log_stati[-1].stato.descrizione if ordine.log_stati else None
        )

        # Aggiorna solo se il nuovo stato è diverso da quello corrente
        if stato_corrente != nuovo_stato:
            # Recupera l'entità dello stato corrispondente
            stato = Stato.query.filter_by(descrizione=nuovo_stato).first()
            if not stato:
                raise ValueError(f"Stato '{nuovo_stato}' non trovato nel database.")

            # Crea un nuovo log dello stato
            nuovo_log = LogStato(id_ordine=id_ordine, id_stato=stato.id)
            nuovo_log.save()
            print(
                f"Log di stato aggiornato: Ordine {id_ordine}, Nuovo Stato: {nuovo_stato}"
            )
        else:
            print(f"Nessuna modifica necessaria allo stato dell'ordine {id_ordine}.")
    except Exception as e:
        print(
            f"Errore durante la propagazione dello stato per l'ordine {id_ordine}: {str(e)}"
        )
        raise
