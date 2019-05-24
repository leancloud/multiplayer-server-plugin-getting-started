from tools.base import config
from tools.base import matcher
from tools.base import util
from tools.base import router
from tools.base import client

LOG = util.get_logger('lobby-shortcuts')


def create_room(client_id, room_id=None, insecure=False):
    lobby_route = router.get_lobby_route(insecure=insecure).get('server')

    resp = {}
    with client.connect_to_ws_addr(client_id, lobby_route) as ws_client:
        resp = ws_client.send_msg_with_expect_msgs(
            {'cmd': 'session', 'op': 'open'},
            [{'cmd': 'session', 'op': 'opened'},
             {'cmd': 'statistic', 'appStats': matcher.MATCH_ANY}])

        resp = ws_client.send_msg_with_expect_msg(
            {'cmd': 'conv', 'op': 'start', 'cid': room_id})
    return {'secure_addr': resp.get('secureAddr'),
            'addr': resp.get('addr'),
            'error': resp.get('error'),
            'lobby_addr': lobby_route}


def join_room(client_id, room_id, conv_resp=matcher.MATCH_ANY, rejoin=False, random_join=False,
              expect_attr={}, insecure=False):
    lobby_route = router.get_lobby_route(insecure=insecure).get('server')

    resp = {}
    with client.connect_to_ws_addr(client_id, lobby_route) as ws_client:
        resp = ws_client.send_msg_with_expect_msgs(
            {'cmd': 'session', 'op': 'open'},
            [{'cmd': 'session', 'op': 'opened'},
             {'cmd': 'statistic', 'appStats': matcher.MATCH_ANY}])

        if random_join:
            resp = ws_client.send_msg_with_expect_msg(
                {'cmd': 'conv', 'op': 'add-random', 'cid': room_id,
                    'rejoin': rejoin,
                 'expectAttr': expect_attr}, resp=conv_resp)
        else:
            resp = ws_client.send_msg_with_expect_msg(
                {'cmd': 'conv', 'op': 'add', 'cid': room_id,
                    'rejoin': rejoin,
                 'randomJoin': random_join,
                 'expectAttr': expect_attr}, resp=conv_resp)

    return {'secure_addr': resp.get('secureAddr'),
            'addr': resp.get('addr'),
            'error': {'reasonCode': resp.get('reasonCode'), 'detail': resp.get('detail')}}


def match_room(client_id, room_id, conv_resp=matcher.MATCH_ANY,
               expect_attr={}, insecure=False):
    lobby_route = router.get_lobby_route(insecure=insecure).get('server')

    resp = {}
    with client.connect_to_ws_addr(client_id, lobby_route) as ws_client:
        resp = ws_client.send_msg_with_expect_msgs(
            {'cmd': 'session', 'op': 'open'},
            [{'cmd': 'session', 'op': 'opened'},
             {'cmd': 'statistic', 'appStats': matcher.MATCH_ANY}])

        resp = ws_client.send_msg_with_expect_msg(
            {'cmd': 'conv', 'op': 'match-random', 'cid': room_id,
             'expectAttr': expect_attr}, resp=conv_resp)

    return {'secure_addr': resp.get('secureAddr'),
            'addr': resp.get('addr'),
            'error': {'reasonCode': resp.get('reasonCode'), 'detail': resp.get('detail')}}


def fetch_rooms_in_lobby(client_id, **kwargs):
    lobby_route = router.get_lobby_route().get('server')

    resp = {}
    with client.connect_to_ws_addr(client_id, lobby_route) as ws_client:
        resp = ws_client.send_msg_with_expect_msgs(
            {'cmd': 'session', 'op': 'open'},
            [{'cmd': 'session', 'op': 'opened'},
             {'cmd': 'statistic', 'appStats': matcher.MATCH_ANY}])

        resp = ws_client.send_msg_with_expect_msgs(
            {'cmd': 'lobby', 'op': 'add'},
            [{'cmd': 'lobby', 'op': 'added'},
             {'cmd': 'lobby', 'op': 'room-list', 'list': matcher.MATCH_ANY}])

    return resp


if __name__ == "__main__":
    config.init_config('q0')
    client_id = "2a"
    print(create_room(client_id))
