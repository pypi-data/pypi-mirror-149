# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.
from PyPlcnextRsc.common.exceptions import InvalidOperationException
from PyPlcnextRsc.common.objects import RscStructMeta, RscStructBuilder, RscSequence, isRscStructInstance
from PyPlcnextRsc.common.tag_type import RscType
from PyPlcnextRsc.common.types.rsc_types import RscTpIntEnum

__all__ = [
    'RscVariant'
]

from PyPlcnextRsc.common.serviceDefinition.marshal import Marshal


class RscVariant:
    """
    This is used to represent an data-object (py-value with its' RscType)

    Create a RscVariant object by providing both the definite :py:class:`~PyPlcnextRsc.common.tag_type.RscType` and python value

    :param value: Python value which to be wrapped in.
    :param rscType: the definite type of the value.

                    .. note::
                        If you are just make RscVariant object mapped to *IEC61131*, use :py:class:`~PyPlcnextRsc.common.tag_type.IecType` is more concrete

    :type rscType: :py:class:`~PyPlcnextRsc.common.tag_type.RscType`

    """

    def __class_getitem__(cls, item):
        """
        for Annotation
        """
        if type(item) == int:
            from PyPlcnextRsc.common.types import RscTpAnnotate

            return RscTpAnnotate[cls, Marshal(maxStringSize=item)]
        else:
            raise ValueError()

    @classmethod
    def of(cls, value):
        """
        Create RscVariant from some special python object that :py:class:`~PyPlcnextRsc.common.tag_type.RscType` is clearly to tell from

            .. warning::
                This is not suitable for some value that is ambiguous , for example you give number 100 use this method,
                but for this method it is not possible to know which `INT` (or in other word, which :py:class:`~PyPlcnextRsc.common.tag_type.RscType`)you are talking about:
                it shell be :py:const:`PyPlcnextRsc.common.tag_type.RscType.Uint8` ? :py:const:`PyPlcnextRsc.common.tag_type.RscType.Int16` ? or :py:const:`PyPlcnextRsc.common.tag_type.RscType.Int64` ...?

                So in this case, you must use :py:func:`~PyPlcnextRsc.common.objects.rsc_variant.RscVariant.__init__` to give the :py:class:`~PyPlcnextRsc.common.tag_type.RscType` explicitly.

        - bool value : the :py:const:`PyPlcnextRsc.common.tag_type.RscType.Bool` will be filled
        - str value : the :py:const:`PyPlcnextRsc.common.tag_type.RscType.Utf8String` will be filled
        - :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscTuple` or :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList` : the :py:const:`PyPlcnextRsc.common.tag_type.RscType.Array` will be filled
        - :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStructMeta` or :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStructBuilder` :the :py:const:`PyPlcnextRsc.common.tag_type.RscType.Struct` will be filled

        :return: RscVariant instance
        """
        _type = type(value)
        if _type == bool:
            return cls(value, RscType.Bool)
        elif _type == str:
            return cls(value, RscType.Utf8String)
        elif isinstance(value, RscSequence):
            return cls(value, RscType.Array)
        elif isinstance(value, RscStructMeta):
            return cls(value, RscType.Struct)
        elif isRscStructInstance(value) or isinstance(value, RscStructBuilder):
            return cls(RscStructMeta.fromInstance(value), rscType=RscType.Struct)
        # TODO ...
        else:
            raise InvalidOperationException("Use __init__ to create RscVariant with its' RscType instead !")

    @classmethod
    def ofEnum(cls, item):
        if not isinstance(item, RscTpIntEnum):
            raise InvalidOperationException("Use __init__ to create RscVariant with its' RscType instead !")
        from PyPlcnextRsc.common.transport.rsc_datatag_ctx import _GetMarshalFromEnum
        _t = type(item)
        return cls(item.value, rscType=_GetMarshalFromEnum(_t).rscType)

    def __init__(self, value, rscType: RscType):
        self._type = rscType
        self._value = value

    def __repr__(self):
        return f"Variant<{self._type.name}>({str(self._value)})"

    __str__ = __repr__

    def GetValue(self) -> any:
        """
        Get the python value in this RscVariant object.

        :return: any python value that represent the corresponding value from PLC

                ..  note::
                    Special case of :py:class:`~PyPlcnextRsc.common.tag_type.RscType`

                    - :py:const:`PyPlcnextRsc.common.tag_type.RscType.Array` : the value type might be :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList`
                    - :py:const:`PyPlcnextRsc.common.tag_type.RscType.Struct`: the value type might be :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStructMeta`

        """
        return self._value

    # def GetValueAsEnum(self,enum):
    #     # TODO

    def GetType(self) -> RscType:
        """
        Get the :py:class:`~PyPlcnextRsc.common.tag_type.RscType` corresponding to the contained value.

        :rtype: RscType
        """
        return self._type

    def GetArrayElementCtx(self):
        """This method is mainly for internal use, to get the element context while this object contains *Array*"""
        if self._type == RscType.Array:
            if isinstance(self._value, RscSequence):
                return self._value.getElementContext()
            else:
                raise InvalidOperationException("only array type value ( RscList or RscTuple ) support, but is " + str(self._value))
        else:
            raise InvalidOperationException("only array type support , but is " + str(self._type))

    def GetFieldCount(self):
        """This method is mainly for internal use, to get the field counts while this object contain *Struct*"""
        if self._type == RscType.Struct:
            if isinstance(self._value, RscStructMeta):
                return len(self._value)
            else:
                raise InvalidOperationException("only struct type value ( RscStructMeta ) support, but is " + str(self._value))
        else:
            raise InvalidOperationException("only struct type support , but is " + str(self._type))

    def __eq__(self, other):
        if type(other) == RscVariant:
            return self.GetType() == other.GetType() and self.GetValue() == other.GetValue()
        else:
            return False
