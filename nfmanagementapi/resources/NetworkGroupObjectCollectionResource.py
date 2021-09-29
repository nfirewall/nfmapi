from nfmanagementapi.models import NetworkGroupObject
from nfmanagementapi.schemata import NetworkGroupObjectSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db
from uuid import uuid4

path = 'network_groups'
endpoint = 'network_groups'


class NetworkGroupObjectCollectionResource(BaseResource):
    def get(self):
        """List network groups
        ---
        description: List all network groups
        tags:
          - Network Groups
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: NetworkGroupObjectSchema
        """
        objects = NetworkGroupObject.query.all()
        schema = NetworkGroupObjectSchema(many = True)
        return schema.dump(objects)

    def post(self):
        """Create network group
        ---
        description: Create a network group
        tags:
          - Network Groups
        requestBody:
          content:
            application/json:
              schema: NetworkGroupObjectSchema
        responses:
          201:
            description: Created
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
            data = NetworkGroupObjectSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        

        object = NetworkGroupObject()
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
        db.session.add(object)
        db.session.commit()
        db.session.refresh(object)
        return NetworkGroupObjectSchema().dump(object)