# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.event import EventResource
from resources.exchange import ExchangeResource
from resources.health_check import HealthCheck
from resources.hello import HelloWorld
from resources.iapi import iapi_resources
from resources.referral import ReferralResource
from resources.leader_board import LeaderBoardResource
from resources.user import User, UserInfo
from resources.referral_sign_message import ReferralSignMessageResource
from resources.payment import Payment
from resources.setting import SettingResource
from resources.royalty import Royalty
from resources.alls import AllsItemResource, OneItemResource, UpcomingResource, ChainsSupportResource
from resources.admin_config import AdminConfigResource
from resources.category import CategoryResource
from resources.whitelist import WhitelistCheckingResource

api_resources = {
    '/hello': HelloWorld,
    '/common/health_check': HealthCheck,
    **{f'/iapi{k}': val for k, val in iapi_resources.items()},
    '/referral': ReferralResource,
    '/referral/validate': ReferralSignMessageResource,
    '/leader_board': LeaderBoardResource,
    '/user': User,
    '/event': EventResource,
    '/exchange': ExchangeResource,
    '/user_info': UserInfo, 
    '/payment': Payment,
    '/setting': SettingResource,
    '/royalty_info': Royalty,
    '/alls': AllsItemResource,
    '/nft/detail': OneItemResource,
    '/config': AdminConfigResource,
    '/category': CategoryResource,
    '/alls/upcoming': UpcomingResource,
    '/chain/support': ChainsSupportResource,
    '/whitelist/check': WhitelistCheckingResource
}
