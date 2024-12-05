from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services.ordine_service import (
    conferma_carrello,
    aggiorna_stato_ordine,
    elimina_ordine,
    visualizza_ordini,
)
from app.schemas.ordine_schema import ordine_schema

# Namespace per Swagger
ordine_ns = Namespace("ordini", description="Gestione degli ordini")

# Modello di input per confermare un ordine
ordine_create_model = ordine_ns.model(
    "OrdineCreate",
    {
        "id_utente": fields.Integer(
            required=True, description="ID dell'utente che conferma il carrello"
        ),
    },
)

# Modello di input per avanzare lo stato di un ordine
ordine_stato_model = ordine_ns.model(
    "OrdineStato",
    {
        "nuovo_stato": fields.String(
            required=True, description="Nuovo stato dell'ordine"
        ),
    },
)


@ordine_ns.route("/")
class OrdineList(Resource):
    @jwt_required()
    def get(self):
        """
        Ottiene tutti gli ordini dell'utente autenticato.
        """
        current_user_id = get_jwt_identity()
        try:
            ordini = visualizza_ordini(current_user_id)
            return {"ordini": ordini}, 200
        except Exception as e:
            return {"message": str(e)}, 400

    @jwt_required()
    @ordine_ns.response(201, "Ordine creato con successo", ordine_schema)
    def post(self):
        """
        Conferma il carrello dell'utente autenticato e crea un ordine.
        """
        current_user_id = get_jwt_identity()
        try:
            ordine = conferma_carrello(current_user_id)
            return {
                "message": "Ordine creato con successo",
                "ordine": ordine.to_dict(),
            }, 201
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": "Errore interno del server."}, 500


@ordine_ns.route("/<int:ordine_id>")
class OrdineResource(Resource):
    @jwt_required()
    def delete(self, ordine_id):
        """
        Elimina un ordine specifico.
        """
        try:
            elimina_ordine(ordine_id)
            return {"message": "Ordine eliminato con successo"}, 200
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": "Errore interno del server."}, 500


@ordine_ns.route("/<int:ordine_id>/stato")
class OrdineStatoResource(Resource):
    @jwt_required()
    @ordine_ns.expect(ordine_stato_model, validate=True)
    def put(self, ordine_id):
        """
        Aggiorna lo stato di un ordine specifico.
        """
        try:
            aggiorna_stato_ordine(ordine_id)
            return {"message": "Stato ordine aggiornato con successo"}, 200
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": "Errore interno del server."}, 500
