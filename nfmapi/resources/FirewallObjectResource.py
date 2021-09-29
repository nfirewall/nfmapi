from nfmapi.models import FirewallObject
from nfmapi.schemata import FirewallObjectSchema, FirewallObjectPatchSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db

path = 'firewall_objects/<uuid>'
endpoint ='firewall_detail'

class FirewallObjectResource(BaseResource):
    def get(self, uuid):
        """Get firewall object
        ---
        description: Get a firewall object
        tags:
          - Firewalls
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
                schema: FirewallObjectSchema
        """
        object = FirewallObject.query.filter_by(uuid=uuid).first_or_404()
        
        return FirewallObjectSchema().dump(object)
        
    def patch(self, uuid):
        """Update firewall object
        ---
        description: Update a firewall object
        tags:
          - Firewalls
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        requestBody:
          content:
            application/json:
              schema: FirewallObjectPatchSchema
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: FirewallObjectSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()

        try:
            data = FirewallObjectPatchSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        object = FirewallObject.query.filter_by(uuid=uuid).first_or_404()
        
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
        return FirewallObjectSchema().dump(object)
        
    def delete(self, uuid):
        """Delete firewall object
        ---
        description: Delete a firewall object
        tags:
          - Firewalls
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
        object = FirewallObject.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(object)
        db.session.commit()
        return {}, 204