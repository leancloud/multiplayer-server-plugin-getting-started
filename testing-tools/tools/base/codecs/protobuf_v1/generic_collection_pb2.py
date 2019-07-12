# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: generic_collection.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='generic_collection.proto',
  package='cn.leancloud.play.proto',
  syntax='proto3',
  serialized_pb=_b('\n\x18generic_collection.proto\x12\x17\x63n.leancloud.play.proto\"\xb3\x03\n\x16GenericCollectionValue\x12\x42\n\x04type\x18\x01 \x01(\x0e\x32\x34.cn.leancloud.play.proto.GenericCollectionValue.Type\x12\x13\n\tint_value\x18\x02 \x01(\x05H\x00\x12\x18\n\x0elong_int_value\x18\x03 \x01(\x03H\x00\x12\x14\n\nbool_value\x18\x04 \x01(\x08H\x00\x12\x16\n\x0cstring_value\x18\x05 \x01(\tH\x00\x12\x15\n\x0b\x62ytes_value\x18\x06 \x01(\x0cH\x00\x12\x15\n\x0b\x66loat_value\x18\x07 \x01(\x02H\x00\x12\x16\n\x0c\x64ouble_value\x18\x08 \x01(\x01H\x00\x12\x16\n\x0eobject_type_id\x18\t \x01(\x05\"\x90\x01\n\x04Type\x12\x08\n\x04NULL\x10\x00\x12\t\n\x05\x42YTES\x10\x01\x12\x08\n\x04\x42YTE\x10\x02\x12\t\n\x05SHORT\x10\x03\x12\x07\n\x03INT\x10\x04\x12\x08\n\x04LONG\x10\x05\x12\x08\n\x04\x42OOL\x10\x06\x12\t\n\x05\x46LOAT\x10\x07\x12\n\n\x06\x44OUBLE\x10\x08\x12\n\n\x06OBJECT\x10\t\x12\n\n\x06STRING\x10\n\x12\x07\n\x03MAP\x10\x0b\x12\t\n\x05\x41RRAY\x10\x0c\x42\x07\n\x05value\"\xfd\x01\n\x11GenericCollection\x12\x43\n\nlist_value\x18\x01 \x03(\x0b\x32/.cn.leancloud.play.proto.GenericCollectionValue\x12L\n\x0fmap_entry_value\x18\x02 \x03(\x0b\x32\x33.cn.leancloud.play.proto.GenericCollection.MapEntry\x1aU\n\x08MapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12<\n\x03val\x18\x02 \x01(\x0b\x32/.cn.leancloud.play.proto.GenericCollectionValueB\x02P\x01\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_GENERICCOLLECTIONVALUE_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='cn.leancloud.play.proto.GenericCollectionValue.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NULL', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BYTES', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BYTE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SHORT', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INT', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LONG', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOOL', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FLOAT', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOUBLE', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJECT', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STRING', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MAP', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ARRAY', index=12, number=12,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=336,
  serialized_end=480,
)
_sym_db.RegisterEnumDescriptor(_GENERICCOLLECTIONVALUE_TYPE)


_GENERICCOLLECTIONVALUE = _descriptor.Descriptor(
  name='GenericCollectionValue',
  full_name='cn.leancloud.play.proto.GenericCollectionValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='cn.leancloud.play.proto.GenericCollectionValue.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='int_value', full_name='cn.leancloud.play.proto.GenericCollectionValue.int_value', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='long_int_value', full_name='cn.leancloud.play.proto.GenericCollectionValue.long_int_value', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='cn.leancloud.play.proto.GenericCollectionValue.bool_value', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='string_value', full_name='cn.leancloud.play.proto.GenericCollectionValue.string_value', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bytes_value', full_name='cn.leancloud.play.proto.GenericCollectionValue.bytes_value', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='float_value', full_name='cn.leancloud.play.proto.GenericCollectionValue.float_value', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='double_value', full_name='cn.leancloud.play.proto.GenericCollectionValue.double_value', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_type_id', full_name='cn.leancloud.play.proto.GenericCollectionValue.object_type_id', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GENERICCOLLECTIONVALUE_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='cn.leancloud.play.proto.GenericCollectionValue.value',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=54,
  serialized_end=489,
)


_GENERICCOLLECTION_MAPENTRY = _descriptor.Descriptor(
  name='MapEntry',
  full_name='cn.leancloud.play.proto.GenericCollection.MapEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='cn.leancloud.play.proto.GenericCollection.MapEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='val', full_name='cn.leancloud.play.proto.GenericCollection.MapEntry.val', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=660,
  serialized_end=745,
)

_GENERICCOLLECTION = _descriptor.Descriptor(
  name='GenericCollection',
  full_name='cn.leancloud.play.proto.GenericCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='list_value', full_name='cn.leancloud.play.proto.GenericCollection.list_value', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='map_entry_value', full_name='cn.leancloud.play.proto.GenericCollection.map_entry_value', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_GENERICCOLLECTION_MAPENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=492,
  serialized_end=745,
)

_GENERICCOLLECTIONVALUE.fields_by_name['type'].enum_type = _GENERICCOLLECTIONVALUE_TYPE
_GENERICCOLLECTIONVALUE_TYPE.containing_type = _GENERICCOLLECTIONVALUE
_GENERICCOLLECTIONVALUE.oneofs_by_name['value'].fields.append(
  _GENERICCOLLECTIONVALUE.fields_by_name['int_value'])
_GENERICCOLLECTIONVALUE.fields_by_name['int_value'].containing_oneof = _GENERICCOLLECTIONVALUE.oneofs_by_name['value']
_GENERICCOLLECTIONVALUE.oneofs_by_name['value'].fields.append(
  _GENERICCOLLECTIONVALUE.fields_by_name['long_int_value'])
_GENERICCOLLECTIONVALUE.fields_by_name['long_int_value'].containing_oneof = _GENERICCOLLECTIONVALUE.oneofs_by_name['value']
_GENERICCOLLECTIONVALUE.oneofs_by_name['value'].fields.append(
  _GENERICCOLLECTIONVALUE.fields_by_name['bool_value'])
_GENERICCOLLECTIONVALUE.fields_by_name['bool_value'].containing_oneof = _GENERICCOLLECTIONVALUE.oneofs_by_name['value']
_GENERICCOLLECTIONVALUE.oneofs_by_name['value'].fields.append(
  _GENERICCOLLECTIONVALUE.fields_by_name['string_value'])
_GENERICCOLLECTIONVALUE.fields_by_name['string_value'].containing_oneof = _GENERICCOLLECTIONVALUE.oneofs_by_name['value']
_GENERICCOLLECTIONVALUE.oneofs_by_name['value'].fields.append(
  _GENERICCOLLECTIONVALUE.fields_by_name['bytes_value'])
_GENERICCOLLECTIONVALUE.fields_by_name['bytes_value'].containing_oneof = _GENERICCOLLECTIONVALUE.oneofs_by_name['value']
_GENERICCOLLECTIONVALUE.oneofs_by_name['value'].fields.append(
  _GENERICCOLLECTIONVALUE.fields_by_name['float_value'])
_GENERICCOLLECTIONVALUE.fields_by_name['float_value'].containing_oneof = _GENERICCOLLECTIONVALUE.oneofs_by_name['value']
_GENERICCOLLECTIONVALUE.oneofs_by_name['value'].fields.append(
  _GENERICCOLLECTIONVALUE.fields_by_name['double_value'])
_GENERICCOLLECTIONVALUE.fields_by_name['double_value'].containing_oneof = _GENERICCOLLECTIONVALUE.oneofs_by_name['value']
_GENERICCOLLECTION_MAPENTRY.fields_by_name['val'].message_type = _GENERICCOLLECTIONVALUE
_GENERICCOLLECTION_MAPENTRY.containing_type = _GENERICCOLLECTION
_GENERICCOLLECTION.fields_by_name['list_value'].message_type = _GENERICCOLLECTIONVALUE
_GENERICCOLLECTION.fields_by_name['map_entry_value'].message_type = _GENERICCOLLECTION_MAPENTRY
DESCRIPTOR.message_types_by_name['GenericCollectionValue'] = _GENERICCOLLECTIONVALUE
DESCRIPTOR.message_types_by_name['GenericCollection'] = _GENERICCOLLECTION

GenericCollectionValue = _reflection.GeneratedProtocolMessageType('GenericCollectionValue', (_message.Message,), dict(
  DESCRIPTOR = _GENERICCOLLECTIONVALUE,
  __module__ = 'generic_collection_pb2'
  # @@protoc_insertion_point(class_scope:cn.leancloud.play.proto.GenericCollectionValue)
  ))
_sym_db.RegisterMessage(GenericCollectionValue)

GenericCollection = _reflection.GeneratedProtocolMessageType('GenericCollection', (_message.Message,), dict(

  MapEntry = _reflection.GeneratedProtocolMessageType('MapEntry', (_message.Message,), dict(
    DESCRIPTOR = _GENERICCOLLECTION_MAPENTRY,
    __module__ = 'generic_collection_pb2'
    # @@protoc_insertion_point(class_scope:cn.leancloud.play.proto.GenericCollection.MapEntry)
    ))
  ,
  DESCRIPTOR = _GENERICCOLLECTION,
  __module__ = 'generic_collection_pb2'
  # @@protoc_insertion_point(class_scope:cn.leancloud.play.proto.GenericCollection)
  ))
_sym_db.RegisterMessage(GenericCollection)
_sym_db.RegisterMessage(GenericCollection.MapEntry)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('P\001'))
# @@protoc_insertion_point(module_scope)