from flask_restx import Api
from app.controller.auth_controller import auth_ns
from app.controller.user_controller import user_ns
from app.controller.logstate_controller import log_stato_ns
from app.controller.order_controller import ordine_ns  # Importa il namespace ordini
from app.controller.product_controller import prodotto_ns
from app.controller.orderdetail_controller import ordine_dettaglio_ns  # Dettagli ordine
from app.controller.category_controller import (
    categoria_ns,
)  # Importa il namespace categorie
from app.controller.cart_controller import carrello_ns
from app.schemas.auth_schema import auth_schema, register_schema
from app.schemas.log_stato_schema import log_stato_schema
from app.schemas.stato_schema import stato_schema
from app.schemas.ordine_schema import ordine_schema
from app.schemas.prodotto_schema import prodotto_model, prodotto_update_model
from app.schemas.categoria_schema import categoria_model, categoria_update_model
from app.schemas.carrello_schema import (
    carrello_item_model,
    carrello_item_output_model,
    carrello_output_model,
)
from app.schemas.ordinedettaglio_schema import (
    ordine_dettaglio_output_model,
    ordine_output_model,
    aggiorna_stato_model,
)


# Configurazione dell'API RESTful con Swagger
api = Api(
    title="Ordinismart API",
    version="1.0",
    description="Documentazione API per il progetto Ordinismart",
    security="Bearer Auth",  # Definisce lo schema di sicurezza
    authorizations={
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Inserisci il token JWT nel formato: Bearer <token>",
        }
    },
)

# Registra i modelli con Swagger
api.models[auth_schema.name] = auth_schema
api.models[register_schema.name] = register_schema
api.models[stato_schema.name] = stato_schema
api.models[log_stato_schema.name] = log_stato_schema
api.models[ordine_schema.name] = ordine_schema
api.models[prodotto_model.name] = prodotto_model
api.models[prodotto_update_model.name] = prodotto_update_model
api.models[categoria_model.name] = categoria_model
api.models[categoria_update_model.name] = categoria_update_model
carrello_ns.models[carrello_item_model.name] = carrello_item_model
carrello_ns.models[carrello_item_output_model.name] = carrello_item_output_model
carrello_ns.models[carrello_output_model.name] = carrello_output_model
ordine_dettaglio_ns.models[ordine_dettaglio_output_model.name] = (
    ordine_dettaglio_output_model
)
ordine_dettaglio_ns.models[ordine_output_model.name] = ordine_output_model
ordine_dettaglio_ns.models[aggiorna_stato_model.name] = aggiorna_stato_model


# Registra i namespace
api.add_namespace(auth_ns, path="/auth")
api.add_namespace(user_ns, path="/user")
api.add_namespace(log_stato_ns, path="/log_stato")
api.add_namespace(ordine_ns, path="/ordini")  # Aggiungi il namespace per gli ordini
api.add_namespace(prodotto_ns, path="/prodotti")
api.add_namespace(categoria_ns, path="/categorie")
api.add_namespace(carrello_ns, path="/carrello")
api.add_namespace(ordine_dettaglio_ns, path="/ordine_dettagli")
