from nfmanagementapi.models import NatRule
from nfmanagementapi.schemata import NatRuleSchema, NatRulePatchSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db

path = 'nat_rules/<uuid>'
endpoint ='nat_rule_detail'

class NatRuleResource(BaseResource):
    def get(self, uuid):
        """Get Nat Rule
        ---
        description: Get a nat rule
        tags:
          - Nat Rules
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
                schema: NatRuleSchema
        """
        object = NatRule.query.filter_by(uuid=uuid).first_or_404()
        
        return NatRuleSchema().dump(object)
        
    def patch(self, uuid):
        """Update Nat Rule
        ---
        description: Update a nat rule
        tags:
          - Nat Rules
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        requestBody:
          content:
            application/json:
              schema: NatRulePatchSchema
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: NatRuleSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()

        try:
            data = NatRulePatchSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        object = NatRule.query.filter_by(uuid=uuid).first_or_404()
        
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
        return NatRuleSchema().dump(object)
        
    def delete(self, uuid):
        """Delete Nat Rule
        ---
        description: Delete a nat rule
        tags:
          - Nat Rules
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
        object = NatRule.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(object)
        db.session.commit()
        return {}, 204