# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from uuid import UUID

from PyPlcnextRsc.common.exceptions import CommonRemotingClientException, CommonRemotingFatalException
from PyPlcnextRsc.common.internalEnums.string_encoding import RscStringEncoding
from PyPlcnextRsc.common.objects import *
from PyPlcnextRsc.common.tag_type import RscType
from PyPlcnextRsc.common.transport.rsc_datatag_ctx import DataTagContext
from PyPlcnextRsc.common.types import *

__all__ = [
    "Read",
    "ReadValue",
    "Write",
    "WriteValue",
]


def _readUuid(tag, reader) -> UUID:
    buff = reader.ReadDataInternal(16)
    return UUID(bytes=bytes([buff[3], buff[2], buff[1], buff[0], buff[5], buff[4], buff[7], buff[6], buff[8], buff[9], buff[10], buff[11], buff[12], buff[13], buff[14], buff[15]]))


def _writeUuid(tag, writer, value: UUID):
    byte = value.bytes
    writer.WriteDataInternal(
        bytes([byte[3], byte[2], byte[1], byte[0], byte[5], byte[4], byte[7], byte[6], byte[8], byte[9], byte[10], byte[11], byte[12], byte[13], byte[14], byte[15]]))


def _readVersion(tag, reader) -> Version:
    ret = Version()
    ret.major = reader.binaryReader.getSignedInteger()
    ret.minor = reader.binaryReader.getSignedInteger()
    ret.build = reader.binaryReader.getSignedInteger()
    ret.revision = reader.binaryReader.getSignedInteger()
    return ret


def _writeVersion(tag, writer, value: Version):
    writer.binaryWriter.setSignedInteger(value.major)
    writer.binaryWriter.setSignedInteger(value.minor)
    writer.binaryWriter.setSignedInteger(value.build)
    writer.binaryWriter.setSignedInteger(value.revision)


_READER_CONVERT_MAP = {
    RscType.Null: lambda tag, reader: None,
    # RscType.End: ...,
    RscType.Void: lambda tag, reader: None,
    RscType.Bool: lambda tag, reader: reader.binaryReader.getBoolean(),
    RscType.Char: lambda tag, reader:
    reader.binaryReader.getChar('utf_8' if tag.string_encoding == RscStringEncoding.Utf8 else 'ascii' if tag.string_encoding == RscStringEncoding.Ansi else 'utf_16_le'),
    RscType.Int8: lambda tag, reader: reader.binaryReader.getSignedByte(),
    RscType.Uint8: lambda tag, reader: reader.binaryReader.getUnsignedByte(),
    RscType.Int16: lambda tag, reader: reader.binaryReader.getSignedShort(),
    RscType.Uint16: lambda tag, reader: reader.binaryReader.getUnsignedShort(),
    RscType.Int32: lambda tag, reader: reader.binaryReader.getSignedInteger(),
    RscType.IecTime: lambda tag, reader: reader.binaryReader.getSignedInteger(),
    RscType.Uint32: lambda tag, reader: reader.binaryReader.getUnsignedInteger(),
    RscType.Int64: lambda tag, reader: reader.binaryReader.getSignedLong(),
    RscType.IecTime64: lambda tag, reader: reader.binaryReader.getSignedLong(),
    RscType.IecDate64: lambda tag, reader: reader.binaryReader.getSignedLong(),
    RscType.IecDateTime64: lambda tag, reader: reader.binaryReader.getSignedLong(),
    RscType.IecTimeOfDay64: lambda tag, reader: reader.binaryReader.getSignedLong(),
    RscType.Uint64: lambda tag, reader: reader.binaryReader.getUnsignedLong(),
    RscType.Real32: lambda tag, reader: reader.binaryReader.getFloat(),
    RscType.Real64: lambda tag, reader: reader.binaryReader.getDouble(),
    RscType.AnsiString: lambda tag, reader: reader.ReadStringInternal(RscStringEncoding.Ansi, readTag=False),
    RscType.Utf8String: lambda tag, reader: reader.ReadStringInternal(RscStringEncoding.Utf8, readTag=False),
    RscType.Utf16String: lambda tag, reader: reader.ReadStringInternal(RscStringEncoding.Utf16, readTag=False),
    RscType.SecureString: lambda tag, reader: reader.ReadStringInternal(tag.string_encoding, readTag=False, isChars=True),
    RscType.Datetime: lambda tag, reader: reader.ReadDateTime(),
    RscType.Stream: lambda tag, reader: RscStream(reader.ReadStream()),
    RscType.Version: _readVersion,
    RscType.Guid: _readUuid,
    # RscType.String: ...,
    # RscType.Struct: ...,
    # RscType.Array: ...,
    # RscType.Object: ...,
    # RscType.Enumerator: ...,
    # RscType.Enum: ...,
    RscType.Dictionary: ...,  # TODO
    # RscType.SecurityToken: ...,
    RscType.Exception: ...,  # TODO

    # RscType.IecDate: ...,
    # RscType.IecDateTime: ...,
    # RscType.IecTimeOfDay: ...,
}

_WRITER_CONVERT_MAP = {
    RscType.Null: lambda tag, writer, value: ...,
    # RscType.End: ...,
    RscType.Void: lambda tag, writer, value: ...,
    RscType.Bool: lambda tag, writer, value: writer.binaryWriter.setBoolean(value),
    RscType.Char: lambda tag, writer, value:
    writer.binaryWriter.setChar(value, 'utf_8' if tag.string_encoding == RscStringEncoding.Utf8 else 'ascii' if tag.string_encoding == RscStringEncoding.Ansi else 'utf_16_le'),
    RscType.Int8: lambda tag, writer, value: writer.binaryWriter.setSignedByte(value),
    RscType.Uint8: lambda tag, writer, value: writer.binaryWriter.setUnsignedByte(value),
    RscType.Int16: lambda tag, writer, value: writer.binaryWriter.setSignedShort(value),
    RscType.Uint16: lambda tag, writer, value: writer.binaryWriter.setUnsignedShort(value),
    RscType.Int32: lambda tag, writer, value: writer.binaryWriter.setSignedInteger(value),
    RscType.IecTime: lambda tag, writer, value: writer.binaryWriter.setSignedInteger(value),
    RscType.Uint32: lambda tag, writer, value: writer.binaryWriter.setUnsignedInteger(value),
    RscType.Int64: lambda tag, writer, value: writer.binaryWriter.setSignedLong(value),
    RscType.IecTime64: lambda tag, writer, value: writer.binaryWriter.setSignedLong(value),
    RscType.IecDate64: lambda tag, writer, value: writer.binaryWriter.setSignedLong(value),
    RscType.IecDateTime64: lambda tag, writer, value: writer.binaryWriter.setSignedLong(value),
    RscType.IecTimeOfDay64: lambda tag, writer, value: writer.binaryWriter.setSignedLong(value),
    RscType.Uint64: lambda tag, writer, value: writer.binaryWriter.setUnsignedLong(value),
    RscType.Real32: lambda tag, writer, value: writer.binaryWriter.setFloat(value),
    RscType.Real64: lambda tag, writer, value: writer.binaryWriter.setDouble(value),
    RscType.AnsiString: lambda tag, writer, value: writer.WriteStringInternal(value, RscStringEncoding.Ansi, writeTag=False, isChars=False),
    RscType.Utf8String: lambda tag, writer, value: writer.WriteStringInternal(value, RscStringEncoding.Utf8, writeTag=False, isChars=False),
    RscType.Utf16String: lambda tag, writer, value: writer.WriteStringInternal(value, RscStringEncoding.Utf16, writeTag=False, isChars=False),
    RscType.SecureString: lambda tag, writer, value: writer.WriteStringInternal(value, tag.string_encoding, writeTag=False, isChars=True),
    RscType.Datetime: lambda tag, writer, value: writer.WriteDateTime(value),
    RscType.Stream: lambda tag, writer, value: writer.WriteStream(value.getBufferIO(), 0x7FFFFFFF),
    RscType.Version: _writeVersion,
    RscType.Guid: _writeUuid,
    # RscType.String: ...,
    # RscType.Struct: ...,
    # RscType.Array: ...,
    # RscType.Object: ...,
    # RscType.Enumerator: _writeEnumerator,
    # RscType.Enum: ...,
    RscType.Dictionary: ...,  # TODO
    # RscType.SecurityToken: ...,
    RscType.Exception: ...,  # TODO

    # RscType.IecDate: ...,
    # RscType.IecDateTime: ...,
    # RscType.IecTimeOfDay: ...,
}


def _ReadObject(rscClient, tag: DataTagContext = None):
    rsc_reader = rscClient.rscReader
    remoting_reader = rsc_reader.remotingReader
    rcv_tag_context = DataTagContext.Read(remoting_reader)
    rcv_tag_type = rcv_tag_context.rsc_type
    if rcv_tag_type == RscType.Struct and not rscClient.hasDataTagging:
        return None
    return RscVariant(value=ReadValue(rcv_tag_context, rscClient, True, isInObject=True), rscType=rcv_tag_type)


def _WriteObject(tag: DataTagContext, rscClient, value: RscVariant):
    if value is not None and value.GetValue() is not None:
        t = value.GetType()
        if t == RscType.Array:
            tag = DataTagContext(rscType=RscType.Array)
            tag.subTag.append(value.GetArrayElementCtx())
        elif t == RscType.Struct:
            tag = DataTagContext(rscType=RscType.Struct)
            tag.fieldCounts = value.GetFieldCount()
            # for field in value.GetValue():
            #     tag.subTag.append(DataTagContext(rscType=field.GetType(), max_string_length=field.GetMaxStringSize()))
        else:
            tag = DataTagContext(rscType=value.GetType(), max_string_length=tag.max_string_length)
        tag.Write(rscClient.rscWriter.remotingWriter)
        WriteValue(tag, value.GetValue(), rscClient, True, isInObject=True)
    else:
        tag = DataTagContext(rscType=RscType.Void)
        tag.Write(rscClient.rscWriter.remotingWriter)
        WriteValue(tag, None, rscClient, True, isInObject=True)


def ReadValue(tagContext: DataTagContext, rscClient, tagAlreadyRead, isInObject=False) -> any:
    rsc_reader = rscClient.rscReader
    remoting_reader = rsc_reader.remotingReader
    _tag_type = tagContext.rsc_type
    if rscClient.hasDataTagging and not tagAlreadyRead and _tag_type not in [RscType.Object, RscType.Enum, RscType.Dictionary]:
        rcv_tag = DataTagContext.Read(remoting_reader)
        if rcv_tag.rsc_type != _tag_type:
            if rcv_tag.rsc_type == RscType.Exception:
                _tag_type = RscType.Exception
            else:
                raise CommonRemotingClientException(
                    f'Remoting Protocol Violation: expected tag {_tag_type.name}, but received {rcv_tag.rsc_type.name}.')
        if _tag_type == RscType.Struct and tagContext.fieldCounts != rcv_tag.fieldCounts:
            raise CommonRemotingClientException(
                f"Remoting Protocol Violation: expected field count '{tagContext.fieldCounts}', but received '{rcv_tag.fieldCounts}' for struct {tagContext.annotation.__name__}")
        # elif _tag_type == RscType.Array:
        #     if tagContext.subTag[0].rsc_type != rcv_tag.subTag[0].rsc_type:
        #         raise CommonRemotingClientException(f"Array element not match !")
    # TODO move 'if' to Dict
    if _tag_type == RscType.Array:
        ret = []
        for i in range(remoting_reader.ReadArrayLength()):
            ret.append(ReadValue(tagContext.subTag[0], rscClient, True, isInObject))

        if isInObject:
            return RscList(ret).setElementContext(tagContext.subTag[0]) if RscTpGetOrigin(tagContext.annotation) == list else RscTuple(ret).setElementContext(tagContext.subTag[0])
        else:
            return ret if RscTpGetOrigin(tagContext.annotation) == list else tuple(ret)

    elif _tag_type == RscType.Struct:
        tmp = []
        if isInObject:
            field_count = tagContext.fieldCounts
            for i in range(field_count):
                tmp.append(_ReadObject(rscClient, tagContext))
            return RscStructMeta(tmp)
        else:
            for tc in tagContext.subTag:
                tmp.append(ReadValue(tc, rscClient, False))
            return tagContext.annotation(*tmp)

    elif _tag_type == RscType.Object:
        return _ReadObject(rscClient, tagContext)
    elif _tag_type == RscType.SecurityToken:
        return SecurityToken(_ReadObject(rscClient, tagContext))
    elif _tag_type == RscType.Enum:
        val = ReadValue(tagContext.subTag[0], rscClient, tagAlreadyRead)
        return tagContext.annotation(value=val)
    elif _tag_type == RscType.Enumerator:
        rcv_element_tp = DataTagContext.Read(remoting_reader).rsc_type
        defined_elementCtx = tagContext.subTag[0]
        defined_tp = defined_elementCtx.rsc_type
        ret = []
        while rcv_element_tp not in [RscType.End, RscType.Null]:
            if rcv_element_tp != defined_tp:
                raise CommonRemotingFatalException('Protocol violation - invalid enumerator tag, must reflect element type.')
            val = ReadValue(defined_elementCtx, rscClient, True)
            ret.append(val)
            rcv_element_tp = DataTagContext.Read(remoting_reader).rsc_type
        return ret

    else:
        primitive_handle = _READER_CONVERT_MAP.get(_tag_type, None)
        if primitive_handle:
            try:
                cc = primitive_handle(tagContext, remoting_reader)
                return cc
            except Exception as E:
                raise RuntimeError("error occur while Read type of " + str(_tag_type), E)
        else:
            raise RuntimeError("Un implement for Tag " + str(_tag_type))


def WriteValue(tagContext: DataTagContext, value: any, rscClient, tagAlreadyWrite, isInObject=False):
    tagContext.checkValueValid(value)
    rsc_writer = rscClient.rscWriter
    remoting_writer = rsc_writer.remotingWriter
    _tag_type = tagContext.rsc_type
    if rscClient.hasDataTagging and not tagAlreadyWrite and _tag_type not in [RscType.Object, RscType.Enum, RscType.Dictionary]:
        # Special check for Array
        if _tag_type == RscType.Array and len(tagContext.subTag) == 0:
            assert isinstance(value, RscSequence)
            tagContext.subTag.append(value.getElementContext())
        tagContext.Write(remoting_writer)
    # TODO move 'if' to Dict
    if _tag_type == RscType.Array:
        assert value is not None
        remoting_writer.WriteArrayLength(len(value))
        for element in value:
            WriteValue(tagContext.subTag[0], element, rscClient, True)
        return
    elif _tag_type == RscType.Struct:
        assert value is not None
        if isInObject:
            if isinstance(value, RscStructMeta):
                for field in value:
                    _WriteObject(tagContext, rscClient, field)
            else:
                raise RuntimeError()
        else:
            for idx, field in enumerate(GetFieldFromInstance(value)):
                c = tagContext.subTag[idx]
                WriteValue(c, field, rscClient, False)

    elif _tag_type == RscType.Object:
        _WriteObject(tagContext, rscClient, value)

    elif _tag_type == RscType.SecurityToken:
        assert value is not None
        _WriteObject(tagContext, rscClient, value.getValue())

    elif _tag_type == RscType.Enum:
        c = tagContext.subTag[0]
        if value is None:
            if hasattr(tagContext.annotation, "NONE"):
                item = tagContext.annotation["NONE"].value
            elif hasattr(tagContext.annotation, "Null"):
                item = tagContext.annotation["Null"].value
            else:
                raise ValueError(f"Must provide an item in enum({tagContext.annotation.__name__}), not None !")
        else:
            item = value.value
        WriteValue(c, item, rscClient, tagAlreadyWrite)

    elif _tag_type == RscType.Enumerator:
        # TODO Not covered and tested
        # if tagContext.subTag[0].rsc_type == RscType.Object:
        #     for val in value:
        #         _WriteObject(tagContext.subTag[0], rscClient, val)
        # else:
        for val in value:
            # tagContext.subTag[0].Write(remoting_writer)
            WriteValue(tagContext.subTag[0], val, rscClient, False)
        remoting_writer.WriteTag(RscType.Null)

    else:
        primitive_handle = _WRITER_CONVERT_MAP.get(_tag_type, None)
        if primitive_handle:
            try:
                primitive_handle(tagContext, remoting_writer, value)
            except Exception as E:
                raise RuntimeError("error occur while Write type of " + str(_tag_type), E)
            return
        else:
            raise RuntimeError("Un implement for Tag " + str(_tag_type))


def Read(valueAnnotation, client):
    ctx = DataTagContext.factory(valueAnnotation)
    return ReadValue(ctx, client, False)


def Write(value, valueAnnotation, client):
    ctx = DataTagContext.factory(valueAnnotation)
    WriteValue(ctx, value, client, False)
