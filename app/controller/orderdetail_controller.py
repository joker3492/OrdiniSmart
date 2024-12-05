from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services.auth_service import verifica_admin
from app.services.ordinedettaglio_service import (
    aggiorna_stato_dettaglio,
    visualizza_dettagli_ordine,
)
from app.schemas.ordinedettaglio_schema import (
    ordine_dettaglio_output_model,
    ordine_output_model,
    aggiorna_stato_model,  # Importa correttamente il modello
)

ordine_dettaglio_ns = Namespace(
    "ordine_dettagli", description="Gestione dei dettagli ordine"
)

# Registra i modelli nel namespace
ordine_dettaglio_ns.models[ordine_dettaglio_output_model.name] = (
    ordine_dettaglio_output_model
)
ordine_dettaglio_ns.models[ordine_output_model.name] = ordine_output_model
ordine_dettaglio_ns.models[aggiorna_stato_model.name] = aggiorna_stato_model


@ordine_dettaglio_ns.route("/<int:ordine_id>")
class DettagliOrdine(Resource):
    @jwt_required()
    @ordine_dettaglio_ns.response(
        200, "Dettagli dell'ordine recuperati", ordine_dettaglio_output_model
    )
    def get(self, ordine_id):
        """Ottiene i dettagli di un ordine specifico."""
        try:
            dettagli = visualizza_dettagli_ordine(ordine_id)
            return {"dettagli": dettagli}, 200
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": "Errore interno del server."}, 500


@ordine_dettaglio_ns.route("/<int:id_dettaglio>/aggiorna_stato")
class AggiornaStatoDettaglio(Resource):
    @jwt_required()
    @ordine_dettaglio_ns.expect(aggiorna_stato_model, validate=True)
    def put(self, id_dettaglio):
        """Aggiorna lo stato di un dettaglio ordine."""
        data = request.json
        nuovo_stato = data.get("nuovo_stato")
        admin_id = int(get_jwt_identity())  # Recupera l'ID dell'admin autenticato

        try:
            # Verifica se l'utente è admin
            verifica_admin(admin_id)  # Controlla i permessi admin
            print(f"Utente admin verificato: ID {admin_id}")
        except PermissionError as e:
            print(f"Errore autorizzazione: {str(e)}")
            return {"message": str(e)}, 403  # Accesso negato

        try:
            # Aggiorna lo stato del dettaglio
            aggiorna_stato_dettaglio(id_dettaglio, nuovo_stato)
            print(
                f"Stato dettaglio aggiornato: Dettaglio {id_dettaglio}, Nuovo Stato: {nuovo_stato}"
            )
            return {"message": "Stato del dettaglio aggiornato con successo."}, 200
        except ValueError as e:
            print(f"Errore valore: {str(e)}")
            return {"message": str(e)}, 400
        except Exception as e:
            print(f"Errore imprevisto: {str(e)}")
            return {"message": "Errore interno del server."}, 500
