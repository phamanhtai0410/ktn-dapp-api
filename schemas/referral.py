# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields


class ReferralResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    public_address = fields.String(default='', missing='')
    code = fields.String(default='', missing='')
    total_user_linked = fields.Int(default=0, missing=0)

class ReferralInputSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    code = fields.String(required=True)