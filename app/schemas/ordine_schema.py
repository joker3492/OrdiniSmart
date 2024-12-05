from flask_restx import Model, fields

# Modello di schema per Ordine
ordine_schema = Model(
    "OrdineSchema",
    {
        "id": fields.Integer(readOnly=True, description="ID dell'ordine"),
        "id_utente": fields.Integer(
            required=True, description="ID dell'utente associato"
        ),
        "data_creazione": fields.DateTime(
            readOnly=True, description="Data di creazione dell'ordine"
        ),
        "totale": fields.Float(readOnly=True, description="Totale dell'ordine"),
    },
)
