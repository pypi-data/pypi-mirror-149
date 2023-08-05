from datetime import datetime

from ariadne import ScalarType

from swh.graphql.utils import utils
from swh.model.model import TimestampWithTimezone
from swh.model.swhids import CoreSWHID

datetime_scalar = ScalarType("DateTime")
swhid_scalar = ScalarType("SWHID")
hash_value_scalar = ScalarType("HashValue")
id_scalar = ScalarType("ID")
string_scalar = ScalarType("String")


@id_scalar.serializer
def serialize_id(value):
    if type(value) is bytes:
        return value.hex()
    return value


@string_scalar.serializer
def serialize_string(value):
    if type(value) is bytes:
        return value.decode("utf-8")
    return value


@hash_value_scalar.serializer
def serialize_hash_value(value):
    return value.hex()


@datetime_scalar.serializer
def serialize_datetime(value):
    # FIXME, handle error and return None
    if type(value) == TimestampWithTimezone:
        value = value.to_datetime()
    if type(value) == datetime:
        return utils.get_formatted_date(value)
    return None


@swhid_scalar.value_parser
def validate_swhid(value):
    return CoreSWHID.from_string(value)


@swhid_scalar.serializer
def serialize_swhid(value):
    return str(value)
