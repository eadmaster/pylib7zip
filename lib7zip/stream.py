import logging
import os

from .py7ziptypes import IID_IInStream, IID_ISequentialInStream,  IID_IOutStream, IID_ISequentialOutStream

from .wintypes import HRESULT
from .winhelpers import guidp2uuid
from . import ffi, wintypes

from .simplecom import IUnknownImpl
log = logging.getLogger(__name__)

class FileInStream(IUnknownImpl):
    """
            Implementation of IInStream and ISequentialInStream on top of python file-like objects

            Creator responsible for closing the file-like objects.
    """
    GUIDS = {
        IID_IInStream: 'IInStream',
        IID_ISequentialInStream: 'ISequentialInStream',
    }

    def __init__(self, file):
        try:
            path = os.fspath(file)
        except TypeError:
            self.filelike = file
        else:
            self.filelike = open(path, 'rb')
        super().__init__()

    def Read(self, me, data, size, processed_size):
        log.debug('Read size=%d', size)
        buf = self.filelike.read(size)
        psize = len(buf)

        if processed_size != ffi.NULL:
            processed_size[0] = psize

        data[0:psize] = buf[0:psize]
        log.debug('processed size: {}'.format(psize))

        return HRESULT.S_OK.value

    def Seek(self, me, offset, origin, newposition):
        log.debug('Seek offset=%d; origin=%d', offset, origin)
        newpos = self.filelike.seek(offset, origin)
        if newposition != ffi.NULL:
            newposition[0] = newpos
        log.debug('new position: %d', newpos)
        return HRESULT.S_OK.value


class WrapInStream:
    def __init__(self, instream):
        self.instream = instream
        instream.vtable.AddRef(instream)

    def __del__(self):
        if self.instream is not None:
            self.close()

    def close(self):
        if self.instream is not None:
            instream = self.instream
            self.instream = None
            instream.vtable.Release(instream)

    def read(self, size: int) -> bytes:
        buf = ffi.new('char[]', size)
        processed_size = ffi.new('uint32_t[1]')
        self.instream.vtable.Read(self.instream, buf, size, processed_size)
        return ffi.buffer(buf, processed_size[0])[:]

    def seek(self, offset: int, origin: int = 0) -> int:
        newposition = ffi.new('uint64_t[1]')
        self.instream.vtable.Seek(self.instream, offset, origin, newposition)
        return newposition[0]


class FileOutStream(IUnknownImpl):
    """
            Implementation of IOutStream and ISequentialOutStream on top of Python file-like objects.

            Creator is responsible for flushing/closing the file-like object
    """
    GUIDS = {
        IID_IOutStream: 'IOutStream',
        IID_ISequentialOutStream: 'ISequentialOutStream',
    }

    def __init__(self, file):
        try:
            path = os.fspath(file)
        except TypeError:
            self.filelike = file
        else:
            self.filelike = open(path, 'wb')
        super().__init__()

    def Write(self, me, data, size, processed_size):
        log.debug('Write %d', size)
        data_arr = ffi.cast('uint8_t*', data)
        buf = bytes(data_arr[0:size])
        #log.debug('data: %s' % buf.decode('ascii'))
        _processed_size = self.filelike.write(buf)
        processed_size[0] = _processed_size
        log.debug('processed_size: %d', _processed_size)
        return HRESULT.S_OK.value

    def Seek(self, me, offset, origin, newposition):
        log.debug('Seek offset=%d; origin=%d', offset, origin)
        newpos = self.filelike.seek(offset, origin)
        if newposition != ffi.NULL:
            newposition[0] = newpos
        log.debug('new position: %d', newpos)
        return HRESULT.S_OK.value
