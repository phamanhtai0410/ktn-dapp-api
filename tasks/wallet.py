# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import requests
import sentry_sdk
from pydash import get

from config import Config
from helper.sign import SignHelper
from helper.socket import SocketEmitter
from models import PointModel
from worker import worker


@worker.task(name='worker.task_wallet_exchange', rate_limit='1000/s')
def task_wallet_exchange(address, amount, signature, event,sign_msg):
    _user = PointModel.find_one({
        'address': address.lower(),
        'event': event
    })

    if get(_user, 'total_points') < amount:
        SocketEmitter.emit(
            room_id=address,
            event='EXCHANGE_FAIL',
            value={
                'status': 'FAIL',
                'msg': 'Account not enough point.'
            }
        )
        return "Fail: Account not enough point"
    _res = requests.post(f'{Config.WALLET_IAPI}/exchange', json={
        'address': address,
        'amount': amount,
        'signature': {
            'sign': signature,
            'msg': sign_msg
        },
        'event': event
    })
    if _res.status_code != 200:
        sentry_sdk.capture_message(f"Fail: send transfer error: {_res.text}")
    return f"Done init transfer for {address}"
