from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.message import Message

EXTENSION_CONTAINER = '___X'


TYPE_CALLABLE_MAP = {
    FieldDescriptor.TYPE_DOUBLE: lambda field_name, v: float(v),
    FieldDescriptor.TYPE_FLOAT: lambda field_name, v: float(v),
    FieldDescriptor.TYPE_INT32: lambda field_name, v: int(v),
    FieldDescriptor.TYPE_INT64: lambda field_name, v: int(v),
    FieldDescriptor.TYPE_UINT32: lambda field_name, v: int(v),
    FieldDescriptor.TYPE_UINT64: lambda field_name, v: int(v),
    FieldDescriptor.TYPE_SINT32: lambda field_name, v: int(v),
    FieldDescriptor.TYPE_SINT64: lambda field_name, v: int(v),
    FieldDescriptor.TYPE_FIXED32: lambda field_name, v: int(v),
    FieldDescriptor.TYPE_FIXED64: lambda field_name, v: int(v),
    FieldDescriptor.TYPE_SFIXED32: lambda field_name, v: int(v),
    FieldDescriptor.TYPE_SFIXED64: lambda field_name, v: int(v),
    FieldDescriptor.TYPE_BOOL: lambda field_name, v: bool(v),
    FieldDescriptor.TYPE_STRING: lambda field_name, v: str(v),
    FieldDescriptor.TYPE_BYTES: lambda field_name, v: bytes(v),
    FieldDescriptor.TYPE_ENUM: lambda field_name, v: int(v),
}


def repeated(type_callable):
    return lambda field_name, value_list: [type_callable(field_name, value) for value in value_list]


def enum_label_name(field, value):
    return field.enum_type.values_by_number[int(value)].name


def _is_map_entry(field):
    return (field.type == FieldDescriptor.TYPE_MESSAGE and
            field.message_type.has_options and
            field.message_type.GetOptions().map_entry)


def protobuf_to_dict(pb, type_callable_map=TYPE_CALLABLE_MAP, use_enum_labels=False,
                     including_default_value_fields=False):
    result_dict = {}
    extensions = {}
    for field, value in pb.ListFields():
        if field.message_type and field.message_type.has_options and field.message_type.GetOptions().map_entry:
            result_dict[field.name] = dict()
            value_field = field.message_type.fields_by_name['value']
            type_callable = _get_field_value_adaptor(
                pb, value_field, type_callable_map,
                use_enum_labels, including_default_value_fields)
            for k, v in value.items():
                result_dict[field.name][k] = type_callable(v)
            continue
        type_callable = _get_field_value_adaptor(pb, field, type_callable_map,
                                                 use_enum_labels, including_default_value_fields)
        if field.label == FieldDescriptor.LABEL_REPEATED:
            type_callable = repeated(type_callable)

        if field.is_extension:
            extensions[str(field.number)] = type_callable(field.name, value)
            continue

        result_dict[field.name] = type_callable(field.name, value)

    # Serialize default value if including_default_value_fields is True.
    if including_default_value_fields:
        for field in pb.DESCRIPTOR.fields:
            # Singular message fields and oneof fields will not be affected.
            if ((
                    field.label != FieldDescriptor.LABEL_REPEATED and
                    field.cpp_type == FieldDescriptor.CPPTYPE_MESSAGE) or
                    field.containing_oneof):
                continue
            if field.name in result_dict:
                # Skip the field which has been serailized already.
                continue
            if _is_map_entry(field):
                result_dict[field.name] = {}
            else:
                result_dict[field.name] = field.default_value

    if extensions:
        result_dict[EXTENSION_CONTAINER] = extensions
    return result_dict


def _get_field_value_adaptor(pb, field, type_callable_map=TYPE_CALLABLE_MAP, use_enum_labels=False,
                             including_default_value_fields=False):
    if field.type == FieldDescriptor.TYPE_MESSAGE:
        # recursively encode protobuf sub-message
        return lambda field_name, pb: protobuf_to_dict(
            pb, type_callable_map=type_callable_map,
            use_enum_labels=use_enum_labels,
            including_default_value_fields=including_default_value_fields,
        )

    if use_enum_labels and field.type == FieldDescriptor.TYPE_ENUM:
        return lambda field_name, value: enum_label_name(field, value)

    if field.type in type_callable_map:
        return type_callable_map[field.type]

    raise TypeError("Field %s.%s has unrecognised type id %d" % (
        pb.__class__.__name__, field.name, field.type))


REVERSE_TYPE_CALLABLE_MAP = {
}


def dict_to_protobuf(pb_klass_or_instance, values, type_callable_map=REVERSE_TYPE_CALLABLE_MAP, strict=False, ignore_none=False):
    """Populates a protobuf model from a dictionary.
    :param pb_klass_or_instance: a protobuf message class, or an protobuf instance
    :type pb_klass_or_instance: a type or instance of a subclass of google.protobuf.message.Message
    :param dict values: a dictionary of values. Repeated and nested values are
       fully supported.
    :param dict type_callable_map: a mapping of protobuf types to callables for setting
       values on the target instance.
    :param bool strict: complain if keys in the map are not fields on the message.
    :param bool strict: ignore None-values of fields, treat them as empty field
    """
    if isinstance(pb_klass_or_instance, Message):
        instance = pb_klass_or_instance
    else:
        instance = pb_klass_or_instance()
    return _dict_to_protobuf(instance, values, type_callable_map, strict, ignore_none)


def _get_field_mapping(pb, dict_value, strict):
    field_mapping = []
    for key, value in dict_value.items():
        if key == EXTENSION_CONTAINER:
            continue
        if key not in pb.DESCRIPTOR.fields_by_name:
            if strict:
                raise KeyError(
                    "%s does not have a field called %s" % (pb, key))
            continue
        field_mapping.append(
            (pb.DESCRIPTOR.fields_by_name[key], value, getattr(pb, key, None)))

    for ext_num, ext_val in dict_value.get(EXTENSION_CONTAINER, {}).items():
        try:
            ext_num = int(ext_num)
        except ValueError:
            raise ValueError("Extension keys must be integers.")
        if ext_num not in pb._extensions_by_number:
            if strict:
                raise KeyError(
                    "%s does not have a extension with number %s. Perhaps you forgot to import it?" % (pb, key))
            continue
        ext_field = pb._extensions_by_number[ext_num]
        pb_val = None
        pb_val = pb.Extensions[ext_field]
        field_mapping.append((ext_field, ext_val, pb_val))

    return field_mapping


def _dict_to_protobuf(pb, value, type_callable_map, strict, ignore_none):
    fields = _get_field_mapping(pb, value, strict)

    for field, input_value, pb_value in fields:
        if ignore_none and input_value is None:
            continue
        if field.label == FieldDescriptor.LABEL_REPEATED:
            if field.message_type and field.message_type.has_options and field.message_type.GetOptions().map_entry:
                value_field = field.message_type.fields_by_name['value']
                for key, value in input_value.items():
                    if value_field.cpp_type == FieldDescriptor.CPPTYPE_MESSAGE:
                        _dict_to_protobuf(getattr(pb, field.name)[
                                          key], value, type_callable_map, strict, ignore_none)
                    else:
                        getattr(pb, field.name)[key] = value
                continue
            for item in input_value:
                if field.type == FieldDescriptor.TYPE_MESSAGE:
                    m = pb_value.add()
                    _dict_to_protobuf(
                        m, item, type_callable_map, strict, ignore_none)
                elif field.type == FieldDescriptor.TYPE_ENUM and isinstance(item, str):
                    pb_value.append(_string_to_enum(field, item))
                else:
                    pb_value.append(item)
            continue

        if field.type == FieldDescriptor.TYPE_MESSAGE:

            _dict_to_protobuf(pb_value, input_value,
                              type_callable_map, strict, ignore_none)
            continue

        if field.type in type_callable_map:
            input_value = type_callable_map[field.type](
                field.name, input_value)

        if field.is_extension:
            pb.Extensions[field] = input_value
            continue

        if field.type == FieldDescriptor.TYPE_ENUM and isinstance(input_value, str):
            input_value = _string_to_enum(field, input_value)

        setattr(pb, field.name, input_value)

    return pb


def _string_to_enum(field, input_value):
    enum_dict = field.enum_type.values_by_name
    try:
        input_value = enum_dict[input_value].number
    except KeyError:
        raise KeyError("`%s` is not a valid value for field `%s`" %
                       (input_value, field.name))
    return input_value


def get_field_names_and_options(pb):
    """
    Return a tuple of field names and options.
    """
    desc = pb.DESCRIPTOR

    for field in desc.fields:
        field_name = field.name
        options_dict = {}
        if field.has_options:
            options = field.GetOptions()
            for subfield, value in options.ListFields():
                options_dict[subfield.name] = value
        yield field, field_name, options_dict


class FieldsMissing(ValueError):
    pass


def validate_dict_for_required_pb_fields(pb, dic):
    """
    Validate that the dictionary has all the required fields for creating a protobuffer object
    from pb class. If a field is missing, raise FieldsMissing.
    In order to mark a field as optional, add [(is_optional) = true] to the field.
    Take a look at the tests for an example.
    """
    missing_fields = []
    for field, field_name, field_options in get_field_names_and_options(pb):
        if not field_options.get('is_optional', False) and field_name not in dic:
            missing_fields.append(field_name)
    if missing_fields:
        raise FieldsMissing('Missing fields: {}'.format(
            ', '.join(missing_fields)))
