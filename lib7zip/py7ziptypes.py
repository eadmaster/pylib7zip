import uuid
from .comtypes import CDEF_IUnknown
from string import Template
from enum import Enum, IntEnum

CDEFS = Template('''
typedef uint32_t PROPID; /*actually an enum, often a different enum for each function...*/

typedef struct {
	$CDEF_IUnknown
	HRESULT (*Read)(void* self, uint8_t *data, uint32_t size, uint32_t *processedSize);
} _ISequentialInStream_vtable;

typedef struct{
	_ISequentialInStream_vtable* vtable;
} ISequentialInStream;

typedef struct {
	$CDEF_IUnknown
	/* Inherited from ISequentialInStream */
	HRESULT (*Read)(void* self, uint8_t *data, uint32_t size, uint32_t *processedSize);
	/* Own methods */
	HRESULT (*Seek)(void* self, int64_t offset, uint32_t seekOrigin, uint64_t *newPosition);
} _IInStream_vtable;

typedef struct{
	_IInStream_vtable* vtable;
} IInStream;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*Write)(void* self, const void *data, uint32_t size, uint32_t *processedSize);
	/*
	if (size > 0) this function must write at least 1 byte.
	This function is allowed to write less than "size".
	You must call Write function in loop, if you need to write exact amount of data
	*/
	HRESULT (*Seek)(void* self, int64_t offset, uint32_t seekOrigin, uint64_t *newPosition);
} _IOutStream_vtable;

typedef struct {
	_IOutStream_vtable* vtable;
} IOutStream;

typedef IOutStream ISequentialOutStream;
typedef _IOutStream_vtable _ISequentialOutStream_vtable;

typedef struct {
	$CDEF_IUnknown
	HRESULT(*SetTotal)(void* self, const uint64_t *files, const uint64_t *bytes);
	HRESULT(*SetCompleted)(void* self, const uint64_t *files, const uint64_t *bytes);
} _IArchiveOpenCallback_vtable;

typedef struct {
	_IArchiveOpenCallback_vtable* vtable;
} IArchiveOpenCallback;

typedef struct {
	$CDEF_IUnknown
	HRESULT(*GetStream)(void* self, uint32_t index, ISequentialInStream **stream);
} IInArchiveGetStream_vtable;

typedef struct {
	IInArchiveGetStream_vtable* vtable;
} IInArchiveGetStream;

typedef struct {
	$CDEF_IUnknown
	HRESULT(*SetTotal)(void* self, uint64_t total);
	HRESULT(*SetCompleted)(void* self, const uint64_t *completeValue);
	HRESULT(*GetStream)(void* self, uint32_t index, ISequentialOutStream **outStream,  int32_t askExtractMode);
	HRESULT(*PrepareOperation)(void* self, int32_t askExtractMode);
	HRESULT(*SetOperationResult)(void* self, int32_t resultEOperationResult);
} _IArchiveExtractCallback_vtable;

typedef struct {_IArchiveExtractCallback_vtable* vtable; } IArchiveExtractCallback;

typedef struct {
	$CDEF_IUnknown
	HRESULT(*SetRatioInfo)(void* self, const uint64_t *inSize, const uint64_t *outSize);
} _ICompressProgressInfo_vtable;
typedef struct {_ICompressProgressInfo_vtable* vtable;} ICompressProgressInfo;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*Open)(void* self, IInStream *stream, const uint64_t *maxCheckStartPosition, IArchiveOpenCallback *openArchiveCallback);
	HRESULT (*Close)(void* self);
	HRESULT (*GetNumberOfItems)(void* self, uint32_t *numItems);
	HRESULT (*GetProperty)(void* self, uint32_t index, PROPID propID, PROPVARIANT *value);
	HRESULT (*Extract)(void* self, const uint32_t* indices, uint32_t numItems, uint32_t testMode, IArchiveExtractCallback *extractCallback);
	HRESULT (*GetArchiveProperty)(void* self, PROPID propID, PROPVARIANT *value);
	HRESULT (*GetNumberOfProperties)(void* self, uint32_t *numProperties);
	HRESULT (*GetPropertyInfo)(void* self, uint32_t index, wchar_t **name, PROPID *propID, VARTYPE *varType);
	HRESULT (*GetNumberOfArchiveProperties)(void* self, uint32_t *numProperties);
	HRESULT (*GetArchivePropertyInfo)(void* self, uint32_t index, wchar_t **name, PROPID *propID, VARTYPE *varType);
} _IInArchive_vtable;

typedef struct {
	_IInArchive_vtable* vtable;
} IInArchive;

typedef struct {
	$CDEF_IUnknown
	HRESULT(*GetNumberOfMethods)(void* self, uint32_t *numMethods);
	HRESULT(*GetProperty)(void* self, uint32_t index, PROPID propID, PROPVARIANT *value);
	HRESULT(*CreateDecoder)(void* self, uint32_t index, const GUID *iid, void **coder);
	HRESULT(*CreateEncoder)(void* self, uint32_t index, const GUID *iid, void **coder);
 } _ICompressCodecsInfo_vtable;

typedef struct {
	_ICompressCodecsInfo_vtable* vtable;
} ICompressCodecsInfo;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*SetCompressCodecsInfo)(void* self, ICompressCodecsInfo *compressCodecsInfo);
} _ISetCompressCodecsInfo_vtable;

typedef struct {_ISetCompressCodecsInfo_vtable* vtable;} ISetCompressCodecsInfo;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*CryptoGetTextPassword)(void* self, wchar_t **password);
} _ICryptoGetTextPassword_vtable;
typedef struct { _ICryptoGetTextPassword_vtable* vtable;} ICryptoGetTextPassword;
 
typedef struct {
	$CDEF_IUnknown
	HRESULT (*CryptoGetTextPassword2)(void* self, int* isdefined, wchar_t **password);
} _ICryptoGetTextPassword2_vtable;
typedef struct { _ICryptoGetTextPassword2_vtable* vtable;} ICryptoGetTextPassword2;
 
typedef struct {
	$CDEF_IUnknown
	HRESULT (*GetProperty)(void* self, PROPID propID, PROPVARIANT *value);
	HRESULT (*GetStream)(void* self, const wchar_t *name, IInStream **inStream);
} _IArchiveOpenVolumeCallback_vtable;
typedef struct { _IArchiveOpenVolumeCallback_vtable* vtable; } IArchiveOpenVolumeCallback;

typedef struct {
	$CDEF_IUnknown
	HRESULT (*SetSubArchiveName)(void* self, const wchar_t *name);
} _IArchiveOpenSetSubArchiveName_vtable;
typedef struct { _IArchiveOpenSetSubArchiveName_vtable* vtable; } IArchiveOpenSetSubArchiveName;
'''
                 ).substitute(CDEF_IUnknown=CDEF_IUnknown)

class FormatProps(IntEnum):
    kName = 0
    kClassID = 1
    kExtension = 2
    kAddExtension = 3
    kUpdate = 4
    kKeepName = 5
    kStartSignature = 6
    kFinishSignature = 7
    kAssociate = 8

class MethodProps(IntEnum):
    kID = 0
    kName = 1
    kDecoder = 2
    kEncoder = 3
    kInStreams = 4
    kOutStreams = 5
    kDescription = 6
    kDecoderIsAssigned = 7
    kEncoderIsAssigned = 8


def createIID(yy, xx):
    return uuid.UUID('{{23170F69-40C1-278A-0000-00{yy:s}00{xx:s}0000}}'.format(xx=xx, yy=yy))
#00 IProgress.h

IID_IProgress = createIID('00', '05')

#01 IFolderArchive.h

IID_IArchiveFolder = createIID('01', '05')
IID_IFolderArchiveExtractCallback = createIID('01', '07')
IID_IOutFolderArchive = createIID('01', '0A')
IID_IFolderArchiveUpdateCallback = createIID('01', '0B')
IID_IArchiveFolderInternal = createIID('01', '0C')
IID_IInFolderArchive = createIID('01', '0E')

#03 IStream.h

IID_ISequentialInStream = createIID('03', '01')
IID_ISequentialOutStream = createIID('03', '02')
IID_IInStream = createIID('03', '03')
IID_IOutStream = createIID('03', '04')
IID_IStreamGetSize = createIID('03', '06')
IID_IOutStreamFlush = createIID('03', '07')


#04 ICoder.h

IID_ICompressProgressInfo = createIID('04', '04')
IID_ICompressCoder = createIID('04', '05')
IID_ICompressCoder2 = createIID('04', '18')
IID_ICompressSetCoderProperties = createIID('04', '20')
IID_ICompressSetDecoderProperties2 = createIID('04', '22')
IID_ICompressWriteCoderProperties = createIID('04', '23')
IID_ICompressGetInStreamProcessedSize = createIID('04', '24')
IID_ICompressSetCoderMt = createIID('04', '25')
IID_ICompressGetSubStreamSize = createIID('04', '30')
IID_ICompressSetInStream = createIID('04', '31')
IID_ICompressSetOutStream = createIID('04', '32')
IID_ICompressSetInStreamSize = createIID('04', '33')
IID_ICompressSetOutStreamSize = createIID('04', '34')
IID_ICompressSetBufSize = createIID('04', '35')
IID_ICompressFilter = createIID('04', '40')
IID_ICompressCodecsInfo = createIID('04', '60')
IID_ISetCompressCodecsInfo = createIID('04', '61')
IID_ICryptoProperties = createIID('04', '80')
IID_ICryptoResetSalt = createIID('04', '88')
IID_ICryptoResetInitVector = createIID('04', '8C')
IID_ICryptoSetPassword = createIID('04', '90')
IID_ICryptoSetCRC = createIID('04', 'A0')


#05 IPassword.h

IID_ICryptoGetTextPassword = createIID('05', '10')
IID_ICryptoGetTextPassword2 = createIID('05', '11')


#06 IArchive.h

IID_ISetProperties = createIID('06', '03')
IID_IArchiveOpenCallback = createIID('06', '10')
IID_IArchiveExtractCallback = createIID('06', '20')
IID_IArchiveOpenVolumeCallback = createIID('06', '30')
IID_IInArchiveGetStream = createIID('06', '40')
IID_IArchiveOpenSetSubArchiveName = createIID('06', '50')
IID_IInArchive = createIID('06', '60')
IID_IArchiveOpenSeq = createIID('06', '61')

IID_IArchiveUpdateCallback = createIID('06', '80')
IID_IArchiveUpdateCallback2 = createIID('06', '82')
IID_IOutArchive = createIID('06', 'A0')


#08 IFolder.h
IID_IFolderFolder = createIID('08', '00')
IID_IEnumProperties = createIID('08', '01')
IID_IFolderGetTypeID = createIID('08', '02')
IID_IFolderGetPath = createIID('08', '03')
IID_IFolderWasChanged = createIID('08', '04')
IID_IFolderOperations = createIID('08', '06')
IID_IFolderGetSystemIconIndex = createIID('08', '07')
IID_IFolderGetItemFullSize = createIID('08', '08')
IID_IFolderClone = createIID('08', '09')
IID_IFolderSetFlatMode = createIID('08', '0A')
IID_IFolderOperationsExtractCallback = createIID('08', '0B')
IID_IFolderProperties = createIID('08', '0E')
IID_IFolderArcProps = createIID('08', '10')
IID_IGetFolderArcProps = createIID('08', '11')

#09 IFolder.h :: FOLDER_MANAGER_INTERFACE
#IID_IFolderManager = createIID('09', '00')


#0A PluginInterface.h
#IID_IInitContextMenu = createIID('0A', '0')
#IID_IPluginOptionsCallback = createIID('0A', '00')
#IID_IPluginOptions = createIID('0A', '0')

#PropID.h

class ArchiveProps(IntEnum):
    """Archive and Archive Item Propertys"""
    noproperty = 0  # kpidNoProperty
    main_sub_file = 1  # kpidMainSubfile
    handler_item_index = 2  # kpidHandlerItemIndex
    path = 3  # kpidPath
    name = 4  # kpidName
    extension = 5  # kpidExtension
    is_dir = 6  # kpidIsDir
    size = 7  # kpidSize
    pack_size = 8  # kpidPackSize
    attrib = 9  # kpidAttrib
    ctime = 10  # kpidCTime
    atime = 11  # kpidATime
    mtime = 12  # kpidMTime
    solid = 13  # kpidSolid
    commented = 14  # kpidCommented
    encrypted = 15  # kpidEncrypted
    split_before = 16  # kpidSplitBefore
    split_after = 17  # kpidSplitAfter
    dictionary_size = 18  # kpidDictionarySize
    crc = 19  # kpidCRC
    type = 20  # kpidType
    is_anti = 21  # kpidIsAnti
    method = 22  # kpidMethod
    host_os = 23  # kpidHostOS
    file_system = 24  # kpidFileSystem
    user = 25  # kpidUser
    group = 26  # kpidGroup
    block = 27  # kpidBlock
    comment = 28  # kpidComment
    position = 29  # kpidPosition
    prefix = 30  # kpidPrefix
    num_sub_dirs = 31  # kpidNumSubDirs
    num_sub_files = 32  # kpidNumSubFiles
    unpack_ver = 33  # kpidUnpackVer
    volume = 34  # kpidVolume
    is_volume = 35  # kpidIsVolume
    offset = 36  # kpidOffset
    links = 37  # kpidLinks
    num_blocks = 38  # kpidNumBlocks
    num_volumes = 39  # kpidNumVolumes
    time_type = 40  # kpidTimeType
    bit64 = 41  # kpidBit64
    big_endian = 42  # kpidBigEndian
    cpu = 43  # kpidCpu
    phy_size = 44  # kpidPhySize
    headers_size = 45  # kpidHeadersSize
    checksum = 46  # kpidChecksum
    characts = 47  # kpidCharacts
    va = 48  # kpidVa
    id = 49   # kpidId
    short_name = 50  # kpidShortName
    creator_app = 51  # kpidCreatorApp
    sector_size = 52  # kpidSectorSize
    posix_attrib = 53  # kpidPosixAttrib
    symlink = 54  # kpidSymLink
    error = 55  # kpidError
    total_size = 56	 # kpidTotalSize
    free_space = 57  # kpidFreeSpace
    cluster_size = 58  # kpidClusterSize
    volume_name = 59  # kpidVolumeName
    local_name = 60  # kpidLocalName
    provider = 61  # kpidProvider
    nt_secure = 62  # kpidNtSecure
    is_alt_stream = 63  # kpidIsAltStream
    is_aux = 64  # kpidIsAux
    is_deleted = 65  # kpidIsDeleted
    is_tree = 66  # kpidIsTree
    sha1 = 67  # kpidSha1
    sha256 = 68  # kpidSha256
    error_type = 69  # kpidErrorType
    num_errors = 70  # kpidNumErrors
    error_flags = 71  # kpidErrorFlags
    warning_flags = 72  # kpidWarningFlags
    warning = 73  # kpidWarning
    num_streams = 74  # kpidNumStreams
    num_alt_streams = 75  # kpidNumAltStreams
    alt_streams_size = 76  # kpidAltStreamsSize
    virtual_size = 77  # kpidVirtualSize
    unpack_size = 78  # kpidUnpackSize
    total_phy_size = 79  # kpidTotalPhySize
    volume_index = 80  # kpidVolumeIndex
    sub_type = 81  # kpidSubType
    short_comment = 82  # kpidShortComment
    code_page = 83  # kpidCodePage
    is_not_arc_type = 84  # kpidIsNotArcType
    phy_size_cant_be_detected = 85  # kpidPhySizeCantBeDetected
    zeros_tail_is_allowed = 86  # kpidZerosTailIsAllowed
    tail_size = 87  # kpidTailSize
    embedded_stub_size = 88  # kpidEmbeddedStubSize
    nt_reparse = 89  # kpidNtReparse
    hard_link = 90  # kpidHardLink
    i_node = 91  # kpidINode
    stream_id = 92  # kpidStreamId
    read_only = 93  # kpidReadOnly
    out_name = 94  # kpidOutName
    copy_link = 95  # kpidCopyLink
    arc_file_name = 96  # kpidArcFileName
    is_hash	= 97  # kpidIsHash

    userdefined = 0x10000  # kpidUserDefined

    @classmethod
    def _missing_(cls, value: int) -> 'ArchiveProps':
        v = int.__new__(cls, value)
        v._name_ = 'kpid{}'.format(value)
        v._value_ = value
        return v

class OperationResult(Enum):
    kOK = 0
    kUnSupportedMethod = 1
    kDataError = 2
    kCRCError = 3

class AskMode(Enum):
    kExtract = 0
    kTest = 1
    kSkip = 2
