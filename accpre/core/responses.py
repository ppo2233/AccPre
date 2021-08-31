from rest_framework.response import Response as DRFResponse
from accpre.core import status_codes


class Response(DRFResponse):
    """ AccPre Response """
    success = 0
    error = -1
    default_err_code = status_codes.SUCCESS_CODE

    def __init__(self, data='', msg='', err_code=False, headers=None):
        output = {
            'code': self.error if err_code else self.success,
            'data': data,
            'err_code': err_code if err_code else self.default_err_code,
            'msg': msg
        }

        super(Response, self).__init__(data=output, headers=headers)
