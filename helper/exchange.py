# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import sentry_sdk
from pydash import get

from connect import dlm
from enums.status import Status
from exception import InvalidSignature, ELockAddress
from helper.sign import SignHelper
from helper.socket import SocketEmitter
from lib import dt_utcnow, BadRequest
from lib.logger import debug
from models import UserModel
from tasks import task_wallet_exchange


class ExchangeHelper:
    @staticmethod
    def get_msg(amount, timestamp):
        return f"I exchange {amount} points from Katana to {amount} USDT at {timestamp} seconds timestamp."

    @staticmethod
    def lock_address(address):
        try:
            _lock = dlm.lock(f'ktn:redlock:exchange:{address}', 60 * 1000)  # 1 minute
            if _lock:
                return True

        except:
            sentry_sdk.capture_exception()
        return False

    @classmethod
    def exchange_point(cls, address, amount, signature, timestamp):
        debug(timestamp < dt_utcnow().timestamp() - 60)
        if timestamp < dt_utcnow().timestamp() - 60*6000:  # 60s
            raise BadRequest("Invalid nonce.", errors=[{
                'nonce': 'Invalid.'
            }])
        _user = UserModel.find_one({
            'address': address.lower()
        })

        _sign_msg = cls.get_msg(amount, timestamp)

        _sign_address = SignHelper.get_address_of_signature(
            signature=signature,
            msg=_sign_msg
        )
        if _sign_address.lower() != address:
            raise InvalidSignature
        if get(_user, 'total_points', 0) < amount:
            raise BadRequest("Account not enough point.")
        if not cls.lock_address(address):
            raise ELockAddress()

        task_wallet_exchange.delay(
            address=address, amount=amount, signature=signature, sign_msg=_sign_msg
        )
        return True

    @classmethod
    def on_callback(cls, data):
        SocketEmitter.emit(
            room_id=get(data, 'address'),
            event='EXCHANGE',
            value=get(data, 'result')
        )
        return {}
