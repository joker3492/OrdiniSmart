from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from flask import request
from app.services.carrello_service import (
    aggiungi_al_carrello,
    rimuovi_dal_carrello,
    visualizza_carrello,
    svuota_carrello,
)
from app.services.auth_service import verifica_utente_standard
from app.schemas.carrello_schema import (
    carrello_item_model,
    carrello_item_output_model,
    carrello_output_model,
)
from app.validation.carrello_schema import CarrelloItemSchema

# Inizializza lo schema per la validazione con Marshmallow
carrello_item_schema = CarrelloItemSchema()

# Namespace per Swagger
carrello_ns = Namespace("carrello", description="Gestione del carrello")

# Registra i modelli per Swagger
carrello_ns.models[carrello_item_model.name] = carrello_item_model
carrello_ns.models[carrello_item_output_model.name] = carrello_item_output_model
carrello_ns.models[carrello_output_model.name] = carrello_output_model


@carrello_ns.route("/")
class CarrelloList(Resource):
    @jwt_required()
    @carrello_ns.response(200, "Success", carrello_output_model)
    def get(self):
        """Visualizza il carrello dell'utente."""
        user_id = int(get_jwt_identity())
        try:
            verifica_utente_standard(user_id)  # Verifica che sia un utente standard
            return {"carrello": visualizza_carrello(user_id)}, 200
        except PermissionError as e:
            return {"message": str(e)}, 403
        except Exception as e:
            return {"message": str(e)}, 400

    @jwt_required()
    @carrello_ns.response(200, "Carrello svuotato con successo")
    def delete(self):
        """Svuota il carrello dell'utente."""
        user_id = int(get_jwt_identity())
        try:
            verifica_utente_standard(user_id)
            return svuota_carrello(user_id), 200
        except PermissionError as e:
            return {"message": str(e)}, 403
        except Exception as e:
            return {"message": str(e)}, 400


@carrello_ns.route("/<int:prodotto_id>")
class CarrelloItem(Resource):
    @jwt_required()
    @carrello_ns.expect(carrello_item_model, validate=True)
    @carrello_ns.response(
        201, "Articolo aggiunto al carrello", carrello_item_output_model
    )
    def post(self, prodotto_id):
        """Aggiunge un prodotto al carrello."""
        user_id = int(get_jwt_identity())
        try:
            verifica_utente_standard(user_id)
            data = request.json  # Payload JSON
            valid_data = carrello_item_schema.load(data)  # Valida il payload
            quantita = valid_data["quantita"]

            articolo = aggiungi_al_carrello(user_id, prodotto_id, quantita)
            return {"articolo": articolo}, 201
        except ValidationError as e:
            return {"message": e.messages}, 400
        except PermissionError as e:
            return {"message": str(e)}, 403
        except Exception as e:
            return {"message": str(e)}, 400

    @jwt_required()
    @carrello_ns.response(200, "Articolo rimosso dal carrello")
    def delete(self, prodotto_id):
        """Rimuove un prodotto dal carrello."""
        user_id = int(get_jwt_identity())
        try:
            verifica_utente_standard(user_id)
            return rimuovi_dal_carrello(user_id, prodotto_id), 200
        except PermissionError as e:
            return {"message": str(e)}, 403
        except Exception as e:
            return {"message": str(e)}, 400


@carrello_ns.route("/")
class CarrelloList(Resource):
    @jwt_required()
    @carrello_ns.response(200, "Success", carrello_output_model)
    def get(self):
        """Visualizza il carrello dell'utente."""
        user_id = int(get_jwt_identity())  # Cast esplicito a int
        try:
            verifica_utente_standard(user_id)  # Verifica che l'utente sia standard
            return {"carrello": visualizza_carrello(user_id)}, 200
        except PermissionError as e:
            return {"message": str(e)}, 403
        except Exception as e:
            return {"message": str(e)}, 400

    @jwt_required()
    @carrello_ns.response(200, "Carrello svuotato con successo")
    def delete(self):
        """Svuota il carrello dell'utente."""
        user_id = int(get_jwt_identity())  # Cast esplicito a int
        try:
            verifica_utente_standard(user_id)
            return svuota_carrello(user_id), 200
        except PermissionError as e:
            return {"message": str(e)}, 403
        except Exception as e:
            return {"message": str(e)}, 400
