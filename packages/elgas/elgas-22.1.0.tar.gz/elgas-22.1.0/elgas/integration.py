from typing import *

import attr
import marshmallow


@attr.s(auto_attribs=True)
class ConfigurationObject:

    parameter_type: int
    data: Dict


class ConfigurationObjectSchema(marshmallow.Schema):

    parameter_type = marshmallow.fields.Integer(required=True)
    data = marshmallow.fields.Dict(required=True)


@attr.s(auto_attribs=True)
class UtilitarianConfigurationObject:
    parameter_type: int
    data: Dict
    series_name: Optional[str] = attr.ib(default=None)


@attr.s(auto_attribs=True)
class UtilitarianConfiguration:
    objects: List[UtilitarianConfigurationObject]


class UtilitarianConfigurationObjectSchema(marshmallow.Schema):

    parameter_type = marshmallow.fields.Integer(required=True)
    data = marshmallow.fields.Dict(required=True)
    series_name = marshmallow.fields.String(required=True, allow_none=True)


class UtilitarianConfigurationSchema(marshmallow.Schema):
    objects = marshmallow.fields.List(
        marshmallow.fields.Nested(UtilitarianConfigurationObjectSchema)
    )
