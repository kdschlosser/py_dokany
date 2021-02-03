import sys
import ctypes
from ctypes.wintypes import (
    DWORD,
    LONG,
    INT,
    BYTE,
    ULONG,
    WCHAR,
    LPCWSTR,
    LPVOID,
    LPDWORD,
    BOOL,
    FILETIME,
    PULONG,
    LPWSTR,
    LPCVOID,
    WORD,
    USHORT,
    CHAR,
    HANDLE,
    BOOLEAN
)


MAX_PATH = 255
ANYSIZE_ARRAY = 1

POINTER = ctypes.POINTER
UCHAR = ctypes.c_ubyte
LONGLONG = ctypes.c_longlong
ULONGLONG = ctypes.c_ulonglong
PULONGLONG = POINTER(ULONGLONG)
CCHAR = CHAR
PWSTR = POINTER(WCHAR)
ACCESS_MASK = DWORD
VOID = ctypes.c_void_p
PVOID = POINTER(VOID)
POINTER = ctypes.POINTER
SECURITY_DESCRIPTOR_CONTROL = USHORT
SECURITY_INFORMATION = DWORD
PSECURITY_INFORMATION = POINTER(SECURITY_INFORMATION)
ULONG64 = ctypes.c_uint64
NTSTATUS = LONG
PVOID64 = VOID


if sys.maxsize > 2**32:
    ULONG_PTR = ctypes.c_uint64
else:
    ULONG_PTR = ctypes.c_ulong

advapi32 = ctypes.windll.Advapi32
kernel32 = ctypes.windll.Kernel32
user32 = ctypes.windll.User32

CloseHandle = kernel32.CloseHandle
CloseHandle.restype = BOOL

GetTokenInformation = advapi32.GetTokenInformation
GetTokenInformation .restype = BOOL

LookupAccountSid = advapi32.LookupAccountSidW
LookupAccountSid.restype = BOOL

GetFileAttributes = kernel32.GetFileAttributesW
GetFileAttributes.restype = DWORD

ImpersonateLoggedOnUser = advapi32.ImpersonateLoggedOnUser
ImpersonateLoggedOnUser.restype = BOOL

CreateDirectory = kernel32.CreateDirectoryW
CreateDirectory.restype = BOOL

RevertToSelf = advapi32.RevertToSelf
RevertToSelf.restype = BOOL

SetLastError = kernel32.SetLastError
SetLastError.restype = VOID

CreateFile = kernel32.CreateFileW
CreateFile.restype = HANDLE

SetFileAttributes = kernel32.SetFileAttributesW
SetFileAttributes.restype = BOOL

LookupPrivilegeValue = advapi32.LookupPrivilegeValueW
LookupPrivilegeValue.restype = BOOL

OpenProcessToken = advapi32.OpenProcessToken
OpenProcessToken.restype = BOOL

GetCurrentProcess = kernel32.GetCurrentProcess
GetCurrentProcess.restype = HANDLE

AdjustTokenPrivileges = advapi32.AdjustTokenPrivileges
AdjustTokenPrivileges.restype = BOOL

RemoveDirectory = kernel32.RemoveDirectoryW
RemoveDirectory.restype = BOOL

DeleteFile = kernel32.DeleteFileW
DeleteFile.restype = BOOL

SetFilePointerEx = kernel32.SetFilePointerEx
SetFilePointerEx.restype = BOOL

ReadFile = kernel32.ReadFile
ReadFile.restype = BOOL

GetFileSize = kernel32.GetFileSize
GetFileSize.restype = DWORD

WriteFile = kernel32.WriteFile
WriteFile.restype = BOOL

FlushFileBuffers = kernel32.FlushFileBuffers
FlushFileBuffers.restype = BOOL

GetFileInformationByHandle = kernel32.GetFileInformationByHandle
GetFileInformationByHandle.restype = BOOL

FindFirstFile = kernel32.FindFirstFileW
FindFirstFile.restype = HANDLE

FindClose = kernel32.FindClose
FindClose.restype = BOOL

FindNextFile = kernel32.FindNextFileW
FindNextFile.restype = BOOL

SetFileInformationByHandle = kernel32.SetFileInformationByHandle
SetFileInformationByHandle.restype = BOOL

LockFile = kernel32.LockFile
LockFile.restype = BOOL

UnlockFile = kernel32.UnlockFile
UnlockFile.restype = BOOL

SetEndOfFile = kernel32.SetEndOfFile
SetEndOfFile.restype = BOOL

GetFileSizeEx = kernel32.GetFileSizeEx
GetFileSizeEx.restype = BOOL

SetFileTime = kernel32.SetFileTime
SetFileTime.restype = BOOL

GetUserObjectSecurity = user32.GetUserObjectSecurity
GetUserObjectSecurity.restype = BOOL

GetSecurityDescriptorLength = advapi32.GetSecurityDescriptorLength
GetSecurityDescriptorLength.restype = DWORD

SetUserObjectSecurity = user32.SetUserObjectSecurity
SetUserObjectSecurity.restype = BOOL


GetVolumeInformation = kernel32.GetVolumeInformationW
GetVolumeInformation.restype = BOOL

GetDiskFreeSpace = kernel32.GetDiskFreeSpaceW
GetDiskFreeSpace.restype = BOOL

FindFirstStream = kernel32.FindFirstStreamW
FindFirstStream.restype = HANDLE

FindNextStream = kernel32.FindNextStreamW
FindNextStream.restype = BOOL


class ENUM(INT):
    pass


wcscpy_s = ctypes.cdll.msvcrt.wcscpy_s
wcscpy_s.restype = ctypes.c_int
wcscpy_s.argtypes = [
    ctypes.c_wchar_p,
    ctypes.c_size_t,
    ctypes.c_wchar_p
]

wcslen = ctypes.cdll.msvcrt.wcslen
wcslen.restype = ctypes.c_size_t
wcslen.argtypes = [ctypes.c_wchar_p]

wcscmp = ctypes.cdll.msvcrt.wcscmp
wcscmp.restype = ctypes.c_int
wcscmp.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]

wcsncpy_s = ctypes.cdll.msvcrt.wcsncpy_s
wcsncpy_s.restype = ctypes.c_int
wcsncpy_s.argtypes = [
    ctypes.c_wchar_p,
    ctypes.c_size_t,
    ctypes.c_wchar_p,
    ctypes.c_size_t
]

wcsncat_s = ctypes.cdll.msvcrt.wcsncat_s
wcsncat_s.restype = ctypes.c_int
wcsncat_s.argtypes = [
    ctypes.c_wchar_p,
    ctypes.c_size_t,
    ctypes.c_wchar_p,
    ctypes.c_size_t
]

_wcsnicmp = ctypes.cdll.msvcrt._wcsnicmp
_wcsnicmp.restype = ctypes.c_int
_wcsnicmp.argtypes = [
    ctypes.c_wchar_p,
    ctypes.c_wchar_p,
    ctypes.c_size_t
]


class _LARGE_INTEGER(ctypes.Union):
    class DUMMYSTRUCTNAME(ctypes.Structure):
        _fields_ = [
            ('LowPart', DWORD),
            ('HighPart', LONG)
        ]

    class u(ctypes.Structure):
        _fields_ = [
            ('LowPart', DWORD),
            ('HighPart', LONG)
        ]

    _fields_ = [
        ('DUMMYSTRUCTNAME', DUMMYSTRUCTNAME),
        ('u', u),
        ('QuadPart', LONGLONG)
    ]

    _anonymous_ = ('DUMMYSTRUCTNAME',)


LARGE_INTEGER = _LARGE_INTEGER


class _SID_IDENTIFIER_AUTHORITY(ctypes.Structure):
    _fields_ = [
        ('Value', UCHAR * 6),
    ]


SID_IDENTIFIER_AUTHORITY = _SID_IDENTIFIER_AUTHORITY
PSID_IDENTIFIER_AUTHORITY = POINTER(_SID_IDENTIFIER_AUTHORITY)


class _SID(ctypes.Structure):
    _fields_ = [
        ('Revision', BYTE),
        ('SubAuthorityCount', BYTE),
        ('IdentifierAuthority', SID_IDENTIFIER_AUTHORITY),
        # [size_is]
        ('SubAuthority', ULONG * 1),
    ]


SID = _SID
PSID = POINTER(SID)


class _SID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ('Sid', PSID),
        ('Attributes', DWORD),
    ]


SID_AND_ATTRIBUTES = _SID_AND_ATTRIBUTES
PSID_AND_ATTRIBUTES = POINTER(_SID_AND_ATTRIBUTES)


class _TOKEN_USER(ctypes.Structure):
    _fields_ = [
        ('User', SID_AND_ATTRIBUTES)
    ]


TOKEN_USER = _TOKEN_USER
PTOKEN_USER = ctypes.POINTER(_TOKEN_USER)


class SID_NAME_USE(ENUM):
    pass


class _SECURITY_IMPERSONATION_LEVEL(ENUM):
    SecurityAnonymous = 0
    SecurityIdentification = 1
    SecurityImpersonation = 2
    SecurityDelegation = 3


SECURITY_IMPERSONATION_LEVEL = _SECURITY_IMPERSONATION_LEVEL

SecurityAnonymous = _SECURITY_IMPERSONATION_LEVEL.SecurityAnonymous
SecurityIdentification = _SECURITY_IMPERSONATION_LEVEL.SecurityIdentification
SecurityImpersonation = _SECURITY_IMPERSONATION_LEVEL.SecurityImpersonation
SecurityDelegation = _SECURITY_IMPERSONATION_LEVEL.SecurityDelegation


class _BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('dwFileAttributes', DWORD),
        ('ftCreationTime', FILETIME),
        ('ftLastAccessTime', FILETIME),
        ('ftLastWriteTime', FILETIME),
        ('dwVolumeSerialNumber', DWORD),
        ('nFileSizeHigh', DWORD),
        ('nFileSizeLow', DWORD),
        ('nNumberOfLinks', DWORD),
        ('nFileIndexHigh', DWORD),
        ('nFileIndexLow', DWORD)
    ]


BY_HANDLE_FILE_INFORMATION = _BY_HANDLE_FILE_INFORMATION
PBY_HANDLE_FILE_INFORMATION = ctypes.POINTER(_BY_HANDLE_FILE_INFORMATION)
LPBY_HANDLE_FILE_INFORMATION = ctypes.POINTER(_BY_HANDLE_FILE_INFORMATION)


class _WIN32_FIND_DATAW(ctypes.Structure):
    _fields_ = [
        ('dwFileAttributes', DWORD),
        ('ftCreationTime', FILETIME),
        ('ftLastAccessTime', FILETIME),
        ('ftLastWriteTime', FILETIME),
        ('nFileSizeHigh', DWORD),
        ('nFileSizeLow', DWORD),
        ('dwReserved0', DWORD),
        ('dwReserved1', DWORD),
        ('cFileName', WCHAR * MAX_PATH),
        ('cAlternateFileName', WCHAR * 14),
    ]


WIN32_FIND_DATAW = _WIN32_FIND_DATAW
PWIN32_FIND_DATAW = POINTER(_WIN32_FIND_DATAW)


class _WIN32_FIND_STREAM_DATA(ctypes.Structure):
    _fields_ = [
        ('StreamSize', LARGE_INTEGER),
        ('cStreamName', WCHAR * (MAX_PATH + 36))
    ]


WIN32_FIND_STREAM_DATA = _WIN32_FIND_STREAM_DATA
PWIN32_FIND_STREAM_DATA = ctypes.POINTER(_WIN32_FIND_STREAM_DATA)


class _ACL(ctypes.Structure):
    _fields_ = [
        ('AclRevision', UCHAR),
        ('Sbz1', UCHAR),
        ('AclSize', USHORT),
        ('AceCount', USHORT),
        ('Sbz2', USHORT),
    ]


ACL = _ACL
PACL = ctypes.POINTER(_ACL)


class _SECURITY_DESCRIPTOR(ctypes.Structure):
    _fields_ = [
        ('Revision', UCHAR),
        ('Sbz1', UCHAR),
        ('Control', SECURITY_DESCRIPTOR_CONTROL),
        ('Owner', PSID),
        ('Group', PSID),
        ('Sacl', PACL),
        ('Dacl', PACL),
    ]


SECURITY_DESCRIPTOR = _SECURITY_DESCRIPTOR
PSECURITY_DESCRIPTOR = ctypes.POINTER(_SECURITY_DESCRIPTOR)


class _SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ('nLength', DWORD),
        ('lpSecurityDescriptor', PSECURITY_DESCRIPTOR),
        ('bInheritHandle', BOOL)
    ]


SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES
PSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)
LPSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)


class _LUID(ctypes.Structure):
    _fields_ = [
        ('LowPart', DWORD),
        ('HighPart', LONG)
    ]


LUID = _LUID
PLUID = POINTER(_LUID)


class _LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ('Luid', LUID),
        ('Attributes', ULONG)
    ]


LUID_AND_ATTRIBUTES = _LUID_AND_ATTRIBUTES
PLUID_AND_ATTRIBUTES = POINTER(_LUID_AND_ATTRIBUTES)


class _TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ('PrivilegeCount', DWORD),
        ('Privileges', LUID_AND_ATTRIBUTES * ANYSIZE_ARRAY)
    ]


TOKEN_PRIVILEGES = _TOKEN_PRIVILEGES
PTOKEN_PRIVILEGES = POINTER(_TOKEN_PRIVILEGES)


class _FILE_DISPOSITION_INFO(ctypes.Structure):
    _fields_ = [
        ('DeleteFile', BOOLEAN)
    ]


FILE_DISPOSITION_INFO = _FILE_DISPOSITION_INFO
PFILE_DISPOSITION_INFO = POINTER(_FILE_DISPOSITION_INFO)


class _FILE_RENAME_INFO(ctypes.Structure):

    class DUMMYUNIONNAME(ctypes.Union):
        _fields_ = [
            ('ReplaceIfExists', BOOLEAN),
            ('Flags', DWORD)
        ]

    _fields_ = [
        ('DUMMYUNIONNAME', DUMMYUNIONNAME),
        ('ReplaceIfExists', BOOLEAN),
        ('RootDirectory', HANDLE),
        ('FileNameLength', DWORD),
        ('FileName', WCHAR * 1)
    ]

    _anonymous_ = ('DUMMYUNIONNAME',)


FILE_RENAME_INFO = _FILE_RENAME_INFO
PFILE_RENAME_INFO = POINTER(_FILE_RENAME_INFO)


# /**
#  * Avoid #include <winternl.h> which as conflict with FILE_INFORMATION_CLASS
#  * definition.
#  * This only for MirrorFindStreams. Link with ntdll.lib still required.
#  *
#  * Not needed if you're not using NtQueryInformationFile!
#  *
#  * BEGIN
#  */
# #pragma warning(push)
# #pragma warning(disable : 4201r)
class _IO_STATUS_BLOCK(ctypes.Structure):
    class DUMMYUNIONNAME(ctypes.Union):
        _fields_ = [
            ('Status', NTSTATUS),
            ('Pointer', PVOID)
        ]

    _fields_ = [
        ('DUMMYUNIONNAME', DUMMYUNIONNAME),
        ('Information', ULONG_PTR)
    ]

    _anonymous_ = ('DUMMYUNIONNAME',)


IO_STATUS_BLOCK = _IO_STATUS_BLOCK
PIO_STATUS_BLOCK = ctypes.POINTER(_IO_STATUS_BLOCK)

from .fileinfo_h import FILE_INFORMATION_CLASS

ntoskrnl = ctypes.WinDLL('NtosKrnl.exe')
NtQueryInformationFile = ntoskrnl.NtQueryInformationFile
NtQueryInformationFile.restype = NTSTATUS
NtQueryInformationFile.argtypes = [HANDLE, PIO_STATUS_BLOCK, PVOID, ULONG, FILE_INFORMATION_CLASS]

