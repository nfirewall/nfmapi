from nfmapi.models import NetworkObject
from nfmapi.schemata import NetworkObjectSchema, NetworkObjectPatchSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db

path = 'network_objects/<uuid>'
endpoint ='network_object_detail'

class NetworkObjectResource(BaseResource):
    def get(self, uuid):
        """Get Network Object
        ---
        description: Get a specific network object
        tags:
          - Network Objects
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: NetworkObjectSchema
        """
        cert = NetworkObject.query.filter_by(uuid=uuid).first_or_404()
        
        return NetworkObjectSchema().dump(cert)
        
    def patch(self, uuid):
        """Update Network Object
        ---
        description: Update a network object
        tags:
          - Network Objects
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        requestBody:
          content:
            application/json:
              schema: NetworkObjectPatchSchema
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: NetworkObjectSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()

        try:
            data = NetworkObjectPatchSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        object = NetworkObject.query.filter_by(uuid=uuid).first_or_404()
        
        for key in data:
            setattr(object, key, data[key])

        db.session.commit()
        db.session.refresh(object)
        return NetworkObjectSchema().dump(object)
        
    def delete(self, uuid):
        """Delete Network Object
        ---
        description: Delete a network object
        tags:
          - Network Objects
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        responses:
          204:
            description: No Content
        """
        object = NetworkObject.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(object)
        db.session.commit()
        return {}, 204