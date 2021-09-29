from flask import jsonify
from flask.views import MethodView
from ..schemata import StatusSchema
from ..models import NetworkObject

path = '/status'
endpoint = 'status'
exclude_from_doc = True

class StatusResource(MethodView):
    def get(self):
        """Get API Specification
        ---
        description: Get the specification of the API
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: StatusSchema

        """
        try:
            NetworkObject.query.all()
        except:
            return StatusSchema().dump({"status": "failed", "version": "0.1"}), 500
        return StatusSchema().dump({"status": "Ok", "version": "0.1"})