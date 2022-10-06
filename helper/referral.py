import string
import random

from constants import Constants
from lib.exception import BadRequest
from lib.utils import dt_utcnow
from models import LeaderBoardModel, ReferralLogModel, ReferralModel
from schemas.referral import ReferralResponseSchema
import pydash as py_

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
    def get_referral_code(public_address):
        if not public_address:
            raise BadRequest('public_address can not null')
        
        _referral = ReferralModel.find_one({
            'public_address': public_address
        })

        _user_leader_board = LeaderBoardModel.find_one({
            'public_address': public_address,
            'event': Constants.TOP_REFERRAL_EVENT_NAME
        })

        if _referral:
            return {
                **_referral,
                'total_user_linked': py_.get(_user_leader_board, 'total_user_linked', 0)
            }

        # TODO: check rules generate ref code if needed later

        _referral = ReferralModel.insert_one({
            'public_address': public_address,
            'code': ReferralHelper.generate_referral_code(code_length=Constants.REFERRAL_CODE_LENGTH),
            'created_by': 'api'
        })

        return {
            **_referral,
            'total_user_linked': 0
        }

    @staticmethod
    def input_referral_code(public_address, ref_code):
        if not public_address:
            raise BadRequest('public_address can not null')

        # check if user had been linked code
        _referral_log = ReferralLogModel.find({
            'public_address': public_address
        })
        
        if _referral_log:
            raise BadRequest('user has been linked with another code')

        _referral = ReferralModel.find_one({
            'code': ref_code
        })

        if not _referral:
            raise BadRequest('referral code not found')
        
        _public_address_linked = py_.get(_referral, 'public_address')

        # user can not input user's own code
        if public_address == _public_address_linked:
            raise BadRequest("user can not input user's own code")

        LeaderBoardModel.col.find_one_and_update({
            'public_address': _public_address_linked,
            'event': Constants.TOP_REFERRAL_EVENT_NAME,
            'updated_by': 'api',
            'updated_time': dt_utcnow()
        }, {
            '$inc': {
                'total_user_linked': 1
            }
        }, upsert=True)


        _referral_log = ReferralLogModel.insert_one({
            'public_address': public_address,
            'public_address_linked': _public_address_linked,
            'code_linked': ref_code,
            'created_by': 'api'
        })

        return _referral_log