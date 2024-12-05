from flask import request, jsonify
from flask_restx import Namespace, Resource
from app.schemas.auth_schema import auth_schema
from app.schemas.auth_schema import register_schema
from app.services.auth_service import login, register
from flask_jwt_extended import jwt_required, get_jwt_identity


auth_ns = Namespace("auth", description="Operazioni di autenticazione")
auth_ns.models[auth_schema.name] = auth_schema  # Registra il modello con il namespace
auth_ns.models[register_schema.name] = (
    register_schema  # Registra il modello con il namespace
)


@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_schema, validate=True)
    @auth_ns.response(201, "Utente registrato con successo")
    @auth_ns.response(400, "Errore di validazione o registrazione")
    def post(self):
        """Registra un nuovo utente"""
        try:
            data = request.json
            response = register(data)
            return response, 201
        except ValueError as e:
            return {"message": str(e)}, 400


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(auth_schema, validate=True)
    def post(self):
        """Gestisce il login degli utenti"""
        try:
            data = request.json
            token = login(data)
            return {"access_token": token}, 200
        except ValueError as e:
            return {"message": str(e)}, 400
