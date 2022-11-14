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

    address = fields.String(default='', missing='')
    code = fields.String(default='', missing='')
    address_linked = fields.String(default='', missing='')
    code_linked = fields.String(default='', missing='')
    point = fields.Int(default=0, missing=0)
    total_earn = fields.Float(default=0, missing=0)
    address_referral_level_1 = fields.List(fields.String(), default=[], missing=[])
    address_referral_level_2 = fields.List(fields.String(), default=[], missing=[])

class ReferralInputSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    code = fields.String(required=True)
    address = fields.String(required=True)
    nonce = fields.Int(required=True)
    signature = fields.String(required=True)

class ReferralRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        
    address = fields.String(required=True)