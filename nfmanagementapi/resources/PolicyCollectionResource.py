from nfmanagementapi.models import Policy
from nfmanagementapi.schemata import PolicySchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db
from uuid import uuid4

path = 'policies'
endpoint = 'policies'


class PolicyCollectionResource(BaseResource):
    def get(self):
        """List policies
        ---
        description: List all policies
        tags:
          - Policies
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: PolicySchema
        """
        objects = Policy.query.all()
        schema = PolicySchema(many = True)
        return schema.dump(objects)

    def post(self):
        """Create policy
        ---
        description: Create a policy
        tags:
          - Policies
        requestBody:
          content:
            application/json:
              schema: PolicySchema
        responses:
          201:
            description: Created
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
            data = PolicySchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        
        object = Policy()
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
        return PolicySchema().dump(object)