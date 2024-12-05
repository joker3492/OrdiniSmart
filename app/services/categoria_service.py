from app.models.categoria import Categoria
from app.models.prodotto import Prodotto
from app.extensions import db
from app.services.auth_service import verifica_admin
from sqlalchemy.exc import IntegrityError


def aggiungi_categoria(descrizione, id_admin):
    """Aggiunge una nuova categoria (accessibile solo agli admin)."""
    # Verifica che l'utente sia admin
    verifica_admin(id_admin)

    if Categoria.query.filter_by(descrizione=descrizione).first():
        raise ValueError("Una categoria con questa descrizione esiste già.")

    categoria = Categoria(descrizione=descrizione)
    try:
        categoria.save()
    except IntegrityError:
        raise ValueError("Una categoria con questa descrizione esiste già.")
    return categoria


def modifica_categoria(id_categoria, nuova_descrizione, id_admin):
    """Modifica una categoria esistente (accessibile solo agli admin)."""
    # Verifica che l'utente sia admin
    verifica_admin(id_admin)

    categoria = Categoria.query.get(id_categoria)
    if not categoria:
        raise ValueError("Categoria non trovata.")

    categoria.descrizione = nuova_descrizione
    categoria.save()
    return categoria


def elimina_categoria(id_categoria, id_admin):
    """Elimina una categoria esistente (accessibile solo agli admin)."""
    # Verifica che l'utente sia admin
    verifica_admin(id_admin)

    categoria = Categoria.query.get(id_categoria)
    if not categoria:
        raise ValueError("Categoria non trovata.")

    # Verifica se ci sono prodotti associati
    prodotti_associati = Prodotto.query.filter_by(id_categoria=id_categoria).all()
    if prodotti_associati:
        raise ValueError(
            "Impossibile eliminare la categoria: ci sono prodotti associati."
        )

    categoria.delete()
    return {"message": "Categoria eliminata con successo."}


def visualizza_categorie():
    """Restituisce tutte le categorie disponibili (accessibile a tutti gli utenti)."""
    return [categoria.to_dict() for categoria in Categoria.query.all()]


def verifica_categoria_esiste(id_categoria):
    """Verifica se una categoria esiste."""
    if not Categoria.query.get(id_categoria):
        raise ValueError("Categoria non esistente.")
