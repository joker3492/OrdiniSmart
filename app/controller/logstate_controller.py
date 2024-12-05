from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.schemas.log_stato_schema import log_stato_schema
from app.models.utente import Utente
from app.models.ordine import Ordine
from app.services.log_stato_service import visualizza_log_stati

log_stato_ns = Namespace("log_stato", description="Gestione dei log stato")


@log_stato_ns.route("/<int:ordine_id>")
class LogStatoResource(Resource):
    @jwt_required()
    @log_stato_ns.response(200, "Elenco dei log stati")
    @log_stato_ns.response(404, "Ordine non trovato")
    @log_stato_ns.response(403, "Accesso negato")
    def get(self, ordine_id):
        """Ottiene tutti i log stato per un ordine specifico"""
        try:
            # Ottieni l'utente autenticato
            current_user_id = get_jwt_identity()
            utente = Utente.query.get(current_user_id)

            # Controlla se l'ordine esiste
            ordine = Ordine.query.get(ordine_id)
            if not ordine:
                return {"message": "Ordine non trovato"}, 404

            # Controlla i permessi
            if not utente.is_admin and ordine.id_utente != utente.id:
                return {"message": "Accesso negato: l'ordine non ti appartiene"}, 403

            # Recupera i log di stato
            log_stati = visualizza_log_stati(ordine_id)
            return {
                "log_stati": log_stati
            }, 200  # log_stati è già una lista di dizionari
        except ValueError as e:
            return {"message": str(e)}, 400
