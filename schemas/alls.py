# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields



class Item(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    nft_id = fields.Integer()
    name = fields.String()
    price = fields.Float()
    image = fields.String()
    rarity = fields.String()
    total_supply = fields.Int()
    address = fields.String()
    chain = fields.String()
    chain_id = fields.Integer()
    dapp_creator_address = fields.String(allow_none=True)
    pay_token_address = fields.String(allow_none=True)
    total_minted = fields.Integer(default=0)


class AllsItemResponse(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    items = fields.List(fields.Nested(Item), default=[], missing=[])
    num_of_page = fields.Int(default=0, missing=0)
    page_size = fields.Int(default=0, missing=0)
    page = fields.Int(default=0, missing=0)


class AllsItemRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    chain = fields.String(allow_none=True)
    category = fields.String(allow_none=True)
    page = fields.Int(default=1, missing=1)
    page_size = fields.Int(default=10, missing=10)
    

class OneItemRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    
    address = fields.String(required=True)
    chain = fields.String(allow_none=True, default='BSC')
    category = fields.String(allow_none=True, default='Character')
    nft_id = fields.Integer(allow_none=True)


class OneItemResponse(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    items = fields.List(fields.Nested(Item), default=[], missing=[])