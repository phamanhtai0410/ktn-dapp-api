# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
import pydash as py_
from connect import security


from schemas.hello import HelloSchema
from schemas.referral import ReferralInputSchema, ReferralResponseSchema
from helper import ReferralHelper
from schemas.referral_log import ReferralLogResponseSchema

class ReferralResource(Resource):

    @security.http(
        login_required=True,
        response=ReferralResponseSchema()
    )
    def get(self, user):
        _public_address = py_.get(user, 'address')
        _referral = ReferralHelper.get_referral_code(public_address=_public_address)
        return _referral

    @security.http(
        login_required=True,
        form_data=ReferralInputSchema(),
        response=ReferralLogResponseSchema()
    )
    def post(self, form_data, user):
        _code = py_.get(form_data, 'code', '')
        _public_address = py_.get(user, 'address')
        _referral = ReferralHelper.input_referral_code(public_address=_public_address, ref_code=_code)
        return _referral
