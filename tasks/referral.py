# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
# from helper.sync import sync_task
import random
import string
from constants import Constants
from lib.utils import dt_utcnow
from models import LeaderBoardModel, ReferralModel
from worker import worker
import pydash as py_


@worker.task(name='worker.generate_referral_code', rate_limit='1000/s')
def task_generate_referral_code(address):
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
    if not address or not isinstance(address, str):
        return 'DONE - address can not null'

    _address = address.lower()
    # NOTE: check for case if user input code of another user first, than log later
    _referral = ReferralModel.find_one({
        'address': _address,
        'code': {
            '$exists': True
        }
    })
    if _referral:
        return 'DONE - referral existed'
    
    _code = generate_referral_code(code_length=Constants.REFERRAL_CODE_LENGTH)
    ReferralModel.col.find_one_and_update({
        'address': _address
    },{
        'address': _address,
        'code': _code,
        'created_by': 'worker',
        'created_time': dt_utcnow()
    })
    return f"DONE - generate referral code for {_address} with {_code}"

@worker.task(name='worker.calculate_referral_rank', rate_limit='1000/s')
def task_calculate_referral_rank():
    _leader_board = LeaderBoardModel.col.find({
        'event': Constants.TOP_REFERRAL_EVENT_NAME
    }).sort('point', -1)
    _rank_count = 1
    for item in _leader_board:
        _rank = py_.get(item, 'rank', 0)
        if _rank != _rank_count:
            _id = py_.get(item, '_id')
            LeaderBoardModel.update_one({
                '_id': _id
            }, {
                'rank': _rank_count,
                'updated_by': 'worker'
            })
        _rank_count += 1
    return f"DONE - calculate referral rank"
