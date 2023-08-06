#
# Copyright (c) 2022, Grigoriy Kramarenko <root@rosix.ru>
# All rights reserved.
# This file is not intended for copy and not for distribution.
#
import asyncio
import json
import logging
from collections import OrderedDict
from time import time
from urllib.parse import urlparse

from aiohttp import ClientSession

logger = logging.getLogger(__name__)
log_debug = logger.debug
log_info = logger.info
log_warn = logger.warning
log_error = logger.error

logger_http = logging.getLogger(logger.name + '.http')
# log_http_debug = logger_http.debug
log_http_info = logger_http.info
# log_http_warn = logger_http.warning
log_http_error = logger_http.error


async def verbose(writer, message, level=1):
    log_debug('verbose(writer=%s, level=%d)', id(writer), level)

    message = message.replace('"', "").replace("'", "")
    command = f'VERBOSE "{message}" {level}\n'
    writer.write(command.encode('utf8'))
    await writer.drain()


class Params(OrderedDict):

    def __str__(self):
        need = (
            'agi_channel',
            'agi_linkedid',
            'agi_uniqueid',
            'agi_callerid',
            'agi_calleridname',
            'agi_dnid',
            'agi_context',
        )
        lines = [
            f'{k}={v!r}' for k, v in self.items()
            if k.startswith('agi_arg_') or k in need]
        return ', '.join(lines)


class BaseServer:
    host = 'localhost'
    port = 4573
    params_class = Params

    def __init__(self, host=None, port=None):
        if host is not None:
            self.host = str(host)
        if port is not None:
            self.port = int(port)

    async def run(self):
        server = await asyncio.start_server(
            self.client_connection, self.host, self.port)
        log_info('AGI started as "agi://%s:%s/".', self.host, self.port)
        async with server:
            await server.serve_forever()

    async def client_connection(self, reader, writer):
        """
        Handles one request from the dialplan.

        Example of received data:
            agi_network: yes
            agi_network_script: callback
            agi_request: agi://localhost:4573/callback
            agi_channel: PJSIP/6001-00000001
            agi_language: en
            agi_type: PJSIP
            agi_uniqueid: 1642727514.2
            agi_version: 16.16.1~dfsg-1
            agi_callerid: 6001
            agi_calleridname: 6001
            agi_callingpres: 0
            agi_callingani2: 0
            agi_callington: 0
            agi_callingtns: 0
            agi_dnid: 1000
            agi_rdnis: unknown
            agi_context: default
            agi_extension: 1000
            agi_priority: 3
            agi_enhanced: 0.0
            agi_accountcode:
            agi_threadid: 140291135710976
            agi_arg_1: agent_call

        """
        start_time = time()

        log_debug('client_connected(reader=%s, writer=%s)',
                  id(reader), id(writer))

        readline = reader.readline
        params = self.params_class()

        while True:
            rawline = await readline()
            line = rawline.strip().decode('utf8')
            if not line:
                break

            if ':' not in line:
                error = 'In the line %r parameter violated.' % line
                await verbose(writer, error)
                writer.close()
                log_error(error)
                return

            param = line.split(':', 1)
            key = param[0].strip()
            data = param[1].strip()
            params[key] = data
            log_debug('%s: %s', key, data)

        return await self.dispatch(params, writer, start_time=start_time)

    async def dispatch(self, params, writer):
        """
        The method for overriding server behavior.
        """
        pass


class Server(BaseServer):
    """
    This is a universal server for which you only need to set the end handlers.

    Handlers can return commands for Asterisk as a byte string.

    The server can process actions in the background, for this the word
    "async" must be present in the request address:

        agi://localhost:4573/callback/async
        or
        agi://localhost:4573/async/callback

    Note that background execution does not return commands to Asterisk.

    """

    # The maximum number of seconds for a connection after which the logging
    # level is raised to WARNING.
    warning_connection = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handlers = {}

    async def dispatch(self, params, writer, start_time):
        conn_name = self.get_connection_name(params)
        log_debug('%s dispatch begin.', conn_name)

        script = params.get('agi_network_script', '')
        async_mode = False
        if script.startswith('async/'):
            async_mode = True
            script = script[6:]
        elif script.endswith('/async'):
            async_mode = True
            script = script[:-6]
        elif script.startswith('sync/'):
            async_mode = False
            script = script[5:]
        elif script.endswith('/sync'):
            async_mode = False
            script = script[:-5]

        if async_mode:
            # await verbose(writer, 'Run in async mode.')
            log_debug('%s run in async mode.', conn_name)
            # By closing writer here, we do not wait for a response from the
            # server and the dialplan exit from AGI, continuing its execution.
            writer.close()
            log_debug('%s closed socket for ASYNC mode.', conn_name)
            close_time = time()
        else:
            # await verbose(writer, 'Run in sync mode.')
            log_debug('%s run in sync mode.', conn_name)
            close_time = 0

        try:
            handler = self.handlers[script]
            commands = await handler(params)
        except Exception as e:
            if not async_mode:
                msg = 'ERROR: %s' % e
                await verbose(writer, msg)
            log_error('%s Request is failed: %s', conn_name, e, exc_info=e)
        else:
            log_debug('%s Request is success.', conn_name)
            # Response commands for AGI.
            if commands:
                if async_mode:
                    log_error('%s in async mode. Response %r is lost!!!',
                              conn_name, commands)
                elif isinstance(commands, bytes):
                    writer.write(commands + b'\n')
                    await writer.drain()
                    log_debug('%s got commands: %r', conn_name, commands)
                else:
                    msg = 'Handler returns a non-byte string!'
                    await verbose(writer, f'ERROR: {msg}')
                    log_error('%s %s', conn_name, msg)
            else:
                log_debug('%s no commands.', conn_name)

        if not async_mode:
            # Closing writer here, we waited for a response from the server
            # and only now the dialplan exit from AGI, continuing its
            # execution.
            writer.close()
            log_debug('%s closed socket for SYNC mode.', conn_name)
            close_time = time()

        connect_seconds = close_time - start_time
        total_seconds = time() - start_time

        if connect_seconds > self.warning_connection:
            log = log_warn
        else:
            log = log_info
        log('Time: connect=%f; total=%f. %s',
            connect_seconds, total_seconds, conn_name)

        log_debug('%s dispatch end.', conn_name)

    def get_connection_name(self, params):
        script = params.get('agi_network_script', '')
        channel = params.get('agi_channel', '')
        return 'Channel %r (%r)' % (channel, script)


class ProxyServer(BaseServer):
    """
    This is a server proxying requests to another http server.
    """

    api_url = 'http://localhost/api'
    api_auth = None
    # The maximum number of seconds for a connection after which the logging
    # level is raised to WARNING.
    warning_connection = 1
    # These are parameters that will not be transmitted to the HTTP server.
    exclude_params = (
        'agi_network',
        'agi_network_script',
        'agi_request',
    )

    def __init__(self, *args, api_url=None, api_auth=None, **kwargs):
        super().__init__(*args, **kwargs)
        if api_url is not None:
            self.api_url = str(api_url)
        if api_auth is not None:
            self.api_auth = int(api_auth)
        self.session = None
        self.parse_api_url()

    def parse_api_url(self):
        url = urlparse(self.api_url)
        self.base_url = f'{url.scheme}://{url.netloc}'

        self.base_path = url.path
        if not self.base_path.endswith('/'):
            self.base_path += '/'

    async def create_session(self):
        self.session = ClientSession(
            auth=self.api_auth, base_url=self.base_url)

    async def run(self):
        await self.create_session()
        return await super().run()

    async def dispatch(self, params, writer, start_time):
        conn_name = self.get_connection_name(params)
        log_debug('%s dispatch begin.', conn_name)

        path = params.get('agi_network_script', '')
        data = {k: v for k, v in params.items()
                if k not in self.exclude_params}
        try:
            commands = await self.post(path, data)
        except Exception as e:
            msg = 'ERROR: %s' % e
            await verbose(writer, msg)
            log_error('%s Request is failed: %s', conn_name, e, exc_info=e)
        else:
            log_debug('%s Request is success.', conn_name)
            # Response commands for AGI.
            if commands:
                if isinstance(commands, bytes):
                    writer.write(commands + b'\n')
                    await writer.drain()
                    log_debug('%s got commands: %r', conn_name, commands)
                else:
                    msg = 'Handler returns a non-byte string!'
                    await verbose(writer, f'ERROR: {msg}')
                    log_error('%s %s', conn_name, msg)
            else:
                log_debug('%s no commands.', conn_name)

        # Closing writer here, we waited for a response from the server
        # and only now the dialplan exit from AGI, continuing its
        # execution.
        writer.close()
        log_debug('%s closed socket.', conn_name)

        connect_seconds = time() - start_time

        if connect_seconds > self.warning_connection:
            log = log_warn
        else:
            log = log_info
        log('Time: connect=%f. %s', connect_seconds, conn_name)

        log_debug('%s dispatch end.', conn_name)

    def get_connection_name(self, params):
        script = params.get('agi_network_script', '')
        channel = params.get('agi_channel', '')
        return 'Channel %r (%r)' % (channel, script)

    async def post(self, path, data):
        if path.startswith('/'):
            path = path[1:]
        path = f'{self.base_path}{path}'

        log_http_info('>>> POST "%s" %s', path, data)

        try:
            async with self._session.post(path, data=data) as r:
                status, result = await self.parse_response(r)
        except Exception as e:
            log_http_error('<<< POST %s', e)
            raise e

        log_http_info('<<< POST %r', result)

        if not (200 <= status < 300):
            raise RuntimeError(f'{status}: {result}')

        return result.encode()

    async def parse_response(self, response):
        status = response.status
        result = await response.text()
        if response.content_type == 'application/json':
            try:
                result = '\n'.join(json.loads(result)['commands'])
            except (ValueError, KeyError) as e:
                result = f'The server returned a broken JSON: {e}'
                status = 501
        return status, result
