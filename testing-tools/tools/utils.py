import time
import sys
from functools import wraps

from tools.base import lobby_shortcuts
from tools.base import client
from tools.base import config


def open_session(client_id, router_resp_fn):
    router_resp = router_resp_fn()
    room_addr = router_resp.get('secure_addr')

    ws_client = client.connect_to_ws_addr(client_id, room_addr)

    ws_client.send_msg_with_expect_msgs({'cmd': 'session',
                                         'op': 'open'},
                                        [{'cmd': 'session',
                                          'op': 'opened'}])
    return ws_client


def create_room(client_id, room_id, player_ttl=None, attr={}, lobby_keys=[], flag=0):
    ws_client = open_session(
        client_id, lambda: lobby_shortcuts.create_room(client_id, room_id=room_id))
    ws_client.send_msg_with_expect_msgs({'cmd': 'conv',
                                         'op': 'start',
                                         'cid': room_id,
                                         'playerTtl': player_ttl,
                                         'attr': attr,
                                         'lobbyAttrKeys': lobby_keys,
                                         'flag': flag},
                                        [{'cmd': 'conv',
                                          'op': 'started',
                                          'masterActorId': 1,
                                          "members": [{"pid": client_id, "actorId": 1, "attr": {}}]}])
    return ws_client


def join_room(client_id, room_id, rejoin=False):
    ws_client = open_session(
        client_id, lambda: lobby_shortcuts.join_room(client_id, room_id, rejoin=rejoin))
    ws_client.send_msg_with_expect_msgs({'cmd': 'conv',
                                         'op': 'add',
                                         'cid': room_id,
                                         'rejoin': rejoin},
                                        [{'cmd': 'conv',
                                          'op': 'added'},
                                         {'cmd': 'events',
                                          'events': []}])
    return ws_client


def create_cluster(client_ids, room_id, player_ttl=None, attr={}, flag=0):
    creator = None
    ret = []
    for id in client_ids:
        if not ret:
            creator = create_room(
                id, room_id, player_ttl=player_ttl, attr=attr, flag=flag)
            ret.append(creator)
        else:
            ret.append(join_room(id, room_id))
        time.sleep(0.5)

    return ret


def flatten(l):
    return [item for sublist in l for item in sublist]


def integration_test(config_bitmap_and_mask=0xFFFFFFFFFFFFFFFF, config_bitmap_or_mask=0x0):
    def integration_test_decorator(testing_fn):
        @wraps(testing_fn)
        def wrap_fn():
            config_tag = 'q0'
            if len(sys.argv) >= 2:
                config_tag = sys.argv[1]

            config.init_config(config_tag)
            config.CONFIG_BITMAP = config.CONFIG_BITMAP & config_bitmap_and_mask
            config.CONFIG_BITMAP = config.CONFIG_BITMAP | config_bitmap_or_mask

            print("\n%s\n" % testing_fn.__name__)
            testing_fn()

            client.close_all_opened_clients()
        return wrap_fn
    return integration_test_decorator
