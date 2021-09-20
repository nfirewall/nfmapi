from nfmapi.models import FilterRule
from nfmapi.schemata import FilterRuleSchema, FilterRulePatchSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db

path = 'filter_rules/<uuid>'
endpoint ='filter_rule_detail'

class FilterRuleResource(BaseResource):
    def get(self, uuid):
        """Get Filter Rule
        ---
        description: Get a specific filter rule
        tags:
          - Filter Rules
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
                schema: FilterRuleSchema
        """
        object = FilterRule.query.filter_by(uuid=uuid).first_or_404()
        
        return FilterRuleSchema().dump(object)
        
    def patch(self, uuid):
        """Update Filter Rule
        ---
        description: Update a filter rule
        tags:
          - Filter Rules
        parameters:
          - name: uuid
            in: path
            description: Object UUID
            schema:
              type: string
        requestBody:
          content:
            application/json:
              schema: FilterRulePatchSchema
        responses:
          200:
            description: OK
            content:
              application/json:
                schema: FilterRuleSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()

        try:
            data = FilterRulePatchSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        object = FilterRule.query.filter_by(uuid=uuid).first_or_404()
        
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
        return FilterRuleSchema().dump(object)
        
    def delete(self, uuid):
        """Delete Filter Rule
        ---
        description: Delete a filter rule
        tags:
          - Filter Rules
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
        object = FilterRule.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(object)
        db.session.commit()
        return {}, 204