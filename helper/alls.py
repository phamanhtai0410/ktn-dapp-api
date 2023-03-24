# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from models import CollectionNFTModel, CollectionBoxModel
from pydash import get

class AllsItemHelper:
    @staticmethod
    def get_by_filter(params={}):
        print(params)
        _filter = {}
        if get(params, 'chain'):
            _filter['chain'] = get(params, 'chain')
        if get(params, 'category'):
            _filter['category'] = get(params, 'category')
        _collections = list(CollectionNFTModel.find(filter=_filter))
        # _boxes = list(CollectionBoxModel.find(filter=_filter))
        _items = []
        # if len(_boxes):
        #     for _box in _boxes:
        #         if get(_box, 'address'):
        #             _items.append({
        #                 'name': get(_box, 'name'),
        #                 'price': get(_box, 'price', 0),
        #                 'image': get(_box, 'image', ''),
        #                 'rarity': 'LOOTBOX',
        #                 'total_supply': get(_box, 'total_supply', 0),
        #                 'address': get(_box, 'address')
        #             })

        if len(_collections):
            for _collection in _collections:
                if get(_collection, 'address'):
                    _types_list = get(_collection, 'types_list')
                    for (_idx, _type) in enumerate(_types_list):
                        _items.append({
                            'nft_id': _idx, # NOTE: this nft_id is index of nft in collection for mint
                            'name': get(_collection, 'name'),
                            'price': get(_type, 'price', 0),
                            'image': get(_type, 'ImageUrl', ''),
                            'rarity': get(_type, 'AssetRarity'),
                            'total_supply': get(_collection, 'total_supply', 0),
                            'address': get(_collection, 'address')
                        })

        _result = {
            'items': _items,
            'num_of_page': 0,
            'page_size': get(params, 'page_size'),
            'page': 0
        }
        # print("Result = ", _result)
        return _result or {}
    
    @staticmethod
    def get_one_by_filter(params={}):
        _filter = {}
        _address = get(params, 'address').lower()
        _filter["address"] = _address
        if get(params, 'chain'):
            _filter['chain'] = get(params, 'chain')
        if get(params, 'category'):
            _filter['category'] = get(params, 'category')
        _collections = CollectionNFTModel.find(filter=_filter)
        # _boxes = list(CollectionBoxModel.find(filter=_filter))
        _items = []
        # if len(_boxes):
        #     for _box in _boxes:
        #         if get(_box, 'address'):
        #             _items.append({
        #                 'name': get(_box, 'name'),
        #                 'price': get(_box, 'price', 0),
        #                 'image': get(_box, 'image', ''),
        #                 'rarity': 'LOOTBOX',
        #                 'total_supply': get(_box, 'total_supply', 0),
        #                 'address': get(_box, 'address')
        #             })

        if len(_collections):
            for _collection in _collections:
                if get(_collection, 'address'):
                    _types_list = get(_collection, 'types_list')
                    for (_idx, _type) in enumerate(_types_list):
                        _items.append({
                            'nft_id': _idx, # NOTE: this nft_id is index of nft in collection for mint
                            'name': get(_collection, 'name'),
                            'price': get(_type, 'price', 0),
                            'image': get(_type, 'ImageUrl', ''),
                            'rarity': get(_type, 'AssetRarity'),
                            'total_supply': get(_collection, 'total_supply', 0),
                            'address': get(_collection, 'address')
                        })
        _result = {
            'items': _items,
        
        }
        return _result or {}
    
    