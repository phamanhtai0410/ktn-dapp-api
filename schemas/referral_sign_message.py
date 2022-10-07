# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields


class ReferralSignMessageRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        
    address = fields.String(required=True)
    code = fields.String(required=True)

class ReferralSignMessageResponse(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    nonce = fields.Int()
    msg = fields.String()
    code = fields.String()
