# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import requests
from flask import request
from email import message
from flask_restful import Resource
from pydash import get
import pydash as py_
from connect import security


from schemas.payment import PaymentRequestParams, PaymentListResponseParams
from helper import PaymentHelper

class Payment(Resource):
    @security.http(
        params=PaymentRequestParams(),
        response=PaymentListResponseParams()
    )
    def get(self, params):
        _chain_id = py_.get(params, 'chain_id')
        res = PaymentHelper.get_payment_method(_chain_id)
        return res