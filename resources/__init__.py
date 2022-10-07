# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.health_check import HealthCheck
from resources.hello import HelloWorld
from resources.iapi import iapi_resources
from resources.referral import ReferralResource
from resources.leader_board import LeaderBoardResource
from resources.user import User

api_resources = {
    '/hello': HelloWorld,
    '/common/health_check': HealthCheck,
    **{f'/iapi{k}': val for k, val in iapi_resources.items()},
    '/referral': ReferralResource,
    '/leader_board': LeaderBoardResource,
    '/user': User
}
