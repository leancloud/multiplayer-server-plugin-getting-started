from tools.base import client
from tools import utils
from tools.base import lobby_shortcuts
from tools.base.matcher import MATCH_ANY
from tools.base import config


@utils.integration_test()
def test_game_plugin():
    if not config.TEST_WITH_HOOK:
        return

    room_id = "master_is_watching_you_plugin_room"
    client_a, client_b, client_c = 'Alpha', 'Bravo', 'Charlie'

    ca = utils.open_session(
        client_a,
        lambda: lobby_shortcuts.create_room(client_a, room_id=room_id))
    ca.send_msg_with_expect_msgs({
        'cmd': 'conv',
        'op': 'start',
        'cid': room_id,
        'maxMember': 23,
        'pluginName': 'master is watching you plugin'
    }, [{
        'cmd': 'conv',
        'op': 'started',
        'masterActorId': 1,
        "members": [{
            "pid": client_a,
            "actorId": 1,
            "attr": {}
        }],
        "open": True
    }])

    cb, cc = list(
        map(lambda c: utils.join_room(c, room_id), [client_b, client_c]))

    # Charlie send a secret msg to Bravo, but it is caught by master Alpha
    whisper = {'data': "I'm super man"}
    future = client.add_expect_msgs_for_all([ca, cb], [{
        'cmd': 'direct',
        'fromActorId': 3,
        'msg': whisper,
        'timestamp': MATCH_ANY
    }, {
        'cmd': 'direct',
        'fromActorId': 1,
        'msg': {
            'data': "actor 3 is sending sneaky rpc"
        },
        'timestamp': MATCH_ANY
    }])
    cc.send_msg({'cmd': 'direct', 'msg': whisper, 'toActorIds': [2]}, )
    future.get()


if __name__ == '__main__':
    test_game_plugin()
