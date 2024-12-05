from app.models.logstato import LogStato
from app.models.stato import Stato
from datetime import datetime


def recupera_stato(descrizione):
    """
    Recupera uno stato dal database o solleva un'eccezione.
    """
    stato = Stato.query.filter_by(descrizione=descrizione).first()
    if not stato:
        raise ValueError(f"Lo stato '{descrizione}' non esiste nel sistema.")
    return stato


def crea_log(id_ordine, descrizione_stato):
    """
    Crea un log per un ordine specifico.
    """
    stato = recupera_stato(descrizione_stato)
    log_stato = LogStato(
        id_ordine=id_ordine, id_stato=stato.id, data_modifica=datetime.utcnow()
    )
    log_stato.save()
    return log_stato


def visualizza_log_stati(id_ordine):
    """Visualizza tutti i log di stato di un ordine."""
    if not id_ordine:
        raise ValueError("ID ordine non fornito.")

    log_stati = (
        LogStato.query.filter_by(id_ordine=id_ordine)
        .order_by(LogStato.data_modifica)
        .all()
    )
    if not log_stati:
        raise ValueError(
            f"Nessun log di stato trovato per l'ordine con ID {id_ordine}."
        )
    return [log.to_dict() for log in log_stati]
