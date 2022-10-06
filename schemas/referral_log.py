# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields


class ReferralLogResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    address = fields.String(default='', missing='')
    address_linked = fields.String(default='', missing='')
    code_linked = fields.String(default='', missing='')