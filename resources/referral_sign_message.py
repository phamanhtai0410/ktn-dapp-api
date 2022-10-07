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


from helper import ReferralHelper
from schemas.referral_sign_message import ReferralSignMessageRequestParams, ReferralSignMessageResponse

class ReferralSignMessageResource(Resource):

    @security.http(
        response=ReferralSignMessageResponse(),
        params=ReferralSignMessageRequestParams()
    )
    def get(self, params):
        _address = py_.get(params, 'address')
        _code = py_.get(params, 'code')
        _referral = ReferralHelper.get_referral_sign_message(address=_address, ref_code=_code)
        return _referral

