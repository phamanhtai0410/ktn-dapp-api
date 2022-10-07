# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback

from eth_account.messages import defunct_hash_message
from hexbytes import HexBytes
from pydash import get
from web3 import Web3

from lib import dt_utcnow

web3 = Web3()


class WalletHelper:

    @staticmethod
    def get_address_of(signature, msg):
        _address = ''
        _msg_hash = defunct_hash_message(text=msg)

        _address = web3.eth.account.recoverHash(
            _msg_hash,
            signature=signature
        )

        return _address.lower()

    @staticmethod
    def _get_sign_msg(address, nonce):
        return f"I'm signing to KatanaInu using nonce {nonce} at address {address}"

    @staticmethod
    def _get_referral_sign_msg(address, nonce, ref_code):
        return f"I input referral code to KatanaInu with code {ref_code} and nonce {nonce} at address {address}"
        

    @classmethod
    def get_sign_msg(cls, address):
        _nonce = cls.get_nonce()
        return cls._get_sign_msg(address=address, nonce=_nonce), _nonce

    @staticmethod
    def get_nonce():
        return int(dt_utcnow().timestamp())

    @classmethod
    def get_referral_sign_msg(cls, address, ref_code):
        _nonce = cls.get_nonce()
        return cls._get_referral_sign_msg(address=address, nonce=_nonce, ref_code=ref_code), _nonce
        
