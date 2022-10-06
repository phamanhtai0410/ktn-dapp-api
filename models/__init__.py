# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from config import Config
from lib import AsyncDaoModel, DaoModel
from connect import connect_db, redis_cluster, asyncio_mongo

__models__ = []

ReferralModel = DaoModel(connect_db.db.referral, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)

ReferralLogModel = DaoModel(connect_db.db.referral_log, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)

LeaderBoardModel = DaoModel(connect_db.db.leader_board, redis=redis_cluster, broker=Config.BROKER_URL,
                          project=Config.PROJECT)