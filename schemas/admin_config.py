# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields

from constants import Constants


class WhiteListMintObj(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    start_time = fields.Integer(default=0, missing=0)
    end_time = fields.Integer(default=0, missing=0)

class AdminConfigResponse(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    whitelist_mint = fields.Nested(WhiteListMintObj, default={}, missing={})