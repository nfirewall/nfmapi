from nfmapi.models import ServiceObject
from nfmapi.schemata import ServiceObjectSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db
from uuid import uuid4

path = 'service_objects'
endpoint = 'service_objects'


class ServiceObjectCollectionResource(BaseResource):
    def get(self):
        """List Service Objects
        ---
        description: List all service objects
        tags:
          - Service Objects
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: ServiceObjectSchema
        """
        certs = ServiceObject.query.all()
        schema = ServiceObjectSchema(many = True)
        return schema.dump(certs)

    def post(self):
        """Create service object
        ---
        description: Create a service object
        tags:
          - Service Objects
        requestBody:
          content:
            application/json:
              schema: ServiceObjectSchema
        responses:
          201:
            description: Created
            content:
              application/json:
                schema: ServiceObjectSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        messages = []
        json_data = request.get_json()
        try:
            data = ServiceObjectSchema().load(json_data)
        except ValidationError as err:
            for msg in err.messages:
                messages.append("{}: {}".format(msg, err.messages[msg]))
            return {"messages": messages}, 422
        

        service_object = ServiceObject()
        error = False
        for key in data:
            try:
                setattr(service_object, key, data[key])
            except ValueError as e:
                error = True
                messages.append(e.args[0])
        if error:
            return {"messages": messages}, 422
        db.session.add(service_object)
        db.session.commit()
        db.session.refresh(service_object)
        return ServiceObjectSchema().dump(service_object)