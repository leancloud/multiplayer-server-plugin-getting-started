from tools.base.codecs.protobuf_v1 import messages_pb2
from tools.base.codecs.protobuf_v1 import generic_collection_pb2
from tools.base.codecs.protobuf_v1 import converter
from tools.base.codecs.protobuf_v1 import common
from google.protobuf.descriptor import FieldDescriptor
from functools import wraps

import copy
import json
import re


def camel_case_to_snake_case(val):
    tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', val)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp).lower()


def snake_case_to_came_case(val):
    tmp = val.split('_')
    return tmp[0] + "".join(map(lambda x: x.capitalize(), tmp[1:]))


def __convert(msg, convert_key_fn):
    if isinstance(msg, dict):
        ret = dict()
        for k, v in msg.items():
            ret[convert_key_fn(
                k)] = __convert(v, convert_key_fn)
        return ret
    elif isinstance(msg, list):
        ret = list()
        for v in msg:
            ret.append(__convert(v, convert_key_fn))
        return ret
    else:
        return msg


def msg_from_camel_case_to_snake_case(msg):
    return __convert(msg, camel_case_to_snake_case)


def msg_from_snake_case_to_camel_case(msg):
    return __convert(msg, snake_case_to_came_case)


def serialize_wrapper(body_field, func):
    @wraps(func)
    def wrapper(self, msg):
        ret = func(self, msg)
        ret = msg_from_camel_case_to_snake_case(ret)
        return converter.dict_to_protobuf(
            messages_pb2.Body, {body_field: ret}, type_callable_map=common.SERIALIZE_TYPE_CALLABLE_MAP)
    return wrapper


def deserialize_wrapper(body_field, func):
    @wraps(func)
    def wrapper(self, body):
        command = messages_pb2.Body()
        command.ParseFromString(body)
        cmd = converter.protobuf_to_dict(
            command, type_callable_map=common.DESERIALIZE_TYPE_CALLABLE_MAP)
        cmd = cmd.get(body_field, {})
        cmd = msg_from_snake_case_to_camel_case(cmd)
        return func(self, cmd)
    return wrapper


class CommandMeta(type):
    def __new__(cm, name, bases, attr_dict):
        body_field = attr_dict['body_field']
        attr_dict['serialize'] = serialize_wrapper(
            body_field, attr_dict['serialize'])
        attr_dict['deserialize'] = deserialize_wrapper(
            body_field, attr_dict['deserialize'])
        return type.__new__(cm, name, bases, attr_dict)


class SessionOpenRequest(metaclass=CommandMeta):
    body_field = "request"

    def serialize(self, msg):
        common.pile_up(msg, ['sessionOpen'])
        return msg

    def deserialize(self, body):
        return common.smash(body, ['sessionOpen'])


class Direct(metaclass=CommandMeta):
    body_field = "direct"

    def serialize(self, msg):
        return msg

    def deserialize(self, body):
        return body


class Event(metaclass=CommandMeta):
    body_field = "events"

    def serialize(self, msg):
        return msg

    def deserialize(self, events):
        if 'events' not in events:
            events['events'] = []
        return events


class Ack(metaclass=CommandMeta):
    body_field = "response"

    def serialize(self, msg):
        common.pile_up(msg, ['ack'])
        return msg

    def deserialize(self, body):
        return common.smash(body, ['ack'])


def parepare_open_visible_in_room_options(msg):
    if 'open' in msg:
        msg['open'] = {'value': msg.get('open', True)}
    if 'visible' in msg:
        msg['visible'] = {'value': msg.get('visible', True)}


def parse_open_visible_in_room_options(msg):
    if 'open' in msg:
        msg['open'] = msg['open'].get('value', False)
    if 'visible' in msg:
        msg['visible'] = msg['visible'].get('value', False)


class CreateRoomRequest(metaclass=CommandMeta):
    body_field = "request"

    def serialize(self, msg):
        parepare_open_visible_in_room_options(msg)
        common.pile_up(msg, ['createRoom', ['createRoom', 'roomOptions']])
        return msg

    def deserialize(self, session):
        msg = common.smash(
            session, [['createRoom', 'roomOptions'], 'createRoom'])
        parse_open_visible_in_room_options(msg)
        return msg


class CreateRoomResponse(metaclass=CommandMeta):
    body_field = "response"

    def serialize(self, msg):
        parepare_open_visible_in_room_options(msg)
        common.pile_up(
            msg, ['createRoom', ['createRoom', 'roomOptions'], 'errorInfo'])
        return msg

    def deserialize(self, session):
        msg = common.smash(
            session, [['createRoom', 'roomOptions'], 'createRoom', 'errorInfo'])
        parse_open_visible_in_room_options(msg)
        return msg


class JoinRoomRequest(metaclass=CommandMeta):
    body_field = "request"

    def serialize(self, msg):
        parepare_open_visible_in_room_options(msg)
        common.pile_up(msg, ['joinRoom', ['joinRoom', 'roomOptions']])
        return msg

    def deserialize(self, req):
        msg = common.smash(req, [['joinRoom', 'roomOptions'], 'joinRoom'])
        parse_open_visible_in_room_options(msg)
        return msg


class JoinRoomResponse(metaclass=CommandMeta):
    body_field = "response"

    def serialize(self, msg):
        parepare_open_visible_in_room_options(msg)
        common.pile_up(
            msg, ['joinRoom', ['joinRoom', 'roomOptions'], 'errorInfo'])
        return msg

    def deserialize(self, res):
        msg = common.smash(
            res, [['joinRoom', 'roomOptions'], 'joinRoom', 'errorInfo'])
        parse_open_visible_in_room_options(msg)
        return msg


class MembersOnlineNotification(metaclass=CommandMeta):
    body_field = "room_notification"

    def serialize(self, msg):
        common.pile_up(msg, ['joinRoom'])
        return msg

    def deserialize(self, noti):
        return common.smash(noti, ['joinRoom'])


class MembersOfflineNotification(metaclass=CommandMeta):
    body_field = "room_notification"

    def serialize(self, msg):
        common.pile_up(msg, ['leftRoom'])
        return msg

    def deserialize(self, req):
        return common.smash(req, ['leftRoom'])


class KickFromRoomRequest(metaclass=CommandMeta):
    body_field = "request"

    def serialize(self, msg):
        common.pile_up(msg, ['kickMember'])
        return msg

    def deserialize(self, req):
        return common.smash(req, ['kickMember'])


class KickFromRoomResponse(metaclass=CommandMeta):
    body_field = "response"

    def serialize(self, msg):
        common.pile_up(msg, ['kickMember'])
        common.pile_up(msg, ['errorInfo'])
        return msg

    def deserialize(self, req):
        return common.smash(req, ['kickMember', 'errorInfo'])


class UpdateRoomRequest(metaclass=CommandMeta):
    body_field = "request"

    def serialize(self, msg):
        common.pile_up(msg, ['updateProperty'])
        return msg

    def deserialize(self, req):
        return common.smash(req, ['updateProperty'])


class UpdateRoomResponse(metaclass=CommandMeta):
    body_field = "response"

    def serialize(self, msg):
        common.pile_up(msg, ['updateProperty', 'errorInfo'])
        return msg

    def deserialize(self, req):
        return common.smash(req, ['updateProperty', 'errorInfo'])


class UpdateRoomNotification(metaclass=CommandMeta):
    body_field = "room_notification"

    def serialize(self, msg):
        common.pile_up(msg, ['updateProperty'])
        return msg

    def deserialize(self, req):
        return common.smash(req, ['updateProperty'])


class UpdateRoomSysPropsRequest(metaclass=CommandMeta):
    body_field = "request"

    def serialize(self, msg):
        sysAttr = msg.get('sysAttr', {})
        if sysAttr:
            if 'open' in sysAttr:
                sysAttr['open'] = {'value': sysAttr.get('open')}
            if 'visible' in sysAttr:
                sysAttr['visible'] = {'value': sysAttr.get('visible')}
            if 'expectMembers' in sysAttr:
                sysAttr['expectMembers'] = json.dumps(
                    sysAttr.get('expectMembers'))
        common.pile_up(msg, ['updateSysProperty'])
        return msg

    def deserialize(self, req):
        req = common.smash(req, ['updateSysProperty'])
        sysAttr = req.get('sysAttr', {})
        if sysAttr:
            if 'open' in sysAttr:
                sysAttr['open'] = sysAttr['open'].get('value', False)
            if 'visible' in sysAttr:
                sysAttr['visible'] = sysAttr['visible'].get('value', False)
            if 'expectMembers' in sysAttr:
                sysAttr['expectMembers'] = json.loads(
                    sysAttr.get('expectMembers'))
        return req


class UpdateRoomSysPropsResponse(metaclass=CommandMeta):
    body_field = "response"

    def serialize(self, msg):
        sysAttr = msg.get('sysAttr', {})
        if sysAttr:
            if 'open' in sysAttr:
                sysAttr['open'] = {'value': sysAttr.get('open')}
            if 'visible' in sysAttr:
                sysAttr['visible'] = {'value': sysAttr.get('visible')}
            if 'expectMembers' in sysAttr:
                sysAttr['expectMembers'] = json.dumps(
                    sysAttr.get('expectMembers'))
        common.pile_up(msg, ['updateSysProperty', 'errorInfo'])
        return msg

    def deserialize(self, req):
        req = common.smash(req, ['updateSysProperty', 'errorInfo'])
        sysAttr = req.get('sysAttr', {})
        if sysAttr:
            if 'open' in sysAttr:
                sysAttr['open'] = sysAttr['open'].get('value', False)
            if 'visible' in sysAttr:
                sysAttr['visible'] = sysAttr['visible'].get('value', False)
            if 'expectMembers' in sysAttr:
                sysAttr['expectMembers'] = json.loads(
                    sysAttr.get('expectMembers'))
        return req


class UpdateRoomSysPropsNotification(metaclass=CommandMeta):
    body_field = "room_notification"

    def serialize(self, msg):
        sysAttr = msg.get('sysAttr', {})
        if sysAttr:
            if 'open' in sysAttr:
                sysAttr['open'] = {'value': sysAttr.get('open')}
            if 'visible' in sysAttr:
                sysAttr['visible'] = {'value': sysAttr.get('visible')}
            if 'expectMembers' in sysAttr:
                sysAttr['expectMembers'] = json.dumps(
                    sysAttr.get('expectMembers'))
        common.pile_up(msg, ['updateSysProperty'])
        return msg

    def deserialize(self, req):
        req = common.smash(req, ['updateSysProperty'])
        sysAttr = req.get('sysAttr', {})
        if sysAttr:
            if 'open' in sysAttr:
                sysAttr['open'] = sysAttr['open'].get('value', False)
            if 'visible' in sysAttr:
                sysAttr['visible'] = sysAttr['visible'].get('value', False)
            if 'expectMembers' in sysAttr:
                sysAttr['expectMembers'] = json.loads(
                    sysAttr.get('expectMembers'))
        return req


class UpdateMasterClientRequest(metaclass=CommandMeta):
    body_field = "request"

    def serialize(self, msg):
        common.pile_up(msg, ['updateMasterClient'])
        return msg

    def deserialize(self, req):
        return common.smash(req, ['updateMasterClient'])


class UpdateMasterClientResponse(metaclass=CommandMeta):
    body_field = "response"

    def serialize(self, msg):
        common.pile_up(msg, ['updateMasterClient', 'errorInfo'])
        return msg

    def deserialize(self, req):
        return common.smash(req, ['updateMasterClient', 'errorInfo'])


class UpdateMasterClientNotification(metaclass=CommandMeta):
    body_field = "room_notification"

    def serialize(self, msg):
        common.pile_up(msg, ['updateMasterClient'])
        return msg

    def deserialize(self, req):
        return common.smash(req, ['updateMasterClient'])


class Request(metaclass=CommandMeta):
    body_field = "request"

    def serialize(self, msg):
        return msg

    def deserialize(self, body):
        return body


class Response(metaclass=CommandMeta):
    body_field = "response"

    def serialize(self, msg):
        common.pile_up(msg, ['errorInfo'])
        return msg

    def deserialize(self, res):
        return common.smash(res, ['errorInfo'])


class JoinLobbyRequest(metaclass=CommandMeta):
    body_field = "request"

    def serialize(self, msg):
        common.pile_up(msg, ['joinLobby'])
        return msg

    def deserialize(self, session):
        return common.smash(session, ['joinLobby'])


class RoomListCommand(metaclass=CommandMeta):
    body_field = "room_list"

    def serialize(self, msg):
        msg['list'] = list(map(
            lambda x: parepare_open_visible_in_room_options(x) or x, msg['list']))
        return msg

    def deserialize(self, body):
        body['list'] = list(
            map(lambda x: parse_open_visible_in_room_options(x) or x, body['list']))
        return body


class Statistic(metaclass=CommandMeta):
    body_field = "statistic"

    def serialize(self, msg):
        return msg

    def deserialize(self, body):
        return body


class Error(metaclass=CommandMeta):
    body_field = "error"

    def serialize(self, msg):
        common.pile_up(msg, ['errorInfo'])
        return msg

    def deserialize(self, body):
        return common.smash(body, ['errorInfo'])


CLIENT_TO_SERVER_ROUTE = {
    'session' + 'open': SessionOpenRequest(),
    'conv' + 'start': CreateRoomRequest(),
    'conv' + 'add': JoinRoomRequest(),
    'conv' + 'add-random': JoinRoomRequest(),
    'conv' + 'match-random': JoinRoomRequest(),
    'conv' + 'kick': KickFromRoomRequest(),
    'conv' + 'update': UpdateRoomRequest(),
    'conv' + 'update-player-prop': UpdateRoomRequest(),
    'conv' + 'update-system-property': UpdateRoomSysPropsRequest(),
    'conv' + 'update-master-client': UpdateMasterClientRequest(),
    'direct': Direct(),
    'events': Event(),
    'ack': Ack(),
    'statistic': Statistic(),
    'lobby' + 'add': JoinLobbyRequest(),
}

SERVER_TO_CLIENT_ROUTE = {
    'conv' + 'started': CreateRoomResponse(),
    'conv' + 'added': JoinRoomResponse(),
    'conv' + 'random-added': JoinRoomResponse(),
    'conv' + 'random-matched': JoinRoomResponse(),
    'conv' + 'members-joined': MembersOnlineNotification(),
    'conv' + 'members-online': MembersOnlineNotification(),
    'conv' + 'members-offline': MembersOfflineNotification(),
    'conv' + 'members-left': MembersOfflineNotification(),
    'conv' + 'kicked': KickFromRoomResponse(),
    'conv' + 'kicked-notice': MembersOfflineNotification(),
    'conv' + 'updated': UpdateRoomResponse(),
    'conv' + 'updated-notify': UpdateRoomNotification(),
    'conv' + 'player-prop-updated': UpdateRoomResponse(),
    'conv' + 'player-props': UpdateRoomNotification(),
    'conv' + 'system-property-updated': UpdateRoomSysPropsResponse(),
    'conv' + 'system-property-updated-notify': UpdateRoomSysPropsNotification(),
    'conv' + 'master-client-updated': UpdateMasterClientResponse(),
    'conv' + 'master-client-changed': UpdateMasterClientNotification(),
    'direct': Direct(),
    'events': Event(),
    'ack': Ack(),
    'statistic': Statistic(),
    'lobby' + 'room-list': RoomListCommand(),
    'error': Error(),
}


def get_client_to_server_codec(cmd, op):
    k = cmd if op is None else cmd + op
    return CLIENT_TO_SERVER_ROUTE.get(k, Request())


def get_server_to_client_codec(cmd, op):
    k = cmd if op is None else cmd + op
    return SERVER_TO_CLIENT_ROUTE.get(k, Response())


def serialize_to_server_msg(msg):
    cmd = msg.get('cmd')
    op = msg.get('op')
    command = common.serialize_common_fields(msg)

    codec = get_client_to_server_codec(cmd, op)
    body = codec.serialize(msg)

    if body is not None:
        command.body = body.SerializeToString()
    return command.SerializeToString()


def deserialize_to_server_msg(msg):
    command = messages_pb2.Command()
    command.ParseFromString(msg)
    cmd, op = common.deserialize_common_fields(command)

    codec = get_client_to_server_codec(cmd, op)
    msg = codec.deserialize(command.body)

    msg['cmd'] = cmd
    if op:
        msg['op'] = op
    return msg


def serialize_to_client_msg(msg):
    cmd = msg.get('cmd')
    op = msg.get('op')
    command = common.serialize_common_fields(msg)

    codec = get_server_to_client_codec(cmd, op)
    body = codec.serialize(msg)

    if body is not None:
        command.body = body.SerializeToString()
    return command.SerializeToString()


def deserialize_to_client_msg(msg):
    command = messages_pb2.Command()
    command.ParseFromString(msg)
    cmd, op = common.deserialize_common_fields(command)

    codec = get_server_to_client_codec(cmd, op)
    msg = codec.deserialize(command.body)

    msg['cmd'] = cmd
    if op:
        msg['op'] = op
    return msg


class ClientToServerProtobufSerializer:
    def serialize(self, msg):
        msg = copy.deepcopy(msg)
        return serialize_to_server_msg(msg)

    def deserialize(self, msg):
        return deserialize_to_client_msg(msg)


class ServerToClientProtobufSerializer:
    def serialize(self, msg):
        msg = copy.deepcopy(msg)
        return serialize_to_client_msg(msg)

    def deserialize(self, msg):
        return deserialize_to_server_msg(msg)
