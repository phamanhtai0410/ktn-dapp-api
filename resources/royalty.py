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
        _user_address = str(py_.get(params, 'address')).lowercase()
        _withdraw_history_length = py_.get(params, "withdraw_history_length")
        res = RoyaltyHelper.get_all_collections_by_user(_user_address, _withdraw_history_length)
        return res