#
# Copyright (c) 2022, Grigoriy Kramarenko <root@rosix.ru>
# All rights reserved.
# This file is distributed under BSD 3-Clause License.
#

"""
Data models of Asterisk:
https://wiki.asterisk.org/wiki/display/AST/Asterisk+16+REST+Data+Models

The models "App" and "Event" was appened.

"""

import logging
from pprint import pformat
from time import time

from ..utils import parse_datetime
from .exceptions import Error404

logger = logging.getLogger(__name__)
log_debug = logger.debug


class SubscriptionSet(set):

    def __init__(self, client):
        self.client = client

    def __str__(self):
        return self.human_string.replace('\n', '; ')

    @property
    def human_string(self):
        return '\n'.join([x.human_string for x in self.get_handler_set()])

    def get_handler_set(self):
        for handlers in self.client._handlers.values():
            for hid in self:
                if hid in handlers:
                    yield handlers[hid]


class Subscriber:
    def __init__(self, client):
        self.client = client
        self.subscriptions = SubscriptionSet(client)

    def __del__(self):
        self.unsubscribe_all()

    def subscribe(self, event_name, handle, **kwargs):
        unsubscribe, hid = self.client.subscribe(event_name, handle, **kwargs)
        self.subscriptions.add(hid)
        return unsubscribe

    def unsubscribe(self, hids):
        if not hids:
            raise ValueError(
                'Parameter `hids` must be non blank string or set of strings.')
        hids = self.client.unsubscribe(hids)
        self.subscriptions.difference_update(hids)

    def unsubscribe_all(self):
        hids = self.subscriptions
        if hids:
            self.client.unsubscribe(hids)
            hids.clear()

    def unsubscribe_events(self, *names):
        all_hids = self.subscriptions
        all_handlers = self.client._handlers

        hids = set()
        for name in names:
            handlers = all_handlers.get(name, {})
            for hid in handlers.keys():
                if hid in all_hids:
                    hids.add(hid)
        if hids:
            self.unsubscribe(hids)


class App(Subscriber):
    name = None

    def __init__(self, client, name=''):
        super().__init__(client)
        if name:
            self.name = name
        if not self.name:
            raise ValueError('Specify a name for your subclass of App.')
        log_debug('App %s was initialized.', self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<App %s>' % self.name

    def subscribe(self, event_name, handle, **kwargs):
        kwargs['app'] = self
        return super().subscribe(event_name, handle, **kwargs)

    async def on_install(self):
        """
        The method for overriding the application installation.
        """
        pass

    async def on_uninstall(self):
        """
        The method for overriding the application uninstallation.
        """
        pass

    async def on_connect(self):
        """
        The method for overriding the behavior when establishing a connection.
        """
        pass

    async def on_disconnect(self):
        """
        The method for overriding the behavior when a connection is broken.
        """
        pass

    async def handle_stasis_start(self, event, **kwargs):
        """
        A method for overriding the channel's entry into the application.
        """
        pass

    async def handle_stasis_end(self, event, **kwargs):
        """
        A method for overriding the channel's eleave from the application.
        """
        pass

    async def asterisk_details(self):
        """
        Get details of an application.
        """

        path = f'/applications/{self.name}'
        result = await self.client.get(path)
        return result

    async def asterisk_subscribe(self, source):
        """
        Subscribe an application to a event source. Returns the state of the
        application after the subscriptions have changed.

        eventSource: URI for event source (channel:{channelId},
        bridge:{bridgeId}, endpoint:{tech}[/{resource}],
        deviceState:{deviceName})

        """

        if not isinstance(source, str):
            source = ','.join(source)
        params = {'eventSource': source}
        path = f'/applications/{self.name}/subscription'
        result = await self.client.post(path, params=params)
        return result

    async def asterisk_unsubscribe(self, source):
        """
        Unsubscribe an application from an event source. Returns the state of
        the application after the subscriptions have changed.
        """

        if not isinstance(source, str):
            source = ','.join(source)
        params = {'eventSource': source}
        path = f'/applications/{self.name}/subscription'
        result = await self.client.delete(path, params=params)
        return result

    async def asterisk_filter(self, filter_data):
        """
        Filter application events types. Allowed and/or disallowed event type
        filtering can be done. The body (parameter) should specify
        a JSON key/value object that describes the type of event filtering
        needed. One, or both of the following keys can be designated:

        "allowed" - Specifies an allowed list of event types
        "disallowed" - Specifies a disallowed list of event types

        Further, each of those key's value should be a JSON array that holds
        zero, or more JSON key/value objects. Each of these objects must
        contain the following key with an associated value:

        "type" - The type name of the event to filter

        The value must be the string name (case sensitive) of the event type
        that needs filtering. For example:

        { "allowed": [ { "type": "StasisStart" }, { "type": "StasisEnd" } ] }

        As this specifies only an allowed list, then only those two event type
        messages are sent to the application. No other event messages are sent.

        The following rules apply:

            * If the body is empty, both the allowed and disallowed filters are
              set empty.
            * If both list types are given then both are set to their
              respective values (note, specifying an empty array for a given
              type sets that type to empty).
            * If only one list type is given then only that type is set. The
              other type is not updated.
            * An empty "allowed" list means all events are allowed.
            * An empty "disallowed" list means no events are disallowed.
            * Disallowed events take precedence over allowed events if the
              event type is specified in both lists.
        """

        data = {'filter': filter_data}
        path = f'/applications/{self.name}/eventFilter'
        result = await self.client.put(path, json=data)
        return result


class DummyApp(App):
    """
    The dummy application can be used to call subscribers before connecting
    them to bridge.
    """
    name = 'dummy'


class Event(dict):

    def __init__(self, client, data):
        self.client = client
        name = data.get('type', 'unknown')
        if name == 'ChannelUserevent':
            name = data.get('eventname')
        self.name = name
        self.update(data)

    def __str__(self):
        return self.human_string

    def __repr__(self):
        return f'<Event {self.human_string}>'

    @staticmethod
    def pformat(event_data):
        name = event_data['type']
        app = event_data.get('application', '???')
        lines = pformat(event_data, indent=1).split('\n')
        lines[0] = f' {lines[0][1:]}'
        lines = '\n'.join([f'   {line}' for line in lines])
        return f'Event {name} in {app} {{\n{lines}'

    @property
    def human_string(self):
        name = self.name
        parts = [f"[{self['application']}]", name]

        if name == 'Dial':
            parts.append(self.get('dialstatus'))
            parts.append(self.get('dialstring'))
            peer = self.get('peer')
            if peer:
                parts.append(peer['name'])
                parts.append(f"[{peer['id']}]")
                parts.append(f"caller={peer['caller']}")

        if 'channel' in self:
            channel = self['channel']
            parts.append('Channel')
            parts.append(channel['name'])
            parts.append(f"[{channel['id']}]")

        if 'bridge' in self:
            bridge = self['bridge']
            parts.append('Bridge')
            parts.append(bridge['id'])
            parts.append(bridge['channels'])

        if 'device_state' in self:
            device_state = self['device_state']
            parts.append(device_state['name'])
            parts.append(device_state['state'])

        if name == 'ChannelVarset':
            variable = self['variable']
            value = self['value']
            parts.append(f'{variable}={value}')

        if name == 'StasisStart':
            params = channel['dialplan']['app_data']
            parts.append(f'Stasis({params})')

        if self['type'] == 'ChannelUserevent':
            userevent = self['userevent']
            params = ','.join([
                f'{k}={v}' for k, v in userevent.items() if k != 'eventname'])
            parts.append(f'Data({params})')

        return ' '.join(map(str, [x for x in parts if x]))

    @property
    def human_multistring(self):
        return self.pformat(self)

    @property
    def timestamp(self):
        if 'timestamp' in self:
            return parse_datetime(self['timestamp'])


class DetailsMixin:

    async def exists(self):
        """
        Checking for existence in Asterisk.
        """
        path = f'{self.model_path}/{self.id}'
        try:
            await self.client.get(path)
        except Error404:
            return False
        return True

    async def details(self, update=True):
        """
        Returns information from Asterisk. May be update data in instance
        (by default).
        """
        path = f'{self.model_path}/{self.id}'
        result = await self.client.get(path)
        if update:
            self.data.update(result)
        return result


class Model(Subscriber):
    id_field = 'id'
    model_path = None

    def __init__(self, client, data=None):
        super().__init__(client)
        self.data = {} if data is None else data

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_id_from_data(self, data):
        return data.get(self.id_field)

    @property
    def id(self):
        return self.get_id_from_data(self.data)

    def __getitem__(self, name):
        return self.data[name]

    def __getattr__(self, name):
        return self.data.get(name)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def subscribe(self, event_name, handle, **kwargs):
        kwargs['object'] = self
        return super().subscribe(event_name, handle, **kwargs)


class Bridge(Model, DetailsMixin):
    model_path = '/bridges'

    @classmethod
    async def get_bridges(cls, client, as_objects=True):
        """
        List all active bridges in Asterisk.
        """
        return await client.get_objects(cls, as_objects=as_objects)

    async def create(self, id=None, types=None, name=None):
        params = {}
        if types is not None:
            if not isinstance(types, str):
                types = ','.join(types)
            params['type'] = types
        if name is not None:
            params['name'] = name
        if id is not None:
            params['bridgeId'] = id
        path = self.model_path
        result = await self.client.post(path, params=params)
        self.data.update(result)
        return result

    async def update(self, types=None, name=None):
        params = {}
        if types is not None:
            if not isinstance(types, str):
                types = ','.join(types)
            params['type'] = types
        if name is not None:
            params['name'] = name
        path = f'{self.model_path}/{self.id}'
        result = await self.client.post(path, params=params)
        self.data.update(result)
        return result

    async def save(self):
        types = self.data.get('type')
        name = self.data.get('name')
        return await self.update(self, types=types, name=name)

    async def destroy(self):
        path = f'{self.model_path}/{self.id}'
        try:
            return await self.client.delete(path)
        finally:
            self.unsubscribe_all()

    async def add_channels(self, *channel_ids, role=None, absorb_dtmf=False,
                           mute=False):
        params = {
            'channel': ','.join(channel_ids),
        }
        if role is not None:
            params['role'] = role
        if absorb_dtmf:
            params['absorbDTMF'] = 'true'
        if mute:
            params['mute'] = 'true'
        path = f'{self.model_path}/{self.id}/addChannel'
        result = await self.client.post(path, params=params)
        return result

    async def remove_channels(self, *channel_ids):
        params = {
            'channel': ','.join(channel_ids),
        }
        path = f'{self.model_path}/{self.id}/removeChannel'
        result = await self.client.post(path, params=params)
        return result

    async def start_moh(self, moh_class='default'):
        """
        Play music on hold to a bridge or change the MOH class that is playing.
        """
        params = {
            'mohClass': moh_class,
        }
        path = f'{self.model_path}/{self.id}/moh'
        result = await self.client.post(path, params=params)
        return result

    async def stop_moh(self):
        path = f'{self.model_path}/{self.id}/moh'
        result = await self.client.delete(path)
        return result

    async def play(self, media, **extra):
        """
        Start playback of media on a bridge. The media URI may be any of a
        number of URI's. Currently sound:, recording:, number:, digits:,
        characters:, and tone: URI's are supported.

        This operation creates a playback resource that can be used to control
        the playback of media (pause, rewind, fast forward, etc.)
        """

        params = {'media': media}

        if extra:
            params.update(extra)

        path = f'{self.model_path}/{self.id}/play'
        result = await self.client.post(path, params=params)
        playback = Playback(self.client, result)
        return playback

    async def record(self, name, format='wav', max_duration_seconds=None,
                     max_silence_seconds=None, if_exists=None, beep=False,
                     terminate_on=None):
        """
        Start a recording. This records the mixed audio from all channels
        participating in this bridge.
        """

        params = {'name': name, 'format': format}

        if max_duration_seconds is not None and max_duration_seconds >= 0:
            params['maxDurationSeconds'] = max_duration_seconds

        if max_silence_seconds is not None and max_silence_seconds >= 0:
            params['maxSilenceSeconds'] = max_silence_seconds

        if if_exists is not None:
            params['ifExists'] = if_exists

        if beep:
            params['beep'] = 'true'

        if terminate_on is not None:
            params['terminateOn'] = terminate_on

        path = f'{self.model_path}/{self.id}/record'
        result = await self.client.post(path, params=params)
        result['bridge_id'] = self.id
        record = LiveRecording(self.client, result)
        return record

    async def set_video_source(self, channel_id):
        """
        Set a channel as the video source in a multi-party mixing bridge.

        This operation has no effect on bridges with two or fewer participants.
        """
        path = f'{self.model_path}/{self.id}/videoSource/{channel_id}'
        result = await self.client.post(path)
        return result

    async def clear_video_source(self):
        """
        Removes any explicit video source in a multi-party mixing bridge.

        This operation has no effect on bridges with two or fewer participants.
        When no explicit video source is set, talk detection will be used to
        determine the active video stream.
        """
        path = f'{self.model_path}/{self.id}/videoSource'
        result = await self.client.delete(path)
        return result


class Channel(Model, DetailsMixin):
    model_path = '/channels'

    dtmf_sequence = ''
    dtmf_sequence_time = 0

    def __str__(self):
        if self.name:
            return self.name
        return f'NEW_CHANNEL:{self.id}'

    def __repr__(self):
        return f'<Channel {self.name} {self.state} ({self.id})>'

    @property
    def created(self):
        if 'creationtime' in self.data:
            return parse_datetime(self.data['creationtime'])

    @classmethod
    async def make_external_media(cls, client, app, external_host,
                                  audio_format, channel_id=None,
                                  variables=None, **extra):
        """
        Start an External Media session. Create a channel to an External Media
        source/sink.
        """

        params = {
            'app': app,
            'external_host': external_host,
            'format': audio_format,
        }

        if channel_id is not None:
            params['channelId'] = channel_id

        extra = {k: v for k, v in extra.items() if v is not None}
        if extra:
            params.update(extra)

        if variables is not None:
            data = {'variables': variables}
        else:
            data = None

        path = f'{cls.model_path}/externalMedia'
        result = await client.post(path, params=params, json=data)
        channel = cls(client, result)
        return channel

    @classmethod
    async def get_channels(cls, client, as_objects=True):
        """
        List all active channels in Asterisk.
        """
        return await client.get_objects(cls, as_objects=as_objects)

    async def rtp_statistics(self):
        """
        RTP stats on a channel.
        """
        path = f'{self.model_path}/{self.id}/rtp_statistics'
        result = await self.client.get(path)
        return result

    async def answer(self):
        path = f'{self.model_path}/{self.id}/answer'
        result = await self.client.post(path)
        return result

    async def hangup(self):
        path = f'{self.model_path}/{self.id}'
        result = await self.client.delete(path)
        return result

    async def continue_dialplan(self, context=None, extension=None,
                                priority=None, label=None):
        """
        Exit application; continue execution in the dialplan.
        """
        params = {}
        if context is not None:
            params['context'] = context
        if extension is not None:
            params['extension'] = extension
        if priority is not None:
            params['priority'] = int(priority)
        # The label to continue to - will supersede 'priority' if both
        # are provided.
        if label is not None:
            params['label'] = label
        path = f'{self.model_path}/{self.id}/continue'
        result = await self.client.post(path, params=params)
        return result

    async def destroy(self):
        try:
            return await self.hangup()
        finally:
            self.unsubscribe_all()

    async def originate(self, endpoint, app_args=None, caller_id=None,
                        channel_id=None, other_channel_id=None, variables=None,
                        **extra):
        """
        Create a new channel (originate). The new channel is created
        immediately and a snapshot of it returned. If a Stasis application
        is provided it will be automatically subscribed to the originated
        channel for further events and updates.
        """

        params = {'endpoint': endpoint}
        if app_args is not None:
            if not isinstance(app_args, str):
                app_args = ','.join(map(str, app_args))
            params['appArgs'] = app_args
        if caller_id is not None:
            params['callerId'] = caller_id

        _id = self.id
        if channel_id is not None:
            params['channelId'] = channel_id
        elif _id is not None:
            params['channelId'] = _id

        if other_channel_id is not None:
            params['otherChannelId'] = other_channel_id

        extra = {k: v for k, v in extra.items() if v is not None}
        if extra:
            params.update(extra)

        if variables is not None:
            data = {'variables': variables}
        else:
            data = None

        path = self.model_path
        result = await self.client.post(path, params=params, json=data)
        self.data.update(result)
        return result

    async def create(self, endpoint, app, app_args=None, channel_id=None,
                     other_channel_id=None, variables=None, **extra):
        """
        Create channel.
        """

        params = {'endpoint': endpoint, 'app': app}
        if app_args is not None:
            if not isinstance(app_args, str):
                app_args = ','.join(map(str, app_args))
            params['appArgs'] = app_args

        _id = self.id
        if channel_id is not None:
            params['channelId'] = channel_id
        elif _id is not None:
            params['channelId'] = _id

        if other_channel_id is not None:
            params['otherChannelId'] = other_channel_id

        extra = {k: v for k, v in extra.items() if v is not None}
        if extra:
            params.update(extra)

        if variables is not None:
            data = {'variables': variables}
        else:
            data = None

        path = f'{self.model_path}/create'
        result = await self.client.post(path, params=params, json=data)
        self.data.update(result)
        return result

    async def dial(self, caller, timeout=None):
        """
        Dial a created channel.
        """

        params = {'caller': caller}
        if timeout is not None:
            params['timeout'] = timeout

        path = f'{self.model_path}/{self.id}/dial'
        result = await self.client.post(path, params=params)
        return result

    async def hold(self):
        path = f'{self.model_path}/{self.id}/hold'
        result = await self.client.post(path)
        return result

    async def unhold(self):
        path = f'{self.model_path}/{self.id}/hold'
        result = await self.client.delete(path)
        return result

    async def mute(self):
        path = f'{self.model_path}/{self.id}/mute'
        result = await self.client.post(path)
        return result

    async def unmute(self):
        path = f'{self.model_path}/{self.id}/mute'
        result = await self.client.delete(path)
        return result

    async def start_moh(self, moh_class='default'):
        """
        Play music on hold to a channel. Using media operations such as /play
        on a channel playing MOH in this manner will suspend MOH without
        resuming automatically.
        If continuing music on hold is desired, the stasis application must
        reinitiate music on hold.
        """
        params = {
            'mohClass': moh_class,
        }
        path = f'{self.model_path}/{self.id}/moh'
        result = await self.client.post(path, params=params)
        return result

    async def stop_moh(self):
        path = f'{self.model_path}/{self.id}/moh'
        result = await self.client.delete(path)
        return result

    async def get_variable(self, name):
        path = f'{self.model_path}/{self.id}/variable'
        params = {'variable': name}
        result = await self.client.get(path, params=params)
        return result.get('value')

    async def set_variable(self, name, value):
        path = f'{self.model_path}/{self.id}/variable'
        params = {
            'variable': name,
            'value': str(value),
        }
        result = await self.client.post(path, params=params)
        return result

    async def record(self, name, format='wav', max_duration_seconds=None,
                     max_silence_seconds=None, if_exists=None, beep=False,
                     terminate_on=None):
        """
        Start a recording. Record audio from a channel. Note that this will
        not capture audio sent to the channel. The bridge itself has a record
        feature if that's what you want.
        """

        params = {'name': name, 'format': format}

        if max_duration_seconds is not None and max_duration_seconds >= 0:
            params['maxDurationSeconds'] = max_duration_seconds

        if max_silence_seconds is not None and max_silence_seconds >= 0:
            params['maxSilenceSeconds'] = max_silence_seconds

        if if_exists is not None:
            params['ifExists'] = if_exists

        if beep:
            params['beep'] = 'true'

        if terminate_on is not None:
            params['terminateOn'] = terminate_on

        path = f'{self.model_path}/{self.id}/record'
        result = await self.client.post(path, params=params)
        result['channel_id'] = self.id
        record = LiveRecording(self.client, result)
        return record

    async def snoop(self, app, app_args=None, spy=None, whisper=None,
                    snoop_id=None):
        """
        Start snooping. Snoop (spy/whisper) on a specific channel.
        """

        params = {'app': app}

        if app_args:
            if not isinstance(app_args, str):
                app_args = ','.join(map(str, app_args))
            params['appArgs'] = app_args
        if spy is not None:
            assert spy in ('none', 'both', 'out', 'in')
            params['spy'] = spy
        if whisper is not None:
            assert whisper in ('none', 'both', 'out', 'in')
            params['whisper'] = whisper
        if snoop_id is not None:
            params['snoopId'] = snoop_id

        path = f'{self.model_path}/{self.id}/snoop'
        result = await self.client.post(path, params=params)
        channel = Channel(self.client, result)
        return channel

    async def play(self, media, **extra):
        """
        Start playback of media. The media URI may be any of a number of URI's.
        Currently sound:, recording:, number:, digits:, characters:,
        and tone: URI's are supported.

        This operation creates a playback resource that can be used to control
        the playback of media (pause, rewind, fast forward, etc.)
        """

        params = {'media': media}

        if extra:
            params.update(extra)

        path = f'{self.model_path}/{self.id}/play'
        result = await self.client.post(path, params=params)
        playback = Playback(self.client, result)
        return playback

    async def move(self, app, app_args=None):
        """
        Move the channel from one Stasis application to another.
        """

        params = {'app': str(app)}
        if app_args:
            if not isinstance(app_args, str):
                app_args = ','.join(map(str, app_args))
            params['appArgs'] = app_args

        path = f'{self.model_path}/{self.id}/move'
        result = await self.client.post(path, params=params)
        return result

    async def redirect(self, endpoint):
        """
        Redirect the channel to a different location.
        """

        params = {'endpoint': endpoint}
        path = f'{self.model_path}/{self.id}/redirect'
        result = await self.client.post(path, params=params)
        return result

    async def start_ring(self):
        """
        Indicate ringing to a channel.
        """

        path = f'{self.model_path}/{self.id}/ring'
        result = await self.client.post(path)
        return result

    async def stop_ring(self):
        """
        Stop ringing indication on a channel if locally generated.
        """

        path = f'{self.model_path}/{self.id}/ring'
        result = await self.client.delete(path)
        return result

    async def start_silence(self):
        """
        Play silence to a channel. Using media operations such as /play on a
        channel playing silence in this manner will suspend silence without
        resuming automatically.
        """

        path = f'{self.model_path}/{self.id}/silence'
        result = await self.client.post(path)
        return result

    async def stop_silence(self):
        """
        Stop playing silence to a channel.
        """

        path = f'{self.model_path}/{self.id}/silence'
        result = await self.client.delete(path)
        return result

    async def send_dtmf(self, dtmf, before=None, between=None, duration=None,
                        after=None):
        """
        Send provided DTMF to a given channel.
        """

        # dtmf: string - DTMF To send.
        params = {'dtmf': str(dtmf)}

        # before: int - Amount of time to wait before DTMF digits
        # (specified in milliseconds) start.
        if before is not None:
            params['before'] = int(before)
        # between: int - Amount of time in between DTMF digits
        # (specified in milliseconds). Default: 100
        if between is not None:
            params['between'] = int(between)
        # duration: int - Length of each DTMF digit
        # (specified in milliseconds). Default: 100
        if duration is not None:
            params['duration'] = int(duration)
        # after: int - Amount of time to wait after DTMF digits
        # (specified in milliseconds) end.
        if after is not None:
            params['after'] = int(after)

        path = f'{self.model_path}/{self.id}/dtmf'
        result = await self.client.post(path, params=params)
        return result

    def clear_dtmf_sequence(self):
        self.dtmf_sequence = ''

    def add_to_dtmf_sequence(self, dtmf, autoclear_timeout=5):
        dtmf_sequence_time = self.dtmf_sequence_time
        now = time()
        # Clearing the outdated.
        if autoclear_timeout and dtmf_sequence_time \
                and dtmf_sequence_time < (now - autoclear_timeout):
            self.dtmf_sequence = ''
        self.dtmf_sequence += dtmf
        self.dtmf_sequence_time = now
        return self.dtmf_sequence


class DeviceState(Model, DetailsMixin):
    id_field = 'name'
    model_path = '/deviceStates'

    @property
    def state(self):
        return self.data.get('state')

    @classmethod
    async def get_device_states(cls, client, as_objects=True):
        """
        List all ARI controlled device states.
        """
        return await client.get_objects(cls, as_objects=as_objects)

    async def update(self, new_state):
        """
        Change the state of a device controlled by ARI.
        (Note - implicitly creates the device state).
        """

        assert new_state in ('NOT_INUSE', 'INUSE', 'BUSY', 'INVALID',
                             'UNAVAILABLE', 'RINGING', 'RINGINUSE', 'ONHOLD')

        params = {'deviceState': new_state}
        path = f'{self.model_path}/{self.id}'
        result = await self.client.put(path, params=params)
        self.data['state'] = new_state
        return result

    async def save(self):
        new_state = self.state or 'NOT_INUSE'
        return await self.update(new_state)

    async def destroy(self):
        """
        Destroy a device-state controlled by ARI.
        """
        path = f'{self.model_path}/{self.id}'
        result = await self.client.delete(path)
        return result


class Endpoint(Model, DetailsMixin):
    id_field = ('technology', 'resource')
    model_path = '/endpoints'

    def get_id_from_data(self, data):
        technology = data.get('technology')
        if technology is None:
            return
        resource = data.get('resource')
        if resource is None:
            return
        return '%s/%s' % (technology, resource)

    @property
    def technology(self):
        return self.data.get('technology')

    @property
    def resource(self):
        return self.data.get('resource')

    @property
    def state(self):
        return self.data.get('state')

    @property
    def channel_ids(self):
        return self.data.get('channel_ids')

    @classmethod
    async def get_endpoints(cls, client, tech=None, as_objects=True):
        """
        List all endpoints.
        """
        if tech:
            path = f'{cls.model_path}/{tech}'
        else:
            path = cls.model_path
        return await client.get_objects(cls, as_objects=as_objects, path=path)

    async def send_message(self, from_endpoint, body, variables=None):
        """
        Send a message to some endpoint in a technology.
        """

        # The endpoint resource or technology specific identity to send this
        # message from. Valid resources are sip, pjsip, and xmpp.
        params = {'from': from_endpoint, 'body': body}

        if variables is not None:
            data = {'variables': variables}
        else:
            data = None

        path = f'{self.model_path}/{self.id}/sendMessage'
        result = await self.client.put(path, params=params, json=data)
        return result


class LiveRecording(Model, DetailsMixin):
    id_field = 'name'
    model_path = '/recordings/live'

    def __str__(self):
        return str(self.name)

    def get_filename(self, data=None):
        if data is None:
            data = self.data
        name = data.get('name')
        ext = data.get('format')
        return f'{name}.{ext}'

    async def stop(self):
        """
        Stop a live recording and store it.
        """

        path = f'{self.model_path}/{self.id}/stop'
        await self.client.post(path)

        data = {
            'name': self.name,
            'format': self.format,
        }
        return StoredRecording(self.client, data)

    async def pause(self):
        """
        Pause a live recording. Pausing a recording suspends silence detection,
        which will be restarted when the recording is unpaused. Paused time is
        not included in the accounting for maxDurationSeconds.
        """

        path = f'{self.model_path}/{self.id}/pause'
        result = await self.client.post(path)
        return result

    async def unpause(self):
        """
        Unpause a live recording.
        """

        path = f'{self.model_path}/{self.id}/pause'
        result = await self.client.delete(path)
        return result

    async def mute(self):
        """
        Mute a live recording. Muting a recording suspends silence detection,
        which will be restarted when the recording is unmuted.
        """

        path = f'{self.model_path}/{self.id}/mute'
        result = await self.client.post(path)
        return result

    async def unmute(self):
        """
        Unmute a live recording.
        """

        path = f'{self.model_path}/{self.id}/mute'
        result = await self.client.delete(path)
        return result


class Mailbox(Model, DetailsMixin):
    id_field = 'name'
    model_path = '/mailboxes'

    @classmethod
    async def get_mailboxes(cls, client, as_objects=True):
        """
        List all mailboxes.
        """
        return await client.get_objects(cls, as_objects=as_objects)

    async def update(self, old, new):
        """
        Change the state of a mailbox. (Note - implicitly creates the mailbox).
        """

        params = {
            'oldMessages': int(old),
            'newMessages': int(new),
        }

        path = f'{self.model_path}/{self.id}'
        result = await self.client.put(path, params=params)
        return result

    async def delete(self):
        """
        Destroy a mailbox.
        """

        path = f'{self.model_path}/{self.id}'
        result = await self.client.delete(path)
        return result


class Playback(Model, DetailsMixin):
    model_path = '/playbacks'

    async def control(self, operation):
        """
        Control a playback.
        """

        assert operation in (
            'restart', 'pause', 'unpause', 'reverse', 'forward')
        params = {'operation': operation}

        path = f'{self.model_path}/{self.id}/control'
        result = await self.client.post(path, params=params)
        return result

    async def delete(self):
        """
        Stop a playback.
        """

        path = f'{self.model_path}/{self.id}'
        result = await self.client.delete(path)
        return result


class Sound(Model, DetailsMixin):
    model_path = '/sounds'

    @classmethod
    async def get_sounds(cls, client, as_objects=True):
        """
        List all sounds.
        """
        return await client.get_objects(cls, as_objects=as_objects)


class StoredRecording(Model, DetailsMixin):
    id_field = 'name'
    model_path = '/recordings/stored'

    @classmethod
    async def get_recordings(cls, client, as_objects=True):
        """
        List recordings that are complete.
        """
        return await client.get_objects(cls, as_objects=as_objects)

    async def delete(self):
        """
        Delete a stored recording.
        """

        path = f'{self.model_path}/{self.id}'
        result = await self.client.delete(path)
        return result

    async def get_file(self):
        """
        Get the file associated with the stored recording.
        """

        path = f'{self.model_path}/{self.id}/file'
        result = await self.client.get(path)
        return result

    async def copy(self, new_name):
        """
        Copy a stored recording.
        """
        params = {'destinationRecordingName': new_name}

        path = f'{self.model_path}/{self.id}/copy'
        result = await self.client.post(path, params=params)
        return result
