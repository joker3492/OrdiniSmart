from flask_restx import Model, fields

# Modello di schema per l'autenticazione
auth_schema = Model(
    "AuthSchema",
    {
        "username": fields.String(required=True, description="Nome utente"),
        "password": fields.String(required=True, description="Password"),
    },
)

# Modello di schema per la registrazione
register_schema = Model(
    "RegisterSchema",
    {
        "username": fields.String(required=True, description="Nome utente"),
        "password": fields.String(required=True, description="Password"),
        "is_admin": fields.Boolean(
            description="Indica se l'utente è un amministratore"
        ),
    },
)
