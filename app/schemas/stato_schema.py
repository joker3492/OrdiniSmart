from flask_restx import Model, fields

stato_schema = Model(
    "Stato",
    {
        "id": fields.Integer(description="ID dello stato"),
        "descrizione": fields.String(
            required=True, description="Descrizione dello stato"
        ),
    },
)
