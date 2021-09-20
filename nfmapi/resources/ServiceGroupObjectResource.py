from nfmapi.models import ServiceGroupObject
from nfmapi.schemata import ServiceGroupObjectSchema, ServiceGroupObjectPatchSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db

path = 'service_groups/<uuid>'
endpoint ='service_group_detail'

class ServiceGroupObjectResource(BaseResource):
    def get(self, uuid):
        """Get service group
        ---
        description: Get a service group
        tags:
          - Service Groups
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
                schema: ServiceGroupObjectSchema
        """
        object = ServiceGroupObject.query.filter_by(uuid=uuid).first_or_404()
        
        return ServiceGroupObjectSchema().dump(object)
        
    def patch(self, uuid):
        """Update service group
        ---
        description: Update a service group
        tags:
          - Service Groups
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        requestBody:
          content:
            application/json:
              schema: ServiceGroupObjectPatchSchema
        responses:
          200:
            description: OK
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
            data = ServiceGroupObjectPatchSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        object = ServiceGroupObject.query.filter_by(uuid=uuid).first_or_404()
        
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
        return ServiceGroupObjectSchema().dump(object)
        
    def delete(self, uuid):
        """Delete service group
        ---
        description: Delete a service group
        tags:
          - Service Groups
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
        object = ServiceGroupObject.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(object)
        db.session.commit()
        return {}, 204