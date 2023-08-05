import struct

import attr
import marshmallow
from marshmallow import post_load

from elgas.utils import pop_many


@attr.s(auto_attribs=True)
class GasComposition:
    co2: float
    n2: float
    combustion_heat: float
    relative_density: float
    h2: float
    h2s: float
    he: float
    h2o: float
    o2: float
    ar: float
    co: float
    c1h4: float
    c2h6: float
    c3h8: float
    ic4h10: float
    nc4h10: float
    ic5h12: float
    nc5h12: float
    c6h14: float
    c7h16: float
    c8h18: float
    c9h20: float
    c10h22: float

    @classmethod
    def from_bytes(cls, in_data: bytes):
        data = bytearray(in_data)

        return cls(
            co2=struct.unpack("<f", pop_many(data, 4))[0],
            n2=struct.unpack("<f", pop_many(data, 4))[0],
            combustion_heat=struct.unpack("<f", pop_many(data, 4))[0],
            relative_density=struct.unpack("<f", pop_many(data, 4))[0],
            h2=struct.unpack("<f", pop_many(data, 4))[0],
            h2s=struct.unpack("<f", pop_many(data, 4))[0],
            he=struct.unpack("<f", pop_many(data, 4))[0],
            h2o=struct.unpack("<f", pop_many(data, 4))[0],
            o2=struct.unpack("<f", pop_many(data, 4))[0],
            ar=struct.unpack("<f", pop_many(data, 4))[0],
            co=struct.unpack("<f", pop_many(data, 4))[0],
            c1h4=struct.unpack("<f", pop_many(data, 4))[0],
            c2h6=struct.unpack("<f", pop_many(data, 4))[0],
            c3h8=struct.unpack("<f", pop_many(data, 4))[0],
            ic4h10=struct.unpack("<f", pop_many(data, 4))[0],
            nc4h10=struct.unpack("<f", pop_many(data, 4))[0],
            ic5h12=struct.unpack("<f", pop_many(data, 4))[0],
            nc5h12=struct.unpack("<f", pop_many(data, 4))[0],
            c6h14=struct.unpack("<f", pop_many(data, 4))[0],
            c7h16=struct.unpack("<f", pop_many(data, 4))[0],
            c8h18=struct.unpack("<f", pop_many(data, 4))[0],
            c9h20=struct.unpack("<f", pop_many(data, 4))[0],
            c10h22=struct.unpack("<f", pop_many(data, 4))[0],
        )


class GasCompositionSchema(marshmallow.Schema):

    co2 = marshmallow.fields.Float(required=True, as_string=True)
    n2 = marshmallow.fields.Float(required=True, as_string=True)
    combustion_heat = marshmallow.fields.Float(required=True, as_string=True)
    relative_density = marshmallow.fields.Float(required=True, as_string=True)
    h2 = marshmallow.fields.Float(required=True, as_string=True)
    h2s = marshmallow.fields.Float(required=True, as_string=True)
    he = marshmallow.fields.Float(required=True, as_string=True)
    h2o = marshmallow.fields.Float(required=True, as_string=True)
    o2 = marshmallow.fields.Float(required=True, as_string=True)
    ar = marshmallow.fields.Float(required=True, as_string=True)
    co = marshmallow.fields.Float(required=True, as_string=True)
    c1h4 = marshmallow.fields.Float(required=True, as_string=True)
    c2h6 = marshmallow.fields.Float(required=True, as_string=True)
    c3h8 = marshmallow.fields.Float(required=True, as_string=True)
    ic4h10 = marshmallow.fields.Float(required=True, as_string=True)
    nc4h10 = marshmallow.fields.Float(required=True, as_string=True)
    ic5h12 = marshmallow.fields.Float(required=True, as_string=True)
    nc5h12 = marshmallow.fields.Float(required=True, as_string=True)
    c6h14 = marshmallow.fields.Float(required=True, as_string=True)
    c7h16 = marshmallow.fields.Float(required=True, as_string=True)
    c8h18 = marshmallow.fields.Float(required=True, as_string=True)
    c9h20 = marshmallow.fields.Float(required=True, as_string=True)
    c10h22 = marshmallow.fields.Float(required=True, as_string=True)

    @post_load
    def make_object(self, data, **kwargs):
        return GasComposition(**data)
