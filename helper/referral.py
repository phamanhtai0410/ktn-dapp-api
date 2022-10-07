import string
import random

from constants import Constants
from helper.wallet import WalletHelper
from lib.exception import BadRequest
from lib.utils import dt_utcnow
from models import LeaderBoardModel, ReferralLogModel, ReferralModel
from schemas.referral import ReferralResponseSchema
import pydash as py_

from eth_account.messages import defunct_hash_message
from web3 import Web3


web3 = Web3()

class ReferralHelper:

    @staticmethod
    def generate_referral_code(code_length):
        ref_code = ''
        while True:
            all_chars = list(string.digits + string.ascii_uppercase)
            random.shuffle(all_chars)
            ref_code = ''.join(all_chars[:code_length])
            check_ref_code = ReferralModel.find_one(
                filter={
                    'code': ref_code
                }
            )
            if not check_ref_code:
                return ref_code 
    
    @staticmethod
    def get_referral_code(address):
        if not address:
            raise BadRequest('address can not null')

        _address = address.lower()

        _referral = ReferralModel.find_one_with_cache({
            'address': _address
        }, query=None)

        if not _referral:
            raise BadRequest('referral not found')

        _user_leader_board = LeaderBoardModel.find_one({
            'address': _address,
            'event': Constants.TOP_REFERRAL_EVENT_NAME
        })

        return {
            **_referral,
            'total_user_linked': py_.get(_user_leader_board, 'total_user_linked', 0)
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
        _referral_log = ReferralLogModel.find({
            'address': _address
        })
        
        if _referral_log:
            raise BadRequest('user has been linked with another code')

        _referral = ReferralModel.find_one_with_cache({
            'code': ref_code
        }, query=None)

        if not _referral:
            raise BadRequest('referral code not found')
        
        _address_linked = py_.get(_referral, 'address')

        # user can not input user's own code
        if _address == _address_linked:
            raise BadRequest("user can not input user's own code")

        LeaderBoardModel.col.find_one_and_update({
            'address': _address_linked,
            'event': Constants.TOP_REFERRAL_EVENT_NAME
        }, {
            '$inc': {
                'total_user_linked': 1
            },
            '$set': {
                'updated_by': 'api',
                'updated_time': dt_utcnow()
            }
        }, upsert=True)

        ReferralModel.update_one({
            'address': _address
        }, {
            'address_linked': _address_linked,
            'code_linked': ref_code,
            'updated_by': 'api'
        })


        _referral_log = ReferralLogModel.insert_one({
            'address': _address,
            'address_linked': _address_linked,
            'code_linked': ref_code,
            'created_by': 'api'
        })

        return _referral_log