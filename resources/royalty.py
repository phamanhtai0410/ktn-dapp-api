# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask import request
from flask_restful import Resource
import pydash as py_
from connect import security


from schemas.referral import ReferralInputSchema, ReferralRequestParams, ReferralResponseSchema
from helper import RoyaltyHelper
from schemas.royalty import RoyaltyNFTRequestParams

class Royalty(Resource):

    @security.http(
        params=RoyaltyNFTRequestParams()
    )
    def get(self, params):
        _user_address = py_.get(params, 'address')
        # return ""
        # print(t)
        res = RoyaltyHelper.get_all_collections_by_user(_user_address)
        print(res)
        return res