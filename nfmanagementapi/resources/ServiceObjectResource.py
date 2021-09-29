from nfmanagementapi.models import ServiceObject
from nfmanagementapi.schemata import ServiceObjectSchema, ServiceObjectPatchSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db

path = 'service_objects/<uuid>'
endpoint ='service_object_detail'

class ServiceObjectResource(BaseResource):
    def get(self, uuid):
        """Get Service Object
        ---
        description: Get a service object
        tags:
          - Service Objects
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
                schema: ServiceObjectSchema
        """
        object = ServiceObject.query.filter_by(uuid=uuid).first_or_404()
        
        return ServiceObjectSchema().dump(object)
        
    def patch(self, uuid):
        """Update Service Object
        ---
        description: Update a service object
        tags:
          - Service Objects
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        requestBody:
          content:
            application/json:
              schema: ServiceObjectPatchSchema
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: ServiceObjectSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()

        try:
            data = ServiceObjectPatchSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        object = ServiceObject.query.filter_by(uuid=uuid).first_or_404()
        
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
        return ServiceObjectSchema().dump(object)
        
    def delete(self, uuid):
        """Delete Service Object
        ---
        description: Delete a service object
        tags:
          - Service Objects
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
        object = ServiceObject.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(object)
        db.session.commit()
        return {}, 204