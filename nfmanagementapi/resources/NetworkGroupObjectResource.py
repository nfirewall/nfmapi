from nfmanagementapi.models import NetworkGroupObject
from nfmanagementapi.schemata import NetworkGroupObjectSchema, NetworkGroupObjectPatchSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db

path = 'network_groups/<uuid>'
endpoint ='network_group_detail'

class NetworkGroupObjectResource(BaseResource):
    def get(self, uuid):
        """Get network group
        ---
        description: Get a network group
        tags:
          - Network Groups
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
                schema: NetworkGroupObjectSchema
        """
        object = NetworkGroupObject.query.filter_by(uuid=uuid).first_or_404()
        
        return NetworkGroupObjectSchema().dump(object)
        
    def patch(self, uuid):
        """Update network group
        ---
        description: Update a network group
        tags:
          - Network Groups
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        requestBody:
          content:
            application/json:
              schema: NetworkGroupObjectPatchSchema
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: NetworkGroupObjectSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()

        try:
            data = NetworkGroupObjectPatchSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        object = NetworkGroupObject.query.filter_by(uuid=uuid).first_or_404()
        
        messages = []
        error = False

        for key in data:
            try:
                setattr(object, key, data[key])
            except ValueError as e:
                error = True
                messages.append(e.args[0])
        if error:
            return {"messages": messages}, 422

        db.session.commit()
        db.session.refresh(object)
        return NetworkGroupObjectSchema().dump(object)
        
    def delete(self, uuid):
        """Delete network group
        ---
        description: Delete a network group
        tags:
          - Network Groups
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
        object = NetworkGroupObject.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(object)
        db.session.commit()
        return {}, 204