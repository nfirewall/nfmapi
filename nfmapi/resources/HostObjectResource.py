from nfmapi.models import HostObject
from nfmapi.schemata import HostObjectSchema, HostObjectPatchSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db

path = 'host_objects/<uuid>'
endpoint ='host_object_detail'

class HostObjectResource(BaseResource):
    def get(self, uuid):
        """Get Host Object
        ---
        description: Get a specific host object
        tags:
          - Host Objects
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
                schema: HostObjectSchema
        """
        cert = HostObject.query.filter_by(uuid=uuid).first_or_404()
        
        return HostObjectSchema().dump(cert)
        
    def patch(self, uuid):
        """Update Host Object
        ---
        description: Update a host object
        tags:
          - Host Objects
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        requestBody:
          content:
            application/json:
              schema: HostObjectPatchSchema
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: HostObjectSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()

        try:
            data = HostObjectPatchSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        object = HostObject.query.filter_by(uuid=uuid).first_or_404()
        
        for key in data:
            setattr(object, key, data[key])

        db.session.commit()
        db.session.refresh(object)
        return HostObjectSchema().dump(object)
        
    def delete(self, uuid):
        """Delete Host Object
        ---
        description: Delete a host object
        tags:
          - Host Objects
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
        object = HostObject.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(object)
        db.session.commit()
        return {}, 204