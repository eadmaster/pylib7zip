from enum import IntEnum
"""
Windows Types CFFI Definitions
"""

CDEFS = """
typedef unsigned short VARTYPE;

typedef uint8_t GUID[16];

typedef struct {
	uint32_t dwLowDateTime;
	uint32_t dwHighDateTime;
} FILETIME;

typedef struct {
	VARTYPE           vt;
	unsigned short    wReserved1;
	unsigned short    wReserved2;
	unsigned short    wReserved3;
	union {
		char              cVal;
		uint8_t           bVal;
		int16_t           iVal;
		uint16_t          uiVal;
		int32_t           lVal;
		uint32_t          ulVal;
		float             fltVal;
		double            dblVal;
		char*             pcVal;
		wchar_t*          bstrVal;
		uint64_t          uhVal;
		GUID*             puuid;
		FILETIME          filetime;
		/* snip */
	};
} PROPVARIANT;


typedef uint32_t HRESULT;
typedef wchar_t* BSTR;
typedef wchar_t OLECHAR;

HRESULT PropVariantClear(PROPVARIANT *pvar);
BSTR SysAllocString(const OLECHAR *str);
void SysFreeString(BSTR bstr);
"""

#HRESULT values
class HRESULT(IntEnum):
    S_OK = 0x00000000  # Operation successful
    S_FALSE = 1       # Operation successful but returned no results
    E_ABORT = 0x80004004  # Operation aborted
    E_ACCESSDENIED = 0x80070005  # General access denied error
    E_FAIL = 0x80004005  # Unspecified failure
    E_HANDLE = 0x80070006  # Handle that is not valid
    E_INVALIDARG = 0x80070057  # One or more arguments are not valid
    E_NOINTERFACE = 0x80004002  # No such interface supported
    E_NOTIMPL = 0x80004001  # Not implemented
    E_OUTOFMEMORY = 0x8007000E  # Failed to allocate necessary memory
    E_POINTER = 0x80004003  # Pointer that is not valid
    E_UNEXPECTED = 0x8000FFFF  # Unexpected failure

    @property
    def desc(self):
        descriptions = {
            HRESULT.S_OK : 'Operation Successful',
            HRESULT.S_FALSE : 'Operation Successful but returned no results',
            HRESULT.E_ABORT : 'Operation Aborted',
            HRESULT.E_ACCESSDENIED : 'General Access Denied Error',
            HRESULT.E_FAIL : 'Unspecified Failure',
            HRESULT.E_HANDLE : 'Handle that is not valid',
            HRESULT.E_INVALIDARG : 'One or more arguments are not valid',
            HRESULT.E_NOINTERFACE : 'No such interface supported',
            HRESULT.E_NOTIMPL : 'Not implemented',
            HRESULT.E_OUTOFMEMORY : 'Failed to allocate necessary memory',
            HRESULT.E_POINTER : 'Pointer that is not valid',
            HRESULT.E_UNEXPECTED : 'Unexpected failure',
        }

        try:
            return descriptions[self]
        except KeyError:
            return 'Unknown Error Code'

#VARTYPE type values
#TODO IntEnum
class VARTYPE(IntEnum):
    VT_EMPTY = 0
    VT_NULL = 1
    VT_I1 = 16
    VT_UI1 = 17
    VT_I2 = 2
    VT_UI2 = 18
    VT_I4 = 3
    VT_UI4 = 19
    VT_INT = 22
    VT_UINT = 23
    VT_I8 = 20
    VT_UI8 = 21
    VT_R4 = 4
    VT_R8 = 5
    VT_BOOL = 11
    VT_ERROR = 10
    VT_CY = 6
    VT_DATE = 7
    VT_FILETIME = 64
    VT_CLSID = 72
    VT_CF = 71
    VT_BSTR = 8
    VT_BSTR_BLOB = 0xfff
    VT_BLOB = 65
    VT_BLOBOBJECT = 70
    VT_LPSTR = 30
    VT_LPWSTR = 31
    VT_UNKNOWN = 13
    VT_DISPATCH = 9
    VT_STREAM = 66
    VT_STREAMED_OBJECT = 68
    VT_STORAGE = 67
    VT_STORED_OBJECT = 69
    VT_VERSIONED_STREAM = 73
    VT_DECIMAL = 14
    VT_VECTOR = 0x1000
    VT_ARRAY = 0x2000
    VT_BYREF = 0x4000
    VT_VARIANT = 12
    VT_TYPEMASK = 0xFFF
