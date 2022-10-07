# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask import request
from flask_restful import Resource

from schemas.hello import HelloSchema
from connect import security
from tasks.referral import task_generate_referral_code


class HelloWorld(Resource):

    @security.http(
        # login_required=True
    )
    def get(self):
        task_generate_referral_code.delay(address=request.args.get('address'))
        return {'hello': 'world'}

    @security.http(
        form_data=HelloSchema(),  # form_data
        params=HelloSchema(),  # params
        login_required=True  # user
    )
    def post(self, form_data, params, user):
        
        return {}
