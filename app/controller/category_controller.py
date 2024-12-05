from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.categoria_service import (
    aggiungi_categoria,
    modifica_categoria,
    elimina_categoria,
    visualizza_categorie,
)
from app.schemas.categoria_schema import categoria_model, categoria_update_model

categoria_ns = Namespace("categorie", description="Gestione delle categorie")
categoria_ns.models[categoria_model.name] = categoria_model
categoria_ns.models[categoria_update_model.name] = categoria_update_model


@categoria_ns.route("/")
class CategoriaList(Resource):
    @jwt_required()
    def get(self):
        """Visualizza tutte le categorie (accessibile a tutti gli utenti)."""
        categorie = visualizza_categorie()
        return {"categorie": categorie}, 200

    @jwt_required()
    @categoria_ns.expect(categoria_model, validate=True)
    def post(self):
        """Aggiunge una nuova categoria (accessibile solo agli admin)."""
        current_user_id = get_jwt_identity()
        data = request.json
        try:
            categoria = aggiungi_categoria(data["descrizione"], current_user_id)
            return {
                "message": "Categoria creata con successo",
                "categoria": categoria.to_dict(),
            }, 201
        except PermissionError as e:
            return {"message": str(e)}, 403
        except ValueError as e:
            return {"message": str(e)}, 400


@categoria_ns.route("/<int:id_categoria>")
class CategoriaResource(Resource):
    @jwt_required()
    @categoria_ns.expect(categoria_update_model, validate=True)
    def put(self, id_categoria):
        """Modifica una categoria esistente (accessibile solo agli admin)."""
        current_user_id = get_jwt_identity()
        data = request.json
        try:
            categoria = modifica_categoria(
                id_categoria, data["descrizione"], current_user_id
            )
            return {
                "message": "Categoria aggiornata con successo",
                "categoria": categoria.to_dict(),
            }, 200
        except PermissionError as e:
            return {"message": str(e)}, 403
        except ValueError as e:
            return {"message": str(e)}, 400

    @jwt_required()
    def delete(self, id_categoria):
        """Elimina una categoria (accessibile solo agli admin)."""
        current_user_id = get_jwt_identity()
        try:
            response = elimina_categoria(id_categoria, current_user_id)
            return response, 200
        except PermissionError as e:
            return {"message": str(e)}, 403
        except ValueError as e:
            if "prodotti associati" in str(e).lower():
                return {
                    "message": "Categoria non eliminabile: ci sono prodotti associati"
                }, 400
        return {"message": str(e)}, 400
