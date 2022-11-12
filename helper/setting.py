import string
import random

from pydash import get

from constants import Constants
from exceptions.referral import InvalidReferralCodeEx, InvalidUserHasInputCode, InvalidUserInputOwnCode
from helper.wallet import WalletHelper
from lib.exception import BadRequest
from lib.utils import dt_utcnow
from models import LeaderBoardModel, ReferralLogModel, ReferralModel, PointModel, SettingModel
import pydash as py_

from web3 import Web3

web3 = Web3()

class SettingHelper:
    
    @staticmethod
    def get_setting():
        _setting = SettingModel.find_one({
            "key": "setting"
        }, cache=True)
        return _setting

    