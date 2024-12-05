from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from marshmallow import ValidationError
from app.services.prodotto_service import (
    aggiungi_prodotto,
    modifica_prodotto,
    elimina_prodotto,
    visualizza_prodotti,
)
from app.services.auth_service import verifica_admin, verifica_admin_e_proprietario
from app.validation.prodotto_schema import ProdottoSchema
from app.schemas.prodotto_schema import (
    prodotto_model,
    prodotto_update_model,
    prodotto_output_model,
)

prodotto_ns = Namespace("prodotti", description="Gestione dei prodotti")
prodotto_schema = ProdottoSchema()

# Registra i modelli in Swagger
prodotto_ns.models[prodotto_model.name] = prodotto_model
prodotto_ns.models[prodotto_update_model.name] = prodotto_update_model
prodotto_ns.models[prodotto_output_model.name] = prodotto_output_model


@prodotto_ns.route("/")
class ProdottoList(Resource):
    @jwt_required()
    @prodotto_ns.expect(prodotto_model, validate=True)
    def post(self):
        """Aggiunge un nuovo prodotto (solo per admin)."""
        current_user_id = get_jwt_identity()
        try:
            verifica_admin(current_user_id)  # Verifica se è admin
            data = request.json
            valid_data = prodotto_schema.load(data)  # Validazione schema

            prodotto = aggiungi_prodotto(id_admin=current_user_id, **valid_data)
            return {
                "message": "Prodotto creato con successo",
                "prodotto": prodotto.to_dict(),
            }, 201
        except PermissionError as e:
            return {"message": str(e)}, 403
        except ValidationError as err:
            return {"errors": err.messages}, 400
        except ValueError as e:
            return {"message": str(e)}, 400

    def get(self):
        """Visualizza tutti i prodotti (opzionalmente filtrati per categoria)."""
        id_categoria = request.args.get("id_categoria", type=int)
        prodotti = visualizza_prodotti(id_categoria)
        return {"prodotti": prodotti}, 200


@prodotto_ns.route("/<int:id_prodotto>")
class ProdottoResource(Resource):
    @jwt_required()
    @prodotto_ns.expect(prodotto_update_model, validate=True)
    def put(self, id_prodotto):
        """Modifica un prodotto esistente (solo admin e proprietario)."""
        current_user_id = int(get_jwt_identity())  # Cast esplicito a int
        try:
            verifica_admin_e_proprietario(id_prodotto, current_user_id)

            data = request.json
            valid_data = prodotto_schema.load(data)  # Validazione schema

            prodotto = modifica_prodotto(
                id_prodotto=id_prodotto,
                id_admin=current_user_id,
                **valid_data,
            )
            print("Debug - PUT - Prodotto aggiornato con successo.")
            return {
                "message": "Prodotto aggiornato con successo",
                "prodotto": prodotto.to_dict(),
            }, 200
        except PermissionError as e:
            print(f"Debug - PUT - PermissionError: {str(e)}")
            return {"message": str(e)}, 403
        except ValidationError as err:
            print(f"Debug - PUT - ValidationError: {err.messages}")
            return {"errors": err.messages}, 400
        except ValueError as e:
            print(f"Debug - PUT - ValueError: {str(e)}")
            return {"message": str(e)}, 400

    @jwt_required()
    def delete(self, id_prodotto):
        """Elimina un prodotto esistente (solo admin e proprietario)."""
        current_user_id = int(get_jwt_identity())  # Cast esplicito a int

        print(f"Debug - DELETE - ID utente autenticato: {current_user_id}")
        print(f"Debug - DELETE - Prodotto richiesto per eliminazione: {id_prodotto}")

        try:
            verifica_admin_e_proprietario(id_prodotto, current_user_id)

            response = elimina_prodotto(id_prodotto, id_admin=current_user_id)
            print(f"Debug - DELETE - Prodotto eliminato con successo.")
            return response, 200
        except PermissionError as e:
            print(f"Debug - DELETE - PermissionError: {str(e)}")
            return {"message": str(e)}, 403
        except ValueError as e:
            print(f"Debug - DELETE - ValueError: {str(e)}")
            return {"message": str(e)}, 400
