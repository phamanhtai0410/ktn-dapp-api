# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields


class SettingResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    referral_cookies = fields.Integer()
