#
# Copyright (c) 2022, Grigoriy Kramarenko <root@rosix.ru>
# All rights reserved.
# This file is distributed under BSD 3-Clause License.
#

from aiohttp import ClientError


class AsteriskError(ClientError):

    def __init__(self, status, result):
        self.status = status
        self.result = result
        if isinstance(result, dict) and 'error' in result:
            message = result['error']
        else:
            message = str(result)
        super().__init__(f'Status {status}. {message}')


class Error400(AsteriskError):
    pass


class Error403(AsteriskError):
    pass


class Error404(AsteriskError):
    pass


class Error405(AsteriskError):
    pass


class Error409(AsteriskError):
    pass


class Error422(AsteriskError):
    pass


class Error500(AsteriskError):
    pass


CODE_ERRORS = {
    400: Error400,
    403: Error403,
    404: Error404,
    405: Error405,
    409: Error409,
    422: Error422,
    500: Error500,
}
