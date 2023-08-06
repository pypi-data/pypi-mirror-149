# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

import io

__all__ = ["RscStream"]

from typing import Union


class RscStream:
    """
    This is used to represent a stream object

    Normally used to transfer files with device
    """

    @classmethod
    def ofFile(cls, filePath: str):
        """
        create a RscStream from local file directly

        :param filePath: file path of the local file
        :type filePath: str
        """
        return cls(open(filePath, "rb"))

    @classmethod
    def ofData(cls, data: Union[str, bytes, bytearray]):
        """
        create a RscStream from data directly

        :param data: data to be wrapped in stream object
        :type data: str,bytes,bytearray
        """
        if isinstance(data, str):
            body = data.encode('utf-8')
        elif isinstance(data, (bytes, bytearray)):
            body = data
        elif hasattr(data, 'Read'):
            body = data.read()
        else:
            raise ValueError()
        bs = io.BytesIO()
        bs.write(body)
        bs.seek(0, 0)
        return cls(bs)

    def getBufferIO(self) -> io.BytesIO:
        """
        get the inner IO reference

        :return: bytesIO in this stream
        :rtype: BytesIO
        """
        return self._bytesBuffer

    def getValue(self) -> bytes:
        """
        get all bytes in this stream

        :return: data
        :rtype: bytes
        """
        return self.getBufferIO().getvalue()

    def saveToFile(self, filePath: str):
        """
        save the current stream to file

        .. note::

            this method only call **open(filePath, "wb")** internal , so you must create directory before execute this method if necessary.

        :param filePath: path of the target file to Write
        :type filePath: str
        """
        with open(filePath, "wb") as f:
            f.write(self.getValue())

    def getSize(self):
        """
        get the current byte size in this stream object

        :return: size of bytes
        :rtype: int
        """
        buffer = self.getBufferIO()
        current_position = buffer.tell()
        buffer.seek(0, 2)
        total_length = buffer.tell()
        buffer.seek(current_position)
        return total_length

    def __init__(self, bytesBuffer):
        self._bytesBuffer = bytesBuffer

    def __del__(self):
        self.getBufferIO().close()
    # @classmethod
    # def ofFile(cls, filePath: str):
    #     with open(filePath, "rb") as f:
    #         bs = io.BytesIO()
    #         bs.Write(f.Read())
    #         bs.seek(0, 0)
    #         return cls(bs)
