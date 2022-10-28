
from distutils.log import error
from lib.exception import BadRequest
from exception import InvalidNonce, InvalidSignature
from eth_account.messages import defunct_hash_message
from lib.utils import util_web3, dt_utcnow
from email import message
from operator import truediv
from models import UserModel
from tasks import referral
from .wallet import WalletHelper



class UserHelper:
    
    @staticmethod
    def validate_nonce(_nonce):
        _dt = dt_utcnow().timestamp() - _nonce
        if 360 >= _dt >= 0:
            return True

        return False

    
    @staticmethod
    def get_sign_message(address):
        if not address:
            raise BadRequest('address can not null')
        _address =  address.lower()
        _message,_nonce = WalletHelper.get_sign_msg(_address)
        return {"message":_message,
                "address": _address,
                "nonce":_nonce}
    
    @classmethod
    def verify_signature(cls, address,nonce,signature):
   
        if not cls.validate_nonce(nonce): 
            raise InvalidNonce('nonce invalid')
        _address = address.lower()
        _message = WalletHelper._get_sign_msg(_address, nonce)
        _signer = WalletHelper.get_address_of(signature,_message)
        if _address == _signer:
            _user = UserModel.find_one(
                filter={
                    'address': _address
                }, cache=True)
            if not _user:
                referral.task_generate_referral_code.delay(address = _address) 
                UserModel.insert_one({
                    'address': _address,
                    'created_by': 'thanh'
                }, worker=True)
            
            return {"result":"Valid!",
                    "address": _address}
        raise InvalidSignature('signature invalid')
    
    def get_user_info(address):
        _address = address.lower()
        _user = UserModel.find_one(
            filter={
                'address': _address
            }, cache=True)
        if not _user:
            raise BadRequest('address not found', errors=[{
                'address': 'not found.'
            }])
        return _user
