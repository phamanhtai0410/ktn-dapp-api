# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = False
    PROJECT = "dapp-api"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    # Setup db
    MONGO_URI = os.getenv('MONGO_URI')
    # Authentication
    AUTH_ADDRESS = os.getenv('AUTH_ADDRESS', '')

    CELERY_IMPORTS = ['tasks']
    ENABLE_UTC = True

    # Config celery worker

    BROKER_URL = os.getenv('BROKER_URL')
    CELERY_QUEUES = os.getenv('CELERY_QUEUES')

    CELERY_ROUTES = {
        'worker.task_hello': {'queue': 'hello-queue'},
        'worker.generate_referral_code': {'queue': 'ktn-dapp-queue'},
        'worker.calculate_referral_rank': {'queue': 'ktn-dapp-queue'},
        'worker.task_wallet_exchange': {'queue': 'ktn-dapp-exchange-queue'}
    }
    PUBLIC_PATH = os.getenv('PUBLIC_PATH')
    REDIS_CLUSTER = json.loads(os.getenv('REDIS_CLUSTER'))
    WALLET_IAPI = os.getenv('WALLET_IAPI')
    REDLOCK_REDIS = json.loads(os.getenv('REDLOCK_REDIS', '[]'))

    # BASE TOKEN ADDRESS
    TOKEN_USDT = os.getenv("TOKEN_USDT")
    TOKEN_WBNB = os.getenv("TOKEN_WBNB")
