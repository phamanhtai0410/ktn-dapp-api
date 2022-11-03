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
from helper.leader_board import LeaderBoardHelper

from schemas.leader_board import LeaderBoardRequestParams, LeaderBoardResponse


class LeaderBoardResource(Resource):

    @security.http(
        params=LeaderBoardRequestParams(),
        response=LeaderBoardResponse()
    )
    def get(self, params):
        _search = py_.get(params, 'search')
        _page = py_.get(params, 'page')
        _page_size = py_.get(params, 'page_size')
        _event = py_.get(params, 'event', Constants.TOP_REFERRAL_EVENT_NAME)
        _referral = LeaderBoardHelper.get_leader_board(event=_event, page=_page, page_size=_page_size, search=_search)
        return _referral
