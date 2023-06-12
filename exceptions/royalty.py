from lib.exception import BadRequest

class InvalidRoyaltyCodeEx(Exception):
    def __init__(self, msg='Royalty code is invalid.', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_INVALID_ROYALTY_CODE'
        
    pass
