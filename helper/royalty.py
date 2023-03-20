
from distutils.log import error
from lib.exception import BadRequest
from exception import InvalidNonce, InvalidSignature
from eth_account.messages import defunct_hash_message
from lib.utils import util_web3, dt_utcnow
from email import message
from operator import truediv
# from models import RoyaltyModel, RoyaltyWithdrawHistoryModel, AdminUserModel, CollectionBoxModel, CollectionNFTModel, SignatureLogsModel
from pydash import get
from constants import Constants

from pymongo import MongoClient
from lib.utils import dt_utcnow
from config import Config
from bson.json_util import dumps
import json
from connect import redis_cluster
from config import Config


db = MongoClient(Config.MONGO_URI, connect=False)['katana-dapp']

RoyaltyWithdrawHistoryModel = db['royalty_withdraw_history']
RoyaltyModel = db['royalty']
AdminUserModel = db['admin_users']

CollectionNFTModel = db['collection']
CollectionBoxModel = db['boxes']
SignatureLogsModel = db['signature_logs']


class RoyaltyHelper:
    @staticmethod
    def price_key(_token_symbol):
        return f"katana-dapp.price_cmc/{_token_symbol.lower()}"
    
    @classmethod
    def sum_royalty(self, _royalty_obj):
        if not type(_royalty_obj) == 'dict':
            return 0

        _sum = 0
        for key, value in _royalty_obj.items():
            _price = redis_cluster.get(self.price_key(key))
            _sum += int(key) * int(_price)
        
        return _sum

    @staticmethod
    def gen_query_project_royalty_fee():
        _dict = {
            "$project": {
                "_id": 0
            }
        }
        for _token in Constants.ROYALTY_FEE_TOKENS_LIST:
            _dict["$project"][f"{_token}_balance"] = {
                "$cond": [
                    {
                        "$eq": [
                            "$balances.symbol",
                            _token
                        ]
                    },
                    "$balances.balance",
                    0
                ]
            }
        return  _dict
    
    @staticmethod
    def gen_group_royalty_fee():
        _dict = {
                    "$group": {
                        "_id": 0
                    }
                }
        for _token in Constants.ROYALTY_FEE_TOKENS_LIST:
            _dict["$group"][_token] = {"$sum": f"{_token}_balance"}
        return  _dict

    @classmethod
    def get_all_collections_by_user(self, address, withdraw_history_length):
        _is_admin = False

        """
            Find admin user with address wallet login
        """
        _user_wallet = AdminUserModel.find_one({'address': address})

        if not _user_wallet:
            raise 'RoyaltyInfo: Wallet does not exist in any royalty'
        
        if get(_user_wallet, "is_admin"):
            _is_admin = True

        """
            Calculate the properties that needs to responses:
                + Withdrawal History 
                + List NFT collections
                + List Box collections
                + Is_ADMIN or not
        """
        if _is_admin:
            """
                Withdrawal History of all in the system
            """
            _withdraw_history = RoyaltyWithdrawHistoryModel.find({}).sort("block_time", -1).limit(withdraw_history_length)
            
        else:
            """
                Withdrawal History of current royalty user
            """
            _withdraw_history = RoyaltyWithdrawHistoryModel.find({
                'address': address
            }).sort("block_time", -1).limit(withdraw_history_length)

        """
            Collection List of all in the system
        """
        _find_collections_nft =  list(CollectionNFTModel.find({}).sort('created_time', -1))
        _find_collections_box =  list(CollectionBoxModel.find({}).sort('created_time', -1))

        _collection_nft = []
        _collection_box = []

        if len(_find_collections_box) > 0:
            for _box in _find_collections_box:
                _res_box = {}
                _res_box['name'] = get(_box, 'name')
                if _is_admin:

                    """
                        Sum of primary sale in each box collection
                    """
                    _sum_primary_sale = SignatureLogsModel.aggregate([
                        {
                            "$match": {
                                "collection": get(_box, 'address')
                            }
                        },
                        {
                            "$unwind": "$items"
                        },
                        {
                            "$group": {
                                "_id": 0,
                                "total_value": {"$sum": "$items.price_after_discount"}
                            }
                        }
                    ])
                    _sum_price = list(_sum_primary_sale)
                    _res_box['primary_sale'] = {
                        "symbol": Constants.ROYALTY_PRIMARY_SALES_TOKEN,
                        "balance": _sum_price[0].get("total_value", 0) if len(_sum_price) > 0 else 0
                    }
                    
                    """
                        Sum of the royalty in each box collection
                    """
                    _sum_royalties = list(RoyaltyModel.aggregate([
                        {
                            "$match": {
                                "collection_address": get(_box, "address")
                            }
                        },
                        {
                            "$unwind": "$balances"
                        },
                        self.gen_query_project_royalty_fee(),
                        self.gen_group_royalty_fee()
                    ]))

                    # List royalty by currency
                    _list_royalties = get(RoyaltyModel.find_one({
                        "collection_address": get(_box, "address")
                    }), "balances", [
                        {
                            "symbol": _token,
                            "balance": 0
                        }
                        for _token in Constants.ROYALTY_FEE_TOKENS_LIST
                    ])

                    _res_box['royalty'] = {
                        "sum": self.sum_royalty(_sum_royalties[0] if len(_sum_royalties) else 0),
                        "details": _list_royalties
                    }
                    
                    _res_box['total_income'] = _res_box['primary_sale']['balance'] + _res_box['royalty']['sum']
                else:
                    _res_box['total_income'] = 0
                    _res_box['primary_sale'] = 0
                    _royalty = RoyaltyModel.find_one(
                        filter={
                            "collection_address": get(_box, "address"),
                            "user_address": address
                        }
                    )
                    _res_box['royalty'] = self.sum_royalty(get(_royalty, "balances"))
                    _res_box['total_income'] = _res_box['royalty']
                _collection_box.append(_res_box)
        
        if len(_find_collections_nft) > 0:
            for _nft in _find_collections_nft:
                _res_nft = {}
                _res_nft['name'] = get(_nft, 'name')
                if _is_admin:

                    """
                        Sum of primary sales of each NFT collection
                    """
                    _sum_primary_sale = SignatureLogsModel.aggregate([
                        {
                            "$match": {
                                "collection": get(_nft, 'address')
                            }
                        },
                        {
                            "$unwind": "$items"
                        },
                        {
                            "$group": {
                                "_id": 0,
                                "total_value": {"$sum": "$items.price_after_discount"}
                            }
                        }
                    ])
                    _sum_price = list(_sum_primary_sale)
                    _res_nft['primary_sale'] = {
                        "symbol": Constants.ROYALTY_PRIMARY_SALES_TOKEN,
                        "balance": _sum_price[0].get("total_value", 0) if len(_sum_price) > 0 else 0
                    }

                    """
                        Sum of the royalty of each NFT collection
                    """
                    _sum_royalties = list(RoyaltyModel.aggregate([
                        {
                            "$match": {
                                "collection_address": get(_nft, "address")
                            }
                        },
                        {
                            "$unwind": "$balances"
                        },
                        self.gen_query_project_royalty_fee(),
                        self.gen_group_royalty_fee()
                    ]))

                    # List royalty by currency
                    _list_royalties = get(RoyaltyModel.find_one({
                        "collection_address": get(_nft, "address")
                    }), "balances", [
                        {
                            "symbol": _token,
                            "balance": 0
                        }
                        for _token in Constants.ROYALTY_FEE_TOKENS_LIST
                    ])

                    _res_nft['royalty'] = {
                        "sum": self.sum_royalty(_sum_royalties[0] if len(_sum_royalties) > 0 else 0),
                        "details": _list_royalties
                    }

                    _res_nft['total_income'] = _res_nft['primary_sale']['balance'] + _res_nft['royalty']['sum']
                else:
                    _res_nft['total_income'] = 0
                    _res_nft['primary_sale'] = 0
                    _royalty = RoyaltyModel.find_one(
                        filter={
                            "collection_address": get(_nft, "address"),
                            "user_address": address
                        }
                    )
                    _res_nft['royalty'] = self.sum_royalty(get(_royalty, "balances"))
                    _res_nft['total_income'] = _res_nft['royalty']
                _collection_nft.append(_res_nft)

        _overview = {
            'total_income': sum([_item['total_income'] for _item in _collection_nft]) + sum([_item['total_income'] for _item in _collection_box]),
            'total_royalty': sum([_item['royalty']['sum'] for _item in _collection_nft]) + sum([_item['royalty']['sum'] for _item in _collection_box]),
            'total_primary_sale': sum([_item['primary_sale']['balance'] for _item in _collection_nft]) + sum([_item['primary_sale']['balance'] for _item in _collection_box])
        }

        _res = {
            'withdraw_history': _withdraw_history,
            'collection_nft': _collection_nft,
            'collection_box': _collection_box,
            'is_admin': _is_admin,
            'overview': _overview,
            'token_address': {
                "wBNB": Config.TOKEN_WBNB,
                "USDT": Config.TOKEN_USDT
            }
        }
        # print(a)
        _res = json.loads(dumps(_res))
        return _res