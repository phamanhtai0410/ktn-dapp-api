# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from config import Config
from lib import AsyncDaoModel, DaoModel
from connect import connect_db, redis_cluster, asyncio_mongo
from .leader_board import LeaderBoardDao
from .point import PointDao
from .user import UserDao
from .referral_log import ReferralLogDao
from .royalty import RoyaltyDao, RoyaltyWithdrawHistoryDao, AdminUserDao, CollectionBoxDao, CollectionNFTDao, NFTDao, SignatureLogsDao

__models__ = ['ReferralModel', 'ReferralLogModel', 'LeaderBoardModel', 'UserModel', 
        'RoyaltyModel', 'RoyaltyWithdrawHistoryModel', 'AdminUserModel', 'CollectionBoxModel', 'CollectionNFTModel',
        'NFTModel', 'SignatureLogsModel'
]

ReferralModel = DaoModel(connect_db.db.referral, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)

ReferralLogModel = ReferralLogDao(connect_db.db.referral_log, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)

LeaderBoardModel = LeaderBoardDao(connect_db.db.leader_board, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)

UserModel = UserDao(connect_db.db.user, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)


PaymentModel  = DaoModel(connect_db.db.payment,redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT) 

EventModel = DaoModel(connect_db.db.events, redis=redis_cluster)

PointModel = PointDao(connect_db.db.points, redis=redis_cluster)

SettingModel = DaoModel(connect_db.db.setting, redis=redis_cluster)

RoyaltyModel = DaoModel(connect_db.db.royalty, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)

RoyaltyWithdrawHistoryModel = DaoModel(connect_db.db.royalty_withdraw_history, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)

AdminUserModel = DaoModel(connect_db.db.admin_users, redis=redis_cluster, broker=Config.BROKER_URL,
                project=Config.PROJECT)

CollectionBoxModel = DaoModel(connect_db.db.boxes, redis=redis_cluster, broker=Config.BROKER_URL,
                project=Config.PROJECT)

CollectionNFTModel = DaoModel(connect_db.db.collection, redis=redis_cluster, broker=Config.BROKER_URL,
                project=Config.PROJECT)

NFTModel = DaoModel(connect_db.db.nfts, redis=redis_cluster)

SignatureLogsModel = DaoModel(connect_db.db.signature_logs, redis=redis_cluster)

AdminDefaultConfigsModel = DaoModel(connect_db.db.admin_default_configs, redis=redis_cluster)

NftWhitelistModel = DaoModel(connect_db.db.nft_whitelist, redis=redis_cluster)

CategoryModel = DaoModel(connect_db.db.collection_category, redis=redis_cluster)

PreLaunchNftWhitelist = DaoModel(connect_db.db.pre_launch_nft_whitelist, redis=redis_cluster)

EmailSubscribeModel = DaoModel(connect_db.db.email_subscribe, redis=redis_cluster)
