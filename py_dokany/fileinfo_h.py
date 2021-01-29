import ctypes
from ctypes.wintypes import (
    INT,
    ULONG,
    WCHAR,
    BOOLEAN,
    LARGE_INTEGER,
    HANDLE,
    LONG,
    USHORT,
    DWORD,
    WORD,
    CHAR,
    BYTE
)

POINTER = ctypes.POINTER
CCHAR = CHAR

PWSTR = POINTER(WCHAR)

ULONGLONG = ctypes.c_ulonglong
ACCESS_MASK = DWORD


class ENUM(INT):
    pass


class _FILE_ID_128(ctypes.Structure):
    pass


FILE_ID_128 = _FILE_ID_128


class _FILE_ALIGNMENT_INFORMATION(ctypes.Structure):
    pass


FILE_ALIGNMENT_INFORMATION = _FILE_ALIGNMENT_INFORMATION
PFILE_ALIGNMENT_INFORMATION = POINTER(_FILE_ALIGNMENT_INFORMATION)


class _FILE_NAME_INFORMATION(ctypes.Structure):
    pass


FILE_NAME_INFORMATION = _FILE_NAME_INFORMATION
PFILE_NAME_INFORMATION = POINTER(_FILE_NAME_INFORMATION)


class _FILE_ATTRIBUTE_TAG_INFORMATION(ctypes.Structure):
    pass


FILE_ATTRIBUTE_TAG_INFORMATION = _FILE_ATTRIBUTE_TAG_INFORMATION
PFILE_ATTRIBUTE_TAG_INFORMATION = POINTER(_FILE_ATTRIBUTE_TAG_INFORMATION)


class _FILE_DISPOSITION_INFORMATION(ctypes.Structure):
    pass


FILE_DISPOSITION_INFORMATION = _FILE_DISPOSITION_INFORMATION
PFILE_DISPOSITION_INFORMATION = POINTER(_FILE_DISPOSITION_INFORMATION)


class _FILE_DISPOSITION_INFORMATION_EX(ctypes.Structure):
    pass


FILE_DISPOSITION_INFORMATION_EX = _FILE_DISPOSITION_INFORMATION_EX
PFILE_DISPOSITION_INFORMATION_EX = POINTER(_FILE_DISPOSITION_INFORMATION_EX)


class _FILE_END_OF_FILE_INFORMATION(ctypes.Structure):
    pass


FILE_END_OF_FILE_INFORMATION = _FILE_END_OF_FILE_INFORMATION
PFILE_END_OF_FILE_INFORMATION = POINTER(_FILE_END_OF_FILE_INFORMATION)


class _FILE_VALID_DATA_LENGTH_INFORMATION(ctypes.Structure):
    pass


FILE_VALID_DATA_LENGTH_INFORMATION = _FILE_VALID_DATA_LENGTH_INFORMATION
PFILE_VALID_DATA_LENGTH_INFORMATION = POINTER(_FILE_VALID_DATA_LENGTH_INFORMATION)


class _FILE_BASIC_INFORMATION(ctypes.Structure):
    pass


FILE_BASIC_INFORMATION = _FILE_BASIC_INFORMATION
PFILE_BASIC_INFORMATION = POINTER(_FILE_BASIC_INFORMATION)


class _FILE_STANDARD_INFORMATION(ctypes.Structure):
    pass


FILE_STANDARD_INFORMATION = _FILE_STANDARD_INFORMATION
PFILE_STANDARD_INFORMATION = POINTER(_FILE_STANDARD_INFORMATION)


class _FILE_POSITION_INFORMATION(ctypes.Structure):
    pass


FILE_POSITION_INFORMATION = _FILE_POSITION_INFORMATION
PFILE_POSITION_INFORMATION = POINTER(_FILE_POSITION_INFORMATION)


class _FILE_DIRECTORY_INFORMATION(ctypes.Structure):
    pass


FILE_DIRECTORY_INFORMATION = _FILE_DIRECTORY_INFORMATION
PFILE_DIRECTORY_INFORMATION = POINTER(_FILE_DIRECTORY_INFORMATION)


class _FILE_FULL_DIR_INFORMATION(ctypes.Structure):
    pass


FILE_FULL_DIR_INFORMATION = _FILE_FULL_DIR_INFORMATION
PFILE_FULL_DIR_INFORMATION = POINTER(_FILE_FULL_DIR_INFORMATION)


class _FILE_ID_FULL_DIR_INFORMATION(ctypes.Structure):
    pass


FILE_ID_FULL_DIR_INFORMATION = _FILE_ID_FULL_DIR_INFORMATION
PFILE_ID_FULL_DIR_INFORMATION = POINTER(_FILE_ID_FULL_DIR_INFORMATION)


class _FILE_BOTH_DIR_INFORMATION(ctypes.Structure):
    pass


FILE_BOTH_DIR_INFORMATION = _FILE_BOTH_DIR_INFORMATION
PFILE_BOTH_DIR_INFORMATION = POINTER(_FILE_BOTH_DIR_INFORMATION)


class _FILE_ID_BOTH_DIR_INFORMATION(ctypes.Structure):
    pass


FILE_ID_BOTH_DIR_INFORMATION = _FILE_ID_BOTH_DIR_INFORMATION
PFILE_ID_BOTH_DIR_INFORMATION = POINTER(_FILE_ID_BOTH_DIR_INFORMATION)


class _FILE_ID_EXTD_BOTH_DIR_INFORMATION(ctypes.Structure):
    pass


FILE_ID_EXTD_BOTH_DIR_INFORMATION = _FILE_ID_EXTD_BOTH_DIR_INFORMATION
PFILE_ID_EXTD_BOTH_DIR_INFORMATION = POINTER(_FILE_ID_EXTD_BOTH_DIR_INFORMATION)


class _FILE_NAMES_INFORMATION(ctypes.Structure):
    pass


FILE_NAMES_INFORMATION = _FILE_NAMES_INFORMATION
PFILE_NAMES_INFORMATION = POINTER(_FILE_NAMES_INFORMATION)


class _FILE_INTERNAL_INFORMATION(ctypes.Structure):
    pass


FILE_INTERNAL_INFORMATION = _FILE_INTERNAL_INFORMATION
PFILE_INTERNAL_INFORMATION = POINTER(_FILE_INTERNAL_INFORMATION)


class _FILE_ID_INFORMATION(ctypes.Structure):
    pass


FILE_ID_INFORMATION = _FILE_ID_INFORMATION
PFILE_ID_INFORMATION = POINTER(_FILE_ID_INFORMATION)


class _FILE_EA_INFORMATION(ctypes.Structure):
    pass


FILE_EA_INFORMATION = _FILE_EA_INFORMATION
PFILE_EA_INFORMATION = POINTER(_FILE_EA_INFORMATION)


class _FILE_ACCESS_INFORMATION(ctypes.Structure):
    pass


FILE_ACCESS_INFORMATION = _FILE_ACCESS_INFORMATION
PFILE_ACCESS_INFORMATION = POINTER(_FILE_ACCESS_INFORMATION)


class _FILE_MODE_INFORMATION(ctypes.Structure):
    pass


FILE_MODE_INFORMATION = _FILE_MODE_INFORMATION
PFILE_MODE_INFORMATION = POINTER(_FILE_MODE_INFORMATION)


class _FILE_ALL_INFORMATION(ctypes.Structure):
    pass


FILE_ALL_INFORMATION = _FILE_ALL_INFORMATION
PFILE_ALL_INFORMATION = POINTER(_FILE_ALL_INFORMATION)


class _FILE_ALLOCATION_INFORMATION(ctypes.Structure):
    pass


FILE_ALLOCATION_INFORMATION = _FILE_ALLOCATION_INFORMATION
PFILE_ALLOCATION_INFORMATION = POINTER(_FILE_ALLOCATION_INFORMATION)


class _FILE_LINK_INFORMATION(ctypes.Structure):
    pass


FILE_LINK_INFORMATION = _FILE_LINK_INFORMATION
PFILE_LINK_INFORMATION = POINTER(_FILE_LINK_INFORMATION)


class _FILE_RENAME_INFORMATION(ctypes.Structure):
    pass


FILE_RENAME_INFORMATION = _FILE_RENAME_INFORMATION
PFILE_RENAME_INFORMATION = POINTER(_FILE_RENAME_INFORMATION)


class _FILE_STREAM_INFORMATION(ctypes.Structure):
    pass


FILE_STREAM_INFORMATION = _FILE_STREAM_INFORMATION
PFILE_STREAM_INFORMATION = POINTER(_FILE_STREAM_INFORMATION)


class _FILE_FS_LABEL_INFORMATION(ctypes.Structure):
    pass


FILE_FS_LABEL_INFORMATION = _FILE_FS_LABEL_INFORMATION
PFILE_FS_LABEL_INFORMATION = POINTER(_FILE_FS_LABEL_INFORMATION)


class _FILE_FS_VOLUME_INFORMATION(ctypes.Structure):
    pass


FILE_FS_VOLUME_INFORMATION = _FILE_FS_VOLUME_INFORMATION
PFILE_FS_VOLUME_INFORMATION = POINTER(_FILE_FS_VOLUME_INFORMATION)


class _FILE_FS_SIZE_INFORMATION(ctypes.Structure):
    pass


FILE_FS_SIZE_INFORMATION = _FILE_FS_SIZE_INFORMATION
PFILE_FS_SIZE_INFORMATION = POINTER(_FILE_FS_SIZE_INFORMATION)


class _FILE_FS_FULL_SIZE_INFORMATION(ctypes.Structure):
    pass


FILE_FS_FULL_SIZE_INFORMATION = _FILE_FS_FULL_SIZE_INFORMATION
PFILE_FS_FULL_SIZE_INFORMATION = POINTER(_FILE_FS_FULL_SIZE_INFORMATION)


class _FILE_FS_ATTRIBUTE_INFORMATION(ctypes.Structure):
    pass


FILE_FS_ATTRIBUTE_INFORMATION = _FILE_FS_ATTRIBUTE_INFORMATION
PFILE_FS_ATTRIBUTE_INFORMATION = POINTER(_FILE_FS_ATTRIBUTE_INFORMATION)


class _FILE_NETWORK_OPEN_INFORMATION(ctypes.Structure):
    pass


FILE_NETWORK_OPEN_INFORMATION = _FILE_NETWORK_OPEN_INFORMATION
PFILE_NETWORK_OPEN_INFORMATION = POINTER(_FILE_NETWORK_OPEN_INFORMATION)


class _FILE_NETWORK_PHYSICAL_NAME_INFORMATION(ctypes.Structure):
    pass


FILE_NETWORK_PHYSICAL_NAME_INFORMATION = _FILE_NETWORK_PHYSICAL_NAME_INFORMATION
PFILE_NETWORK_PHYSICAL_NAME_INFORMATION = POINTER(_FILE_NETWORK_PHYSICAL_NAME_INFORMATION)


class _UNICODE_STRING(ctypes.Structure):
    pass


UNICODE_STRING = _UNICODE_STRING
PUNICODE_STRING = POINTER(_UNICODE_STRING)


# /* Dokan : user-mode file system library for Windows Copyright (C) 2015 -
# 2019 Adrien J. < liryna.stark@gmail.com > and Maxime C. < maxime@islog.com >
# Copyright (C) 2007 - 2011 Hiroki Asakawa < info@dokan-dev.net >
# http://dokan-dev.github.io This program is free software; you can
# redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation; either version
# 3 of the License, or (at your option) any later version. This program is
# distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details. You
# should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see < http://www.gnu.org/licenses/ > .

IRP_MJ_CREATE = 0x00
IRP_MJ_CREATE_NAMED_PIPE = 0x01
IRP_MJ_CLOSE = 0x02
IRP_MJ_READ = 0x03
IRP_MJ_WRITE = 0x04
IRP_MJ_QUERY_INFORMATION = 0x05
IRP_MJ_SET_INFORMATION = 0x06
IRP_MJ_QUERY_EA = 0x07
IRP_MJ_SET_EA = 0x08
IRP_MJ_FLUSH_BUFFERS = 0x09
IRP_MJ_QUERY_VOLUME_INFORMATION = 0x0A
IRP_MJ_SET_VOLUME_INFORMATION = 0x0B
IRP_MJ_DIRECTORY_CONTROL = 0x0C
IRP_MJ_FILE_SYSTEM_CONTROL = 0x0D
IRP_MJ_DEVICE_CONTROL = 0x0E
IRP_MJ_INTERNAL_DEVICE_CONTROL = 0x0F
IRP_MJ_SHUTDOWN = 0x10
IRP_MJ_LOCK_CONTROL = 0x11
IRP_MJ_CLEANUP = 0x12
IRP_MJ_CREATE_MAILSLOT = 0x13
IRP_MJ_QUERY_SECURITY = 0x14
IRP_MJ_SET_SECURITY = 0x15
IRP_MJ_POWER = 0x16
IRP_MJ_SYSTEM_CONTROL = 0x17
IRP_MJ_DEVICE_CHANGE = 0x18
IRP_MJ_QUERY_QUOTA = 0x19
IRP_MJ_SET_QUOTA = 0x1A
IRP_MJ_PNP = 0x1B
IRP_MJ_PNP_POWER = IRP_MJ_PNP
IRP_MJ_MAXIMUM_FUNCTION = 0x1B
IRP_MN_LOCK = 0x01
IRP_MN_UNLOCK_SINGLE = 0x02
IRP_MN_UNLOCK_ALL = 0x03
IRP_MN_UNLOCK_ALL_BY_KEY = 0x04


class _FILE_INFORMATION_CLASS(ENUM):
    FileDirectoryInformation = 1
    FileFullDirectoryInformation = 2
    FileBothDirectoryInformation = 3
    FileBasicInformation = 4
    FileStandardInformation = 5
    FileInternalInformation = 6
    FileEaInformation = 7
    FileAccessInformation = 8
    FileNameInformation = 9
    FileRenameInformation = 10
    FileLinkInformation = 11
    FileNamesInformation = 12
    FileDispositionInformation = 13
    FilePositionInformation = 14
    FileFullEaInformation = 15
    FileModeInformation = 16
    FileAlignmentInformation = 17
    FileAllInformation = 18
    FileAllocationInformation = 19
    FileEndOfFileInformation = 20
    FileAlternateNameInformation = 21
    FileStreamInformation = 22
    FilePipeInformation = 23
    FilePipeLocalInformation = 24
    FilePipeRemoteInformation = 25
    FileMailslotQueryInformation = 26
    FileMailslotSetInformation = 27
    FileCompressionInformation = 28
    FileObjectIdInformation = 29
    FileCompletionInformation = 30
    FileMoveClusterInformation = 31
    FileQuotaInformation = 32
    FileReparsePointInformation = 33
    FileNetworkOpenInformation = 34
    FileAttributeTagInformation = 35
    FileTrackingInformation = 36
    FileIdBothDirectoryInformation = 37
    FileIdFullDirectoryInformation = 38
    FileValidDataLengthInformation = 39
    FileShortNameInformation = 40
    FileIoCompletionNotificationInformation = 41
    FileIoStatusBlockRangeInformation = 42
    FileIoPriorityHintInformation = 43
    FileSfioReserveInformation = 44
    FileSfioVolumeInformation = 45
    FileHardLinkInformation = 46
    FileProcessIdsUsingFileInformation = 47
    FileNormalizedNameInformation = 48
    FileNetworkPhysicalNameInformation = 49
    FileIdGlobalTxDirectoryInformation = 50
    FileIsRemoteDeviceInformation = 51
    FileUnusedInformation = 52
    FileNumaNodeInformation = 53
    FileStandardLinkInformation = 54
    FileRemoteProtocolInformation = 55
    FileRenameInformationBypassAccessCheck = 56
    FileLinkInformationBypassAccessCheck = 57
    FileVolumeNameInformation = 58
    FileIdInformation = 59
    FileIdExtdDirectoryInformation = 60
    FileReplaceCompletionInformation = 61
    FileHardLinkFullIdInformation = 62
    FileIdExtdBothDirectoryInformation = 63
    FileDispositionInformationEx = 64
    FileRenameInformationEx = 65
    FileRenameInformationExBypassAccessCheck = 66
    FileDesiredStorageClassInformation = 67
    FileStatInformation = 68
    FileMemoryPartitionInformation = 69
    FileMaximumInformation = 70


FILE_INFORMATION_CLASS = _FILE_INFORMATION_CLASS
PFILE_INFORMATION_CLASS = POINTER(_FILE_INFORMATION_CLASS)


class _FSINFOCLASS(ENUM):
    FileFsVolumeInformation = 1
    FileFsLabelInformation = 2
    FileFsSizeInformation = 3
    FileFsDeviceInformation = 4
    FileFsAttributeInformation = 5
    FileFsControlInformation = 6
    FileFsFullSizeInformation = 7
    FileFsObjectIdInformation = 8
    FileFsDriverPathInformation = 9
    FileFsVolumeFlagsInformation = 10
    FileFsMaximumInformation = 11


FS_INFORMATION_CLASS = _FSINFOCLASS
PFS_INFORMATION_CLASS = POINTER(_FSINFOCLASS)


_FILE_ID_128._fields_ = [
    ('Identifier', BYTE * 16),
]

# \struct FILE_ALIGNMENT_INFORMATION
# \brief Used as an argument to the ZwQueryInformationFile routine.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileAllInformation
_FILE_ALIGNMENT_INFORMATION._fields_ = [
    # For more information, see DEVICE_OBJECT and Initializing a Device
    # Object.
    ('AlignmentRequirement', ULONG),
]

# \struct FILE_NAME_INFORMATION
# \brief Used as argument to the ZwQueryInformationFile and
# ZwSetInformationFile routines.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileNameInformation
_FILE_NAME_INFORMATION._fields_ = [
    # Specifies the length, in bytes, of the file name string.
    ('FileNameLength', ULONG),
    # Specifies the first character of the file name string. This is
    # followed in memory by the remainder of the string.
    ('FileName', WCHAR * 1),
]

# \struct FILE_ATTRIBUTE_TAG_INFORMATION
# \brief Used as an argument to ZwQueryInformationFile.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileAttributeTagInformation
_FILE_ATTRIBUTE_TAG_INFORMATION._fields_ = [
    # For descriptions of these flags, see the documentation of the
    # GetFileAttributes function in the Microsoft Windows SDK.
    ('FileAttributes', ULONG),
    # this member specifies the reparse tag. Otherwise, this member is
    # unused.
    ('ReparseTag', ULONG),
]

# \struct FILE_DISPOSITION_INFORMATION
# \brief Used as an argument to the ZwSetInformationFile routine.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileDispositionInformation
_FILE_DISPOSITION_INFORMATION._fields_ = [
    # Otherwise, set to FALSE. Setting this member to FALSE has no effect
    # if the handle was opened with FILE_FLAG_DELETE_ON_CLOSE.
    ('DeleteFile', BOOLEAN),
]

# Specifies the system should not delete a file.
FILE_DISPOSITION_DO_NOT_DELETE = 0x00000000

# Specifies the system should delete a file.
FILE_DISPOSITION_DELETE = 0x00000001

# Specifies the system should perform a POSIX - style delete.
FILE_DISPOSITION_POSIX_SEMANTICS = 0x00000002

# Specifies the system should force an image section check.
FILE_DISPOSITION_FORCE_IMAGE_SECTION_CHECK = 0x00000004

# Specifies if the system sets or clears the on - close state.
FILE_DISPOSITION_ON_CLOSE = 0x00000008

# \struct FILE_DISPOSITION_INFORMATION_EX
# \brief Used as an argument to the ZwSetInformationFile routine.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileDispositionInformationEx
_FILE_DISPOSITION_INFORMATION_EX._fields_ = [
    # \li \c FILE_DISPOSITION_ON_CLOSE Specifies if the system sets or
    # clears the on-close state.
    ('Flags', ULONG),
]

# \struct FILE_END_OF_FILE_INFORMATION
# \brief Used as an argument to the ZwSetInformationFile routine.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileEndOfFileInformation
_FILE_END_OF_FILE_INFORMATION._fields_ = [
    # The absolute new end of file position as a byte offset from the
    # start of the file.
    ('EndOfFile', LARGE_INTEGER),
]

# \struct FILE_VALID_DATA_LENGTH_INFORMATION
# \brief Used as an argument to ZwSetInformationFile.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileValidDataLengthInformation
_FILE_VALID_DATA_LENGTH_INFORMATION._fields_ = [
    # This parameter must be a positive value that is greater than the
    # current valid data length, but less than or equal to the current
    # file size.
    ('ValidDataLength', LARGE_INTEGER),
]

# \struct FILE_BASIC_INFORMATION
# \brief Used as an argument to routines that query or set file
# information.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileBasicInformation and FileAllInformation
_FILE_BASIC_INFORMATION._fields_ = [
    # Specifies the time that the file was created.
    ('CreationTime', LARGE_INTEGER),
    # Specifies the time that the file was last accessed.
    ('LastAccessTime', LARGE_INTEGER),
    # Specifies the time that the file was last written to.
    ('LastWriteTime', LARGE_INTEGER),
    # Specifies the last time the file was changed.
    ('ChangeTime', LARGE_INTEGER),
    # see the documentation for the GetFileAttributes function in the
    # Microsoft Windows SDK.
    ('FileAttributes', ULONG),
]

# \struct FILE_STANDARD_INFORMATION
# \brief Used as an argument to routines that query or set file
# information.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileStandardInformation and FileAllInformation
_FILE_STANDARD_INFORMATION._fields_ = [
    # The file allocation size in bytes. Usually, this value is a multiple
    # of the sector or cluster size of the underlying physical device.
    ('AllocationSize', LARGE_INTEGER),
    # The end of file location as a byte offset.
    ('EndOfFile', LARGE_INTEGER),
    # The number of hard links to the file.
    ('NumberOfLinks', ULONG),
    # The delete pending status. TRUE indicates that a file deletion has
    # been requested.
    ('DeletePending', BOOLEAN),
    # The file directory status. TRUE indicates the file object represents
    # a directory.
    ('Directory', BOOLEAN),
]

# \struct FILE_POSITION_INFORMATION
# \brief Used as an argument to routines that query or set file
# information.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FilePositionInformation and FileAllInformation
_FILE_POSITION_INFORMATION._fields_ = [
    # The byte offset of the current file pointer.
    ('CurrentByteOffset', LARGE_INTEGER),
]

# \struct FILE_DIRECTORY_INFORMATION
# \brief Used to query detailed information for the files in a directory.
_FILE_DIRECTORY_INFORMATION._fields_ = [
    # This member is zero if no other entries follow this one.
    ('NextEntryOffset', ULONG),
    # in which the position of a file within the parent directory is not
    # fixed and can be changed at any time to maintain sort order.
    ('FileIndex', ULONG),
    # Time when the file was created.
    ('CreationTime', LARGE_INTEGER),
    # Last time the file was accessed.
    ('LastAccessTime', LARGE_INTEGER),
    # Last time information was written to the file.
    ('LastWriteTime', LARGE_INTEGER),
    # Last time the file was changed.
    ('ChangeTime', LARGE_INTEGER),
    # EndOfFile is the offset to the byte immediately following the last
    # valid byte in the file.
    ('EndOfFile', LARGE_INTEGER),
    # File allocation size, in bytes. Usually, this value is a multiple of
    # the sector or cluster size of the underlying physical device.
    ('AllocationSize', LARGE_INTEGER),
    # \li \c FILE_ATTRIBUTE_COMPRESSED
    ('FileAttributes', ULONG),
    # Specifies the length of the file name string.
    ('FileNameLength', ULONG),
    # This is followed in memory by the remainder of the string.
    ('FileName', WCHAR * 1),
]

# \struct FILE_FULL_DIR_INFORMATION
# \brief Used to query detailed information for the files in a directory.
_FILE_FULL_DIR_INFORMATION._fields_ = [
    # This member is zero if no other entries follow this one.
    ('NextEntryOffset', ULONG),
    # in which the position of a file within the parent directory is not
    # fixed and can be changed at any time to maintain sort order.
    ('FileIndex', ULONG),
    # Time when the file was created.
    ('CreationTime', LARGE_INTEGER),
    # Last time the file was accessed.
    ('LastAccessTime', LARGE_INTEGER),
    # Last time information was written to the file.
    ('LastWriteTime', LARGE_INTEGER),
    # Last time the file was changed.
    ('ChangeTime', LARGE_INTEGER),
    # EndOfFile is the offset to the byte immediately following the last
    # valid byte in the file.
    ('EndOfFile', LARGE_INTEGER),
    # File allocation size, in bytes. Usually, this value is a multiple of
    # the sector or cluster size of the underlying physical device.
    ('AllocationSize', LARGE_INTEGER),
    # \li \c FILE_ATTRIBUTE_COMPRESSED
    ('FileAttributes', ULONG),
    # Specifies the length of the file name string.
    ('FileNameLength', ULONG),
    # Combined length, in bytes, of the extended attributes (EA) for the
    # file.
    ('EaSize', ULONG),
    # This is followed in memory by the remainder of the string.
    ('FileName', WCHAR * 1),
]

# \struct FILE_ID_FULL_DIR_INFORMATION
# \brief Used to query detailed information for the files in a directory.
_FILE_ID_FULL_DIR_INFORMATION._fields_ = [
    # This member is zero if no other entries follow this one.
    ('NextEntryOffset', ULONG),
    # in which the position of a file within the parent directory is not
    # fixed and can be changed at any time to maintain sort order.
    ('FileIndex', ULONG),
    # Time when the file was created.
    ('CreationTime', LARGE_INTEGER),
    # Last time the file was accessed.
    ('LastAccessTime', LARGE_INTEGER),
    # Last time information was written to the file.
    ('LastWriteTime', LARGE_INTEGER),
    # Last time the file was changed.
    ('ChangeTime', LARGE_INTEGER),
    # EndOfFile is the offset to the byte immediately following the last
    # valid byte in the file.
    ('EndOfFile', LARGE_INTEGER),
    # File allocation size, in bytes. Usually, this value is a multiple of
    # the sector or cluster size of the underlying physical device.
    ('AllocationSize', LARGE_INTEGER),
    # \li \c FILE_ATTRIBUTE_COMPRESSED
    ('FileAttributes', ULONG),
    # Specifies the length of the file name string.
    ('FileNameLength', ULONG),
    # Combined length, in bytes, of the extended attributes (EA) for the
    # file.
    ('EaSize', ULONG),
    # "file object ID" that was added to NTFS for Microsoft Windows 2000.)
    ('FileId', LARGE_INTEGER),

    # This is followed in memory by the remainder of the string.
    ('FileName', WCHAR * 1),
]
# \struct FILE_BOTH_DIR_INFORMATION
# \brief Used to query detailed information for the files in a directory.
_FILE_BOTH_DIR_INFORMATION._fields_ = [

    # This member is zero if no other entries follow this one.
    ('NextEntryOffset', ULONG),
    # in which the position of a file within the parent directory is not
    # fixed and can be changed at any time to maintain sort order.
    ('FileIndex', ULONG),

    # Time when the file was created.
    ('CreationTime', LARGE_INTEGER),

    # Last time the file was accessed.
    ('LastAccessTime', LARGE_INTEGER),

    # Last time information was written to the file.
    ('LastWriteTime', LARGE_INTEGER),

    # Last time the file was changed.
    ('ChangeTime', LARGE_INTEGER),
    # EndOfFile is the offset to the byte immediately following the last
    # valid byte in the file.
    ('EndOfFile', LARGE_INTEGER),

    # File allocation size, in bytes. Usually, this value is a multiple of
    # the sector or cluster size of the underlying physical device.
    ('AllocationSize', LARGE_INTEGER),

    # \li \c FILE_ATTRIBUTE_COMPRESSED
    ('FileAttributes', ULONG),

    # Specifies the length of the file name string.
    ('FileNameLength', ULONG),
    # Combined length, in bytes, of the extended attributes (EA) for the
    # file.
    ('EaSize', ULONG),

    # Specifies the length, in bytes, of the SHORT file name string.
    ('ShortNameLength', CCHAR),

    # Unicode string containing the SHORT (8.3) name for the file.
    ('ShortName', WCHAR * 12),
    # Specifies the first character of the file name string. This is
    # followed in memory by the remainder of the string.
    ('FileName', WCHAR * 1),
]
# \struct FILE_ID_BOTH_DIR_INFORMATION
# \brief Used to query detailed information for the files in a directory.
_FILE_ID_BOTH_DIR_INFORMATION._fields_ = [

    # This member is zero if no other entries follow this one.
    ('NextEntryOffset', ULONG),
    # in which the position of a file within the parent directory is not
    # fixed and can be changed at any time to maintain sort order.
    ('FileIndex', ULONG),

    # Time when the file was created.
    ('CreationTime', LARGE_INTEGER),

    # Last time the file was accessed.
    ('LastAccessTime', LARGE_INTEGER),

    # Last time information was written to the file.
    ('LastWriteTime', LARGE_INTEGER),

    # Last time the file was changed.
    ('ChangeTime', LARGE_INTEGER),
    # EndOfFile is the offset to the byte immediately following the last
    # valid byte in the file.
    ('EndOfFile', LARGE_INTEGER),

    # File allocation size, in bytes. Usually, this value is a multiple of
    # the sector or cluster size of the underlying physical device.
    ('AllocationSize', LARGE_INTEGER),

    # \li \c FILE_ATTRIBUTE_COMPRESSED
    ('FileAttributes', ULONG),

    # Specifies the length of the file name string.
    ('FileNameLength', ULONG),
    # Combined length, in bytes, of the extended attributes (EA) for the
    # file.
    ('EaSize', ULONG),

    # Specifies the length, in bytes, of the SHORT file name string.
    ('ShortNameLength', CCHAR),

    # Unicode string containing the SHORT (8.3) name for the file.
    ('ShortName', WCHAR * 12),
    # (Note that the FileId is not the same as the 16-byte "file object ID"
    # that was added to NTFS for Microsoft Windows 2000.)
    ('FileId', LARGE_INTEGER),

    # Specifies the first character of the file name string. This is
    # followed in memory by the remainder of the string.
    ('FileName', WCHAR * 1),
]
# \struct FILE_ID_EXTD_BOTH_DIR_INFORMATION
# \brief Used to query detailed information for the files in a directory.
_FILE_ID_EXTD_BOTH_DIR_INFORMATION._fields_ = [

    # This member is zero if no other entries follow this one.
    ('NextEntryOffset', ULONG),
    # in which the position of a file within the parent directory is not
    # fixed and can be changed at any time to maintain sort order.
    ('FileIndex', ULONG),

    # Time when the file was created.
    ('CreationTime', LARGE_INTEGER),

    # Last time the file was accessed.
    ('LastAccessTime', LARGE_INTEGER),

    # Last time information was written to the file.
    ('LastWriteTime', LARGE_INTEGER),

    # Last time the file was changed.
    ('ChangeTime', LARGE_INTEGER),
    # EndOfFile is the offset to the byte immediately following the last
    # valid byte in the file.
    ('EndOfFile', LARGE_INTEGER),

    # File allocation size, in bytes. Usually, this value is a multiple of
    # the sector or cluster size of the underlying physical device.
    ('AllocationSize', LARGE_INTEGER),

    # \li \c FILE_ATTRIBUTE_COMPRESSED
    ('FileAttributes', ULONG),

    # Specifies the length of the file name string.
    ('FileNameLength', ULONG),
    # Combined length, in bytes, of the extended attributes (EA) for the
    # file.
    ('EaSize', ULONG),

    # Tag value for the reparse point.
    ('ReparsePointTag', ULONG),
    # The 128-byte file reference number for the file. This number is
    # generated and assigned to the file by the file system.
    ('FileId', FILE_ID_128),

    # Specifies the length, in bytes, of the SHORT file name string.
    ('ShortNameLength', CCHAR),

    # Unicode string containing the SHORT (8.3) name for the file.
    ('ShortName', WCHAR * 12),
    # Specifies the first character of the file name string. This is
    # followed in memory by the remainder of the string.
    ('FileName', WCHAR * 1),
]
# \struct FILE_NAMES_INFORMATION
# \brief Used to query detailed information about the names of files in a
# directory.
_FILE_NAMES_INFORMATION._fields_ = [

    # This member is zero if no other entries follow this one.
    ('NextEntryOffset', ULONG),
    # in which the position of a file within the parent directory is not
    # fixed and can be changed at any time to maintain sort order.
    ('FileIndex', ULONG),

    # Specifies the length of the file name string.
    ('FileNameLength', ULONG),
    # Specifies the first character of the file name string. This is
    # followed in memory by the remainder of the string.
    ('FileName', WCHAR * 1),
]

ANSI_DOS_STAR = '<'
ANSI_DOS_QM = '>'
ANSI_DOS_DOT = '"'
DOS_STAR = '<'
DOS_QM = '>'
DOS_DOT = '"'

# \struct FILE_INTERNAL_INFORMATION
# \brief Used to query for the file system's 8-byte file reference number
# for a file.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileInternalInformation
_FILE_INTERNAL_INFORMATION._fields_ = [

    # (Note that this is not the same as the 16-byte "file object ID"
    # that was added to NTFS for Microsoft Windows 2000.)
    ('IndexNumber', LARGE_INTEGER),
]
# \struct FILE_ID_INFORMATION
# \brief Contains identification information for a file.
# This structure is returned from the GetFileInformationByHandleEx
# function when FileIdInfo is passed in the FileInformationClass parameter.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileIdInformation
_FILE_ID_INFORMATION._fields_ = [

    # The serial number of the volume that contains a file.
    ('VolumeSerialNumber', ULONGLONG),
    # To determine whether two open handles represent the same file,
    # combine the identifier and the volume serial number for each file
    # and compare them.
    ('FileId', FILE_ID_128),
]
# \struct FILE_EA_INFORMATION
# \brief Used to query for the size of the extended attributes (EA) for a
# file.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileEaInformation and FileAllInformation
_FILE_EA_INFORMATION._fields_ = [

    # Specifies the combined length, in bytes, of the extended attributes
    # for the file.
    ('EaSize', ULONG),
]
# \struct FILE_ACCESS_INFORMATION
# \brief Used to query for or set the access rights of a file.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileAllInformation
_FILE_ACCESS_INFORMATION._fields_ = [

    # This member is a value of type ACCESS_MASK.
    ('AccessFlags', ACCESS_MASK),
]
# \struct FILE_MODE_INFORMATION
# \brief Used to query or set the access mode of a file.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileAllInformation
_FILE_MODE_INFORMATION._fields_ = [

    # \li \c FILE_DELETE_ON_CLOSE
    ('Mode', ULONG),
]
# \struct FILE_ALL_INFORMATION
# \brief Structure is a container for several FILE_XXX_INFORMATION
# structures.
# The struct is requested during IRP_MJ_QUERY_INFORMATION with query
# FileAllInformation
# \see FILE_BASIC_INFORMATION
_FILE_ALL_INFORMATION._fields_ = [
    ('BasicInformation', FILE_BASIC_INFORMATION),

    # \see FILE_STANDARD_INFORMATION
    ('StandardInformation', FILE_STANDARD_INFORMATION),

    # \see FILE_INTERNAL_INFORMATION
    ('InternalInformation', FILE_INTERNAL_INFORMATION),

    # \see FILE_EA_INFORMATION
    ('EaInformation', FILE_EA_INFORMATION),

    # \see FILE_ACCESS_INFORMATION
    ('AccessInformation', FILE_ACCESS_INFORMATION),

    # \see FILE_POSITION_INFORMATION
    ('PositionInformation', FILE_POSITION_INFORMATION),

    # \see FILE_MODE_INFORMATION
    ('ModeInformation', FILE_MODE_INFORMATION),

    # \see FILE_ALIGNMENT_INFORMATION
    ('AlignmentInformation', FILE_ALIGNMENT_INFORMATION),

    # \see FILE_NAME_INFORMATION
    ('NameInformation', FILE_NAME_INFORMATION),
]
# \struct FILE_ALLOCATION_INFORMATION
# \brief Used to set the allocation size for a file.
# The struct is requested during IRP_MJ_SET_INFORMATION with query
# FileAllocationInformation
_FILE_ALLOCATION_INFORMATION._fields_ = [

    # of the sector or cluster size of the underlying physical device.
    ('AllocationSize', LARGE_INTEGER),
]
# \struct FILE_LINK_INFORMATION
# \brief Used to create an NTFS hard link to an existing file.
# The struct is requested during IRP_MJ_SET_INFORMATION with query
# FileLinkInformation
_FILE_LINK_INFORMATION._fields_ = [

    # Set to FALSE if the link creation operation should fail if the link
    # already exists.
    ('ReplaceIfExists', BOOLEAN),

    # Otherwise it is a handle for the directory where the link is to be
    # created.
    ('RootDirectory', HANDLE),

    # Length, in bytes, of the file name string.
    ('FileNameLength', ULONG),
    # (See the Remarks section for ZwQueryInformationFile for details on the syntax of this file name string.)
    #
    ('FileName', WCHAR * 1),
]
# \struct FILE_RENAME_INFORMATION
# \brief Used to rename a file.
# The struct is requested during IRP_MJ_SET_INFORMATION with query
# FileRenameInformation
_FILE_RENAME_INFORMATION._fields_ = [

    # Set to FALSE if the rename operation should fail if a file with the
    # given name already exists.
    ('ReplaceIfExists', BOOLEAN),

    # it is a handle for the root directory under which the file will
    # reside after it is renamed.
    ('RootDirectory', HANDLE),

    # Length, in bytes, of the new name for the file.
    ('FileNameLength', ULONG),

    # Otherwise, it specifies only the file name or a relative pathname.
    ('FileName', WCHAR * 1),
]
# \struct FILE_STREAM_INFORMATION
# \brief Used to enumerate the streams for a file.
# The struct is requested during IRP_MJ_SET_INFORMATION query
# FileStreamInformation
_FILE_STREAM_INFORMATION._fields_ = [

    # This member is zero if no other entries follow this one.
    ('NextEntryOffset', ULONG),

    # Length, in bytes, of the StreamName string.
    ('StreamNameLength', ULONG),

    # Size, in bytes, of the stream.
    ('StreamSize', LARGE_INTEGER),

    # or cluster size of the underlying physical device.
    ('StreamAllocationSize', LARGE_INTEGER),

    # Unicode string that contains the name of the stream.
    ('StreamName', WCHAR * 1),
]
# \struct FILE_FS_LABEL_INFORMATION
# \brief Used to set the label for a file system volume.
# The struct is requested during IRP_MJ_SET_VOLUME_INFORMATION query
# FileFsLabelInformation
_FILE_FS_LABEL_INFORMATION._fields_ = [

    # Length, in bytes, of the name for the volume.
    ('VolumeLabelLength', ULONG),

    # Name for the volume.
    ('VolumeLabel', WCHAR * 1),
]
# \struct FILE_FS_VOLUME_INFORMATION
# \brief Used to query information about a volume on which a file system
# is mounted.
# The struct is requested during IRP_MJ_QUERY_VOLUME_INFORMATION query
# FileFsVolumeInformation
_FILE_FS_VOLUME_INFORMATION._fields_ = [

    # Time when the volume was created.
    ('VolumeCreationTime', LARGE_INTEGER),

    # Serial number of the volume.
    ('VolumeSerialNumber', ULONG),

    # Length, in bytes, of the name of the volume.
    ('VolumeLabelLength', ULONG),
    # TRUE if the file system supports object-oriented file system
    # objects, FALSE otherwise.
    ('SupportsObjects', BOOLEAN),

    # Name of the volume.
    ('VolumeLabel', WCHAR * 1),
]
# \struct FILE_FS_SIZE_INFORMATION
# \brief Used to query sector size information for a file system volume.
# The struct is requested during IRP_MJ_QUERY_VOLUME_INFORMATION query
# FileFsSizeInformation
_FILE_FS_SIZE_INFORMATION._fields_ = [

    # If per-user quotas are in use, this value may be less than the total
    # number of allocation units on the disk.
    ('TotalAllocationUnits', LARGE_INTEGER),

    # If per-user quotas are in use, this value may be less than the total
    # number of free allocation units on the disk.
    ('AvailableAllocationUnits', LARGE_INTEGER),

    # Number of sectors in each allocation unit.
    ('SectorsPerAllocationUnit', ULONG),

    # Number of bytes in each sector.
    ('BytesPerSector', ULONG),
]
# \struct FILE_FS_FULL_SIZE_INFORMATION
# \brief Used to query sector size information for a file system volume.
# The struct is requested during IRP_MJ_QUERY_VOLUME_INFORMATION query
# FileFsFullSizeInformation
_FILE_FS_FULL_SIZE_INFORMATION._fields_ = [

    # If per-user quotas are in use, this value may be less than the total
    # number of allocation units on the disk.
    ('TotalAllocationUnits', LARGE_INTEGER),

    # If per-user quotas are in use, this value may be less than the total
    # number of free allocation units on the disk.
    ('CallerAvailableAllocationUnits', LARGE_INTEGER),

    # Total number of free allocation units on the volume.
    ('ActualAvailableAllocationUnits', LARGE_INTEGER),

    # Number of sectors in each allocation unit.
    ('SectorsPerAllocationUnit', ULONG),

    # Number of bytes in each sector.
    ('BytesPerSector', ULONG),
]
# \struct FILE_FS_ATTRIBUTE_INFORMATION
# \brief Used to query attribute information for a file system.
# The struct is requested during IRP_MJ_QUERY_VOLUME_INFORMATION query
# FileFsAttributeInformation
_FILE_FS_ATTRIBUTE_INFORMATION._fields_ = [

    # \see
    # https://msdn.microsoft.com/en-us/library/windows/hardware/ff540251(v=vs.85).aspx
    #
    ('FileSystemAttributes', ULONG),

    # A file name component is that portion of a file name between
    # backslashes.
    ('MaximumComponentNameLength', LONG),

    # Length, in bytes, of the file system name.
    ('FileSystemNameLength', ULONG),

    # File system name.
    ('FileSystemName', WCHAR * 1),
]
# \struct FILE_NETWORK_OPEN_INFORMATION
# \brief Used as an argument to ZwQueryInformationFile.
# The struct is requested during IRP_MJ_QUERY_VOLUME_INFORMATION query
# FileNetworkOpenInformation
_FILE_NETWORK_OPEN_INFORMATION._fields_ = [

    # Specifies the time that the file was created.
    ('CreationTime', LARGE_INTEGER),

    # Specifies the time that the file was last accessed.
    ('LastAccessTime', LARGE_INTEGER),

    # Specifies he time that the file was last written to.
    ('LastWriteTime', LARGE_INTEGER),

    # Specifies the time that the file was last changed.
    ('ChangeTime', LARGE_INTEGER),
    # this value is a multiple of the sector or cluster size of the
    # underlying physical device.
    ('AllocationSize', LARGE_INTEGER),

    # EndOfFile is the offset to the byte immediately following the last
    # valid byte in the file.
    ('EndOfFile', LARGE_INTEGER),

    # see the documentation of the GetFileAttributes function in the
    # Microsoft Windows SDK.
    ('FileAttributes', ULONG),
]
# \struct FILE_NETWORK_PHYSICAL_NAME_INFORMATION
# \brief Contains the full UNC physical pathname for a file or directory
# on a remote file share.
# The struct is requested during IRP_MJ_QUERY_VOLUME_INFORMATION query
# FileNetworkPhysicalNameInformation
_FILE_NETWORK_PHYSICAL_NAME_INFORMATION._fields_ = [

    # The length, in bytes, of the physical name in FileName.
    ('FileNameLength', ULONG),

    # The full UNC path of the network file share of the target.
    ('FileName', WCHAR * 1),
]


SL_RESTART_SCAN = 0x01
SL_RETURN_SINGLE_ENTRY = 0x02
SL_INDEX_SPECIFIED = 0x04
SL_FORCE_ACCESS_CHECK = 0x01
SL_OPEN_PAGING_FILE = 0x02
SL_OPEN_TARGET_DIRECTORY = 0x04
SL_CASE_SENSITIVE = 0x80


def ALIGN_DOWN(length, type_):
    return length & ~(ctypes.sizeof(type_) - 1)


def ALIGN_UP(length, type_):
    return ALIGN_DOWN(length + ctypes.sizeof(type_) - 1, type_)


def ALIGN_DOWN_POINTER(address, type_):
    return address & ~(ctypes.sizeof(type_) - 1)


def ALIGN_UP_POINTER(address, type_):
    return ALIGN_DOWN_POINTER(address + ctypes.sizeof(type_) - 1, type_)


def WordAlign(Val):
    return ALIGN_UP(Val, WORD)


def WordAlignPtr(Ptr):
    return ALIGN_UP_POINTER(Ptr, WORD)


def LongAlign(Val):
    return ALIGN_UP(Val, LONG)


def LongAlignPtr(Ptr):
    return ALIGN_UP_POINTER(Ptr, LONG)


def QuadAlign(Val):
    return ALIGN_UP(Val, ULONGLONG)


def QuadAlignPtr(Ptr):
    return ALIGN_UP_POINTER(Ptr, ULONGLONG)


def IsPtrQuadAligned(Ptr):
    return QuadAlign(Ptr) == Ptr


# from wdm.h
FILE_SUPERSEDE = 0x00000000
FILE_OPEN = 0x00000001
FILE_CREATE = 0x00000002
FILE_OPEN_IF = 0x00000003
FILE_OVERWRITE = 0x00000004
FILE_OVERWRITE_IF = 0x00000005
FILE_MAXIMUM_DISPOSITION = 0x00000005
FILE_DIRECTORY_FILE = 0x00000001
FILE_WRITE_THROUGH = 0x00000002
FILE_SEQUENTIAL_ONLY = 0x00000004
FILE_NO_INTERMEDIATE_BUFFERING = 0x00000008
FILE_SYNCHRONOUS_IO_ALERT = 0x00000010
FILE_SYNCHRONOUS_IO_NONALERT = 0x00000020
FILE_NON_DIRECTORY_FILE = 0x00000040
FILE_CREATE_TREE_CONNECTION = 0x00000080
FILE_COMPLETE_IF_OPLOCKED = 0x00000100
FILE_NO_EA_KNOWLEDGE = 0x00000200
FILE_OPEN_REMOTE_INSTANCE = 0x00000400
FILE_RANDOM_ACCESS = 0x00000800
FILE_DELETE_ON_CLOSE = 0x00001000
FILE_OPEN_BY_FILE_ID = 0x00002000
FILE_OPEN_FOR_BACKUP_INTENT = 0x00004000
FILE_NO_COMPRESSION = 0x00008000
FILE_OPEN_REQUIRING_OPLOCK = 0x00010000
FILE_DISALLOW_EXCLUSIVE = 0x00020000

FILE_SESSION_AWARE = 0x00040000

FILE_RESERVE_OPFILTER = 0x00100000
FILE_OPEN_REPARSE_POINT = 0x00200000
FILE_OPEN_NO_RECALL = 0x00400000
FILE_OPEN_FOR_FREE_SPACE_QUERY = 0x00800000
FILE_VALID_OPTION_FLAGS = 0x00FFFFFF
FILE_SUPERSEDED = 0x00000000
FILE_OPENED = 0x00000001
FILE_CREATED = 0x00000002
FILE_OVERWRITTEN = 0x00000003
FILE_EXISTS = 0x00000004
FILE_DOES_NOT_EXIST = 0x00000005
FILE_WRITE_TO_END_OF_FILE = 0xFFFFFFFF
FILE_USE_FILE_POINTER_POSITION = 0xFFFFFFFE

# \struct UNICODE_STRING
# \brief Structure is used to define Unicode strings.
_UNICODE_STRING._fields_ = [
    # The length, in bytes, of the string stored in Buffer.
    ('Length', USHORT),
    # The length, in bytes, of Buffer.
    ('MaximumLength', USHORT),
    # Pointer to a buffer used to contain a string of wide characters.
    ('Buffer', PWSTR),
]
