# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

import functools
import logging
from copy import deepcopy
from io import StringIO

__all__ = ['NewSchemaInstance', 'ReceiveAsSchemaInstance', 'DataTypeStore']

from typing import TextIO, Union

from PyPlcnextRsc import RscType, RscList, RscStruct, RscSequence, RscTpAnnotate, RscStructBuilder, RscStructMeta, RscVariant, IecType

log = logging.getLogger(__name__)


def _remove_comment(lines):
    ret = []
    is_in_block = False

    for line in lines:
        ret_line = []
        for _identifier in line:
            if "*/" in _identifier:
                if not is_in_block:
                    raise ValueError()
                _identifier = _identifier[_identifier.index("*/") + 2:]
                if _identifier:
                    ret_line.append(_identifier)
                is_in_block = False
                continue

            if is_in_block:
                continue

            if "/*" in _identifier:
                is_in_block = True
                _identifier = _identifier[:_identifier.index("/*")]
                if _identifier:
                    ret_line.append(_identifier)
                continue
            if "//" in _identifier:
                _identifier = _identifier[:_identifier.index("//")]
                if _identifier:
                    ret_line.append(_identifier)
                break

            if "#" in _identifier:  # deprecated in future to support default value
                _identifier = _identifier[:_identifier.index("#")]
                if _identifier:
                    ret_line.append(_identifier)
                break

            ret_line.append(_identifier)

        if ret_line:
            ret.append(ret_line)
    return ret


def _move_TYPE_Label(lines):
    for line in lines:
        for _identifier in line:
            if _identifier.upper() in ["TYPE", "END_TYPE"]:
                line.remove(_identifier)


def _splitSpecial(identifiers):
    Ids = identifiers
    NEED_SPLIT = {";", ":", "[", "]", "..", "=",
                  # "#", # for future
                  # ","# for future
                  }
    for symbol in NEED_SPLIT:
        tmp = []
        s_len = len(symbol)
        for identifier in Ids:

            def _doSplit(current):
                if symbol in current and len(current) > s_len:
                    left, right = current.split(symbol, 1)
                    if left:
                        tmp.append(left)
                    tmp.append(symbol)
                    if right:
                        _doSplit(right)
                else:
                    tmp.append(current)

            if symbol in identifier and len(identifier) > s_len:
                _doSplit(identifier)
            else:
                tmp.append(identifier)

        Ids = tmp

    identifiers.clear()
    identifiers.extend(Ids[:])


class _Cursor:
    def __init__(self, identifiers):
        self._identifiers = identifiers
        self._max_cursor = len(identifiers) - 1
        self._current_cursor = 0

    @property
    def max(self):
        return self._max_cursor

    @property
    def left(self):
        return self.max - self.cursor + 1

    @property
    def cursor(self):
        return self._current_cursor

    @cursor.setter
    def cursor(self, value):
        self._current_cursor = value

    def seek(self, offset, whence=1):
        if whence == 0:  # from beginning
            self.cursor = offset
        elif whence == 1:  # from current
            self.cursor += offset
        elif whence == 2:  # from ending
            if offset > 0:
                raise
            self.cursor += self._max_cursor + offset

    def __getitem__(self, length):
        seek = True
        if type(length) == tuple:
            length, seek = length
        c = self.cursor
        ret = self._identifiers[c:c + length]
        if seek:
            self.seek(length, 1)
        if length == 1:
            return ret[0]
        else:
            return ret

    def distanceToNext(self, character):
        try:
            _i = self._identifiers.index(character, self.cursor)
            return _i - self.cursor + 1
        except ValueError as e:
            raise e

    def getUntilNext(self, character, seek=False, seekLast=False):
        ret = []
        dis = self.distanceToNext(character)
        if dis == 2:
            ret.append(self[1, seek])
        else:
            ret.extend(self[dis - 1, seek])
        if seekLast:
            self.seek(1, 1)
        return ret

    def consumeCharacter(self, character):
        if self[1, False].upper() != character.upper():
            raise
        else:
            self.seek(1, 1)

    def consumeOptional(self, character):
        if self.left == 0:
            return
        if self[1, False].upper() != character.upper():
            pass
        else:
            self.seek(1, 1)


def _getPrimitiveRscTypeFromHint(family):
    upper = family.upper()
    if hasattr(IecType, upper):
        return getattr(IecType, upper)


class _Schema:
    @classmethod
    def factory(cls, cursor, hints, not_add_hint=False):
        if cursor[2, False][-1] != ":":
            type_name = "#Anonymous"
        else:
            type_name = cursor[1]
            cursor.consumeCharacter(":")

        type_family = cursor[1]
        if type_family.upper() == "ARRAY":
            ins = _ArraySchema.factory(cursor, hints, not_add_hint)
            ins.name = type_name
            ins.family = "ARRAY"
        elif type_family.upper() == "STRUCT":
            ins = _StructSchema.factory(cursor, hints, not_add_hint)
            ins.name = type_name
            ins.family = "STRUCT"
        else:
            ins = cls()
            ins.name = type_name
            ins.family = type_family
            primitive = _getPrimitiveRscTypeFromHint(type_family)
            if primitive:
                ins.rsc_Type = primitive
            else:
                _h = hints.get(type_family, None)
                if _h:
                    final = deepcopy(_h)
                    final.name = ins.name
                    ins = final
                else:
                    raise ValueError("Unknow type of " + type_family)
        cursor.consumeOptional(";")
        if type_name != "#Anonymous" and not not_add_hint:
            hints[type_name] = ins
        return ins

    def __init__(self):
        self.name = ""
        self.family = ""

        self.rsc_Type = RscType.Null

    def __repr__(self):
        return f"PRIM<{self.family}>({self.name})"


class _StructSchema(_Schema):
    @classmethod
    def factory(cls, cursor: _Cursor, hints, not_add_hint=False):
        fields = []
        while cursor[1, False].upper() != "END_STRUCT":
            fields.append(_Schema.factory(cursor, hints, not_add_hint=True))
        cursor.consumeCharacter("END_STRUCT")
        ins = cls()
        ins.fields = fields
        ins.rsc_Type = RscType.Struct
        return ins

    def __init__(self):
        super().__init__()
        self.fields = None

    def __repr__(self):
        s = "STRUCT<"
        for f in self.fields:
            s += f.__repr__()
        s += '>'
        return s


class _ArraySchema(_Schema):
    @classmethod
    def factory(cls, cursor: _Cursor, hints, not_add_hint=False):
        ins = cls()
        ins.rsc_Type = RscType.Array
        cursor.getUntilNext("[", seekLast=True, seek=True)
        ins.bound_lower = int(cursor[1])
        cursor.consumeCharacter("..")
        ins.bound_upper = int(cursor[1])
        cursor.consumeCharacter("]")
        cursor.consumeCharacter("OF")
        _type = cursor.getUntilNext(";", seekLast=False, seek=False)
        if len(_type) == 1:
            primitive = _getPrimitiveRscTypeFromHint(_type[0])
            if primitive:
                ins.element_rsc_type = primitive
            else:
                next_dimension = hints.get(_type[0], None)
                if not next_dimension:
                    raise ValueError("Unknow type of " + _type[0])
                ins.next_dimension_or_struct = next_dimension
                if isinstance(next_dimension, _ArraySchema):
                    ins.element_rsc_type = RscType.Array
                elif isinstance(next_dimension, _StructSchema):
                    ins.element_rsc_type = RscType.Struct
            cursor.seek(1, 1)
        else:
            next_dimension = _Schema.factory(cursor, hints, not_add_hint)
            ins.next_dimension_or_struct = next_dimension
            ins.element_rsc_type = RscType.Array
        return ins

    def __init__(self):
        super().__init__()
        self.bound_upper = 0
        self.bound_lower = 0

        self.next_dimension_or_struct = None
        self.element_rsc_type = RscType.Null

    @property
    def size(self):
        return self.bound_upper - self.bound_lower + 1

    def __repr__(self):
        return f"ARRAY<{self.element_rsc_type.name}>[{self.bound_lower}..{self.bound_upper}]"


_RSC_DEFAULT_VALUES = {
    RscType.Int64: 0,
    RscType.Int32: 0,
    RscType.Int16: 0,
    RscType.Int8: 0,
    RscType.Uint64: 0,
    RscType.Uint32: 0,
    RscType.Uint16: 0,
    RscType.Uint8: 0,
    RscType.Bool: False,
    RscType.Real64: 0.0,
    RscType.Real32: 0.0,
    RscType.Utf8String: "",
    RscType.IecTime: 0,
    RscType.IecTime64: 0,
    RscType.IecDate64: 0,
    RscType.IecDateTime64: 0,
    RscType.IecTimeOfDay64: 0
}


def _make_array_for_write(schema) -> RscList:
    ret = RscList()
    if schema.bound_lower != 0:
        ret.setOffset(schema.bound_lower)
    size = schema.size
    ret.setDesireLength(size)
    element_type = schema.element_rsc_type
    if element_type == RscType.Array:
        next_dimension_schema = schema.next_dimension_or_struct
        ret.setNextDimension(_make_array_for_write(next_dimension_schema), size)
    elif element_type == RscType.Struct:
        ret.setElementAnnotate(_getRscStructTypeFromSchema(schema.next_dimension_or_struct), size, _make_struct_for_write(schema.next_dimension_or_struct))
    else:
        ret.setElementRscType(element_type, size, _RSC_DEFAULT_VALUES[element_type])

    return ret


@functools.lru_cache(maxsize=None, typed=True)
def _getRscStructTypeFromSchema(schema) -> RscStruct:
    if log.isEnabledFor(logging.DEBUG):
        log.debug(f"make RscStructType for schema({schema.name})")
    param = {}
    for field in schema.fields:
        if field.rsc_Type == RscType.Array:
            param[field.name] = RscSequence
        elif field.rsc_Type == RscType.Struct:
            param[field.name] = _getRscStructTypeFromSchema(field)
        else:
            _default = _RSC_DEFAULT_VALUES[field.rsc_Type]
            param[field.name] = RscTpAnnotate[type(_default), field.rsc_Type]
    return RscStruct(schema.name, **param)


def _make_struct_for_write(schema) -> RscStructBuilder:
    tp = _getRscStructTypeFromSchema(schema)
    field_defaults = {}
    for field in schema.fields:
        if field.rsc_Type == RscType.Array:
            field_defaults[field.name] = _make_array_for_write(field)
        elif field.rsc_Type == RscType.Struct:
            field_defaults[field.name] = _make_struct_for_write(field)
        else:
            field_defaults[field.name] = _RSC_DEFAULT_VALUES[field.rsc_Type]
    return RscStructBuilder(tp, field_defaults)


def _receiveArray(schema: _ArraySchema, value, builderMode=False):
    assert isinstance(value, RscSequence)
    should_element_size = schema.size
    should_element_rsc_type = schema.element_rsc_type
    fact_element_size = len(value)  # don't care the syntax warning
    fact_element_rsc_type = value.getElementRscType()
    if should_element_rsc_type != fact_element_rsc_type:
        raise ValueError(f"Expect type {should_element_rsc_type.name} in Array({schema.name}) but is {fact_element_rsc_type.name}")
    if should_element_size != fact_element_size:
        raise ValueError(f"Expect element count is {should_element_size} in Array({schema.name}) but is {fact_element_size}")

    ret = RscList()
    if schema.bound_lower != 0:
        ret.setOffset(schema.bound_lower)
    if should_element_rsc_type == RscType.Array:
        inner = None
        for current in value:  # don't care the syntax warning
            inner = _receiveArray(schema.next_dimension_or_struct, current)
            ret.append(inner)
        ret.setNextDimension(inner)
    elif should_element_rsc_type == RscType.Struct:
        inner = None
        for current in value:  # don't care the syntax warning
            inner = _receiveStruct(schema.next_dimension_or_struct, current, builderMode=builderMode)
            ret.append(inner)
        ret.setElementAnnotate(type(inner))
    else:
        # direct copy if rsc_type is primitive
        ret.extend(value[:])
        ret.setElementRscType(should_element_rsc_type)
    return ret


def _receiveStruct(schema: _StructSchema, value, builderMode=False):
    assert isinstance(value, RscStructMeta)
    should_fields_entries = schema.fields
    should_field_count = len(should_fields_entries)
    fact_field_count = len(value)
    if should_field_count != fact_field_count:
        raise ValueError(f"Expect field count {should_field_count} in Struct({schema.name}) but is {fact_field_count}")
    tp = _getRscStructTypeFromSchema(schema)
    _values = {}
    for idx in range(should_field_count):
        current_schema = should_fields_entries[idx]
        current_value = value[idx]
        if isinstance(current_schema, _ArraySchema):
            if current_value.GetType() != RscType.Array:
                raise ValueError(f"Expect field {current_schema.name} in Struct({schema.name}) is Array but is {current_value.GetType()}")
            _values[current_schema.name] = _receiveArray(current_schema, current_value.GetValue())
        elif isinstance(current_schema, _StructSchema):
            if current_value.GetType() != RscType.Struct:
                raise ValueError(f"Expect field {current_schema.name} in Struct({schema.name}) is Struct but is {current_value.GetType()}")
            _values[current_schema.name] = _receiveStruct(current_schema, current_value.GetValue(), builderMode=builderMode)
        else:
            if current_schema.rsc_Type != current_value.GetType():
                raise ValueError(f"Expect field {current_schema.name} in Struct({schema.name}) is {current_schema.rsc_Type.name} but is {current_value.GetType()}")
            _values[current_schema.name] = current_value.GetValue()
    if builderMode:
        return RscStructBuilder(tp, _values)
    else:
        return tp(**_values)  # don't care the syntax warning


####################################################################################
####################################################################################


def NewSchemaInstance(schema):
    """
    Construct a new data type instance defined by schema
    this instance is used for Write complex data to PLCnext

    .. note::

        In the created instance , all values have been set to its' default value,
        means that if user don't change the element (field) in it, it can also
        send to PLCnext successfully , but all elements (or fields) are *0* , *0.0* , *False* or *""(empty str)*

    :param schema: type schema, get from :py:func:`PyPlcnextRsc.tools.PlcDataTypeSchema.DataTypeStore.__getitem__`
    :return: a new data type instance for user to fill elements or fields
    """
    if isinstance(schema, _ArraySchema):
        return _make_array_for_write(schema)
    elif isinstance(schema, _StructSchema):
        return _make_struct_for_write(schema)


def ReceiveAsSchemaInstance(schema, variant: RscVariant, builderMode: bool = False):
    """
    Receive the certain value from :py:class:`~PyPlcnextRsc.common.objects.rsc_variant.RscVariant` as data_type defined in schema

    :param schema: type schema
    :param variant: from IDataAccessService or ISubscriptionService or some other service , which represent
                    the meta-value of the data_type defined in schema
    :type variant: :py:class:`~PyPlcnextRsc.common.objects.rsc_variant.RscVariant`
    :param builderMode: if set true, all the struct received will be the :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStructBuilder`,
                            so it is possible for user to change the fields' value and send back to device directly.
    :type builderMode: bool
    :return: final value , which has the same element type or fields defined in schema
    """
    if isinstance(schema, _ArraySchema):
        if isinstance(variant, RscVariant):
            if variant.GetType() != RscType.Array:
                raise ValueError(f"Type Mismatch! Expect Array({schema.name}) but is {variant.GetType().name}")
            _val = variant.GetValue()
            return _receiveArray(schema, _val, builderMode=builderMode)
        elif isinstance(variant, RscSequence):
            return _receiveArray(schema, variant, builderMode=builderMode)
        else:
            raise ValueError(f"Unknow Value type:{type(variant)}")

    elif isinstance(schema, _StructSchema):
        if isinstance(variant, RscVariant):
            if variant.GetType() != RscType.Struct:
                raise ValueError(f"Type Mismatch! Expect Struct({schema.name}) but is {variant.GetType().name}")
            _val = variant.GetValue()
            return _receiveStruct(schema, _val, builderMode=builderMode)
        elif isinstance(variant, RscStructMeta):
            return _receiveStruct(schema, variant, builderMode=builderMode)
        else:
            raise ValueError(f"Unknow Value type:{type(variant)}")


class DataTypeStore:
    """
    This is a helper function for python user to create the equivalent variable model to *IEC61131*, it is the
    most convenient way to construct a complex value such as **Array** and **Struct** for sending or receiving.

    Basic usage:

        .. code:: python

            from PyPlcnextRsc import Device, RscVariant, GUISupplierExample
            from PyPlcnextRsc.Arp.Plc.Gds.Services import IDataAccessService, WriteItem
            from PyPlcnextRsc.tools import DataTypeStore

            if __name__ == "__main__":
                TypeStore = DataTypeStore.fromString(
                    '''
                    TYPE
                    DemoStruct : STRUCT
                        Field1 : INT;
                        Field2 : BOOL;
                    END_STRUCT
                    DemoArray : ARRAY[0..10] OF INT;
                    END_TYPE
                    ''')
                with Device('192.168.1.10', secureInfoSupplier=GUISupplierExample) as device:
                    # create DemoStruct
                    demo1 = TypeStore.NewSchemaInstance("DemoStruct")
                    demo1.Field1 = 123
                    demo1.Field2 = True
                    # create DemoArray
                    demo2 = TypeStore.NewSchemaInstance("DemoArray")
                    demo2[:] = [i * 2 for i in range(11)]
                    # get raw data access service
                    data_access_service = IDataAccessService(device)
                    # Write demo1 to PLCnext
                    data_access_service.Write((WriteItem("Arp.Plc.Eclr/demo1", RscVariant.of(demo1)),))
                    # Read demo1
                    read_item = data_access_service.Read(("Arp.Plc.Eclr/demo1",))[0]
                    rcv_demo1 = TypeStore.ReceiveAsSchemaInstance("DemoStruct", read_item.Value)
                    print(rcv_demo1)
                    # ---------------
                    data_access_service.Write((WriteItem("Arp.Plc.Eclr/demo2", RscVariant.of(demo2)),))
                    read_item = data_access_service.Read(("Arp.Plc.Eclr/demo2",))[0]
                    rcv_demo2 = TypeStore.ReceiveAsSchemaInstance("DemoArray", read_item.Value)
                    print(rcv_demo2)
    """

    @classmethod
    def fromFile(cls, file_or_filename: Union[str, TextIO]):
        """
        Create the DataTypeStore using local file.

        :param file_or_filename: file object or the path of the local file.
        :type file_or_filename: TextIO or str

        """
        try:
            file_contents = file_or_filename.read()
            return cls.fromString(file_contents)
        except AttributeError:
            with open(file_or_filename, 'r') as f:
                ins = cls(f)
            return ins

    @classmethod
    def fromString(cls, string: str):
        """
        Using DataType string to create the DataTypeStore

        :param string: the DataType code.
        :type string: str
        """
        return cls(StringIO(string))

    def __init__(self, SIO):
        lines = list(filter(lambda _l: len(_l) != 0, [_l.split() for _l in SIO.readlines()]))
        lines = _remove_comment(lines)
        _move_TYPE_Label(lines)
        identifiers = []
        for _l in lines:
            identifiers.extend(_l)
        _splitSpecial(identifiers)
        # print(identifiers)
        cursor = _Cursor(identifiers)
        hints = dict()
        if cursor.max < 0:
            ...
            # print("EMPTY")
        while cursor.left > 0:
            _Schema.factory(cursor, hints)
        self._schemas = hints

    def __getitem__(self, item) -> any:
        """
        Get type schema

        :param item: type named defined in DataTypeStore
        :type item: str
        :return: type schema
        """
        return self._getSchema(item)

    def _getSchema(self, item):
        _t = self._schemas.get(item, None)
        if not _t:
            raise ValueError("Unknow Type of " + item)
        return _t

    def NewSchemaInstance(self, data_type_name: str):
        """
        Construct a new data type instance defined by schema
        this instance is used for Write complex data to PLCnext

        .. note::

            In the created instance , all values have been set to its' default value,
            means that if user don't change the element (field) in it, it can also
            send to PLCnext successfully ,but all elements (or fields) are *0*,*0.0*,*False* or *""(empty str)*

        :param data_type_name: type named defined in DataTypeStore
        :type data_type_name: str
        :return: a new data type instance for user to fill elements or fields
        """
        schema = self._getSchema(data_type_name)
        return NewSchemaInstance(schema)

    def ReceiveAsSchemaInstance(self, data_type_name: str, variant: RscVariant, builderMode: bool = False):
        """
        Receive the certain value from PLCnext as data_type defined in schema

        :param data_type_name: type named defined in DataTypeStore
        :type data_type_name: str
        :param variant: from IDataAccessService or ISubscriptionService or some other service , which represent
                        the meta-value of the data_type defined in schema
        :type variant: :py:class:`~PyPlcnextRsc.common.objects.rsc_variant.RscVariant`
        :param builderMode: if set true, all the struct received will be the :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStructBuilder`,
                            so it is possible for user to change the fields' value and send back to device directly.
        :type builderMode: bool
        :return: final value , which has the same element type or fields defined in schema
        """
        schema = self._schemas.get(data_type_name, None)
        return ReceiveAsSchemaInstance(schema, variant, builderMode)
