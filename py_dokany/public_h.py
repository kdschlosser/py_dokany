import ctypes
import sys
from ctypes.wintypes import (
    USHORT,
    WCHAR,
    ULONG,
    BOOLEAN,
    DWORD,
    LARGE_INTEGER,
    HANDLE,
    LONG
)

MAX_PATH = 255
VOID = ctypes.c_void_p
PVOID = ctypes.POINTER(VOID)
POINTER = ctypes.POINTER
ACCESS_MASK = DWORD
SECURITY_DESCRIPTOR_CONTROL = USHORT
UCHAR = ctypes.c_ubyte
PSID = PVOID
SECURITY_INFORMATION = DWORD
ULONG64 = ctypes.c_uint64
NTSTATUS = LONG
PVOID64 = VOID


class _SECURITY_DESCRIPTOR(ctypes.Structure):
    pass


SECURITY_DESCRIPTOR = _SECURITY_DESCRIPTOR
PSECURITY_DESCRIPTOR = ctypes.POINTER(_SECURITY_DESCRIPTOR)


class _ACL(ctypes.Structure):
    pass


ACL = _ACL
PACL = ctypes.POINTER(_ACL)


_SECURITY_DESCRIPTOR._fields_ = [
    ('Revision', UCHAR),
    ('Sbz1', UCHAR),
    ('Control', SECURITY_DESCRIPTOR_CONTROL),
    ('Owner', PSID),
    ('Group', PSID),
    ('Sacl', PACL),
    ('Dacl', PACL),
]

_ACL._fields_ = [
    ('AclRevision', UCHAR),
    ('Sbz1', UCHAR),
    ('AclSize', USHORT),
    ('AceCount', USHORT),
    ('Sbz2', USHORT),
]


class _DOKAN_UNICODE_STRING_INTERMEDIATE(ctypes.Structure):
    pass


DOKAN_UNICODE_STRING_INTERMEDIATE = _DOKAN_UNICODE_STRING_INTERMEDIATE
PDOKAN_UNICODE_STRING_INTERMEDIATE = POINTER(_DOKAN_UNICODE_STRING_INTERMEDIATE)


class _DOKAN_NOTIFY_PATH_INTERMEDIATE(ctypes.Structure):
    pass


DOKAN_NOTIFY_PATH_INTERMEDIATE = _DOKAN_NOTIFY_PATH_INTERMEDIATE
PDOKAN_NOTIFY_PATH_INTERMEDIATE = POINTER(_DOKAN_NOTIFY_PATH_INTERMEDIATE)


class _DOKAN_ACCESS_STATE_INTERMEDIATE(ctypes.Structure):
    pass


DOKAN_ACCESS_STATE_INTERMEDIATE = _DOKAN_ACCESS_STATE_INTERMEDIATE
PDOKAN_ACCESS_STATE_INTERMEDIATE = POINTER(_DOKAN_ACCESS_STATE_INTERMEDIATE)


class _DOKAN_ACCESS_STATE(ctypes.Structure):
    pass


DOKAN_ACCESS_STATE = _DOKAN_ACCESS_STATE
PDOKAN_ACCESS_STATE = POINTER(_DOKAN_ACCESS_STATE)


class _DOKAN_IO_SECURITY_CONTEXT_INTERMEDIATE(ctypes.Structure):
    pass


DOKAN_IO_SECURITY_CONTEXT_INTERMEDIATE = _DOKAN_IO_SECURITY_CONTEXT_INTERMEDIATE
PDOKAN_IO_SECURITY_CONTEXT_INTERMEDIATE = POINTER(_DOKAN_IO_SECURITY_CONTEXT_INTERMEDIATE)


class _DOKAN_IO_SECURITY_CONTEXT(ctypes.Structure):
    pass


DOKAN_IO_SECURITY_CONTEXT = _DOKAN_IO_SECURITY_CONTEXT
PDOKAN_IO_SECURITY_CONTEXT = POINTER(_DOKAN_IO_SECURITY_CONTEXT)


class _CREATE_CONTEXT(ctypes.Structure):
    pass


CREATE_CONTEXT = _CREATE_CONTEXT
PCREATE_CONTEXT = POINTER(_CREATE_CONTEXT)


class _CLEANUP_CONTEXT(ctypes.Structure):
    pass


CLEANUP_CONTEXT = _CLEANUP_CONTEXT
PCLEANUP_CONTEXT = POINTER(_CLEANUP_CONTEXT)


class _CLOSE_CONTEXT(ctypes.Structure):
    pass


CLOSE_CONTEXT = _CLOSE_CONTEXT
PCLOSE_CONTEXT = POINTER(_CLOSE_CONTEXT)


class _DIRECTORY_CONTEXT(ctypes.Structure):
    pass


DIRECTORY_CONTEXT = _DIRECTORY_CONTEXT
PDIRECTORY_CONTEXT = POINTER(_DIRECTORY_CONTEXT)


class _READ_CONTEXT(ctypes.Structure):
    pass


READ_CONTEXT = _READ_CONTEXT
PREAD_CONTEXT = POINTER(_READ_CONTEXT)


class _WRITE_CONTEXT(ctypes.Structure):
    pass


WRITE_CONTEXT = _WRITE_CONTEXT
PWRITE_CONTEXT = POINTER(_WRITE_CONTEXT)


class _FILEINFO_CONTEXT(ctypes.Structure):
    pass


FILEINFO_CONTEXT = _FILEINFO_CONTEXT
PFILEINFO_CONTEXT = POINTER(_FILEINFO_CONTEXT)


class _SETFILE_CONTEXT(ctypes.Structure):
    pass


SETFILE_CONTEXT = _SETFILE_CONTEXT
PSETFILE_CONTEXT = POINTER(_SETFILE_CONTEXT)


class _VOLUME_CONTEXT(ctypes.Structure):
    pass


VOLUME_CONTEXT = _VOLUME_CONTEXT
PVOLUME_CONTEXT = POINTER(_VOLUME_CONTEXT)


class _LOCK_CONTEXT(ctypes.Structure):
    pass


LOCK_CONTEXT = _LOCK_CONTEXT
PLOCK_CONTEXT = POINTER(_LOCK_CONTEXT)


class _FLUSH_CONTEXT(ctypes.Structure):
    pass


FLUSH_CONTEXT = _FLUSH_CONTEXT
PFLUSH_CONTEXT = POINTER(_FLUSH_CONTEXT)


class _UNMOUNT_CONTEXT(ctypes.Structure):
    pass


UNMOUNT_CONTEXT = _UNMOUNT_CONTEXT
PUNMOUNT_CONTEXT = POINTER(_UNMOUNT_CONTEXT)


class _SECURITY_CONTEXT(ctypes.Structure):
    pass


SECURITY_CONTEXT = _SECURITY_CONTEXT
PSECURITY_CONTEXT = POINTER(_SECURITY_CONTEXT)


class _SET_SECURITY_CONTEXT(ctypes.Structure):
    pass


SET_SECURITY_CONTEXT = _SET_SECURITY_CONTEXT
PSET_SECURITY_CONTEXT = POINTER(_SET_SECURITY_CONTEXT)


class _EVENT_CONTEXT(ctypes.Structure):
    pass


EVENT_CONTEXT = _EVENT_CONTEXT
PEVENT_CONTEXT = POINTER(_EVENT_CONTEXT)


class _VOLUME_METRICS(ctypes.Structure):
    pass


VOLUME_METRICS = _VOLUME_METRICS
PVOLUME_METRICS = POINTER(_VOLUME_METRICS)


class _EVENT_INFORMATION(ctypes.Structure):
    pass


EVENT_INFORMATION = _EVENT_INFORMATION
PEVENT_INFORMATION = POINTER(_EVENT_INFORMATION)


class _EVENT_DRIVER_INFO(ctypes.Structure):
    pass


EVENT_DRIVER_INFO = _EVENT_DRIVER_INFO
PEVENT_DRIVER_INFO = POINTER(_EVENT_DRIVER_INFO)


class _EVENT_START(ctypes.Structure):
    pass


EVENT_START = _EVENT_START
PEVENT_START = POINTER(_EVENT_START)


class _DOKAN_RENAME_INFORMATION(ctypes.Structure):
    pass


DOKAN_RENAME_INFORMATION = _DOKAN_RENAME_INFORMATION
PDOKAN_RENAME_INFORMATION = POINTER(_DOKAN_RENAME_INFORMATION)


class _DOKAN_LINK_INFORMATION(ctypes.Structure):
    pass


DOKAN_LINK_INFORMATION = _DOKAN_LINK_INFORMATION
PDOKAN_LINK_INFORMATION = POINTER(_DOKAN_LINK_INFORMATION)


class _DOKAN_CONTROL(ctypes.Structure):
    pass


DOKAN_CONTROL = _DOKAN_CONTROL
PDOKAN_CONTROL = POINTER(_DOKAN_CONTROL)


# /* Dokan : user-mode file system library for Windows Copyright (C) 2015 -
# 2019 Adrien J. < liryna.stark@gmail.com > and Maxime C. < maxime@islog.com >
# Copyright (C) 2017 - 2018 Google, Inc. Copyright (C) 2007 - 2011 Hiroki
# Asakawa < info@dokan-dev.net > http://dokan-dev.github.io This program is
# free software; you can redistribute it and/or modify it under the terms of
# the GNU Lesser General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version. This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details. You should have received a copy of the GNU Lesser General
# Public License along with this program. If not, see <
# http://www.gnu.org/licenses/ > .
DOKAN_MAJOR_API_VERSION = "1"


DOKAN_DRIVER_VERSION = 0x0000190
EVENT_CONTEXT_MAX_SIZE = 1024 * 32


def CTL_CODE(DeviceType, Function, Method, Access):
    return (
            (DeviceType << 16) |
            (Access << 14) |
            (Function << 2) |
            Method
    )


METHOD_BUFFERED = 0x00000000
FILE_ANY_ACCESS = 0x00000000
FILE_DEVICE_UNKNOWN = 0x00000022
METHOD_OUT_DIRECT = 0x00000002
METHOD_NEITHER = 0x00000003
FILE_DEVICE_FILE_SYSTEM = 0x00000009

IOCTL_GET_VERSION = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x800,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
IOCTL_SET_DEBUG_MODE = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x801,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
IOCTL_EVENT_WAIT = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x802,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
IOCTL_EVENT_INFO = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x803,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
IOCTL_EVENT_RELEASE = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x804,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
IOCTL_EVENT_START = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x805,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
IOCTL_EVENT_WRITE = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x806,
    METHOD_OUT_DIRECT,
    FILE_ANY_ACCESS,
)
IOCTL_KEEPALIVE = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x809,
    METHOD_NEITHER,
    FILE_ANY_ACCESS,
)
IOCTL_SERVICE_WAIT = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x80A,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
IOCTL_RESET_TIMEOUT = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x80B,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
IOCTL_GET_ACCESS_TOKEN = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x80C,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
IOCTL_EVENT_MOUNTPOINT_LIST = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x80D,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
IOCTL_MOUNTPOINT_CLEANUP = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x80E,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)

# DeviceIoControl code to send to a keepalive handle to activate it
# (see the
# documentation for the keepalive flags in the DokanFCB struct).
FSCTL_ACTIVATE_KEEPALIVE = CTL_CODE(
    FILE_DEVICE_FILE_SYSTEM,
    0x80F,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)

# DeviceIoControl code to send path notification request.
FSCTL_NOTIFY_PATH = CTL_CODE(
    FILE_DEVICE_FILE_SYSTEM,
    0x810,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)

# DeviceIoControl code to retrieve the VOLUME_METRICS struct for the
# targeted
# volume.
IOCTL_GET_VOLUME_METRICS = CTL_CODE(
    FILE_DEVICE_UNKNOWN,
    0x811,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)
DRIVER_FUNC_INSTALL = 0x01
DRIVER_FUNC_REMOVE = 0x02
DOKAN_MOUNTED = 1
DOKAN_USED = 2
DOKAN_START_FAILED = 3
DOKAN_DEVICE_MAX = 10
DOKAN_DEFAULT_SECTOR_SIZE = 512
DOKAN_DEFAULT_ALLOCATION_UNIT_SIZE = 512
DOKAN_DEFAULT_DISK_SIZE = 1024 * 1024 * 1024

# used in CCB.Flags and FCB.Flags
DOKAN_FILE_DIRECTORY = 1
DOKAN_FILE_DELETED = 2
DOKAN_FILE_OPENED = 4
DOKAN_DIR_MATCH_ALL = 8
DOKAN_DELETE_ON_CLOSE = 16
DOKAN_PAGING_IO = 32
DOKAN_SYNCHRONOUS_IO = 64
DOKAN_WRITE_TO_END_OF_FILE = 128
DOKAN_NOCACHE = 256
DOKAN_RETRY_CREATE = 512
DOKAN_FILE_CHANGE_LAST_WRITE = 1024

# used in DOKAN_START.DeviceType
DOKAN_DISK_FILE_SYSTEM = 0
DOKAN_NETWORK_FILE_SYSTEM = 1

# Special files that are tagged for specfic FS purpose when their FCB is
# init.
# Note: This file names can no longer be used by userland FS correctly.
DOKAN_KEEPALIVE_FILE_NAME = "\\__drive_fs_keepalive"
DOKAN_NOTIFICATION_FILE_NAME = "\\drive_fs_notification"

# The minimum FCB garbage collection interval, below which the parameter is
# ignored
# (instantaneous deletion with an interval of 0 is more efficient than
# using the machinery with a tight interval).
MIN_FCB_GARBAGE_COLLECTION_INTERVAL = 500

# This structure is used for copying UNICODE_STRING from the kernel mode
# driver
# into the user mode driver.
# https://msdn.microsoft.com/en-us/library/windows/hardware/ff564879(v=vs.85).aspx
# 
_DOKAN_UNICODE_STRING_INTERMEDIATE._fields_ = [
    ('Length', USHORT),
    ('MaximumLength', USHORT),
    ('Buffer', WCHAR * 1),
]

# This structure is used for sending notify path information from the user
# mode
# driver to the kernel mode driver. See below links for parameter details
# for
# CompletionFilter and Action, and FsRtlNotifyFullReportChange call.
# https://msdn.microsoft.com/en-us/library/windows/hardware/ff547026(v=vs.85).aspx
# 
# https://msdn.microsoft.com/en-us/library/windows/hardware/ff547041(v=vs.85).aspx
# 
_DOKAN_NOTIFY_PATH_INTERMEDIATE._fields_ = [
    ('CompletionFilter', ULONG),
    ('Action', ULONG),
    ('Length', USHORT),
    ('Buffer', WCHAR * 1),
]

# This structure is used for copying ACCESS_STATE from the kernel mode
# driver
# into the user mode driver.
# https://msdn.microsoft.com/en-us/library/windows/hardware/ff538840(v=vs.85).aspx
# 
_DOKAN_ACCESS_STATE_INTERMEDIATE._fields_ = [
    ('SecurityEvaluated', BOOLEAN),
    ('GenerateAudit', BOOLEAN),
    ('GenerateOnClose', BOOLEAN),
    ('AuditPrivileges', BOOLEAN),
    ('Flags', ULONG),
    ('RemainingDesiredAccess', ACCESS_MASK),
    ('PreviouslyGrantedAccess', ACCESS_MASK),
    ('OriginalDesiredAccess', ACCESS_MASK),
    # if 0 that means there is no security descriptor
    ('SecurityDescriptorOffset', ULONG),
    # DOKAN_UNICODE_STRING_INTERMEDIATE
    ('UnicodeStringObjectNameOffset', ULONG),
    # DOKAN_UNICODE_STRING_INTERMEDIATE
    ('UnicodeStringObjectTypeOffset', ULONG),
]


class _UNICODE_STRING(ctypes.Structure):
    _fields_ = [
        ('Length', USHORT),
        ('MaximumLength', USHORT),
        ('Buffer', POINTER(USHORT)),
    ]


UNICODE_STRING = _UNICODE_STRING

_DOKAN_ACCESS_STATE._fields_ = [
    ('SecurityEvaluated', BOOLEAN),
    ('GenerateAudit', BOOLEAN),
    ('GenerateOnClose', BOOLEAN),
    ('AuditPrivileges', BOOLEAN),
    ('Flags', ULONG),
    ('RemainingDesiredAccess', ACCESS_MASK),
    ('PreviouslyGrantedAccess', ACCESS_MASK),
    ('OriginalDesiredAccess', ACCESS_MASK),
    ('SecurityDescriptor', PSECURITY_DESCRIPTOR),
    ('ObjectName', UNICODE_STRING),
    ('ObjectType', UNICODE_STRING),
]

# This structure is used for copying IO_SECURITY_CONTEXT from the kernel
# mode
# driver into the user mode driver.
# https://msdn.microsoft.com/en-us/library/windows/hardware/ff550613(v=vs.85).aspx
# 
_DOKAN_IO_SECURITY_CONTEXT_INTERMEDIATE._fields_ = [
    ('AccessState', DOKAN_ACCESS_STATE_INTERMEDIATE),
    ('DesiredAccess', ACCESS_MASK),
]

_DOKAN_IO_SECURITY_CONTEXT._fields_ = [
    ('AccessState', DOKAN_ACCESS_STATE),
    ('DesiredAccess', ACCESS_MASK),
]


_CREATE_CONTEXT._fields_ = [
    ('SecurityContext', DOKAN_IO_SECURITY_CONTEXT_INTERMEDIATE),
    ('FileAttributes', ULONG),
    ('CreateOptions', ULONG),
    ('ShareAccess', ULONG),
    ('FileNameLength', ULONG),
    # Offset from the beginning of this structure to the string
    ('FileNameOffset', ULONG),
]

_CLEANUP_CONTEXT._fields_ = [
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]

_CLOSE_CONTEXT._fields_ = [
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]

_DIRECTORY_CONTEXT._fields_ = [
    ('FileInformationClass', ULONG),
    ('FileIndex', ULONG),
    ('BufferLength', ULONG),
    ('DirectoryNameLength', ULONG),
    ('SearchPatternLength', ULONG),
    ('SearchPatternOffset', ULONG),
    ('DirectoryName', WCHAR * 1),
    ('SearchPatternBase', WCHAR * 1),
]

_READ_CONTEXT._fields_ = [
    ('ByteOffset', LARGE_INTEGER),
    ('BufferLength', ULONG),
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]

_WRITE_CONTEXT._fields_ = [
    ('ByteOffset', LARGE_INTEGER),
    ('BufferLength', ULONG),
    ('BufferOffset', ULONG),
    ('RequestLength', ULONG),
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 2),
]

_FILEINFO_CONTEXT._fields_ = [
    ('FileInformationClass', ULONG),
    ('BufferLength', ULONG),
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]

_SETFILE_CONTEXT._fields_ = [
    ('FileInformationClass', ULONG),
    ('BufferLength', ULONG),
    ('BufferOffset', ULONG),
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]

_VOLUME_CONTEXT._fields_ = [
    ('FsInformationClass', ULONG),
    ('BufferLength', ULONG),
]

_LOCK_CONTEXT._fields_ = [
    ('ByteOffset', LARGE_INTEGER),
    ('Length', LARGE_INTEGER),
    ('Key', ULONG),
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]

_FLUSH_CONTEXT._fields_ = [
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]

_UNMOUNT_CONTEXT._fields_ = [
    ('DeviceName', WCHAR * 64),
    ('Option', ULONG),
]

_SECURITY_CONTEXT._fields_ = [
    ('SecurityInformation', SECURITY_INFORMATION),
    ('BufferLength', ULONG),
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]

_SET_SECURITY_CONTEXT._fields_ = [
    ('SecurityInformation', SECURITY_INFORMATION),
    ('BufferLength', ULONG),
    ('BufferOffset', ULONG),
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]


class Operation(ctypes.Union):
    pass


Operation._fields_ = [
    ('Directory', DIRECTORY_CONTEXT),
    ('Read', READ_CONTEXT),
    ('Write', WRITE_CONTEXT),
    ('File', FILEINFO_CONTEXT),
    ('Create', CREATE_CONTEXT),
    ('Close', CLOSE_CONTEXT),
    ('SetFile', SETFILE_CONTEXT),
    ('Cleanup', CLEANUP_CONTEXT),
    ('Lock', LOCK_CONTEXT),
    ('Volume', VOLUME_CONTEXT),
    ('Flush', FLUSH_CONTEXT),
    ('Unmount', UNMOUNT_CONTEXT),
    ('Security', SECURITY_CONTEXT),
    ('SetSecurity', SET_SECURITY_CONTEXT),
]
_EVENT_CONTEXT.Operation = Operation


_EVENT_CONTEXT._fields_ = [
    ('Length', ULONG),
    ('MountId', ULONG),
    ('SerialNumber', ULONG),
    ('ProcessId', ULONG),
    ('MajorFunction', UCHAR),
    ('MinorFunction', UCHAR),
    ('Flags', ULONG),
    ('FileFlags', ULONG),
    ('Context', ULONG64),
    ('Operation', _EVENT_CONTEXT.Operation),
]

# The output from IOCTL_GET_VOLUME_METRICS.
_VOLUME_METRICS._fields_ = [
    ('NormalFcbGarbageCollectionCycles', ULONG64),
    # A "cycle" can consist of multiple "passes".
    ('NormalFcbGarbageCollectionPasses', ULONG64),
    ('ForcedFcbGarbageCollectionPasses', ULONG64),
    ('FcbAllocations', ULONG64),
    ('FcbDeletions', ULONG64),
    # A "cancellation" is when a single FCB's garbage collection gets
    # canceled.
    ('FcbGarbageCollectionCancellations', ULONG64),
    # being forward to userland.
    ('LargeIRPRegistrationCanceled', ULONG64),
]
WRITE_MAX_SIZE = EVENT_CONTEXT_MAX_SIZE - ctypes.sizeof(EVENT_CONTEXT) - 256 * ctypes.sizeof(WCHAR)


class Operation(ctypes.Union):
    pass


class Directory(ctypes.Structure):
    pass


Directory._fields_ = [
    ('Index', ULONG),
]
Operation.Directory = Directory


class Create(ctypes.Structure):
    pass


Create._fields_ = [
    ('Flags', ULONG),
    ('Information', ULONG),
]
Operation.Create = Create


class Read(ctypes.Structure):
    pass


Read._fields_ = [
    ('CurrentByteOffset', LARGE_INTEGER),
]
Operation.Read = Read


class Write(ctypes.Structure):
    pass


Write._fields_ = [
    ('CurrentByteOffset', LARGE_INTEGER),
]
Operation.Write = Write


class Delete(ctypes.Structure):
    pass


Delete._fields_ = [
    ('DeleteOnClose', UCHAR),
]
Operation.Delete = Delete


class ResetTimeout(ctypes.Structure):
    pass


ResetTimeout._fields_ = [
    ('Timeout', ULONG),
]
Operation.ResetTimeout = ResetTimeout


class AccessToken(ctypes.Structure):
    pass


AccessToken._fields_ = [
    ('Handle', HANDLE),
]
Operation.AccessToken = AccessToken


Operation._fields_ = [
    ('Directory', Operation.Directory),
    ('Create', Operation.Create),
    ('Read', Operation.Read),
    ('Write', Operation.Write),
    ('Delete', Operation.Delete),
    ('ResetTimeout', Operation.ResetTimeout),
    ('AccessToken', Operation.AccessToken),
]
_EVENT_INFORMATION.Operation = Operation


_EVENT_INFORMATION._fields_ = [
    ('SerialNumber', ULONG),
    ('Status', NTSTATUS),
    ('Flags', ULONG),
    ('Operation', _EVENT_INFORMATION.Operation),
    ('Context', ULONG64),
    ('BufferLength', ULONG),
    ('Buffer', UCHAR * 8),
]

# Dokan mount options
DOKAN_EVENT_ALTERNATIVE_STREAM_ON = 1
DOKAN_EVENT_WRITE_PROTECT = 1 << 1
DOKAN_EVENT_REMOVABLE = 1 << 2
DOKAN_EVENT_MOUNT_MANAGER = 1 << 3
DOKAN_EVENT_CURRENT_SESSION = 1 << 4
DOKAN_EVENT_FILELOCK_USER_MODE = 1 << 5

# Whether any oplock functionality should be disabled.
DOKAN_EVENT_DISABLE_OPLOCKS = 1 << 6
DOKAN_EVENT_ENABLE_FCB_GC = 1 << 7

# CaseSenitive FileName: NTFS can look to be case-insensitive
# but in some situation it can also be case-sensitive :
# * NTFS keep the filename casing used during Create internally.
# * Open "MyFile" on NTFS can open "MYFILE" if it exists.
# * FILE_FLAG_POSIX_SEMANTICS (IRP_MJ_CREATE: SL_CASE_SENSITIVE)
# can be used during Create to make the lookup case-sensitive.
# * Since Win10, NTFS can have specific directories
# case-sensitive / insensitive, even if the device tags says otherwise.
# Dokan choose to support case-sensitive or case-insensitive filesystem
# but not those NTFS specific scenarios.
DOKAN_EVENT_CASE_SENSITIVE = 1 << 8

# Enables unmounting of network drives via file explorer
DOKAN_EVENT_ENABLE_NETWORK_UNMOUNT = 1 << 9


_EVENT_DRIVER_INFO._fields_ = [
    ('DriverVersion', ULONG),
    ('Status', ULONG),
    ('DeviceNumber', ULONG),
    ('MountId', ULONG),
    ('DeviceName', WCHAR * 64),
]

_EVENT_START._fields_ = [
    ('UserVersion', ULONG),
    ('DeviceType', ULONG),
    ('Flags', ULONG),
    ('MountPoint', WCHAR * 260),
    ('UNCName', WCHAR * 64),
    ('IrpTimeout', ULONG),
]


if sys.getwindowsversion().major == 10:
    # FileRenameInformation
    class DUMMYUNIONNAME(ctypes.Union):
        pass


    DUMMYUNIONNAME._fields_ = [
        ('ReplaceIfExists', BOOLEAN),
        # FileRenameInformationEx
        ('Flags', ULONG),
    ]
    _DOKAN_RENAME_INFORMATION.DUMMYUNIONNAME = DUMMYUNIONNAME


_TEMP__DOKAN_RENAME_INFORMATION = [
]
if sys.getwindowsversion().major == 10:
    _TEMP__DOKAN_RENAME_INFORMATION += [
        ('DUMMYUNIONNAME', _DOKAN_RENAME_INFORMATION.DUMMYUNIONNAME),
    ]
else:
    _TEMP__DOKAN_RENAME_INFORMATION += [
        ('ReplaceIfExists', BOOLEAN),
    ]
# END IF


_TEMP__DOKAN_RENAME_INFORMATION += [
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]
_DOKAN_RENAME_INFORMATION._fields_ = _TEMP__DOKAN_RENAME_INFORMATION


_DOKAN_LINK_INFORMATION._fields_ = [
    ('ReplaceIfExists', BOOLEAN),
    ('FileNameLength', ULONG),
    ('FileName', WCHAR * 1),
]

# \struct DOKAN_CONTROL
# \brief Dokan Control
# File System Type */
_TEMP__DOKAN_CONTROL = [
    ('Type', ULONG),
    # Mount point. Can be "M:\" (drive letter) or "C:\mount\dokan"
    # (path in NTFS) */
    ('MountPoint', WCHAR * MAX_PATH),
    # UNC name used for network volume */
    ('UNCName', WCHAR * 64),
    # Disk Device Name */
    ('DeviceName', WCHAR * 64),
]

_TEMP__DOKAN_CONTROL += [
    # MinGW also do not support PVOID64 so we convert it to ULONG64
    # see 902.
    ('VolumeDeviceObject', PVOID64),
]

_TEMP__DOKAN_CONTROL += [
    # Session ID of calling process */
    ('SessionId', ULONG),
    # Contains information about the flags on the mount */
    ('MountOptions', ULONG),
]
_DOKAN_CONTROL._fields_ = _TEMP__DOKAN_CONTROL
