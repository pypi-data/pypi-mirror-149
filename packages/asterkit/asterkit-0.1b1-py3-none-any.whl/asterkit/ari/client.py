#
# Copyright (c) 2022, Grigoriy Kramarenko <root@rosix.ru>
# All rights reserved.
# This file is distributed under BSD 3-Clause License.
#

import asyncio
import json
import logging
from collections import OrderedDict
from time import time
from urllib.parse import urljoin
from uuid import uuid4

from aiohttp import BasicAuth, ClientSession, WSMsgType
from aiohttp.client_exceptions import ClientError

from .exceptions import AsteriskError, CODE_ERRORS
from .models import App, Event, Model

logger = logging.getLogger(__name__)
# log_debug = logger.debug
log_info = logger.info
# log_warn = logger.warning
log_error = logger.error

logger_http = logging.getLogger(logger.name + '.http')
# log_http_debug = logger_http.debug
log_http_info = logger_http.info
# log_http_warn = logger_http.warning
log_http_error = logger_http.error

logger_ws = logging.getLogger(logger.name + '.ws')
log_ws_debug = logger_ws.debug
log_ws_info = logger_ws.info
log_ws_warn = logger_ws.warning
log_ws_error = logger_ws.error


def make_ari_path(path):
    if not path.startswith('/'):
        path = f'/{path}'
    if not path.startswith('/ari/'):
        path = f'/ari{path}'
    return path


async def parse_response(response):
    status = response.status

    # Download file.
    if response.content_type == 'application/octet-stream':
        result = await response.read()
        return status, result

    # Not necessarily it will be application/json.
    result = await response.text()
    try:
        result = json.loads(result)
    except ValueError:
        pass
    return status, result


class LazyMessage:

    def __init__(self, message):
        self.message = message

    def __bool__(self):
        return bool(self.message)

    def __str__(self):
        event_data = self.get_event_data()
        if event_data is None:
            return f'Message {self.message}'
        return Event.pformat(event_data)

    def __repr__(self):
        event_data = self.get_event_data()
        if event_data is None:
            text = self.message
        else:
            text = str(event_data)
        return f'<Message: {text}>'

    def get_event_data(self):
        string = self.message
        try:
            data = json.loads(string)
        except ValueError:
            log_error('The message not in JSON format: %r', string)
            return

        if not isinstance(data, dict):
            log_error('The message is not dictionary: %r', string)
            return

        if 'type' not in data:
            log_error('The message does not contain the type: %r', string)
            return

        return data


class Handler(dict):

    def __str__(self):
        return self.human_string

    @property
    def age(self):
        return time() - self['added']

    @property
    def callback_name(self):
        return self['callback'].__qualname__

    @property
    def human_string(self):
        return '%s: %s, app=%s, object=%s, hid=%s' % (
            self['event'],
            self.callback_name,
            self['app'] or '',
            self['object'] or '',
            self['id'],
        )


class Client:
    ssl = False
    host = 'localhost'
    port = 8088
    username = 'asterisk'
    password = 'asterisk'
    reconnection_timeout = 1.0

    def __init__(self, host=None, port=None, username=None, password=None,
                 ssl=None, reconnection_timeout=None):
        if host is not None:
            self.host = str(host)
        if port is not None:
            self.port = int(port)
        if username is not None:
            self.username = str(username)
        if password is not None:
            self.password = str(password)
        if ssl is not None:
            self.ssl = bool(ssl)
        if reconnection_timeout is not None:
            self.reconnection_timeout = float(reconnection_timeout)

        self.event_models = {}
        self.is_connected = False
        self._apps = {}
        self._handlers = {}
        self._session = None
        self._websocket = None

        self.subscribe('StasisStart', self.handle_stasis_start)
        self.subscribe('StasisEnd', self.handle_stasis_end)
        self.subscribe('ApplicationReplaced', self.handle_application_replaced)

        self._request_id = 0

    def __str__(self):
        return self.base_url

    def __repr__(self):
        return '<Client %s>' % self.base_url

    def get_request_id(self):
        rid = self._request_id
        if rid >= 99999:
            rid = 1
        else:
            rid += 1
        self._request_id = rid
        return rid

    @property
    def base_url(self):
        domain = f'{self.host}:{self.port}'
        proto = 'https' if self.ssl else 'http'
        return f'{proto}://{domain}'

    def subscribe(self, name, callback, app=None, object=None, **options):
        """
        Register callback for events with given name.
        """

        assert 'event' not in options, \
            'Please exclude `event` from your options or rename it.'
        assert 'hid' not in options, \
            'Please exclude `hid` from your options or rename it.'

        all_handlers = self._handlers
        handlers = all_handlers.get(name)
        if handlers is None:
            all_handlers[name] = handlers = OrderedDict()

        # List of fields for find the object in the event.
        fields_for_object = []

        if object:
            if name in self.event_models:
                model = self.event_models.get(name)
            else:
                model = self.event_models.get('ChannelUserevent')
            if model:
                object_model_name = object.model_name
                for k, v in model['properties'].items():
                    if v.get('type') == object_model_name:
                        fields_for_object.append(k)

        if isinstance(app, str):
            app_name = app
        elif isinstance(app, App):
            app_name = app.name
        else:
            app_name = ''

        def checker(event):
            """
            Checks whether the event is related to the app or/and object.
            """
            if app_name and app_name != event.get('application'):
                log_ws_debug(
                    'Checker: need app %s. Return False. %s', app, event)
                return False

            if not object:
                log_ws_debug(
                    'Checker: not for object. Return True. %s', event)
                return True

            object_id = object.id
            if object_id is None:
                log_ws_debug(
                    'Checker: object.id is None. Return True. %s', event)
                return False

            get_id_from_data = object.get_id_from_data

            for field in fields_for_object:
                if field in event:
                    data = event[field]
                    if data:
                        if object_id == get_id_from_data(data):
                            log_ws_debug(
                                'Checker: object found. Return True. %s',
                                event)
                            return True
                        # else:
                        #     ws_debug('Checker: %r != %r.', data, object)
                    # else:
                    #     ws_debug(
                    #         'Checker: no %r data in event %s.', field, event)
                # else:
                #     lws_debug(
                #         'Checker: no %r field in event %s.', field, event)

            log_ws_debug('Checker: object %s passed. Return False. %s',
                         object, event)
            return False

        hid = str(uuid4())
        handler = Handler({
            'id': hid,
            'event': name,
            'callback': callback,
            'options': options,
            'checker': checker,
            'app': app,
            'object': object,
            'added': time()
        })
        handlers[hid] = handler

        def unsubscribe():
            self.unsubscribe(hid, handlers)

        log_info('Subscribe %s. For %s %d handlers.',
                 handler, name, len(handlers))

        return unsubscribe, hid

    def unsubscribe(self, hids, handlers=None):
        if not isinstance(hids, (list, tuple, set)):
            hids = (hids,)

        # Recursive runing for root.
        if handlers is None:
            for event_handlers in self._handlers.values():
                self.unsubscribe(hids, event_handlers)
            return hids

        for hid in hids:
            if hid in handlers:
                handler = handlers.pop(hid)
                log_info('Unsubscribe %s', handler)
        return hids

    def get_all_hids(self):
        for handlers in self._handlers.values():
            for hid in handlers.keys():
                yield hid

    def get_count_handlers(self):
        count = 0
        for handlers in self._handlers.values():
            count += len(handlers)
        return count

    def filter_handlers(self, event):
        """
        Returns the filtered handlers for Event.
        """

        L = []
        for name in (event.name, '*'):
            handlers = self._handlers.get(name, {})
            for hid, handler in handlers.items():
                if handler['checker'](event):
                    log_ws_info('Accept %s', handler)
                    L.append(handler)
                else:
                    log_ws_info('Passed %s', handler)
        return L

    async def add_apps(self, *apps):
        if self.is_connected:
            raise RuntimeError('First you need to disconnect the client.')

        instances = []

        for app in apps:
            if isinstance(app, App):
                pass
            elif issubclass(app, App):
                app = app(client=self)
            else:
                raise ValueError(
                    'Your app must be subclass or instance of App.')

            self._apps[app.name] = app
            instances.append(app)
            await app.on_install()

        return instances

    async def remove_apps(self, *apps):
        if self.is_connected:
            raise RuntimeError('First you need to disconnect the client.')

        for app in apps:
            if isinstance(app, App):
                name = app.name
            elif isinstance(app, str):
                name = app
            else:
                raise ValueError('Your app must be instance or name of App.')

            instance = self._apps.pop(name, None)
            if instance:
                await instance.on_uninstall()

            return bool(instance)

    async def on_connect(self):
        for app in self._apps.values():
            await app.on_connect()

    async def on_disconnect(self):
        for app in self._apps.values():
            await app.on_disconnect()

    async def handle_stasis_start(self, event, **kwargs):
        app = self._apps.get(event['application'])
        if app and hasattr(app, 'handle_stasis_start'):
            channel = event['channel']['name']
            log_info('Channel %s has enter to the %r.', channel, app.name)
            await app.handle_stasis_start(event, **kwargs)

    async def handle_stasis_end(self, event, **kwargs):
        app = self._apps.get(event['application'])
        if app and hasattr(app, 'handle_stasis_end'):
            await app.handle_stasis_end(event, **kwargs)
            channel = event['channel']['name']
            log_info('Channel %s has left the %r.', channel, app.name)

    async def handle_application_replaced(self, event, **kwargs):
        app = self._apps.get(event['application'])
        if app:
            logger.critical('%r has been replaced.', app)

    async def apply_handler(self, event, handler):
        callback = handler['callback']
        try:
            log_ws_info('Exec Event %s ON %s', event, handler.callback_name)
            await callback(
                event=event, hid=handler['id'], **handler['options'])
        except Exception as e:
            log_ws_error(
                'Handler %s is broken.', handler, exc_info=e)
            return 0
        else:
            return 1

    async def connect(self, listen_all_events=False):
        """
        Creates a connection with Asterisk.
        """

        assert self._apps, 'Add one or more applications before connection.'

        auth = BasicAuth(self.username, self.password)

        self._session = ClientSession(auth=auth, base_url=self.base_url)

        # Load the event models.

        events = await self.get('/api-docs/events.json')
        self.event_models = events['models']

        # Connect to websocket.

        apps = ','.join(self._apps.keys())
        ws_url = urljoin(self.base_url, f'/ari/events?app={apps}')
        if listen_all_events:
            ws_url += '&subscribeAll=true'

        TEXT = WSMsgType.TEXT
        ERROR = WSMsgType.ERROR

        loop = asyncio.get_event_loop()
        run_thread = asyncio.run_coroutine_threadsafe

        all_handlers = self._handlers
        apply_handler = self.apply_handler
        filter_handlers = self.filter_handlers

        async def prepare_message(message):
            data = message.get_event_data()
            if data is None:
                return

            count = 0
            event = Event(client=self, data=data)
            if '*' in all_handlers or event.name in all_handlers:
                handlers = filter_handlers(event)
                tasks = [apply_handler(event, h) for h in handlers]
                if tasks:
                    L = await asyncio.gather(*tasks)
                    count = sum(L)

            if count:
                log_ws_info('Done Event %s (%s handlers)', event, count)
            else:
                log_ws_info('Skip Event %s', event)

        async def wsconnect(timeout=0):
            if timeout:
                log_ws_warn(
                    'Reconnection will be in %f seconds.', timeout)
                await asyncio.sleep(timeout)

            async with ClientSession(auth=auth) as session:
                async with session.ws_connect(ws_url) as websocket:
                    log_ws_info('Websocket was connected to %r.', ws_url)
                    self.is_connected = True
                    self._websocket = websocket
                    await self.on_connect()
                    async for msg in websocket:
                        if not self.is_connected:
                            await websocket.close()
                            break
                        if msg.type == TEXT:
                            lazy_message = LazyMessage(msg.data)
                            log_ws_debug('Received %s', lazy_message)
                            if not lazy_message:
                                await websocket.close()
                                break
                            else:
                                run_thread(prepare_message(lazy_message), loop)
                        elif msg.type == ERROR:
                            log_ws_debug('Received error: %r', msg)
                            await websocket.close()
                            break
                await self.on_disconnect()

        timeout = 0
        while True:
            try:
                await wsconnect(timeout)
            except ClientError as e:
                timeout = self.reconnection_timeout
                log_ws_error(e)
            if not self.is_connected:
                break

        try:
            await self.disconnect()
        except Exception:
            pass
        log_ws_info('Websocket was disconnected from %r.', ws_url)

    async def disconnect(self):
        """
        Closes the Asterisk connection.
        """
        self.is_connected = False
        if hasattr(self, '_session') and self._session:
            await self._session.close()
        if hasattr(self, '_websocket') and self._websocket:
            await self._websocket.close()

    async def get(self, path, **kwargs):
        rid = self.get_request_id()
        path = make_ari_path(path)

        log_http_info('>>> GET[%05d] "%s" %s', rid, path, kwargs)

        try:
            async with self._session.get(path, **kwargs) as r:
                status, result = await parse_response(r)
        except Exception as e:
            log_http_error('<<< GET[%05d] %s', rid, e)
            raise e

        log_http_info('>>> GET[%05d] %r', rid, result)

        if status in CODE_ERRORS:
            raise CODE_ERRORS[status](status, result)
        if not (200 <= status < 300):
            raise AsteriskError(status, result)

        return result

    async def post(self, path, **kwargs):
        rid = self.get_request_id()
        path = make_ari_path(path)

        log_http_info('>>> POST[%05d] "%s" %s', rid, path, kwargs)

        try:
            async with self._session.post(path, **kwargs) as r:
                status, result = await parse_response(r)
        except Exception as e:
            log_http_error('<<< POST[%05d] %s', rid, e)
            raise e

        log_http_info('<<< POST[%05d] %r', rid, result)

        if status in CODE_ERRORS:
            raise CODE_ERRORS[status](status, result)
        if not (200 <= status < 300):
            raise AsteriskError(status, result)

        return result

    async def put(self, path, **kwargs):
        rid = self.get_request_id()
        path = make_ari_path(path)

        log_http_info('>>> PUT[%05d] "%s" %s', rid, path, kwargs)

        try:
            async with self._session.put(path, **kwargs) as r:
                status, result = await parse_response(r)
        except Exception as e:
            log_http_error('<<< PUT[%05d] %s', rid, e)
            raise e

        log_http_info('<<< PUT[%05d] %r', rid, result)

        if status in CODE_ERRORS:
            raise CODE_ERRORS[status](status, result)
        if not (200 <= status < 300):
            raise AsteriskError(status, result)

        return result

    async def delete(self, path, **kwargs):
        rid = self.get_request_id()
        path = make_ari_path(path)

        log_http_info('>>> DELETE[%05d] "%s" %s', rid, path, kwargs)

        try:
            async with self._session.delete(path, **kwargs) as r:
                status, result = await parse_response(r)
        except Exception as e:
            log_http_error('<<< DELETE[%05d] %s', rid, e)
            raise e

        log_http_info('<<< DELETE[%05d] %r', rid, result)

        if status in CODE_ERRORS:
            raise CODE_ERRORS[status](status, result)
        if not (200 <= status < 300):
            raise AsteriskError(status, result)

        return result

    async def request(self, method, path, params=None, data=None):
        method = getattr(self, method.lower())
        return method(path=path, params=params, data=data)

    async def send_user_event(self, event_name, app, source=None,
                              variables=None):
        """
        Generate a user event.
        """

        params = {'application': app}
        if source is not None:
            params['source'] = source

        if variables is not None:
            data = {'variables': variables}
        else:
            data = None

        path = f'/events/user/{event_name}'
        result = await self.post(path, params=params, json=data)
        return result

    async def get_objects(self, model, as_objects=True, path=None):
        """
        Returns list of instances for Model from Asterisk.
        """

        assert issubclass(model, Model)

        if not path:
            path = model.model_path

        result = await self.get(path)
        if as_objects:
            result = [model(self, data) for data in result]
        return result

    async def get_object_by_id(self, model, id):
        """
        Returns instance of Model is exists in Asterisk or Raise Error404.
        """

        assert issubclass(model, Model)

        path = f'{model.model_path}/{id}'
        result = await self.get(path)
        return model(self, result)

    async def delete_object_by_id(self, model, id):
        """
        Delete object from Asterisk and returns result of request.
        """

        assert issubclass(model, Model)

        path = f'{model.model_path}/{id}'
        result = await self.delete(path)
        return result
