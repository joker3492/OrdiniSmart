from flask_restx import Model, fields

prodotto_model = Model(
    "Prodotto",
    {
        "id_categoria": fields.Integer(required=True, description="ID della categoria"),
        "nome": fields.String(required=True, description="Nome del prodotto"),
        "url_foto": fields.String(required=False, description="URL dell'immagine"),
        "prezzo": fields.Float(required=True, description="Prezzo del prodotto"),
        "quantita": fields.Integer(required=True, description="Quantità disponibile"),
    },
)


# Modello per aggiornare un prodotto esistente
prodotto_update_model = Model(
    "ProdottoUpdate",
    {
        "nome": fields.String(description="Nuovo nome del prodotto"),
        "url_foto": fields.String(required=False, description="URL dell'immagine"),
        "prezzo": fields.Float(description="Nuovo prezzo del prodotto"),
        "quantita": fields.Integer(description="Nuova quantità disponibile"),
    },
)

# Modello per rappresentare un prodotto (inclusivo di ID)
prodotto_output_model = Model(
    "ProdottoOutput",
    {
        "id": fields.Integer(readOnly=True, description="ID del prodotto"),
        "id_categoria": fields.Integer(readOnly=True, description="ID della categoria"),
        "nome": fields.String(readOnly=True, description="Nome del prodotto"),
        "url_foto": fields.String(required=False, description="URL dell'immagine"),
        "prezzo": fields.Float(readOnly=True, description="Prezzo del prodotto"),
        "quantita": fields.Integer(readOnly=True, description="Quantità disponibile"),
    },
)
