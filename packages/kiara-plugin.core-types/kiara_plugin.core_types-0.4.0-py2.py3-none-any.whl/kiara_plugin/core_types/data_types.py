# -*- coding: utf-8 -*-

"""This module contains the value type classes that are used in the ``kiara_plugin.core_types`` package.
"""

import datetime
import sys
from typing import Any, Iterable, Mapping, Type

import orjson
from kiara.data_types import DataTypeCharacteristics, DataTypeConfig
from kiara.data_types.included_core_types import SCALAR_CHARACTERISTICS, AnyType
from kiara.models.python_class import PythonClass
from kiara.models.values.value import SerializedData, Value
from kiara.utils import orjson_dumps
from kiara.utils.hashing import compute_hash
from pydantic import BaseModel

from kiara_plugin.core_types.models import DictModel, ListModel


class BooleanType(AnyType[bool, DataTypeConfig]):
    "A boolean."

    _data_type_name = "boolean"

    @classmethod
    def python_class(cls) -> Type:
        return bool

    def serialize(self, data: bool) -> SerializedData:
        result = self.serialize_as_json(data)
        return result

    def _retrieve_characteristics(self) -> DataTypeCharacteristics:
        return SCALAR_CHARACTERISTICS

    def calculate_size(self, data: bool) -> int:
        return 24

    def calculate_hash(cls, data: bool) -> int:
        return 1 if data else 0

    def parse_python_obj(self, data: Any) -> bool:

        if data is True or data is False:
            return data
        elif data == 0:
            return False
        elif data == 1:
            return True
        elif isinstance(data, str):
            if data.lower() == "true":
                return True
            elif data.lower() == "false":
                return False
        raise Exception(f"Can't parse value '{data}' as boolean.")

    def validate(cls, value: Any):
        pass


class IntegerType(AnyType[int, DataTypeConfig]):
    """An integer."""

    _data_type_name = "integer"

    @classmethod
    def python_class(cls) -> Type:
        return int

    def serialize(self, data: bool) -> SerializedData:
        result = self.serialize_as_json(data)
        return result

    def calculate_hash(cls, data: int) -> int:
        return data

    def calculate_size(self, data: int) -> int:
        return sys.getsizeof(data)

    def _retrieve_characteristics(self) -> DataTypeCharacteristics:
        return SCALAR_CHARACTERISTICS

    def parse_python_obj(self, data: Any) -> int:
        return int(data)


class FloatType(AnyType[float, DataTypeConfig]):
    "A float."

    _data_type_name = "float"

    @classmethod
    def python_class(cls) -> Type:
        return float

    def serialize(self, data: bool) -> SerializedData:
        result = self.serialize_as_json(data)
        return result

    def calculate_value_hash(cls, data: float) -> int:
        return compute_hash(data)

    def calculate_size(self, data: int) -> int:
        return sys.getsizeof(data)

    def _retrieve_characteristics(self) -> DataTypeCharacteristics:
        return SCALAR_CHARACTERISTICS

    def _validate(cls, value: Any) -> Any:

        if not isinstance(value, float):
            raise ValueError(f"Invalid type '{type(value)}' for float: {value}")


class DateType(AnyType[datetime.datetime, DataTypeConfig]):
    """A date.

    Internally, this will always be represented as a Python ``datetime`` object. Iff provided as input, it can also
    be as string, in which case the [``dateutils.parser.parse``](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse) method will be used to parse the string into a datetime object.
    """

    _data_type_name = "date"

    @classmethod
    def python_class(cls) -> Type:
        return datetime.datetime

    def serialize(self, data: bool) -> SerializedData:
        result = self.serialize_as_json(data)
        return result

    def calculate_hash(cls, data: datetime.datetime) -> int:
        return compute_hash(data)

    def calculate_size(self, data: datetime.datetime) -> int:
        return sys.getsizeof(data)

    def _retrieve_characteristics(self) -> DataTypeCharacteristics:
        return SCALAR_CHARACTERISTICS

    def parse_python_obj(self, data: Any) -> datetime.datetime:

        from dateutil import parser

        if isinstance(data, str):
            d = parser.parse(data)
            return d
        elif isinstance(data, datetime.date):
            _d = datetime.datetime(year=data.year, month=data.month, day=data.day)
            return _d

        raise Exception(f"Can't parse data into a 'datetime' object: {data}")

    def validate(cls, value: Any):
        assert isinstance(value, datetime.datetime)


class ListValueType(AnyType[ListModel, DataTypeConfig]):
    """A dictionary.

    In addition to the actual dictionary value, this value type comes also with an optional schema, describing the
    dictionary. In case no schema was attached, a simple generic one is attached.
    """

    _data_type_name = "list"

    @classmethod
    def python_class(cls) -> Type:
        return ListModel

    def calculate_size(self, data: ListModel) -> int:
        return data.size

    def calculate_hash(self, data: ListModel) -> int:
        return data.value_hash

    def _retrieve_characteristics(self) -> DataTypeCharacteristics:
        return DataTypeCharacteristics(is_scalar=False, is_json_serializable=True)

    def parse_python_obj(self, data: Any) -> ListModel:

        python_cls = data.__class__
        data = None
        schema = None

        if isinstance(data, Iterable):
            schema = {"title": "list", "type": "object"}
            data = data
        elif isinstance(data, str):
            try:
                data = orjson.loads(data)
                if not isinstance(data, str) and isinstance(list, Iterable):
                    schema = {"title": "dict", "type": "object"}
            except Exception:
                if isinstance(data, str):
                    raise Exception(
                        "Can't create list: can't parse string as json into list."
                    )

        if data is None or schema is None:
            raise Exception(f"Invalid data for value type 'dict': {data}")

        result = {
            "data": data,
            "item_schema": schema,
            "python_class": PythonClass.from_class(python_cls).dict(),
        }
        return ListModel.construct(**result)

    def _validate(self, data: ListModel) -> None:

        if not isinstance(data, ListModel):
            raise Exception(f"Invalid type: {type(data)}.")

    def render_as__string(self, value: Value, render_config: Mapping[str, Any]) -> str:

        data: ListModel = value.data
        return orjson_dumps(data.list_data, option=orjson.OPT_INDENT_2)


class DictValueType(AnyType[DictModel, DataTypeConfig]):
    """A dictionary.

    In addition to the actual dictionary value, this value type comes also with an optional schema, describing the
    dictionary. In case no schema was attached, a simple generic one is attached.
    """

    _data_type_name = "dict"

    @classmethod
    def python_class(cls) -> Type:
        return DictModel

    def calculate_size(self, data: DictModel) -> int:
        return data.size

    def calculate_hash(self, data: DictModel) -> int:
        return data.value_hash

    def _retrieve_characteristics(self) -> DataTypeCharacteristics:
        return DataTypeCharacteristics(is_scalar=False, is_json_serializable=True)

    def parse_python_obj(self, data: Any) -> DictModel:

        python_cls = data.__class__
        dict_data = None
        schema = None
        if isinstance(data, Mapping):
            schema = {"title": "dict", "type": "object"}
            dict_data = data
        elif isinstance(data, BaseModel):
            dict_data = data.dict()
            schema = data.schema()
        elif isinstance(data, str):
            try:
                dict_data = orjson.loads(data)
                schema = {"title": "dict", "type": "object"}
            except Exception:
                pass

        if dict_data is None or schema is None:
            raise Exception(f"Invalid data for value type 'dict': {data}")

        result = {
            "data": dict_data,
            "data_schema": schema,
            "python_class": PythonClass.from_class(python_cls).dict(),
        }
        return DictModel.construct(**result)

    def _validate(self, data: DictModel) -> None:

        if not isinstance(data, DictModel):
            raise Exception(f"Invalid type: {type(data)}.")

    def render_as__string(self, value: Value, render_config: Mapping[str, Any]) -> str:

        data: DictModel = value.data
        return orjson_dumps(data.dict_data, option=orjson.OPT_INDENT_2)
