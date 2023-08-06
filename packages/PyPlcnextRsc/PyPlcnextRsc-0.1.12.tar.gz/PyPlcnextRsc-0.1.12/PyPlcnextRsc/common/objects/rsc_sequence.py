# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.
from collections.abc import Iterable, Sized
from copy import deepcopy

from PyPlcnextRsc.common.exceptions import InvalidOperationException
from PyPlcnextRsc.common.tag_type import RscType

__all__ = [
    "RscSequence",
    "RscList",
    "RscTuple",
]


class RscSequence:
    """
    COMMON ABSTRACT CLASS FOR :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList` & :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscTuple`

    ALSO USED IN USER STRUCT DEF
    """

    def setElementRscType(self, rscType: RscType):
        """
        Configure the sequence by passing in primitive type (:py:class:`~PyPlcnextRsc.common.tag_type.RscType`)

        .. warning::

            This method only support primitive types,

            If next-dimension is *Array*, use :py:func:`~PyPlcnextRsc.common.objects.rsc_sequence.RscSequence.setNextDimension` instead.

            else if element is *Struct*, use :py:func:`~PyPlcnextRsc.common.objects.rsc_sequence.RscSequence.setElementAnnotate` instead.

        :param rscType: the element type
        :type rscType: :py:class:`~PyPlcnextRsc.common.tag_type.RscType`
        :return: self

        """
        if rscType == RscType.Array:
            raise InvalidOperationException("use setNextDimension instead")
        if rscType == RscType.Struct:
            raise InvalidOperationException("use setElementAnnotate instead")
        from PyPlcnextRsc.common.transport.rsc_datatag_ctx import DataTagContext
        ctx = DataTagContext(rscType=rscType)
        self.setElementContext(ctx)
        return self

    def setElementAnnotate(self, annotate):
        """
        Configure by annotate

        Used if element type is Primitive type or :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct`

        :param annotate: field type annotation ,

                    such as 'RscTpAnnotate[int, Marshal(rscType=RscType.Int16)]' or defined :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct`

        :return: self

        """
        from PyPlcnextRsc.common.objects.rsc_struct import RscStructBuilder
        from PyPlcnextRsc.common.transport.rsc_datatag_ctx import DataTagContext
        if isinstance(annotate, RscStructBuilder):
            annotate = annotate._proto
        ctx = DataTagContext.factory(annotate)
        self.setElementContext(ctx)
        return self

    def setNextDimension(self, nextDimension):
        """
        Configure by next :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscSequence` or :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList`

        .. warning::

            Only used for define a multi-dimension array.

        :param nextDimension: next configured :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscSequence` or :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList`
        :type nextDimension: :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscSequence` or factory of :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList`
        :return: self

        """
        if id(nextDimension) == id(self):
            raise InvalidOperationException("can not add self as next dimension")
        if isinstance(nextDimension, RscSequence):
            setattr(self, '_next_dimension', nextDimension)
        # factory
        elif hasattr(nextDimension, 'getSingleton'):
            setattr(self, '_next_dimension', nextDimension.getSingleton())
        else:
            raise InvalidOperationException("should pass in 'RscSequence' instance or 'RscList.factory' instance")
        return self

    # ----------------------------------------------------------------

    def getElementRscType(self) -> RscType:
        """
        Get the :py:class:`~PyPlcnextRsc.common.tag_type.RscType` of the element.

        :return: the :py:class:`~PyPlcnextRsc.common.tag_type.RscType` of the element.
        :rtype: RscType

        """
        # 注意这个不能用于向RSC发送（array标签不完整）
        if hasattr(self, '_element_context'):
            return self._element_context.rsc_type
        if hasattr(self, '_next_dimension'):
            return RscType.Array
        return RscType.Null

    def setElementContext(self, context):
        """
        Set the DataTagContext of the element, this is used internally.

        :param context: DataTagContext of the element

        """
        # also called when reading array from PLC
        setattr(self, '_element_context', context)
        return self

    def getElementContext(self):
        """
        Get the DataTagContext of the element,, this is used internally.

        :return: DataTagContext

        """
        # used when writing array to PLC
        ret = getattr(self, '_element_context', None)
        if ret is None:
            _nd = getattr(self, '_next_dimension', None)
            if _nd is None:
                raise InvalidOperationException("missing array information")
            from PyPlcnextRsc.common.transport import DataTagContext
            ret = DataTagContext(rscType=RscType.Array)
            ret.subTag.append(_nd.getElementContext())
            self.setElementContext(ret)
        return ret

    def setDesireLength(self, length):
        """
        if the desire length is set, the framework will check the length before sending to device.
        this will auto set by :py:class:`PyPlcnextRsc.tools.PlcDataTypeSchema` internally.

        :param length: the desired length of this sequence.
        :type length: int
        """
        self._desire_length = length

    def getDesireLength(self):
        """
        Get the desired length internal. if not set return -1

        :return: the desired length , -1 if not set
        :rtype: int
        """
        if hasattr(self, '_desire_length'):
            return self._desire_length
        else:
            return -1


class RscList(list, RscSequence):
    """
    Use List to represent an array for transferring with device.


    .. tip::

        Since V0.1.4 :

            '_friendlyMode' :

                if an element is struct type in this array , use this method is quick !

                .. code:: python

                    MyArrayOfStruct[1] = {"Field1": 200, "Field2": False}  # or (200,False) or [200,False]
                    MyArrayOfStruct[2] = (300, True)

                and  this can override all above values (this example showed '[:]' you can
                use other slice which you want such as '[0:8]' '[1:-1]'... )

                .. code:: python

                    MyArrayOfStruct[:] = [{"Field1": 200, "Field2": False}, (200, True), (300, True)]

    """

    class _factory:
        FACTORIES = {}

        @classmethod
        def get(cls, funcName, *args):
            key = (funcName, args)
            if key in cls.FACTORIES:
                return cls.FACTORIES[key]
            else:
                ret = cls(funcName, *args)
                cls.FACTORIES[key] = ret
            return ret

        def __init__(self, funcName, *args):
            self._funcName = funcName
            self._arguments = args
            self._singleton = RscList()
            if hasattr(self._singleton, funcName):
                getattr(self._singleton, funcName)(*args)
            else:
                raise InvalidOperationException("wrong funcName :" + self._funcName)

        def create(self, *args, **kwargs):
            ret = RscList(*args, **kwargs)
            return getattr(ret, self._funcName)(*self._arguments)

        def getSingleton(self):
            return self._singleton

    @classmethod
    def factory(cls, funcName, *args):
        """
        Make a *RscList* factory, this is only a helper function to create :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList` of same structure.

        Usage:

            .. code:: python

                middle_layer_factory = RscList.factory('createNextDimension', RscType.Int16, 3)
                middle1 = middle_layer_factory.create()
                middle1[0].extend((1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 11))
                middle1[1].extend((1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 11))
                middle1[2].extend((1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 11))

                middle2 = middle_layer_factory.create()
                middle2[0].extend((2, 1, 0, 1, 1, 1, 1, 1, 1, 1, 11))
                middle2[1].extend((2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 11))
                middle2[2].extend((2, 3, 2, 1, 1, 1, 1, 1, 1, 1, 11))

                outer = RscList((middle1, middle2)).setNextDimension(middle_layer_factory)

        :param funcName: the exist function name for configure the :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList`.
        :type funcName: str
        :param args: the function arguments corresponding to the 'funcName'.
        :return: return a factory instance , which has a **create()** method to call for construct a new :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList`
                by the provided parameters.

        """
        return cls._factory.get(funcName, *args)

    def setOffset(self, offset: int):
        """
        Set the start offset of this array object , because in *IEC61131*, an array can be defined with lower bound not equal to *0*

        .. warning::
            Although lower bound not equal to *0* is acceptable by this method, but still not recommend to use that kind of array definition! because it can be confused.
            and slice function of python can not work normally if use negative index.

        :param offset: lower bound of the array
        :type offset: int

        """
        self._offset = offset

    def _useFriendlyMode(self):
        return getattr(self, "_friendlyMode", True) is True

    def __getitem__(self, item):
        return super().__getitem__(self.__applyOffset(item))

    def __setitem__(self, key, gived_value):
        offset = self.__applyOffset(key)
        _friendly = self._useFriendlyMode()
        if type(offset) == slice:
            # this part handle 'RscListInstance[:] = [[1,2],[1,2],[1,2]]',transmitting the operation to element RscStructBuilder's _internal_setter if condition fits
            if _friendly and isinstance(gived_value, (Iterable, Sized)):
                vals = super().__getitem__(offset)
                if len(vals) != len(gived_value):
                    raise ValueError(f"Expect {len(vals)} element{'s' if len(vals) > 1 else ''} in array, but supplied {len(gived_value)} !")

                if self.getElementRscType() == RscType.Struct:
                    for selfVal, gived_val in zip(vals, gived_value):
                        assert hasattr(selfVal, '_getRscStruct')
                        if not hasattr(gived_value, "_getRscStruct"):
                            selfVal._internal_setter(gived_val)
                        else:
                            # the value index in RawList (because use slice we can't ensure the order, so here use self.index()
                            idx = self.index(selfVal)
                            super().__setitem__(idx, gived_val)
                # elif self.getElementRscType() == RscType.Array:
                #     ...
                else:
                    return super().__setitem__(offset, gived_value)
            else:
                return super().__setitem__(offset, gived_value)
        elif _friendly:
            # this part handle 'RscListInstance[X] = [1,2]',
            # transmitting the operation to element(RscStructBuilder or RscList)'s _internal_setter if condition fits
            selfVal = super().__getitem__(offset)
            if self.getElementRscType() == RscType.Struct and hasattr(selfVal, '_getRscStruct') and not hasattr(gived_value, "_getRscStruct"):
                selfVal._internal_setter(gived_value)
            elif self.getElementRscType() == RscType.Array and isinstance(selfVal, RscList) and not isinstance(gived_value, RscList):
                selfVal._internal_setter(gived_value)
            else:
                return super().__setitem__(offset, gived_value)
        else:
            return super().__setitem__(offset, gived_value)

    def _internal_setter(self, value):
        """fill this array at once using tuple or list or other array-like object"""
        if not isinstance(value, (Iterable, Sized)):
            raise ValueError("Must use Iterable and Sized type value (such as tuple, list) to fill the array")
        if len(self) != len(value):
            raise ValueError(f"Expect {len(self)} element{'s' if len(self) > 1 else ''} in array, but is {len(value)} !")
        self[:] = value  # override the content

    def __applyOffset(self, item):
        # deal with situation if defined like ARRAY[-10..10] or ARRAY[1..10]
        if hasattr(self, "_offset") and self._offset != 0:
            _offset = self._offset
            _t = type(item)
            if _t == int:
                item = item - _offset
            elif _t == slice:
                start = item.start - _offset
                stop = item.stop - _offset
                item = slice(start, stop, item.step)
        return item

    def __repr__(self):
        return f"RscList<{self.getElementRscType().name}>" + super().__repr__()

    def createNextDimension(self, elementRscType: RscType, count: int, reserve: int = 0, default: any = None):
        """
        Helper function to create next dimension ,only support for primitive python type as next dimension's element type!

        :param elementRscType: :py:class:`~PyPlcnextRsc.common.tag_type.RscType` of the element
        :type elementRscType: :py:class:`~PyPlcnextRsc.common.tag_type.RscType`
        :param count: the count of element in current dimension to reserve
        :type count: int
        :param reserve: the count of element in next dimension to reserve
        :type count: int
        :param default: the value to fill in next dimension
        :return: self

        """
        self.setNextDimension(RscList().setElementRscType(elementRscType, reserve, default), count)
        # self.clear()
        # for i in range(count):
        #     inner = RscList().setElementRscType(elementRscType, reserve, default)
        #     self.append(inner)
        return self

    def reserve(self, reserve: int = 0, default: any = None, use_deepcopy: bool = False):
        """
        Use the provided value(default) to fill the array

        :param reserve: element count to reserve
        :type reserve: int
        :param default: the value to fill
        :param use_deepcopy: true if use deepcopy to fill the element,default is False
        :type use_deepcopy: bool

        """
        if reserve > 0:
            left = reserve - len(self)
            if left > 0:
                if use_deepcopy:
                    for _ in range(left):
                        self.append(deepcopy(default))
                else:
                    self.extend([default] * left)

    def setElementRscType(self, rscType: RscType, reserve: int = 0, default: any = None):
        """
        Overload the :py:func:`~PyPlcnextRsc.common.objects.rsc_sequence.RscSequence.setElementRscType`, add the :py:func:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList.reserve` method.

        :param rscType: the element type
        :type rscType: :py:class:`~PyPlcnextRsc.common.tag_type.RscType`
        :param reserve: element count to reserve
        :type reserve: int
        :param default: the value to fill

        """
        self.reserve(reserve, default)
        super().setElementRscType(rscType)
        return self

    def setElementAnnotate(self, annotate, reserve: int = 0, default: any = None):
        """
        Overload the :py:func:`~PyPlcnextRsc.common.objects.rsc_sequence.RscSequence.setElementAnnotate`, add the :py:func:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList.reserve` method.

        :param annotate: field type annotation ,

                    such as 'RscTpAnnotate[int, Marshal(rscType=RscType.Int16)]' or defined :py:class:`~PyPlcnextRsc.common.objects.rsc_struct.RscStruct`

        :param reserve: element count to reserve
        :type reserve: int
        :param default: the value to fill

        """

        self.reserve(reserve, default, True)
        super().setElementAnnotate(annotate)
        return self

    def setNextDimension(self, nextDimension, count: int = None):
        """
        Overload the :py:func:`~PyPlcnextRsc.common.objects.rsc_sequence.RscSequence.setNextDimension`, add support for reserve.

        :param nextDimension: next configured :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscSequence` or :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList`
        :type nextDimension: :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscSequence` or factory of :py:class:`~PyPlcnextRsc.common.objects.rsc_sequence.RscList`
        :param count: element count to reserve
        :type count: int
        :return: self

        """
        super().setNextDimension(nextDimension)
        if count:
            self.clear()
            # is factory
            if hasattr(nextDimension, 'getSingleton'):
                self.reserve(count, nextDimension.create(), True)
            else:
                self.reserve(count, nextDimension, True)
        return self

    def __eq__(self, other):
        """
        Overload the list.__eq__, now must the other element's :py:class:`~PyPlcnextRsc.common.tag_type.RscType`
        same with self's element type is possible to return True

        :param other: other instance to compare
        :return: true if 'other' is same with self

        """
        if super(RscList, self).__eq__(other):
            try:
                return other.getElementRscType() == self.getElementRscType()
            except:
                pass
        return False


class RscTuple(tuple, RscSequence):
    """
    Use Tuple to represent an array for transferring with device

    """

    def __repr__(self):
        return f"RscTuple<{self.getElementRscType().name}>" + super().__repr__()

    def setOffset(self, offset):
        """
        see doc from :py:func:`PyPlcnextRsc.common.objects.rsc_sequence.RscList.setOffset`

        """
        self._offset = offset

    def __getitem__(self, item):
        return super().__getitem__(self.__applyOffset(item))

    def __applyOffset(self, item):
        if hasattr(self, "_offset") and self._offset != 0:
            _offset = self._offset
            _t = type(item)
            if _t == int:
                item = item - _offset
            elif _t == slice:
                start = item.start - _offset
                stop = item.stop - _offset
                item = slice(start, stop, item.step)
        return item

    def __eq__(self, other):
        """
        Overload the tuple.__eq__, now must the other element's :py:class:`~PyPlcnextRsc.common.tag_type.RscType`
        same with self's element type is possible to return True

        :param other: other instance to compare
        :return: true if 'other' is same with self

        """
        if super(RscTuple, self).__eq__(other):
            try:
                return other.getElementRscType() == self.getElementRscType()
            except:
                pass
        return False
