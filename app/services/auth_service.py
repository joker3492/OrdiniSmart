from app.models.utente import Utente
from app.models.prodotto import Prodotto
from flask_jwt_extended import create_access_token


def login(data):
    """Logica di autenticazione per gli utenti"""
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise ValueError("Username e password sono obbligatori")

    utente = Utente.query.filter_by(username=username).first()

    if not utente or not utente.check_password(password):
        raise ValueError("Credenziali non valide")

    # Genera un token JWT
    access_token = create_access_token(
        identity=str(utente.id),  # L'identity deve essere una stringa
        additional_claims={
            "is_admin": utente.is_admin
        },  # Aggiungi claims personalizzati
    )
    return access_token


def register(data):
    """Registra un nuovo utente"""
    username = data.get("username")
    password = data.get("password")
    is_admin = data.get("is_admin", False)  # Per default, non è admin

    # Validazioni
    if not username or not password:
        raise ValueError("Username e password sono obbligatori")

    # Controlla se l'utente esiste già
    if Utente.query.filter_by(username=username).first():
        raise ValueError("Il nome utente è già in uso")

    # Crea un nuovo utente
    nuovo_utente = Utente(username=username, is_admin=is_admin)
    nuovo_utente.set_password(password)

    # Salva l'utente nel database
    try:
        nuovo_utente.save()
    except Exception as e:
        raise ValueError(f"Errore durante la registrazione dell'utente: {str(e)}")

    return {"message": "Utente registrato con successo", "id": nuovo_utente.id}


def read_user(user_id):
    """Legge i dettagli di un utente"""
    utente = Utente.query.get(user_id)
    if not utente:
        raise ValueError("Utente non trovato")

    return {
        "id": utente.id,
        "username": utente.username,
        "is_admin": utente.is_admin,
        "data_registrazione": (
            utente.data_registrazione.isoformat() if utente.data_registrazione else None
        ),
        "data_modifica": (
            utente.data_modifica.isoformat() if utente.data_modifica else None
        ),
    }


def update_user(user_id, data):
    """Aggiorna i dettagli di un utente"""
    utente = Utente.query.get(user_id)
    if not utente:
        raise ValueError("Utente non trovato")

    # Aggiorna i campi
    username = data.get("username")
    password = data.get("password")
    is_admin = data.get("is_admin")

    if username:
        utente.username = username
    if password:
        utente.set_password(password)
    if is_admin is not None:
        utente.is_admin = is_admin

    try:
        utente.save()
    except Exception as e:
        raise ValueError("Errore durante l'aggiornamento dell'utente")

    return {"message": "Utente aggiornato con successo"}


def delete_user(user_id):
    """Elimina un utente"""
    utente = Utente.query.get(user_id)
    if not utente:
        raise ValueError("Utente non trovato")

    try:
        utente.delete()
    except Exception as e:
        raise ValueError("Errore durante l'eliminazione dell'utente")

    return {"message": "Utente eliminato con successo"}


def verifica_admin(user_id):
    """
    Verifica se un utente è un admin.
    """
    verifica_ruolo(user_id, deve_essere_admin=True)


def verifica_utente_standard(user_id):
    """
    Verifica se un utente è un utente standard (non admin).
    """
    verifica_ruolo(user_id, deve_essere_admin=False)


def verifica_admin_e_proprietario(id_prodotto, id_admin):
    """
    Verifica che l'utente sia un admin e il proprietario del prodotto.
    """
    verifica_admin(id_admin)  # Verifica che l'utente sia un admin

    prodotto = Prodotto.query.get(id_prodotto)
    if not prodotto:
        raise ValueError(f"Prodotto con ID {id_prodotto} non trovato.")

    if prodotto.id_admin != id_admin:
        raise PermissionError(
            f"L'utente con ID {id_admin} non ha i permessi per modificare o eliminare il prodotto '{prodotto.nome}' (ID: {id_prodotto})."
        )


def verifica_ruolo(user_id, deve_essere_admin=True):
    """
    Verifica il ruolo dell'utente.

    Args:
        user_id (int): ID dell'utente da verificare.
        deve_essere_admin (bool): True se l'utente deve essere admin, False altrimenti.

    Raises:
        ValueError: Se l'utente non esiste.
        PermissionError: Se l'utente non ha il ruolo richiesto.
    """
    utente = Utente.query.get(user_id)
    if not utente:
        raise ValueError(f"Utente con ID {user_id} non trovato.")

    if utente.is_admin != deve_essere_admin:
        ruolo_richiesto = "admin" if deve_essere_admin else "utente standard"
        raise PermissionError(
            f"L'utente con ID {user_id} non ha il ruolo richiesto: {ruolo_richiesto}."
        )
