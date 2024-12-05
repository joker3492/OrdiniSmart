from flask_restx import Model, fields

categoria_model = Model(
    "Categoria",
    {
        "descrizione": fields.String(
            required=True, description="Descrizione della categoria"
        ),
    },
)

categoria_update_model = Model(
    "CategoriaUpdate",
    {
        "descrizione": fields.String(
            required=True, description="Nuova descrizione della categoria"
        ),
    },
)
