# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields

from lib import NotBlank


class MsgQuerySchema(Schema):
    class Meta:
        unknown = EXCLUDE

    amount = fields.Float(required=True)


class ExchangeForm(Schema):
    class Meta:
        unknown = EXCLUDE

    amount = fields.Float(required=True)
    signature = fields.Str(required=True, validate=NotBlank())
    nonce = fields.Float(required=True)
    address = fields.Str(required=True)
