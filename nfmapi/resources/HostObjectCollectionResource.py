from nfmapi.models import HostObject
from nfmapi.schemata import HostObjectSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db
from uuid import uuid4

path = 'host_objects'
endpoint = 'host_objects'


class HostObjectCollectionResource(BaseResource):
    def get(self):
        """List Host Objects
        ---
        description: List all host objects
        tags:
          - Host Objects
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: HostObjectSchema
        """
        objects = HostObject.query.all()
        schema = HostObjectSchema(many = True)
        return schema.dump(objects)

    def post(self):
        """Create host object
        ---
        description: Create a host object
        tags:
          - Host Objects
        requestBody:
          content:
            application/json:
              schema: HostObjectSchema
        responses:
          201:
            description: Created
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
            data = HostObjectSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        

        try:
            data["ipv4"]
        except KeyError:
            data["ipv4"] = None
        try:
            data["ipv6"]
        except KeyError:
            data["ipv6"] = None

        if data["ipv4"] is None and data["ipv6"] is None:
            return {"message": "an IPv4 or IPv6 address must be specified"}, 422
        

        object = HostObject()
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
        return HostObjectSchema().dump(object)