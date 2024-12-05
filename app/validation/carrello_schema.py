from marshmallow import Schema, fields, validates, ValidationError


class CarrelloItemSchema(Schema):
    quantita = fields.Integer(
        required=True,
        description="Quantità del prodotto",
        validate=lambda x: x > 0,  # Deve essere maggiore di zero
    )

    @validates("quantita")
    def validate_quantita(self, value):
        if value <= 0:
            raise ValidationError("La quantità deve essere maggiore di zero.")
