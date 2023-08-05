import json

from google.protobuf.descriptor import FieldDescriptor as FD


class ParseError(Exception):
    pass


def pb2json(pb):
    js = {}
    # fields = pb.DESCRIPTOR.fields #all fields
    fields = pb.ListFields()  # only filled (including extensions)
    for field, value in fields:
        if field.type == FD.TYPE_MESSAGE:
            ftype = pb2json
        elif field.type in _ftype2js:
            ftype = _ftype2js[field.type]
        else:
            raise ParseError(
                "Field %s.%s of type '%d' is not supported" % (pb.__class__.__name__, field.name, field.type,))
        if field.label == FD.LABEL_REPEATED:
            js_value = []
            for v in value:
                js_value.append(ftype(v))
        else:
            if field.name == 'body':
                js_value = json.loads(value)
            else:
                js_value = ftype(value)
        js[field.json_name] = js_value
    return js


_ftype2js = {
    FD.TYPE_DOUBLE: float,
    FD.TYPE_FLOAT: float,
    FD.TYPE_INT64: int,
    FD.TYPE_UINT64: int,
    FD.TYPE_INT32: int,
    FD.TYPE_FIXED64: float,
    FD.TYPE_FIXED32: float,
    FD.TYPE_BOOL: bool,
    FD.TYPE_STRING: str,
    FD.TYPE_BYTES: lambda x: x.encode('string_escape'),
    FD.TYPE_UINT32: int,
    FD.TYPE_ENUM: int,
    FD.TYPE_SFIXED32: float,
    FD.TYPE_SFIXED64: float,
    FD.TYPE_SINT32: int,
    FD.TYPE_SINT64: int,
}
