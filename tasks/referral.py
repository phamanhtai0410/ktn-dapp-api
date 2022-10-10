# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
# from helper.sync import sync_task
from constants import Constants
from models import ReferralModel
from worker import worker
from helper.referral import ReferralHelper


@worker.task(name='worker.generate_referral_code', rate_limit='1000/s')
def task_generate_referral_code(address):
    if not address or not isinstance(address, str):
        return 'DONE - address can not null'

    _address = address.lower()
    _referral = ReferralModel.find_one({
        'address': _address
    })
    if _referral:
        return 'DONE - referral existed'
    
    _code = ReferralHelper.generate_referral_code(code_length=Constants.REFERRAL_CODE_LENGTH)
    ReferralModel.insert_one({
        'address': _address,
        'code': _code,
        'created_by': 'worker'
    })
    return f"DONE - generate referral code for {_address} with {_code}"
