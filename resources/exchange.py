# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from helper.exchange import ExchangeHelper
from lib import dt_utcnow
from schemas.exchange import MsgQuerySchema, ExchangeForm


class ExchangeResource(Resource):

    @security.http(
        params=MsgQuerySchema()
    )
    def get(self, params):
        _timestamp = dt_utcnow().timestamp()

        _msg = ExchangeHelper.get_msg(
            amount=get(params, 'amount'),
            timestamp=_timestamp
        )

        return {
            'msg': _msg,
            'nonce': _timestamp
        }

    @security.http(
        form_data=ExchangeForm()
    )
    def post(self, form_data):
        ExchangeHelper.exchange_point(
            address=get(form_data, 'address').lower(),
            amount=get(form_data, 'amount'),
            signature=get(form_data, 'signature'),
            timestamp=get(form_data, 'nonce')
        )
        return {
            'status': 'PENDING'
        }
