from flask_restx import Namespace, fields
from app.models.stato import Stato

# Namespace per ordine_dettagli
ordine_dettaglio_ns = Namespace(
    "ordine_dettagli", description="Gestione dei dettagli ordine"
)
# Ottieni gli stati validi dalla classe Stato
stati_disponibili = Stato.get_valid_states()

# Modello per aggiornare lo stato
aggiorna_stato_model = ordine_dettaglio_ns.model(
    "AggiornaStato",
    {
        "nuovo_stato": fields.String(
            required=True,
            description="Nuovo stato del dettaglio",
            enum=stati_disponibili,  # Enum con gli stati disponibil
        )
    },
)

# Modello per i dettagli dell'ordine
ordine_dettaglio_output_model = ordine_dettaglio_ns.model(
    "OrdineDettaglio",
    {
        "id": fields.Integer(readOnly=True, description="ID del dettaglio ordine"),
        "id_ordine": fields.Integer(description="ID dell'ordine"),
        "id_prodotto": fields.Integer(description="ID del prodotto"),
        "id_utente": fields.Integer(description="ID dell'utente"),
        "quantita": fields.Integer(description="Quantità del prodotto"),
        "prezzo_unitario": fields.Float(description="Prezzo unitario del prodotto"),
        "totale_dettaglio": fields.Float(description="Totale per questo dettaglio"),
        "stato": fields.String(description="Stato del dettaglio ordine"),
    },
)

# Modello per l'ordine (includendo i dettagli dell'ordine)
ordine_output_model = ordine_dettaglio_ns.model(
    "Ordine",
    {
        "id": fields.Integer(description="ID dell'ordine"),
        "id_utente": fields.Integer(description="ID dell'utente"),
        "totale": fields.Float(description="Totale dell'ordine"),
        "dettagli": fields.List(
            fields.Nested(ordine_dettaglio_output_model),
            description="Lista dei dettagli ordine",
        ),
    },
)
