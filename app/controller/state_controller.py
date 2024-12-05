from flask_restx import Namespace, Resource
from app.models.stato import Stato

stato_ns = Namespace("stati", description="Gestione degli stati")


@stato_ns.route("/")
class StatiResource(Resource):
    def get(self):
        """
        Restituisce la lista degli stati disponibili.
        """
        stati = Stato.query.all()
        return [
            {"id": stato.id, "descrizione": stato.descrizione} for stato in stati
        ], 200
