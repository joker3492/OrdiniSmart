from marshmallow import Schema, fields, validates, ValidationError


class ProdottoSchema(Schema):
    id = fields.Integer(dump_only=True)
    id_categoria = fields.Integer(required=True, description="ID della categoria")
    id_admin = fields.Integer(dump_only=True)  # Gestito automaticamente
    nome = fields.String(
        required=True, validate=lambda x: len(x) > 0, description="Nome del prodotto"
    )
    prezzo = fields.Float(
        required=True,
        description="Prezzo del prodotto",
        validate=lambda x: x > 0,  # Assicura che il prezzo sia maggiore di zero
    )
    quantita = fields.Integer(
        required=True,
        description="Quantità disponibile",
        validate=lambda x: x >= 0,  # Assicura che la quantità non sia negativa
    )
    url_foto = fields.String(
        required=False,
        description="URL dell'immagine del prodotto",
        allow_none=True,  # Consente il valore None
    )

    @validates("url_foto")
    def validate_url_foto(self, value):
        if value and not value.startswith(("http://", "https://")):
            raise ValidationError(
                "L'URL dell'immagine deve essere valido (http/https)."
            )
