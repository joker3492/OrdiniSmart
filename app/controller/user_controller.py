from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import read_user, update_user, delete_user
from app.schemas.auth_schema import register_schema

user_ns = Namespace("user", description="Operazioni sugli utenti")


@user_ns.route("/<int:user_id>")
class UserResource(Resource):
    @user_ns.doc(
        security="Bearer Auth"
    )  # Specifica che questo endpoint utilizza il token JWT
    @user_ns.response(200, "Dettagli utente restituiti con successo")
    @user_ns.response(404, "Utente non trovato")
    @jwt_required()
    def get(self, user_id):
        """Ottiene i dettagli di un utente"""
        try:
            current_user_id = get_jwt_identity()
            if str(current_user_id) != str(user_id):
                return {"message": "Accesso non autorizzato"}, 403
            user = read_user(user_id)
            return user, 200
        except ValueError as e:
            return {"message": str(e)}, 404

    @user_ns.doc(
        security="Bearer Auth"
    )  # Specifica che questo endpoint utilizza il token JWT
    @user_ns.expect(register_schema, validate=True)
    @user_ns.response(200, "Utente aggiornato con successo")
    @user_ns.response(404, "Utente non trovato")
    @jwt_required()
    def put(self, user_id):
        """Aggiorna i dettagli di un utente"""
        try:
            current_user_id = get_jwt_identity()
            if str(current_user_id) != str(user_id):
                return {"message": "Accesso non autorizzato"}, 403
            data = request.json
            response = update_user(user_id, data)
            return response, 200
        except ValueError as e:
            return {"message": str(e)}, 404

    @user_ns.doc(
        security="Bearer Auth"
    )  # Specifica che questo endpoint utilizza il token JWT
    @user_ns.response(200, "Utente eliminato con successo")
    @user_ns.response(404, "Utente non trovato")
    @jwt_required()
    def delete(self, user_id):
        """Elimina un utente"""
        try:
            current_user_id = get_jwt_identity()
            if str(current_user_id) != str(user_id):
                return {"message": "Accesso non autorizzato"}, 403
            response = delete_user(user_id)
            return response, 200
        except ValueError as e:
            return {"message": str(e)}, 404
