from nfmapi.models import ServiceGroupObject
from nfmapi.schemata import ServiceGroupObjectSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db
from uuid import uuid4

path = 'service_groups'
endpoint = 'service_groups'


class ServiceGroupObjectCollectionResource(BaseResource):
    def get(self):
        """List service groups
        ---
        description: List all service groups
        tags:
          - Service Groups
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: ServiceGroupObjectSchema
        """
        objects = ServiceGroupObject.query.all()
        schema = ServiceGroupObjectSchema(many = True)
        return schema.dump(objects)

    def post(self):
        """Create service group
        ---
        description: Create a service group
        tags:
          - Service Groups
        requestBody:
          content:
            application/json:
              schema: ServiceGroupObjectSchema
        responses:
          201:
            description: Created
            content:
              application/json:
                schema: ServiceGroupObjectSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()
        try:
            data = ServiceGroupObjectSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        

        object = ServiceGroupObject()
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
        return ServiceGroupObjectSchema().dump(object)