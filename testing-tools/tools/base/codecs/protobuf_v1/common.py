from tools.base.codecs.protobuf_v1 import messages_pb2
from tools.base.codecs.protobuf_v1 import generic_collection_pb2
from tools.base.codecs.protobuf_v1 import converter
from google.protobuf.descriptor import FieldDescriptor

import copy


class CodecManager:
    _type_to_codecs = dict()
    _type_to_object_type_ids = dict()
    _object_type_id_to_codec = dict()

    @staticmethod
    def register_codec(object_type, object_type_id, codec):
        CodecManager._type_to_codecs[object_type] = codec
        CodecManager._type_to_object_type_ids[object_type] = object_type_id
        CodecManager._object_type_id_to_codec[object_type_id] = codec

    @staticmethod
    def get_codec_by_type(object_type):
        return CodecManager._type_to_codecs[object_type]

    @staticmethod
    def get_codec_by_object_type_id(serialize_id):
        return CodecManager._object_type_id_to_codec[serialize_id]

    @staticmethod
    def get_object_type_id(object_type):
        return CodecManager._type_to_object_type_ids[object_type]


def serialize_generic_value(value):
    v = generic_collection_pb2.GenericCollectionValue()

    if value is None:
        v.type = generic_collection_pb2.GenericCollectionValue.NULL
    elif isinstance(value, bytes):
        v.type = generic_collection_pb2.GenericCollectionValue.BYTES
        v.bytes_value = value
    elif isinstance(value, int):
        v.type = generic_collection_pb2.GenericCollectionValue.LONG
        v.long_int_value = value
    elif isinstance(value, str):
        v.type = generic_collection_pb2.GenericCollectionValue.STRING
        v.string_value = value
    elif isinstance(value, float):
        v.type = generic_collection_pb2.GenericCollectionValue.DOUBLE
        v.double_value = value
    elif isinstance(value, dict):
        v.type = generic_collection_pb2.GenericCollectionValue.MAP
        v.bytes_value = serialize_generic_map(value)
    elif isinstance(value, list):
        v.type = generic_collection_pb2.GenericCollectionValue.ARRAY
        v.bytes_value = serialize_generic_array(value)
    else:
        codec = CodecManager.get_codec_by_type(type(value))
        v.type = generic_collection_pb2.GenericCollectionValue.OBJECT
        v.object_type_id = CodecManager.get_object_type_id(type(value))
        v.bytes_value = codec.serialize(value)
    return v


def deserialize_generic_value(v):
    if v.type == generic_collection_pb2.GenericCollectionValue.NULL:
        return None
    elif v.type == generic_collection_pb2.GenericCollectionValue.BYTES:
        return v.bytes_value
    elif v.type == generic_collection_pb2.GenericCollectionValue.LONG:
        return v.long_int_value
    elif v.type == generic_collection_pb2.GenericCollectionValue.DOUBLE:
        return v.double_value
    elif v.type == generic_collection_pb2.GenericCollectionValue.STRING:
        return v.string_value
    elif v.type == generic_collection_pb2.GenericCollectionValue.MAP:
        return deserialize_generic_map(v.bytes_value)
    elif v.type == generic_collection_pb2.GenericCollectionValue.ARRAY:
        return deserialize_generic_array(v.bytes_value)
    elif v.type == generic_collection_pb2.GenericCollectionValue.OBJECT:
        codec = CodecManager.get_codec_by_object_type_id(v.object_type_id)
        if codec:
            return codec.deserialize(v.bytes_value)


def serialize_generic_array(msg):
    coll = generic_collection_pb2.GenericCollection()

    entries = []
    for v in msg:
        entries.append(serialize_generic_value(v))
    coll.list_value.extend(entries)
    return coll.SerializeToString()


def deserialize_generic_array(msg):
    coll = generic_collection_pb2.GenericCollection()
    coll.ParseFromString(msg)

    v = []
    for e in coll.list_value:
        v.append(deserialize_generic_value(e))
    return v


def serialize_generic_map(msg):
    coll = generic_collection_pb2.GenericCollection()

    entries = []
    for k, v in msg.items():
        e = generic_collection_pb2.GenericCollection.MapEntry()
        e.key = k
        e.val.CopyFrom(serialize_generic_value(v))
        entries.append(e)
    coll.map_entry_value.extend(entries)
    return coll.SerializeToString()


def deserialize_generic_map(msg):
    coll = generic_collection_pb2.GenericCollection()
    coll.ParseFromString(msg)

    v = dict()
    for e in coll.map_entry_value:
        v[e.key] = deserialize_generic_value(e.val)
    return v


DESERIALIZE_TYPE_CALLABLE_MAP = converter.TYPE_CALLABLE_MAP
DESERIALIZE_TYPE_CALLABLE_MAP[FieldDescriptor.TYPE_BYTES] = \
    lambda field_name, v: v if field_name != 'attr' and field_name != 'expect_attr' and field_name != 'msg' else deserialize_generic_map(
        v)
SERIALIZE_TYPE_CALLABLE_MAP = {
    FieldDescriptor.TYPE_BYTES: lambda field_name, v: bytes(
        v) if field_name != 'attr' and field_name != 'expect_attr' and field_name != 'msg' else serialize_generic_map(v)
}


def serialize_common_fields(msg):
    cmd = msg.get('cmd')
    command = messages_pb2.Command()
    command.cmd = messages_pb2.CommandType.Value(cmd)

    if "op" in msg:
        command.op = messages_pb2.OpType.Value(
            msg.get("op").replace("-", "_"))
    return command


def deserialize_common_fields(input_command):
    cmd = messages_pb2.CommandType.Name(input_command.cmd)
    op = None
    if input_command.op:
        op = messages_pb2.OpType.Name(input_command.op).replace("_", "-")
    return cmd, op


def pile_up(msg, paths):
    origin = copy.deepcopy(msg)

    def _pile_up(last_msg, path):
        if path:
            last_msg[path[0]] = _pile_up(
                last_msg.get(path[0], {}), path[1:])
            return last_msg
        else:
            return copy.deepcopy(origin)

    for path in paths:
        if isinstance(path, list):
            msg[path[0]] = _pile_up(msg.get(path[0], {}), path[1:])
        else:
            msg[path] = origin


def smash(msg, paths):
    for path in paths:
        if isinstance(path, list):
            inner_msg = msg
            last_msg = {}
            for p in path:
                last_msg = inner_msg
                if p in inner_msg:
                    inner_msg = inner_msg[p]
                else:
                    last_msg = {}
                    inner_msg = {}
                    break
            last_msg.pop(path[-1], None)
            msg = {**msg, **inner_msg}
        else:
            if path in msg:
                msg = {**msg, **msg[path]}
            msg.pop(path, None)
    return msg
