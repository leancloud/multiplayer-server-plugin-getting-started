"""
webSocket Client
"""
import json
import colorama
from threading import Thread, Event

from tools.base import commands
from tools.base import matcher
from tools.base import util
from tools.base import config
from tools.base.json_serializer import JsonSerializer

from ws4py.client.threadedclient import WebSocketClient
from ws4py.messaging import BinaryMessage
from ws4py.websocket import Heartbeat

LOG = util.get_logger('client')

OPENED_CLIENTS = []


class AbstractExpectMsgFuture(object):
    def __init__(self, expect_resp_list):
        self._next_match_index = 0
        self._expect_resp_list = expect_resp_list
        self._matched_resp_list = []
        self._event = Event()

    def get(self, timeout=None):
        if not self._event.is_set() and not self._event.wait(timeout=timeout):
            raise Exception(
                "Timeout on waiting for expect response: %s" % self._expect_resp_list)

        return self._matched_resp_list

    def match(self, resp):
        if self.is_done():
            raise RuntimeError("future already matched: %s" % resp)

        if self._next_match_index == len(self._expect_resp_list):
            self._event.set()
            return True

        expect_resp = self._expect_resp_list[self._next_match_index]
        if matcher.partial_match_json(expect_resp, resp):
            self._matched_resp_list.append(resp)
            self._next_match_index += 1
            if self._next_match_index == len(self._expect_resp_list):
                self._event.set()
            return True
        else:
            return False

    def is_done(self):
        return self._event.is_set()


class SingleExpectMsgFuture(AbstractExpectMsgFuture):
    def __init__(self, expect_resp):
        super(SingleExpectMsgFuture, self).__init__([expect_resp])

    def get(self, timeout=None):
        super().get(timeout=timeout)

        return self._matched_resp_list.pop()

    def match(self, resp):
        return super().match(resp)


class MultiExpectMsgsFuture(AbstractExpectMsgFuture):
    def __init__(self, expect_resp_list):
        super(MultiExpectMsgsFuture, self).__init__(expect_resp_list)


class ClientsBoundMultiExpectMsgsFuture(object):
    def __init__(self, clients, expect_msgs):
        assert len(clients) != 0
        assert len(expect_msgs) != 0
        self._client_future_map = dict()

        for client in clients:
            self._client_future_map[client] = client.expect_to_receive_msgs(
                expect_msgs)

    def get(self, timeout=5):
        ret = dict()
        for client, future in self._client_future_map.items():
            ret[client] = future.get(timeout)
        return ret


def add_expect_msgs_for_all(clients, expect_msgs):
    return ClientsBoundMultiExpectMsgsFuture(clients, expect_msgs)


class Client(WebSocketClient):
    def __init__(self, addr, peer_id, ping_interval_secs,
                 cmd_manager, codec, protocol="json.1"):
        super(Client, self).__init__(addr, protocols=[protocol])
        self._peer_id = peer_id
        self._serializer = codec
        self._cmd_manager = cmd_manager
        if ping_interval_secs is None:
            self._ping_interval_secs = 10
        else:
            self._ping_interval_secs = ping_interval_secs
        self._future_list = []
        self._heartbeat_job = Heartbeat(self, self._ping_interval_secs)
        self._closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._heartbeat_job.stop()
        super(Client, self).close()

    def handshake_ok(self):
        LOG.info(colorama.Fore.YELLOW + "Handshake OK")
        OPENED_CLIENTS.append(self)
        super().handshake_ok()

        if self._ping_interval_secs != 0:
            ping_thread = Thread(target=self._heartbeat_job.run)
            ping_thread.daemon = True
            ping_thread.start()

    def opened(self):
        LOG.info(colorama.Fore.YELLOW + "Socket opened")

    def _assert_client_not_close(self):
        if self._closed:
            raise RuntimeError(
                "Connection broken, please send msg after connected to server")

    def send_msg(self, cmd_msg_args):
        self._assert_client_not_close()

        msg = self._cmd_manager.complate_msg(cmd_msg_args)

        LOG.info("%s > %s" % (self._peer_id, json.dumps(msg)))

        msg = self._serializer.serialize(msg)
        if not isinstance(msg, str):
            msg = BinaryMessage(bytes=msg)

        super().send(msg)

    def send_msg_with_expect_msg(self, cmd_msg_args, resp=matcher.MATCH_ANY, timeout=5):
        future = SingleExpectMsgFuture(resp)
        self._future_list.append(future)
        self.send_msg(cmd_msg_args)

        return future.get(timeout)

    def send_msg_with_expect_msgs(self, cmd_msg_args, resps, timeout=5):
        future = self.expect_to_receive_msgs(resps)
        self.send_msg(cmd_msg_args)

        return future.get(timeout)

    def received_message(self, message):
        if isinstance(message, BinaryMessage):
            message = message.data
        msg = self._serializer.deserialize(message)

        LOG.info(colorama.Fore.CYAN + "%s < %s" %
                 (self._peer_id, json.dumps(msg)))

        for future in self._future_list:
            if future.match(msg):
                if future.is_done():
                    self._future_list.remove(future)
                break

    def expect_to_receive_msgs(self, expect_msgs):
        self._assert_client_not_close()

        future = MultiExpectMsgsFuture(expect_msgs)
        self._future_list.append(future)
        return future

    def closed(self, code, reason=None):
        self._closed = True
        self._heartbeat_job.stop()
        OPENED_CLIENTS.remove(self)
        LOG.info(colorama.Fore.YELLOW +
                 "WebSocket closed: %s %s" % (code, reason))


class ClientBuilder:
    def __init__(self):
        self._appid = None
        self._peerid = None
        self._addr = None
        self._ping_interval_secs = None
        self._protocol = config.DEFAULT_PROTOCOL

    def with_appid(self, appid):
        self._appid = appid
        return self

    def with_protocol(self, protocol):
        self._protocol = protocol
        return self

    def with_ping_interval_secs(self, interval_secs):
        self._ping_interval_secs = interval_secs
        return self

    def disable_ping(self):
        self._ping_interval_secs = 0
        return self

    def with_peerid(self, peerid):
        self._peerid = peerid
        return self

    def with_addr(self, addr):
        self._addr = addr
        return self

    def build(self):
        cmd_manager = commands.CommandsManager(
            self._appid, self._peerid)
        codec = JsonSerializer()
        return Client(self._addr,
                      self._peerid,
                      self._ping_interval_secs,
                      cmd_manager,
                      codec,
                      protocol=self._protocol)


def client_builder():
    return ClientBuilder()


def connect_to_ws_addr(client_id, addr):
    ws_client = client_builder() \
        .with_addr(addr) \
        .with_appid(config.APP_ID) \
        .with_peerid(client_id) \
        .build()
    LOG.info("%s connecting to %s" % (client_id, addr))
    ws_client.connect()
    return ws_client


def close_all_opened_clients():
    for c in OPENED_CLIENTS:
        c.close()
