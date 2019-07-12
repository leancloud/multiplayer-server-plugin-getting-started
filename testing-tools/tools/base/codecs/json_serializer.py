
import json


def try_decode_msg(msg):
    if msg.get('msg') and isinstance(msg['msg'], dict):
        return msg

    if msg.get('msg') and not isinstance(msg['msg'], str):
        try:
            msg['msg'] = msg['msg'].decode('utf-8')
        except AttributeError:
            pass

    return msg


class JsonSerializer:
    def serialize(self, msg):

        return json.dumps(msg)

    def deserialize(self, msg):
        msg = json.loads(str(msg))
        cmd = msg.get('cmd')
        if cmd == "direct":
            msg = try_decode_msg(msg)
        elif cmd == "events" and msg.get('events'):
            msg['events'] = list(map(try_decode_msg, msg.get('events')))
        return msg
