"""
Build command or parse command
"""
import time
import json
import hmac
import hashlib
import colorama
from functools import wraps

from tools.base import matcher
from tools.base import util
from tools.base import config

LOG = util.get_logger('commands')


def sign(sign_msg, k):
    return hmac.new(k.encode('utf-8'),
                    sign_msg.encode('utf-8'),
                    hashlib.sha256).digest().hex()


def add_sign(cmd_msg, convid=None, action=None, peerids=None):
    peerid = cmd_msg['peerId']
    ts_millis = int(round(time.time() * 1000))
    nonce = cmd_msg.get('nonce', util.generate_id())
    peerid = peerid if convid is None else ':'.join([peerid, convid])
    peerids = '' if peerids is None else ':'.join(sorted(peerids))
    sign_msg = ':'.join(
        ["play", config.APP_ID, peerid, peerids, str(ts_millis), nonce])
    sign_msg = sign_msg if action is None else ':'.join([sign_msg, action])
    cmd_msg['t'] = ts_millis
    cmd_msg['n'] = nonce
    cmd_msg['s'] = sign(sign_msg, config.APP_MASTER_KEY)
    return cmd_msg


def with_sign(cid_field_name=None, pids_field_name=None, action_name=None):
    def sign_decorator(fn):
        @wraps(fn)
        def wrap_sign(self, cmd_msg):
            [cid, pids] = map(cmd_msg.get, [cid_field_name, pids_field_name])
            cmd_msg = add_sign(cmd_msg, convid=cid,
                               peerids=pids, action=action_name)
            return fn(self, cmd_msg)
        return wrap_sign
    return sign_decorator


class Command:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def complate_msg(self, common_args, cmd_msg):
        return cmd_msg

    def get_respond(self, msg):
        return None

    def need_serial_id(self):
        return True


class CommandWithOp(Command):
    def __init__(self, name):
        Command.__init__(self, name)
        self.sub_commands = dict()

    def add(self, sub_command):
        name = sub_command.name
        self.sub_commands[name] = sub_command

    def remove(self, sub_command):
        self.sub_commands.pop(sub_command.name, None)

    def get_respond(self, msg):
        op_field = msg.get('op')
        if op_field is None or op_field not in self.sub_commands:
            return super().get_respond(msg)

        return self.sub_commands[op_field].get_respond(msg)

    def complate_msg(self, common_args, cmd_msg):
        op_field = cmd_msg.get('op')
        msg = None
        if op_field is None or self.sub_commands.get(op_field) is None:
            msg = cmd_msg
        else:
            msg = self.sub_commands[op_field].complate_msg(
                common_args, cmd_msg)
        msg['cmd'] = self.name
        return msg


class RegisteredCommands:
    def __init__(self):
        self._parents = list()
        self._childs = dict()

    def add_parent_cmd_cls(self, cmd_cls):
        self._parents.append(cmd_cls)

    def add_child_cmd_cls(self, parent_name, cmd_cls):
        childs = self._childs.get(parent_name, list())
        childs.append(cmd_cls)
        self._childs[parent_name] = childs

    def parent_cmd_cls_gen(self):
        for cmd_cls in self._parents:
            yield cmd_cls

    def child_cmd_cls_gen(self):
        for parent_name, cmd_cls in self._childs.items():
            # From https://stackoverflow.com/questions/25314547/cell-var-from-loop-warning-from-pylint
            # To by pass the "W0640:Cell variable parent_name defined in loop" warning
            # we pass parent_name as default value to param p
            yield from map(lambda c, p=parent_name: [p, c], cmd_cls)


COMMANDS = RegisteredCommands()


def register_command(parent_name=None):
    def wrapper(cls):
        if parent_name is None:
            COMMANDS.add_parent_cmd_cls(cls)
        else:
            COMMANDS.add_child_cmd_cls(parent_name, cls)
        return cls
    return wrapper


def init_commands():
    commands = dict()
    for parent_cls in COMMANDS.parent_cmd_cls_gen():
        cmd = parent_cls()
        commands[cmd.name] = cmd

    for parent_name, cmd_cls in COMMANDS.child_cmd_cls_gen():
        cmd = cmd_cls()
        commands[parent_name].add(cmd)
    return commands


@register_command()
class ConvCommand(CommandWithOp):
    _name = "conv"

    def __init__(self):
        super().__init__(ConvCommand._name)


@register_command(parent_name="conv")
class ConvStartCommand(Command):
    _op_name = "start"

    def __init__(self):
        super().__init__(ConvStartCommand._op_name)

    def complate_msg(self, common_args, cmd_msg):
        return cmd_msg


@register_command(parent_name="conv")
class ConvAddCommand(Command):
    _op_name = "add"

    def __init__(self):
        super().__init__(ConvAddCommand._op_name)

    def complate_msg(self, common_args, cmd_msg):
        return cmd_msg


@register_command(parent_name="conv")
class ConvRemoveCommand(Command):
    _op_name = "remove"

    def __init__(self):
        super().__init__(ConvRemoveCommand._op_name)

    def complate_msg(self, common_args, cmd_msg):
        return cmd_msg


@register_command()
class SessionCommand(CommandWithOp):
    _name = "session"

    def __init__(self):
        super().__init__(SessionCommand._name)

    def complate_msg(self, common_args, cmd_msg):
        cmd_msg['appId'] = common_args['app_id']
        cmd_msg['peerId'] = common_args['peer_id']
        cmd_msg = super().complate_msg(common_args, cmd_msg)
        return cmd_msg


@register_command(parent_name="session")
class SessionOpenCommand(Command):
    _op_name = "open"

    def __init__(self):
        super().__init__(SessionOpenCommand._op_name)

    def complate_msg(self, common_args, cmd_msg):
        add_sign(cmd_msg)
        cmd_msg['gameVersion'] = config.GAME_VERSION
        cmd_msg['protocolVersion'] = '0'
        cmd_msg['configBitmap'] = config.CONFIG_BITMAP
        return cmd_msg


@register_command(parent_name="session")
class SessionCloseCommand(Command):
    _op_name = "close"

    def __init__(self):
        super().__init__(SessionCloseCommand._op_name)


class CommandsManager:
    def __init__(self, appid, peerid):
        self.commands = init_commands()
        self._next_serial_id = 1
        self._common_args = {'app_id': appid,
                             'peer_id': peerid}
        self._peerid = peerid

    def get_auto_respond_msg(self, msg):
        command = self._get_command(msg)
        if command is not None:
            return command.get_respond(msg)
        return None

    def complate_msg(self, cmd_msg):
        command = self._get_command(cmd_msg)
        if command is None:
            return cmd_msg

        msg = command.complate_msg(self._common_args, cmd_msg)
        if command.need_serial_id():
            msg['i'] = self._next_serial_id
            self._next_serial_id += 1
        return msg

    def _get_command(self, msg):
        cmd = msg.get('cmd')
        if cmd is not None:
            return self.commands.get(cmd)
        else:
            raise RuntimeError("Receive msg without 'cmd': %s" % msg)
