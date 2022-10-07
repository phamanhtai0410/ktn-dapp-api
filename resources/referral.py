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
from helper import ReferralHelper
from schemas.referral_log import ReferralLogResponseSchema

class ReferralResource(Resource):

    @security.http(
        response=ReferralResponseSchema(),
        params=ReferralRequestParams()
    )
    def get(self, params):
        _address = py_.get(params, 'address')
        _referral = ReferralHelper.get_referral_code(address=_address)
        return _referral

    @security.http(
        form_data=ReferralInputSchema(),
        response=ReferralLogResponseSchema()
    )
    def post(self, form_data):
        _code = py_.get(form_data, 'code')
        _address = py_.get(form_data, 'address')
        _nonce = py_.get(form_data, 'nonce')
        _signature = py_.get(form_data, 'signature')
        _referral = ReferralHelper.input_referral_code(
            address=_address, 
            ref_code=_code,
            signature=_signature,
            nonce=_nonce)
        return _referral
