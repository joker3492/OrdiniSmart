from flask_restx import Model, fields

log_stato_schema = Model(
    "LogStato",
    {
        "id_ordine": fields.Integer(required=True, description="ID dell'ordine"),
        "id_stato": fields.Integer(required=True, description="ID dello stato"),
        "data_modifica": fields.DateTime(description="Data della modifica dello stato"),
    },
)
