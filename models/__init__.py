# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from config import Config
from lib import AsyncDaoModel, DaoModel
from connect import connect_db, redis_cluster, asyncio_mongo
from .point import PointDao
from .user import UserDao

__models__ = ['ReferralModel', 'ReferralLogModel', 'LeaderBoardModel', 'UserModel']

ReferralModel = DaoModel(connect_db.db.referral, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)

ReferralLogModel = DaoModel(connect_db.db.referral_log, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)

LeaderBoardModel = DaoModel(connect_db.db.leader_board, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)

UserModel = UserDao(connect_db.db.user, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)


PaymentModel  = DaoModel(connect_db.db.payment,redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT) 

EventModel = DaoModel(connect_db.db.events, redis=redis_cluster)

PointModel = PointDao(connect_db.db.points, redis=redis_cluster)
