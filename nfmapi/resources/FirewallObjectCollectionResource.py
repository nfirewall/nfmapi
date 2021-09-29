from nfmapi.models import FirewallObject
from nfmapi.schemata import FirewallObjectSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db
from sqlalchemy.exc import IntegrityError

path = 'firewall_objects'
endpoint = 'firewall_objects'


class FirewallObjectCollectionResource(BaseResource):
    def get(self):
        """List firewall objects
        ---
        description: List all firewall objects
        tags:
          - Firewalls
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: FirewallObjectSchema
        """
        objects = FirewallObject.query.all()
        schema = FirewallObjectSchema(many = True)
        return schema.dump(objects)

    def post(self):
        """Create firewall object
        ---
        description: Create a firewall object
        tags:
          - Firewalls
        requestBody:
          content:
            application/json:
              schema: FirewallObjectSchema
        responses:
          201:
            description: Created
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
            data = FirewallObjectSchema().load(json_data)
        except ValidationError as err:
            return {"messages": err.messages}, 422
        
        object = FirewallObject()
        error = False
        messages = []
        for key in data:
            try:
                setattr(object, key, data[key])
            except ValueError as e:
                error = True
                messages.append(e.args[0])
        if error:
            return {"messages": messages}, 422
        try:
            db.session.add(object)
            db.session.commit()
            db.session.refresh(object)
        except IntegrityError as e:
            return {"messages": ["Invalid request: SQL integrity failed"]}, 422
        return FirewallObjectSchema().dump(object)