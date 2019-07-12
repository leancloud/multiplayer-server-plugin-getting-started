from tools.base.codecs.protobuf_v1 import protobuf_serializer

import unittest   # The test framework


def test_client_to_server_msg(t, expect):
    serialized = protobuf_serializer.ClientToServerProtobufSerializer(
    ).serialize(expect)
    actual = protobuf_serializer.ServerToClientProtobufSerializer(
    ).deserialize(serialized)
    t.assertEqual(expect, actual)


def test_server_to_client_msg(t, expect):
    serialized = protobuf_serializer.ServerToClientProtobufSerializer(
    ).serialize(expect)
    actual = protobuf_serializer.ClientToServerProtobufSerializer(
    ).deserialize(serialized)
    t.assertEqual(expect, actual)


class Test_Protobuf_Serializer(unittest.TestCase):
    def test_session_command(self):
        expect = {'cmd': 'session', 'op': 'open', 'i': 123, 'appId': 'some app',
                  't': 123457, 's': 'signature', 'n': 'nonce', 'configBitmap': 8888, 'peerId': 'client id',
                  'gameVersion': 'GameTest/1.0', 'sdkVersion': 'testing_tool/1.0', 'protocolVersion': 'proto/1.0'}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': 'session', 'op': 'opened', 'i': 123,
                  'reasonCode': 123, 'detail': 'adsfasdf'}
        test_server_to_client_msg(self, expect)

    def test_direct(self):
        expect = {'cmd': 'direct', 'cached': True, 'eventId': 123, 'receiverGroup': 3, 'cachingOption': 777,
                  'msg': {'expectedMembers': ['expect', 'members', 'is', 'niuniu']}, 'toActorIds': [1, 2, 4, 5, 6, 7, 8]}
        test_client_to_server_msg(self, expect)

        expect = {"fromActorId": 2, "msg": {"properties": {"hello": "world",
                                                           "level": "100"}}, "timestamp": 1559145153466, "cmd": "direct", "eventId": 5}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': 'direct', 'msg': {'data': 'signature', 'null': None}, 'toActorIds': [1, 2, 4, 5, 6, 7, 8],
                  'timestamp': 123123123123, 'fromActorId': 323}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': 'direct', 'cached': True, 'eventId': 123, 'receiverGroup': 555, 'cachingOption': 777,
                  'msg': {'data': 'signature'}, 'toActorIds': [1, 2, 4, 5, 6, 7, 8]}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'direct', 'msg': {'data': 'signature'}, 'toActorIds': [1, 2, 4, 5, 6, 7, 8],
                  'timestamp': 123123123123, 'fromActorId': 323}
        test_server_to_client_msg(self, expect)

    def test_event(self):
        expect = {'cmd': 'events', 'events': []}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'events', 'events': [
            {'cached': True, 'eventId': 123,
             'receiverGroup': 555, 'cachingOption': 777,
             'toActorIds': [1, 2, 4, 5, 6, 7, 8]}]}
        test_server_to_client_msg(self, expect)

    def test_ack(self):
        expect = {'cmd': 'ack', 'timestamp': 1540456835754, 'i': 222}
        test_server_to_client_msg(self, expect)

    def test_statistic(self):
        expect = {'cmd': 'statistic',
                  'appStats': {'countOfRooms': 1111,             'countOfPlayersOnRouter': 22222,
                               'countOfPlayersInRooms': 33333, 'countOfPlayers': 4444}}
        test_server_to_client_msg(self, expect)

    def test_lobby(self):
        expect = {'cmd': 'lobby', 'op': 'add',
                  'lobbyId': 'some lobby', 'i': 123}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': 'lobby', 'op': 'added', 'i': 123}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'lobby', 'op': 'remove', 'i': 123}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': 'lobby', 'op': 'removed', 'i': 123}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'lobby', 'op': 'room-list',
                  'list': [{'maxMembers': 10, 'expectMembers': ['pid1', 'pid2', 'pid3'], 'visible':False, 'open':True,
                            'emptyRoomTtl':12345, 'playerTtl':1234567, 'memberCount':666, 'cid':'game-test',
                            'attr':{'niuniu': {'hahaha': 'a value', 'a': 1, 'b': True}}},
                           {'maxMembers': 11, 'expectMembers': ['pid2', 'pid4', 'pid3'], 'visible':False, 'open':True,
                            'memberCount':666, 'cid':'game-test2'}]}
        test_server_to_client_msg(self, expect)

    def test_start_room(self):
        expect = {'cmd': 'conv', 'op': 'start', 'cid': 'game_room',
                  'i': 222, 'open': True, 'visible': False}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'started', 'open': True, 'visible': False,
                  'cid': 'game_room', 'i': 222, 'addr': "ws://hahah.leancloud.cn"}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'started', 'cid': 'game_room', 'i': 222, 'emptyRoomTtl': 12345, 'playerTtl': 32323,
                  'lobbyAttrKeys': ["haha" "hoho" "niuniu"], 'flag': 2323, 'pluginName': "hook223", 'visible': True, 'open': True,
                  'expectMembers': ["pid1", "pid2", "pid3"], 'masterActorId': 111,
                  'attr': {'hohoho': {'niuniu': {'hahaha': 'a value', 'a': 1, 'b': True}}},
                  'members': [{'pid': 'pid1', 'actorId': 444, 'attr': {'wahaha': {'niuniu': {'hahaha': 'a value', 'a': 1, 'b': True}}}},
                              {'pid': 'pid2', 'actorId': 111, 'attr': {'hoho': {'niuniu': {'hahaha': 'a value', 'a': 1, 'b': True}}}}]}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'started', 'cid': 'game_room', 'i': 222, 'open': True, 'visible': False,
                  'reasonCode': 4105, 'detail': "rejected by app", 'appInfo': {'appCode': 123123, 'appMsg': "wahahahha"}}
        test_server_to_client_msg(self, expect)

    def test_join_room(self):
        expect = {'cmd': 'conv', 'op': 'add',
                  'cid': 'game_room', 'i': 222, 'rejoin': True, 'createOnNotFound': True, 'open': True, 'visible': False}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'add-random', 'cid': 'game_room', 'i': 222,
                  'expectAttr': {'niuniu': {'a': 1, 'b': 2, 'c': False}}, 'open': True, 'visible': False,
                  'expectMembers': ["pid1", "pid2", "pid3"]}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'match-random', 'piggybackPeerId': 'hhhh', 'i': 222,
                  'expectAttr': {'niuniu': {'a': 1, 'b': 2, 'c': False}}, 'open': True, 'visible': False,
                  'expectMembers': ["pid1", "pid2", "pid3"]}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'added', 'open': True, 'visible': False,
                  'cid': 'game_room', 'i': 222, 'addr': "ws://hahah.leancloud.cn"}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'random-added', 'open': True, 'visible': False,
                  'cid': 'game_room', 'i': 222, 'addr': "ws://hahah.leancloud.cn"}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'random-matched', 'open': True, 'visible': False,
                  'cid': 'game_room', 'i': 222, 'addr': "ws://hahah.leancloud.cn"}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'added', 'cid': 'game_room', 'i': 222, 'emptyRoomTtl': 12345, 'playerTtl': 32323,
                  'lobbyAttrKeys': ["haha" "hoho" "niuniu"], 'flag': 2323, 'pluginName': "hook223", 'visible': True, 'open': True,
                  'expectMembers': ["pid1", "pid2", "pid3"], 'masterActorId': 111,
                  'attr': {'hohoho': {'niuniu': {'hahaha': 'a value', 'a': 1, 'b': True}}},
                  'members': [{'pid': 'pid1', 'actorId': 444, 'attr': {'wahaha': {'niuniu': {'hahaha': 'a value', 'a': 1, 'b': True}}}},
                              {'pid': 'pid2', 'actorId': 111, 'attr': {'hoho': {'niuniu': {'hahaha': 'a value', 'a': 1, 'b': True}}}, 'inactive': True}]}
        test_server_to_client_msg(self, expect)

        testing_attr = {'wahaha': {'niuniu': {
            'hahaha': 'a value', 'a': 1, 'b': True}}}
        expect = {'cmd': 'conv', 'op': 'members-joined',
                  'member': {'pid': 'pid1', 'actorId': 444, 'attr': {'wahaha': testing_attr}}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'members-online',
                  'member': {'pid': 'pid1', 'actorId': 444, 'attr': {'wahaha': testing_attr}}}
        test_server_to_client_msg(self, expect)

    def test_remove_from_room(self):
        expect = {'cmd': "conv", 'op': "remove", 'i': 555}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': "conv", 'op': "removed", 'i': 555}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'removed',  'i': 222,
                  'reasonCode': 4105, 'detail': "rejected by app", 'appInfo': {'appCode': 123123, 'appMsg': "wahahahha"}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'members-offline', 'actorId': 323,
                  'initByActor': 111, 'appInfo': {'appMsg': 'reason from app', 'appCode': 1234}, 'byMaster': True}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'members-left', 'actorId': 323,
                  'initByActor': 111, 'appInfo': {'appMsg': 'reason from app', 'appCode': 1234}, 'byMaster': True}
        test_server_to_client_msg(self, expect)

    def test_kick_from_room(self):
        expect = {'cmd': "conv", 'op': "kick", 'i': 555,
                  'targetActorId': 2, 'appInfo': {'appCode': 12312, 'appMsg': "hello"}}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': "conv", 'op': "kicked",
                  'i': 555, 'targetActorId': 123}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'kicked',  'i': 222,
                  'reasonCode': 4105, 'detail': "rejected by app", 'appInfo': {'appCode': 123123, 'appMsg': "wahahahha"}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'kicked-notice',
                  'initByActor': 111, 'appInfo': {'appMsg': 'reason from app', 'appCode': 1234}, 'byMaster': True}
        test_server_to_client_msg(self, expect)

    def test_update_room_props(self):
        testing_attr = {'wahaha': {'niuniu': {
            'hahaha': 'a value', 'a': 1, 'b': True}}}
        expect = {'cmd': "conv", 'op': "update", 'i': 555,
                  'expectAttr': {'hohoho': testing_attr},
                  'attr': {'hahaha': testing_attr, 'null': None}}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': "conv", 'op': "updated", 'i': 555,
                  'attr': {'hahaha': testing_attr, 'null': None}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'updated',  'i': 222,
                  'reasonCode': 4105, 'detail': "rejected by app", 'appInfo': {'appCode': 123123, 'appMsg': "wahahahha"}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': "conv", 'op': "updated-notify", 'initByActor': 66, 'actorId': 23,
                  'attr': {'hahaha': testing_attr}, 'appInfo': {'appCode': 12, 'appMsg': 'wahaha'}, }
        test_server_to_client_msg(self, expect)

    def test_update_player_props(self):
        testing_attr = {'wahaha': {'niuniu': {
            'hahaha': 'a value', 'a': 1, 'b': True}}}
        expect = {'cmd': "conv", 'op': "update-player-prop", 'i': 555,
                  'expectAttr': {'hohoho': testing_attr},
                  'attr': {'hahaha': testing_attr}}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': "conv", 'op': "player-prop-updated",
                  'i': 123, 'attr': {'hahaha': testing_attr}, 'actorId': 666}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'player-prop-updated',  'i': 222,
                  'reasonCode': 4105, 'detail': "rejected by app", 'appInfo': {'appCode': 123123, 'appMsg': "wahahahha"}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': "conv", 'op': "player-props",
                  'initByActor': 872, 'actorId': 222,
                  'attr': {'hahaha': testing_attr}}
        test_server_to_client_msg(self, expect)

    def test_update_room_sys_props(self):
        expect = {'cmd': "conv", 'op': "update-system-property", 'i': 232,
                  'sysAttr': {'open': True, 'visible': True, 'maxMembers': 32,
                              'expectMembers': {'$add': ["d", "e", "f", "g"],
                                                '$remove': ['x', 'y'],
                                                '$set': ['a', 'b'],
                                                '$drop': True}}}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': "conv", 'op': "system-property-updated", 'i': 232,
                  'sysAttr': {'open': True, 'visible': False, 'expectMembers': ["d" "e" "f" "g"],
                              'maxMembers': 22}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': "conv", 'op': "system-property-updated", 'i': 232,
                  'sysAttr': {'expectMembers': []}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': "conv", 'op': "system-property-updated", 'i': 232,
                  'sysAttr': {'open': False}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'system-property-updated',  'i': 222,
                  'reasonCode': 4105, 'detail': "rejected by app", 'appInfo': {'appCode': 123123, 'appMsg': "wahahahha"}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': "conv", 'op': "system-property-updated-notify",
                  'initByActor': 1, 'appInfo': {'appCode': 12, 'appMsg': 'wahaha'},
                  'sysAttr': {'open': True, 'visible': False, 'expectMembers': ["d" "e" "f" "g"]}}
        test_server_to_client_msg(self, expect)

    def test_update_master_client(self):
        expect = {'cmd': "conv", 'op': "update-master-client",
                  'i': 555, 'masterActorId': 123123}
        test_client_to_server_msg(self, expect)

        expect = {'cmd': "conv", 'op': "master-client-updated",
                  'i': 555, 'masterActorId': 123123}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': 'conv', 'op': 'master-client-updated',  'i': 222,
                  'reasonCode': 4105, 'detail': "rejected by app", 'appInfo': {'appCode': 123123, 'appMsg': "wahahahha"}}
        test_server_to_client_msg(self, expect)

        expect = {'cmd': "conv", 'op': "master-client-changed",
                  'initByActor': 1123, 'masterActorId': 123123, 'appInfo': {'appCode': 123123, 'appMsg': "wahahahha"}}
        test_server_to_client_msg(self, expect)

    def test_error(self):
        expect = {'cmd': "error", 'reasonCode': 4105,
                  'detail': "something bad happen"}
        test_server_to_client_msg(self, expect)


if __name__ == '__main__':
    unittest.main()
