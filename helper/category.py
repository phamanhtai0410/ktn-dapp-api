from models import CategoryModel


class CategoryHelper:
    @staticmethod
    def get_all_category():
        _categories = list(CategoryModel.find({}))
        if not _categories:
            return {
                'categories': []
            }
        _list = []
        for _cate in _categories:
            _list.append({
                **_cate,
                # Add soome fields for mock UI
                'min_price': float(150),
                'total_supply': 10000
            })
        return {
            'categories': _list
        }