from app import create_app
from app.extensions import db
from app.models.utente import Utente
from app.models.categoria import Categoria
from app.models.prodotto import Prodotto


def drop_and_create_all():
    """Drop e ricrea tutte le tabelle del database."""
    print("Droppando e ricreando il database...")
    db.drop_all()
    db.create_all()
    print("Database ricreato con successo!")


def create_user(username, password, is_admin):
    """Crea un utente nel database."""
    try:
        user = Utente(username=username, is_admin=is_admin)
        user.set_password(password)
        user.save()
        print(f"Utente creato: {user.username}, Admin: {user.is_admin}")
        return user
    except Exception as e:
        print(f"Errore durante la creazione dell'utente: {e}")


def create_category(descrizione):
    """Crea una categoria nel database."""
    try:
        categoria = Categoria(descrizione=descrizione)
        categoria.save()
        print(f"Categoria creata: {categoria.descrizione}")
        return categoria
    except Exception as e:
        print(f"Errore durante la creazione della categoria: {e}")


def create_product(nome, id_categoria, id_admin, prezzo, quantita, url_foto=None):
    """Crea un prodotto nel database."""
    try:
        prodotto = Prodotto(
            nome=nome,
            id_categoria=id_categoria,
            id_admin=id_admin,
            prezzo=prezzo,
            quantita=quantita,
            url_foto=url_foto,
        )
        prodotto.save()
        print(
            f"Prodotto creato: {prodotto.nome}, Prezzo: {prodotto.prezzo}, Quantità: {prodotto.quantita}, URL Foto: {prodotto.url_foto}"
        )
        return prodotto
    except Exception as e:
        print(f"Errore durante la creazione del prodotto: {e}")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Drop e ricrea il database
        drop_and_create_all()

        # Crea utenti
        admin = create_user(username="admin_user", password="adminpass", is_admin=True)
        user = create_user(
            username="standard_user", password="userpass", is_admin=False
        )

        # Popola il database con due categorie
        categoria1 = create_category("Frutta")
        categoria2 = create_category("Verdura")

        # Aggiungi prodotti collegati alle categorie
        prodotto1 = create_product(
            nome="Mela",
            id_categoria=categoria1.id,
            id_admin=admin.id,
            prezzo=1.5,
            quantita=100,
            url_foto="http://example.com/mela.jpg",
        )
        prodotto2 = create_product(
            nome="Carota",
            id_categoria=categoria2.id,
            id_admin=admin.id,
            prezzo=0.8,
            quantita=200,
            url_foto="http://example.com/carota.jpg",
        )

        print("Database popolato con successo!")
