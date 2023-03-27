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
from helper.admin_config import AdminConfigHelper
from helper.leader_board import LeaderBoardHelper

from schemas.admin_config import AdminConfigResponse


class AdminConfigResource(Resource):

    @security.http(
        response=AdminConfigResponse()
    )
    def get(self):
        _result = AdminConfigHelper.get()
        return _result
