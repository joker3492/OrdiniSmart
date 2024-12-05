from app.models.prodotto import Prodotto
from app.models.categoria import Categoria
from sqlalchemy.exc import IntegrityError
from app.services.categoria_service import verifica_categoria_esiste
from app.extensions import db


def aggiungi_prodotto(
    id_categoria, id_admin, nome, url_foto=None, prezzo=0.0, quantita=0
):
    """Aggiunge un nuovo prodotto."""
    verifica_categoria_esiste(id_categoria)

    prodotto = Prodotto(
        id_categoria=id_categoria,
        id_admin=id_admin,
        nome=nome,
        url_foto=url_foto,
        prezzo=prezzo,
        quantita=quantita,
    )
    try:
        prodotto.save()
        return prodotto
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Errore durante l'inserimento del prodotto.")


def modifica_prodotto(id_prodotto, id_admin, **kwargs):
    """Modifica un prodotto esistente."""
    prodotto = Prodotto.query.get(id_prodotto)
    if not prodotto:
        raise ValueError("Prodotto non trovato.")

    for campo, valore in kwargs.items():
        if hasattr(prodotto, campo):
            setattr(prodotto, campo, valore)

    try:
        prodotto.save()
        return prodotto
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Errore durante l'aggiornamento del prodotto.")


def elimina_prodotto(id_prodotto, id_admin):
    """Elimina un prodotto esistente."""
    prodotto = Prodotto.query.get(id_prodotto)

    if not prodotto:
        raise ValueError(f"Prodotto con ID {id_prodotto} non trovato.")

    print(f"Debug - elimina_prodotto - Prodotto: {prodotto.to_dict()}")

    try:
        prodotto.delete()
        print(f"Debug - elimina_prodotto - Prodotto con ID {id_prodotto} eliminato.")
        return {"message": f"Prodotto con ID {id_prodotto} eliminato con successo."}
    except Exception as e:
        print(f"Debug - elimina_prodotto - Errore: {str(e)}")
        db.session.rollback()
        raise ValueError(f"Errore durante l'eliminazione del prodotto: {str(e)}")


def visualizza_prodotti(id_categoria=None):
    """Restituisce l'elenco dei prodotti, eventualmente filtrati per categoria."""
    query = Prodotto.query
    if id_categoria:
        verifica_categoria_esiste(id_categoria)
        query = query.filter_by(id_categoria=id_categoria)
    return [prodotto.to_dict() for prodotto in query.all()]


def verifica_disponibilita_prodotto(id_prodotto, quantita):
    """
    Verifica se un prodotto ha quantità sufficiente disponibile.
    """
    prodotto = Prodotto.query.get(id_prodotto)
    if not prodotto:
        raise ValueError(f"Prodotto con ID {id_prodotto} non trovato.")
    if prodotto.quantita < quantita:
        raise ValueError(
            f"Quantità richiesta ({quantita}) non disponibile per il prodotto '{prodotto.nome}'. Disponibile: {prodotto.quantita}."
        )
    return prodotto


def scala_quantita_prodotto(prodotto_id, quantita):
    """
    Scala la quantità di un prodotto dopo la conferma dell'ordine.
    """
    prodotto = verifica_disponibilita_prodotto(prodotto_id, quantita)
    prodotto.quantita -= quantita
    try:
        prodotto.save()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante l'aggiornamento della quantità: {str(e)}")


def processa_articolo(prodotto_id, quantita):
    """Verifica disponibilità, scala la quantità e restituisce il prodotto."""
    prodotto = Prodotto.query.get(prodotto_id)
    if not prodotto:
        raise ValueError(f"Prodotto con ID {prodotto_id} non trovato.")

    if prodotto.quantita < quantita:
        raise ValueError(
            f"Quantità insufficiente per il prodotto '{prodotto.nome}'. Disponibile: {prodotto.quantita}."
        )

    prodotto.quantita -= quantita
    try:
        prodotto.save()  # Usa il metodo `save` già presente nel modello
        return prodotto
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Errore durante l'aggiornamento del prodotto: {str(e)}")
