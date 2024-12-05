from flask_restx import Model, fields
from app.schemas.prodotto_schema import prodotto_output_model


carrello_item_model = Model(
    "CarrelloItem",
    {
        "quantita": fields.Integer(required=True, description="Quantità del prodotto"),
    },
)


# Modello per rappresentare un articolo del carrello
carrello_item_output_model = Model(
    "CarrelloItemOutput",
    {
        "id": fields.Integer(
            readOnly=True, description="ID dell'articolo del carrello"
        ),
        "id_utente": fields.Integer(
            readOnly=True, description="ID dell'utente proprietario del carrello"
        ),
        "id_prodotto": fields.Integer(
            readOnly=True, description="ID del prodotto nel carrello"
        ),
        "quantita": fields.Integer(
            readOnly=True, description="Quantità del prodotto nel carrello"
        ),
        "prodotto": fields.Nested(
            prodotto_output_model,
            description="Dettagli del prodotto",
        ),
    },
)

# Modello per rappresentare l'elenco degli articoli nel carrello
carrello_output_model = Model(
    "Carrello",
    {
        "carrello": fields.List(
            fields.Nested(carrello_item_output_model),
            description="Elenco degli articoli nel carrello",
        )
    },
)
