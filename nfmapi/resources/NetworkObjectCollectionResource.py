from nfmapi.models import NetworkObject
from nfmapi.schemata import NetworkObjectSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db
from uuid import uuid4

path = 'network_objects'
endpoint = 'network_objects'


class NetworkObjectCollectionResource(BaseResource):
    def get(self):
        """List Network Objects
        ---
        description: List all network objects
        tags:
          - Network Objects
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: NetworkObjectSchema
        """
        certs = NetworkObject.query.all()
        schema = NetworkObjectSchema(many = True)
        return schema.dump(certs)

    def post(self):
        """Create network object
        ---
        description: Create a network object
        tags:
          - Network Objects
        requestBody:
          content:
            application/json:
              schema: NetworkObjectSchema
        responses:
          201:
            description: Created
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
            data = NetworkObjectSchema().load(json_data)
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
        

        host_object = NetworkObject()
        error = False
        messages = []
        for key in data:
            try:
                setattr(host_object, key, data[key])
            except ValueError as e:
                error = True
                messages.append(e.args[0])
        if error:
            return {"messages": messages}, 422
        db.session.add(host_object)
        db.session.commit()
        db.session.refresh(host_object)
        return NetworkObjectSchema().dump(host_object)