from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt
from app.swagger import api
from flask.json.provider import DefaultJSONProvider
from datetime import datetime
from app.models.stato import Stato


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Converte il datetime in stringa ISO 8601
        return super().default(obj)


def create_app():
    app = Flask(__name__)
    # Configura CORS per permettere richieste dal front-end
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, 
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"])
         
    app.config.from_object("config.Config")

    # Configura il provider JSON personalizzato
    app.json = CustomJSONProvider(app)

    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()
        Stato.seed()
    return app
