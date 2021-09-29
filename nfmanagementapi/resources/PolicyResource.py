from nfmanagementapi.models import Policy
from nfmanagementapi.schemata import PolicySchema, PolicyPatchSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db

path = 'policies/<uuid>'
endpoint ='policy_detail'

class PolicyResource(BaseResource):
    def get(self, uuid):
        """Get policy
        ---
        description: Get a policy
        tags:
          - Policies
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
                schema: PolicySchema
        """
        object = Policy.query.filter_by(uuid=uuid).first_or_404()
        
        return PolicySchema().dump(object)
        
    def patch(self, uuid):
        """Update policy
        ---
        description: Update a policy
        tags:
          - Policies
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        requestBody:
          content:
            application/json:
              schema: PolicyPatchSchema
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: PolicySchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()

        try:
            data = PolicyPatchSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        object = Policy.query.filter_by(uuid=uuid).first_or_404()
        
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
        return PolicySchema().dump(object)
        
    def delete(self, uuid):
        """Delete policy
        ---
        description: Delete a policy
        tags:
          - Policies
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
        object = Policy.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(object)
        db.session.commit()
        return {}, 204