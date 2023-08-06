#
# Copyright (c) 2022, Grigoriy Kramarenko <root@rosix.ru>
# All rights reserved.
# This file is not intended for copy and not for distribution.
#
import asyncio
import logging
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from time import time
from pprint import pformat
from uuid import uuid4

logger = logging.getLogger(__name__)
log_debug = logger.debug
log_info = logger.info
log_warn = logger.warning
log_error = logger.error

EOL = '\r\n'
END_COMMAND = '--END COMMAND--'


class Response(OrderedDict):

    def __str__(self):
        message = self.get('Response', 'blank')
        if 'Output' in self:
            message += ' (with output)'
        return f"<Response: {message}>"

    def get_output(self, as_list=False):
        log_debug('ami.Response.get_output(%s, as_list=%s)', self, as_list)
        output = self.get('Output', '')
        if isinstance(output, str):
            output = output.replace('\r', '')
            if as_list:
                return output.split('\n')
        elif not as_list:
            return '\n'.join(output)
        return output


class Event(OrderedDict):

    def __str__(self):
        lines = pformat(list(self.items()), indent=1).split('\n')
        lines[0] = f' {lines[0][1:]}'
        lines = '\n'.join([f'   {line}' for line in lines])
        return f'Event {self.name} [\n{lines}'

    def __repr__(self):
        return f"<Event: {self.name}>"

    @property
    def name(self):
        return self.get('Event', 'blank')


class ManagerError(Exception):
    pass


class ManagerAuthError(ManagerError):
    pass


async def parse_response(reader, action_id, debug_mode):

    response = Response()
    readline = reader.readline
    internal_output = False

    while True:
        line = await readline()
        line = line.decode('utf8', 'ignore')
        cline = line.rstrip()
        if END_COMMAND in cline:
            cline = ''

        # Окончание ответа пустой строкой.
        if not cline and response:
            break

        if internal_output:
            key = 'Output'
            value = cline
        else:
            parts = line.split(': ', 1)
            # Заголовок вроде 'Asterisk Call Manager/5.0.2'.
            if len(parts) != 2:
                continue

            key = parts[0]
            value = parts[1].rstrip()

        # Ответ на предыдущую, не требующую ответа команду может быть
        # получен, но должен быть пропущен.
        if key == 'Response':
            response[key] = value
        elif key == 'ActionID':
            if action_id != value:
                if debug_mode:
                    log_debug(
                        '... skip response %s: %s ...',
                        response['Response'], value)
                response = Response()
                continue
            response[key] = value
            if debug_mode:
                log_debug('  Response: %s', response['Response'])
                log_debug('  %s: %s', key, value)
            if response['Response'] == 'Follows':
                internal_output = True
        elif 'ActionID' in response:
            if key in response:
                response[key] += f'\n{value}'
            else:
                response[key] = value
            if debug_mode:
                log_debug('  %s: %s', key, value)

    return response


async def parse_output(reader, action_id, debug_mode):
    readline = reader.readline
    output = []

    if debug_mode:
        log_debug('  BEGIN OUTPUT FOR %s', action_id)

    while True:
        line = await readline()
        line = line.decode('utf8', 'ignore')

        # Ответа может не быть совсем, тогда будет получена
        # чужая строка, завершающаяся на EOL.
        # Либо это будет строка '--END COMMAND--\r\n'.
        if line.endswith(EOL):
            log_debug('  END OUTPUT FOR %s', action_id)
            break

        cline = line.rstrip()

        if debug_mode:
            log_debug('    Output: %s', cline)

        output.append(cline)

    return output


async def parse_events(reader, action_id, debug_mode):
    readline = reader.readline

    if debug_mode:
        log_debug('  BEGIN EVENTS FOR %s', action_id)

    events = []
    event = Event()
    wait_events = True

    while wait_events:
        line = await readline()
        line = line.decode('utf8', 'ignore')

        # Окончание ответа пустой строкой.
        if not line.rstrip():
            if event.get('ActionID') == action_id:
                events.append(event)

                if debug_mode:
                    number = len(events)
                    log_debug(
                        '    BEGIN EVENT %d FOR %s',
                        number, action_id)
                    for key, value in event.items():
                        log_debug('      %s: %s', key, value)
                    log_debug(
                        '    END EVENT %d FOR %s',
                        number, action_id)

                if event.get('EventList') == 'Complete':
                    if debug_mode:
                        log_debug(
                            '  END EVENTS FOR %s', action_id)
                    wait_events = False

            event = Event()
            continue

        parts = line.split(': ', 1)
        # Заголовок вроде 'Asterisk Call Manager/5.0.2'
        if len(parts) != 2:
            continue

        key = parts[0]
        value = parts[1].rstrip()

        if key in event:
            event[key] += f'\n{value}'
        else:
            event[key] = value

    return events


async def parse_event(reader, handlers, any_event_handlers, skip_events,
                      debug_mode):
    readline = reader.readline

    event = Event()
    event_handlers = None

    while True:
        line = (await readline()).decode('utf8', 'ignore')

        # Окончание ответа пустой строкой.
        if not line.rstrip():
            break

        parts = line.split(': ', 1)
        # Заголовок вроде 'Asterisk Call Manager/5.0.2'
        if len(parts) != 2:
            continue

        key = parts[0]
        value = parts[1].rstrip()

        if key == 'Event':
            # Незарегистрированное событие пропускаем.
            if value in handlers:
                event_handlers = handlers[value]
            elif value in skip_events or not any_event_handlers:
                event = Event()
                if debug_mode:
                    log_debug('SKIP %s', value)
                continue
            if debug_mode:
                log_debug('EVENT %s', value)
                log_debug('  %s: %s', key, value)
            event[key] = value
        elif event:
            if key in event:
                event[key] += f'\n{value}'
            else:
                event[key] = value
            if debug_mode:
                log_debug('  %s: %s', key, value)

    return event, event_handlers


class BaseManager:
    host = 'localhost'
    port = 5038
    username = 'test'
    password = 'test'

    def __init__(self, host=None, port=None, username=None, password=None):
        if host is not None:
            self.host = str(host)
        if port is not None:
            self.port = int(port)
        if username is not None:
            self.username = str(username)
        if password is not None:
            self.password = str(password)

        self.reader = None
        self.writer = None
        self.is_authenticated = False

    @property
    def is_connected(self):
        writer = self.writer
        return writer and not writer.is_closing()

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.host, self.port)
        await self.login(self.username, self.password)

    async def disconnect(self):
        if self.is_connected:
            # await self.logout()
            self.writer.close()
            await self.writer.wait_closed()
            log_debug('Writer is closed.')
            # TODO: определить, действительно нужна очистка сокета или нет.
            read = self.reader.read
            line = await read(4096)
            while line:
                line = await read(4096)
            log_debug('Reader is clean.')

    async def send(self, message):
        """
        Отправляет сформированное сообщение в сокет.
        """

        if not self.is_connected:
            # Это вызовет self.send(auth_message), но уже с установленным
            # флагом соединения.
            await self.connect()

        self.writer.write(message.encode())
        await self.writer.drain()

    async def send_action(self, action={}, wait_response=True, **kwargs):
        """
        Формирует и отправляет команду в Asterisk и при включённом флаге
        ожидании ответа полностью считывает его и возвращает.

        Если значением в внутри действия будет список, то он будет развёрнут
        в несколько строк с одним и тем же заголовком:

        action = {"Action": "Originate",
                  "Variable": ["var1=value", "var2=value"]}
        await self.send_action(action)

        ...

        Action: Originate
        Variable: var1=value
        Variable: var2=value
        """

        start_time = time()

        # Это необходимо для уменьшения кол-ва вызовов функций логгирования
        # внутри циклов.
        debug_mode = logger.level <= logging.DEBUG

        action.update(kwargs)

        if 'ActionID' not in action:
            # action['ActionID'] = f'{action["Action"]}_{uuid4()}'
            action['ActionID'] = str(uuid4())

        lines = []
        add = lines.append

        # Формируем сообщение для Asterisk.
        if debug_mode:
            log_debug('BEGIN ACTION')
        for key, value in action.items():
            if isinstance(value, (tuple, list)):
                for item in value:
                    line = '%s: %s' % (key, item)
                    add(line)
                    if debug_mode:
                        log_debug('  %s', line)
            else:
                line = '%s: %s' % (key, value)
                add(line)
                if debug_mode:
                    log_debug('  %s', line)
        if debug_mode:
            log_debug('END ACTION')

        add(EOL)
        message = EOL.join(lines)

        preparing_time = time()

        # Отправляем в Asterisk.
        await self.send(message)
        sending_time = time()

        action_name = action['Action']
        if action_name == 'Command':
            action_name += f": {action['Command']}"
        action_id = action['ActionID']

        # Если нужно дождаться ответа, то приступаем к парсингу.
        response = None
        if wait_response:
            if debug_mode:
                log_debug('BEGIN RESPONSE %s', action_id)

            response = await parse_response(self.reader, action_id, debug_mode)

            # Из Asterisk результат команды может быть отправлен отдельно.
            wait_output = (
                response.get('Response') == 'Follows' and
                'Output' not in response)
            if wait_output:
                output = await parse_output(self.reader, action_id, debug_mode)
                if output:
                    response['Output'] = '\n'.join(output)

            # Когда в ответе указано, что будут дополнительные события по
            # данному, мы должны ождаться всех событий в ответ, отфильтровывая
            # чужеродные.
            wait_events = response.get('EventList') == 'start'
            if wait_events:
                events = await parse_events(self.reader, action_id, debug_mode)
                if events:
                    response['EventList'] = events

            if debug_mode:
                log_debug('END RESPONSE %s', action_id)

        finish_time = time()

        prepare_elapsed = preparing_time - start_time
        execute_elapsed = sending_time - preparing_time
        receive_elapsed = finish_time - sending_time
        total_elapsed = finish_time - start_time

        if total_elapsed > 0.1:
            log_warn(
                'Overtime: %f (prepare=%f, execute=%f, receive=%f). '
                'Action %r (%s)',
                total_elapsed, prepare_elapsed, execute_elapsed,
                receive_elapsed, action_name, action_id)
        else:
            log_info(
                'Time: %f (prepare=%f, execute=%f, receive=%f). '
                'Action %r (%s)',
                total_elapsed, prepare_elapsed, execute_elapsed,
                receive_elapsed, action_name, action_id)

        return response

    async def login(self, username, password):
        """
        Аутентифицирует менеджера в Asterisk, выдает ошибку авторизации
        при неудачном входе.
        """

        if self.is_authenticated:
            await self.logout()

        action = {
            'Action': 'Login',
            'Username': username,
            'Secret': password,
        }

        response = await self.send_action(action)

        if response['Response'] == 'Error':
            raise ManagerAuthError(response['Message'])

        self.is_authenticated = True
        return True

    async def logout(self):
        """
        Отправляет команду выхода из системы.
        """

        if self.is_authenticated:
            action = {'Action': 'Logoff'}
            await self.send_action(action)
            self.is_authenticated = True
        return True


class Listener(BaseManager):
    """
    This is a class for building applications with Asterisk listening.
    """

    def __init__(self, pool_executor=ThreadPoolExecutor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pool_executor = pool_executor
        self.handlers = {}
        self.is_listening = False
        self.skip_events = set()

    def register_event(self, event_name, callback):
        handlers = self.handlers
        handlers.setdefault(event_name, [])
        if callback not in handlers[event_name]:
            handlers[event_name].append(callback)
            return True
        return False

    def unregister_event(self, event_name, callback):
        handlers = self.handlers
        if event_name in handlers:
            callbacks = handlers[event_name]
            if callback in callbacks:
                index = callbacks.index(callback)
                callbacks.pop(index)
                return True
        return False

    async def stop(self):
        """
        Останавливает прослушивание событий.
        """
        self.is_listening = False

    async def start(self):
        """
        Запускает прослушивание событий.
        """

        # Это необходимо для уменьшения кол-ва вызовов функций логгирования
        # внутри циклов.
        debug_mode = logger.level <= logging.DEBUG

        if not self.is_connected:
            await self.connect()

        self.is_listening = True

        handlers = self.handlers
        iscoroutine = asyncio.iscoroutinefunction
        loop = asyncio.get_running_loop()
        run_in_executor = loop.run_in_executor
        pool_executor = self.pool_executor

        while self.is_connected and self.is_listening:
            # log_debug('Wait event...')

            any_event_handlers = handlers.get('*')
            event, event_handlers = await parse_event(
                self.reader, handlers, any_event_handlers,
                self.skip_events, debug_mode)

            if event:
                event_name = event['Event']
                event_priv = event['Privilege']
                if debug_mode:
                    log_debug('END EVENT %s', event_name)
                event_ready_time = time()

                if not event_handlers:
                    event_handlers = []
                if any_event_handlers:
                    event_handlers += any_event_handlers

                for handler in event_handlers:
                    handle_start_time = time()

                    if iscoroutine(handler):
                        await handler(event)
                    else:
                        with pool_executor() as pool:
                            await run_in_executor(pool, handler, event)

                    elapsed = time() - handle_start_time

                    if elapsed > 1:
                        log_warn(
                            'Overtime: %f %r (%s)', elapsed,
                            handler, event_name)
                    elif elapsed > 0.1:
                        log_info(
                            'Overtime: %f %r (%s)', elapsed,
                            handler, event_name)

                elapsed = time() - event_ready_time
                log_info(
                    'Time: handle=%f. Event %r (%s).',
                    elapsed, event_name, event_priv)

        log_info('Listener is stopped.')


class Commander(BaseManager):
    """
    This is a class for building applications with executing Asterisk commands
    and disconnecting from it to reduce the load on the server.
    """

    async def absolute_timeout(self, channel, timeout):
        """Set an absolute timeout on a channel"""

        action = {
            'Action': 'AbsoluteTimeout',
            'Channel': channel,
            'Timeout': timeout,
        }
        response = await self.send_action(action)
        return response

    async def atxfer(self, channel, exten, context):
        """Attended transfer."""

        action = {
            'Action': 'Atxfer',
            'Channel': channel,
            'Exten': exten,
            'Context': context,
        }
        response = await self.send_action(action)
        return response

    async def command(self, command):
        """Execute a command"""

        action = {
            'Action': 'Command',
            'Command': command,
        }
        response = await self.send_action(action)
        return response

    async def dbdel(self, family, key):
        action = {
            'Action': 'DBDel',
            'Family': family,
            'Key': key,
        }
        response = await self.send_action(action)
        return response

    async def dbdeltree(self, family, key):
        action = {
            'Action': 'DBDelTree',
            'Family': family,
            'Key': key,
        }
        response = await self.send_action(action)
        return response

    async def dbget(self, family, key):
        action = {
            'Action': 'DBGet',
            'Family': family,
            'Key': key,
        }
        response = await self.send_action(action)
        return response

    async def dbput(self, family, key, val):
        action = {
            'Action': 'DBPut',
            'Family': family,
            'Key': key,
            'Val': val,
        }
        response = await self.send_action(action)
        return response

    async def extension_state(self, exten, context):
        """Get the state of an extension"""

        action = {
            'Action': 'ExtensionState',
            'Exten': exten,
            'Context': context,
        }
        response = await self.send_action(action)
        return response

    async def hangup(self, channel):
        """Hangup the specified channel"""

        action = {
            'Action': 'Hangup',
            'Channel': channel,
        }
        response = await self.send_action(action)
        return response

    async def iaxregistry(self):
        action = {'Action': 'IAXregistry'}
        response = await self.send_action(action)
        return response

    async def mailbox_count(self, mailbox):
        action = {
            'Action': 'MailboxCount',
            'Mailbox': mailbox,
        }
        response = await self.send_action(action)
        return response

    async def mailbox_status(self, mailbox):
        """Get the status of the specfied mailbox"""

        action = {
            'Action': 'MailboxStatus',
            'Mailbox': mailbox,
        }
        response = await self.send_action(action)
        return response

    async def originate(self, channel, exten, context='', priority='',
                        timeout='', application='', data='', caller_id='',
                        run_async=False, earlymedia='false', account='',
                        variables={}):
        """Originate a call"""

        action = {
            'Action': 'Originate',
            'Channel': channel,
            'Exten': exten,
        }
        if context:
            action['Context'] = context
        if priority:
            action['Priority'] = priority
        if timeout:
            action['Timeout'] = timeout
        if application:
            action['Application'] = application
        if data:
            action['Data'] = data
        if caller_id:
            action['CallerID'] = caller_id
        if run_async:
            action['Async'] = 'yes'
        if earlymedia:
            action['EarlyMedia'] = earlymedia
        if account:
            action['Account'] = account
        if variables:
            action['Variable'] = [f'{k}={v}' for k, v in variables.items()]

        response = await self.send_action(action)
        return response

    async def ping(self):
        """Send a ping action to the manager"""

        action = {'Action': 'Ping'}
        response = await self.send_action(action)
        return response

    async def playdtmf(self, channel, digit):
        """Plays a dtmf digit on the specified channel"""

        action = {
            'Action': 'PlayDTMF',
            'Channel': channel,
            'Digit': digit,
        }
        response = await self.send_action(action)
        return response

    async def redirect(self, channel, exten, priority='1', extra_channel='',
                       context=''):
        """Redirect a channel"""

        action = {
            'Action': 'Redirect',
            'Channel': channel,
            'Exten': exten,
            'Priority': priority,
        }
        if context:
            action['Context'] = context
        if extra_channel:
            action['ExtraChannel'] = extra_channel

        response = await self.send_action(action)
        return response

    async def reload(self, module):
        """ Reloads config for a given module """

        action = {
            'Action': 'Reload',
            'Module': module,
        }
        response = await self.send_action(action)
        return response

    async def sipshowpeer(self, peer):
        action = {
            'Action': 'SIPshowpeer',
            'Peer': peer,
        }
        response = await self.send_action(action)
        return response

    async def sipshowregistry(self):
        action = {'Action': 'SIPShowregistry'}
        response = await self.send_action(action)
        return response

    async def sippeers(self):
        action = {'Action': 'Sippeers'}
        response = await self.send_action(action)
        return response

    async def status(self, channel=''):
        """Get a status message from asterisk"""

        action = {
            'Action': 'Status',
            'Channel': channel,
        }
        response = await self.send_action(action)
        return response
