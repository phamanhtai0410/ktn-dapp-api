import string
import random

from pydash import get

from constants import Constants
from exceptions.referral import InvalidReferralCodeEx, InvalidUserHasInputCode, InvalidUserInputOwnCode
from helper.wallet import WalletHelper
from lib.exception import BadRequest
from lib.utils import dt_utcnow
from models import LeaderBoardModel, ReferralLogModel, ReferralModel, PointModel
import pydash as py_

from web3 import Web3

from tasks import task_calculate_referral_rank

web3 = Web3()

class ReferralHelper:
    
    @staticmethod
    def get_referral_code(address):
        if not address:
            raise BadRequest('address can not null')

        _address = address.lower()

        _referral = ReferralModel.find_one({
            'address': _address
        }, cache=True)

        if not _referral:
            raise InvalidReferralCodeEx

        _user_leader_board = LeaderBoardModel.find_one({
            'address': _address,
            'event': Constants.TOP_REFERRAL_EVENT_NAME
        })

        return {
            **_referral,
            'point': py_.get(_user_leader_board, 'point', 0),
            'total_earn': get(PointModel.find_one({
                    'event': 'top_referral',
                    'address': _address
                }), 'total_points', 0)
        }

    @staticmethod
    def get_referral_sign_message(address, ref_code):
        _address = address.lower()
        _msg, _nonce = WalletHelper.get_referral_sign_msg(address=_address, ref_code=ref_code)
        return {
            'code': ref_code,
            'msg': _msg,
            'nonce': _nonce
        }

    @staticmethod
    def input_referral_code(address, signature, ref_code, nonce):
        _now = dt_utcnow().timestamp()
        if _now - nonce > Constants.EXPIRE_REFERRAL_NONCE:
            raise BadRequest(msg="Invalid", errors=[{
                'nonce': "Invalid"
            }])
        _sign_msg = WalletHelper._get_referral_sign_msg(address=address.lower(), ref_code=ref_code, nonce=nonce)
        _address = WalletHelper.get_address_of(signature=signature, msg=_sign_msg)

        if not _address or address.lower() != _address:
            raise BadRequest(msg="Invalid", errors=[{
                'signature': 'Invalid'
            }])

        # check if user had been linked code
        _referral_log = ReferralLogModel.find_one({
            'address': _address
        }, cache=True)
        
        if _referral_log:
            raise InvalidUserHasInputCode

        _referral = ReferralModel.find_one({
            'code': ref_code
        }, cache=True)

        if not _referral:
            raise InvalidReferralCodeEx
        
        _address_linked = py_.get(_referral, 'address')

        # user can not input user's own code
        if _address == _address_linked:
            raise InvalidUserInputOwnCode

        LeaderBoardModel.col.find_one_and_update({
            'address': _address_linked,
            'event': Constants.TOP_REFERRAL_EVENT_NAME
        }, {
            '$inc': {
                'point': 1
            },
            '$set': {
                'updated_by': 'api',
                'updated_time': dt_utcnow()
            }
        }, upsert=True)

        # set level 1 affiliate
        ReferralModel.col.find_one_and_update({
            'address': _address
        }, {
            '$set': {
                'address': _address,
                'address_linked': _address_linked,
                'code_linked': ref_code,
                'updated_by': 'api',
                'updated_time': dt_utcnow(),
        }}, upsert=True)

        # push this address to child of address_linked
        ReferralModel.col.find_one_and_update({
            'address': _address_linked
        }, {
            '$push': {
                'address_referral': address 
            }
        })

        _referral_log = ReferralLogModel.insert_one({
            'address': _address,
            'address_linked': _address_linked,
            'code_linked': ref_code,
            'created_by': 'api'
        }, worker=True)

        task_calculate_referral_rank.delay()

        return _referral_log