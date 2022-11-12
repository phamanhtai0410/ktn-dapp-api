# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
import pydash as py_
from connect import security
from constants import Constants
from helper.setting import SettingHelper
from schemas.setting import SettingResponseSchema



class SettingResource(Resource):

    @security.http(
        response=SettingResponseSchema()
    )
    def get(self):
        _referral = SettingHelper.get_setting()
        return _referral
