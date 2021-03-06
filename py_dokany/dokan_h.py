
#  Dokan : user-mode file system library for Windows

#  Copyright (C) 2015 - 2019 Adrien J. <liryna.stark@gmail.com> and Maxime C. <maxime@islog.com>
#  Copyright (C) 2020 Google, Inc.
#  Copyright (C) 2007 - 2011 Hiroki Asakawa <info@dokan-dev.net>

#  http://dokan-dev.github.io

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

#  Do not include NTSTATUS. Fix  duplicate preprocessor definitions
# define WIN32_NO_STATUS
# include <windows.h>
# undef WIN32_NO_STATUS
# include <ntstatus.h>
import ctypes

from .public_h import (
    PDOKAN_IO_SECURITY_CONTEXT,
    DOKAN_MAJOR_API_VERSION,
    PDOKAN_CONTROL
)
from .windows_api import (
    UCHAR,
    FILETIME,
    LONGLONG,
    PULONGLONG,
    USHORT,
    ULONG,
    ACCESS_MASK,
    NTSTATUS,
    POINTER,
    LPCWSTR,
    INT,
    PWIN32_FIND_DATAW,
    VOID,
    LPCVOID,
    DWORD,
    LPDWORD,
    PSECURITY_DESCRIPTOR,
    PSECURITY_INFORMATION,
    LPWSTR,
    LPVOID,
    ULONG64,
    BOOL,
    WCHAR,
    CHAR,
    PULONG,
    HANDLE,
    LPBY_HANDLE_FILE_INFORMATION,
    PWIN32_FIND_STREAM_DATA,

)


# ifdef _EXPORTING
# Export dokan API see also dokan.def for export */
# define DOKANAPI __stdcall
# else
# Import dokan API */
# define DOKANAPI __declspec(dllimport) __stdcall
# endif

# Change calling convention to standard call */
# define DOKAN_CALLBACK __stdcall
DOKAN_CALLBACK = ctypes.CFUNCTYPE
# ifdef __cplusplus
# extern "C" {
# endif

# @file */

#
# \defgroup Dokan Dokan
# \brief Dokan Library const and methods
#
# @{ */


# The current Dokan version (140 means ver 1.4.0). \ref DOKAN_OPTIONS.Version */
# define DOKAN_VERSION 141
DOKAN_VERSION = 141
# Minimum Dokan version (ver 1.1.0) accepted. */
# define DOKAN_MINIMUM_COMPATIBLE_VERSION 110
DOKAN_MINIMUM_COMPATIBLE_VERSION = 110
# Driver file name including the DOKAN_MAJOR_API_VERSION */
# define DOKAN_DRIVER_NAME L"dokan" DOKAN_MAJOR_API_VERSION L".sys"
DOKAN_DRIVER_NAME = "dokan" + DOKAN_MAJOR_API_VERSION + ".sys"

# Network provider name including the DOKAN_MAJOR_API_VERSION */
# define DOKAN_NP_NAME L"Dokan" DOKAN_MAJOR_API_VERSION
DOKAN_NP_NAME = "Dokan" + DOKAN_MAJOR_API_VERSION

#
# \defgroup DOKAN_OPTION DOKAN_OPTION
# \brief All DOKAN_OPTION flags used in DOKAN_OPTIONS.Options
# \see DOKAN_FILE_INFO
#

# Enable ouput debug message */
DOKAN_OPTION_DEBUG = 1

# Enable ouput debug message to stderr */
DOKAN_OPTION_STDERR = 2

# Enable the use of alternate stream paths in the form
# <file-name>:<stream-name>. If this is not specified then the driver will
# fail any attempt to access a path with a colon.
DOKAN_OPTION_ALT_STREAM = 4

# Enable mount drive as write-protected */
DOKAN_OPTION_WRITE_PROTECT = 8

# Use network drive - Dokan network provider needs to be installed */
DOKAN_OPTION_NETWORK = 16

# Use removable drive
# Be aware that on some environments, the userland application will be denied
# to communicate with the drive which will result in a unwanted unmount.
# \see <a href="https://github.com/dokan-dev/dokany/issues/843">Issue #843</a>
DOKAN_OPTION_REMOVABLE = 32

# Use mount manager */
DOKAN_OPTION_MOUNT_MANAGER = 64

# Mount the drive on current session only */
DOKAN_OPTION_CURRENT_SESSION = 128

# Enable Lockfile/Unlockfile operations. Otherwise Dokan will take care of it */
DOKAN_OPTION_FILELOCK_USER_MODE = 256

# Whether DokanNotifyXXX functions should be enabled, which requires this
# library to maintain a special handle while the file system is mounted.
# Without this flag, the functions always return FALSE if invoked.
DOKAN_OPTION_ENABLE_NOTIFICATION_API = 512

# Whether to disable any oplock support on the volume.
# Regular range locks are enabled regardless.
DOKAN_OPTION_DISABLE_OPLOCKS = 1024

# The advantage of the FCB GC approach is that it prevents filter drivers (Anti-virus)
# from exponentially slowing down procedures like zip file extraction due to
# repeatedly rebuilding state that they attach to the FCB header.
DOKAN_OPTION_ENABLE_FCB_GARBAGE_COLLECTION = 2048

# Enable Case sensitive path.
# By default all path are case insensitive.
# For case sensitive: \dir\File & \diR\file are different files
# but for case insensitive they are the same.
DOKAN_OPTION_CASE_SENSITIVE = 4096

# Allows unmounting of network drive via explorer */
DOKAN_OPTION_ENABLE_UNMOUNT_NETWORK_DRIVE = 8192


# \struct DOKAN_OPTIONS
# \brief Dokan mount options used to describe Dokan device behavior.
# \see DokanMain
#
class _DOKAN_OPTIONS(ctypes.Structure):
    _fields_ = [
        # Version of the Dokan features requested without dots (version "123" is equal to Dokan version 1.2.3). */
        ('Version', USHORT),
        # Number of threads to be used by Dokan library internally. More threads will handle more
        # events at the same time. */
        ('ThreadCount', USHORT),
        # Features enabled for the mount. See \ref DOKAN_OPTION. */
        ('Options', ULONG),
        # FileSystem can store anything here. */
        ('GlobalContext', ULONG64),
        # Mount point. It can be a driver letter like "M:\" or a folder path "C:\mount\dokan" on a NTFS partition. */
        ('MountPoint', LPCWSTR),

        # UNC Name for the Network Redirector
        ('UNCName', LPCWSTR),

        # Max timeout in milliseconds of each request before Dokan gives up to wait events to complete.
        # A timeout request is a sign that the userland implementation is no longer able to properly
        # manage requests in time.
        # The driver will therefore unmount the device when a timeout trigger in order to keep the system stable.
        # The default timeout value is 15 seconds.
        ('Timeout', ULONG),
        # Allocation Unit Size of the volume. This will affect the file size. */
        ('AllocationUnitSize', ULONG),
        # Sector Size of the volume. This will affect the file size. */
        ('SectorSize', ULONG),
    ]


DOKAN_OPTIONS = _DOKAN_OPTIONS
PDOKAN_OPTIONS = POINTER(_DOKAN_OPTIONS)


#
# \struct DOKAN_FILE_INFO
# \brief Dokan file information on the current operation.
#
class _DOKAN_FILE_INFO(ctypes.Structure):
    _fields_ = [
        # Context that can be used to carry information between operations.
        # The context can carry whatever type like \c HANDLE, struct, int,
        # internal reference that will help the implementation understand the request context of the event.
        ('Context', ULONG64),

        # Reserved. Used internally by Dokan library. Never modify. */
        ('DokanContext', ULONG64),

        # A pointer to DOKAN_OPTIONS which was passed to DokanMain. */
        ('DokanOptions', PDOKAN_OPTIONS),

        # Process ID for the thread that originally requested a given I/O operation.
        ('ProcessId', ULONG),

        # Requesting a directory file.
        # Must be set in \ref DOKAN_OPERATIONS.ZwCreateFile if the file appears to be a folder.
        ('IsDirectory', UCHAR),

        # Flag if the file has to be deleted during DOKAN_OPERATIONS. Cleanup event. */
        ('DeleteOnClose', UCHAR),

        # Read or write is paging IO. */
        ('PagingIo', UCHAR),

        # Read or write is synchronous IO. */
        ('SynchronousIo', UCHAR),

        # Read or write directly from data source without cache */
        ('Nocache', UCHAR),

        #  If \c TRUE, write to the current end of file instead of using the Offset parameter. */
        ('WriteToEndOfFile', UCHAR)
    ]


dokan1 = ctypes.cdll.LoadLibrary('dokan1.dll')
DOKAN_FILE_INFO = _DOKAN_FILE_INFO
PDOKAN_FILE_INFO = POINTER(_DOKAN_FILE_INFO)


# \brief FillFindData Used to add an entry in FindFiles operation
# \return 1 if buffer is full, otherwise 0 (currently it never returns 1)
PFillFindData = ctypes.WINFUNCTYPE(INT, PWIN32_FIND_DATAW, PDOKAN_FILE_INFO)
# \brief FillFindStreamData Used to add an entry in FindStreams
# \return 1 if buffer is full, otherwise 0 (currently it never returns 1)
PFillFindStreamData = ctypes.WINFUNCTYPE(INT, PWIN32_FIND_STREAM_DATA, PDOKAN_FILE_INFO)

# clang-format off

# \struct DOKAN_OPERATIONS
# \brief Dokan API callbacks interface
#
# DOKAN_OPERATIONS is a struct of callbacks that describe all Dokan API operations
# that will be called when Windows access to the filesystem.
#
# If an error occurs, return NTSTATUS (https://support.microsoft.com/en-us/kb/113996).
# Win32 Error can be converted to \c NTSTATUS with \ref DokanNtStatusFromWin32
#
# All callbacks can be set to \c NULL or return \c STATUS_NOT_IMPLEMENTED
# if supporting one of them is not desired. Be aware that returning such values to important
# callbacks* such as DOKAN_OPERATIONS.ZwCreateFile / DOKAN_OPERATIONS.ReadFile / ...
# would make the filesystem not work or become unstable.

ZW_CREATE_FILE = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    PDOKAN_IO_SECURITY_CONTEXT,
    ACCESS_MASK,
    ULONG,
    ULONG,
    ULONG,
    ULONG,
    PDOKAN_FILE_INFO
)

CLEANUP = DOKAN_CALLBACK(
    VOID,
    LPCWSTR,
    PDOKAN_FILE_INFO
)

CLOSE_FILE = DOKAN_CALLBACK(
    VOID,
    LPCWSTR,
    PDOKAN_FILE_INFO
)

READ_FILE = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    LPVOID,
    DWORD,
    LPDWORD,
    LONGLONG,
    PDOKAN_FILE_INFO
)

WRITE_FILE = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    LPCVOID,
    DWORD,
    LPDWORD,
    LONGLONG,
    PDOKAN_FILE_INFO
)

FLUSH_FILE_BUFFERS = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    PDOKAN_FILE_INFO
)

GET_FILE_INFORMATION = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    LPBY_HANDLE_FILE_INFORMATION,
    PDOKAN_FILE_INFO
)

FIND_FILES = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    PFillFindData,
    PDOKAN_FILE_INFO
)

FIND_FILES_WITH_PATTERN = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    LPCWSTR,
    PFillFindData,
    PDOKAN_FILE_INFO
)

SET_FILE_ATTRIBUTES = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    DWORD,
    PDOKAN_FILE_INFO
)

SET_FILE_TIME = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    POINTER(FILETIME),
    POINTER(FILETIME),
    POINTER(FILETIME),
    PDOKAN_FILE_INFO
)

DELETE_FILE = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    PDOKAN_FILE_INFO
)

DELETE_DIRECTORY = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    PDOKAN_FILE_INFO
)

MOVE_FILE = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    LPCWSTR,
    BOOL,
    PDOKAN_FILE_INFO
)

SET_END_OF_FILE = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    LONGLONG,
    PDOKAN_FILE_INFO
)

SET_ALLOCATION_SIZE = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    LONGLONG,
    PDOKAN_FILE_INFO
)

LOCK_FILE = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    LONGLONG,
    LONGLONG,
    PDOKAN_FILE_INFO
)

UNLOCK_FILE = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    LONGLONG,
    LONGLONG,
    PDOKAN_FILE_INFO
)

GET_DISK_FREE_SPACE = DOKAN_CALLBACK(
    NTSTATUS,
    PULONGLONG,
    PULONGLONG,
    PULONGLONG,
    PDOKAN_FILE_INFO
)

GET_VOLUME_INFORMATION = DOKAN_CALLBACK(
    NTSTATUS,
    LPWSTR,
    DWORD,
    LPDWORD,
    LPDWORD,
    LPDWORD,
    LPWSTR,
    DWORD,
    PDOKAN_FILE_INFO
)

MOUNTED = DOKAN_CALLBACK(
    NTSTATUS,
    PDOKAN_FILE_INFO
)

UNMOUNTED = DOKAN_CALLBACK(
    NTSTATUS,
    PDOKAN_FILE_INFO
)

GET_FILE_SECURITY = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    PSECURITY_INFORMATION,
    PSECURITY_DESCRIPTOR,
    ULONG,
    PULONG,
    PDOKAN_FILE_INFO
)

SET_FILE_SECURITY = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    PSECURITY_INFORMATION,
    PSECURITY_DESCRIPTOR,
    ULONG,
    PDOKAN_FILE_INFO
)

FIND_STREAMS = DOKAN_CALLBACK(
    NTSTATUS,
    LPCWSTR,
    PFillFindStreamData,
    PDOKAN_FILE_INFO
)


class _DOKAN_OPERATIONS(ctypes.Structure):
    def zw_create_file(self, value):
        size = ctypes.sizeof(value)
        ctypes.memmove(self.ZwCreateFile, value, size)

    zw_create_file = property(fset=zw_create_file)

    _fields_ = [

        # \brief CreateFile Dokan API callback
        #
        # CreateFile is called each time a request is made on a file system object.
        #
        # In case \c OPEN_ALWAYS & \c CREATE_ALWAYS are successfully opening an
        # existing file, \c STATUS_OBJECT_NAME_COLLISION should be returned instead of \c STATUS_SUCCESS .
        # This will inform Dokan that the file has been opened and not created during the request.
        #
        # If the file is a directory, CreateFile is also called.
        # In this case, CreateFile should return \c STATUS_SUCCESS when that directory
        # can be opened and DOKAN_FILE_INFO.IsDirectory has to be set to \c TRUE.
        # On the other hand, if DOKAN_FILE_INFO.IsDirectory is set to \c TRUE
        # but the path targets a file, \c STATUS_NOT_A_DIRECTORY must be returned.
        #
        # DOKAN_FILE_INFO.Context can be used to store Data (like \c HANDLE)
        # that can be retrieved in all other requests related to the Context.
        # To avoid memory leak, Context needs to be released in DOKAN_OPERATIONS.Cleanup.
        #
        # \param FileName File path requested by the Kernel on the FileSystem.
        # \param SecurityContext SecurityContext,
        # see https://msdn.microsoft.com/en-us/library/windows/hardware/ff550613(v=vs.85).aspx
        # \param DesiredAccess Specifies an
        # <a href="https://msdn.microsoft.com/en-us/library/windows/hardware/ff540466(v=vs.85).aspx">
        # ACCESS_MASK</a> value that determines the requested access to the object.
        # \param FileAttributes Specifies one or more FILE_ATTRIBUTE_XXX flags, which
        # represent the file attributes to set if a file is created or overwritten.
        # \param ShareAccess Type of share access, which is specified as zero or any combination of FILE_SHARE_* flags.
        # \param CreateDisposition Specifies the action to perform if the file does or does not exist.
        # \param CreateOptions Specifies the options to apply when the driver creates or opens the file.
        # \param DokanFileInfo Information about the file or directory.
        # \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # \see <a href="https://msdn.microsoft.com/en-us/library/windows/hardware/ff566424(v=vs.85).aspx">
        # See ZwCreateFile for more information about the parameters of this callback (MSDN).</a>
        # \see DokanMapKernelToUserCreateFileFlags
        # LPCWSTR FileName,
        # PDOKAN_IO_SECURITY_CONTEXT SecurityContext,
        # ACCESS_MASK DesiredAccess,
        # ULONG FileAttributes,
        # ULONG ShareAccess,
        # ULONG CreateDisposition,
        # ULONG CreateOptions,
        # PDOKAN_FILE_INFO DokanFileInfo);
        ('ZwCreateFile', ZW_CREATE_FILE),

        # \brief Cleanup Dokan API callback
        #
        # Cleanup request before \ref CloseFile is called.
        #
        # When DOKAN_FILE_INFO.DeleteOnClose is \c TRUE, the file in Cleanup must be deleted.
        # See DeleteFile documentation for explanation.
        #
        # \param FileName File path requested by the Kernel on the FileSystem.
        # \param DokanFileInfo Information about the file or directory.
        # \see DeleteFile
        # \see DeleteDirectory
        # LPCWSTR FileName,
        # PDOKAN_FILE_INFO DokanFileInfo
        ('Cleanup', CLEANUP),

        # \brief CloseFile Dokan API callback
        #
        # Clean remaining Context
        #
        # CloseFile is called at the end of the life of the context.
        # Anything remaining in \ref DOKAN_FILE_INFO.Context must be cleared before returning.
        #
        # \param FileName File path requested by the Kernel on the FileSystem.
        # \param DokanFileInfo Information about the file or directory.
        # LPCWSTR FileName,
        # PDOKAN_FILE_INFO DokanFileInfo
        ('CloseFile', CLOSE_FILE),

        # \brief ReadFile Dokan API callback
        #
        # ReadFile callback on the file previously opened in DOKAN_OPERATIONS.ZwCreateFile.
        # It can be called by different threads at the same time, so the read/context has to be thread safe.
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param Buffer Read buffer that has to be filled with the read result.
        # * \param BufferLength Buffer length and read size to continue with.
        # * \param ReadLength Total data size that has been read.
        # * \param Offset Offset from where the read has to be continued.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see WriteFile
        # */
        # LPCWSTR FileName,
        #     LPVOID Buffer,
        #     DWORD BufferLength,
        #     LPDWORD ReadLength,
        #     LONGLONG Offset,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('ReadFile', READ_FILE),

        # /**
        # * \brief WriteFile Dokan API callback
        # *
        # * WriteFile callback on the file previously opened in DOKAN_OPERATIONS.ZwCreateFile
        # * It can be called by different threads at the same time, sp the write/context has to be thread safe.
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param Buffer Data that has to be written.
        # * \param NumberOfBytesToWrite Buffer length and write size to continue with.
        # * \param NumberOfBytesWritten Total number of bytes that have been written.
        # * \param Offset Offset from where the write has to be continued.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see ReadFile
        # */
        # LPCWSTR FileName,
        #     LPCVOID Buffer,
        #     DWORD NumberOfBytesToWrite,
        #     LPDWORD NumberOfBytesWritten,
        #     LONGLONG Offset,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('WriteFile', WRITE_FILE),

        # /**
        # * \brief FlushFileBuffers Dokan API callback
        # *
        # * Clears buffers for this context and causes any buffered data to be written to the file.
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # */
        # LPCWSTR FileName,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('FlushFileBuffers', FLUSH_FILE_BUFFERS),

        # /**
        # * \brief GetFileInformation Dokan API callback
        # *
        # * Get specific information on a file.
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param Buffer BY_HANDLE_FILE_INFORMATION struct to fill.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # */
        # LPCWSTR FileName,
        #     LPBY_HANDLE_FILE_INFORMATION Buffer,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('GetFileInformation', GET_FILE_INFORMATION),

        # /**
        # * \brief FindFiles Dokan API callback
        # *
        # * List all files in the requested path
        # * \ref DOKAN_OPERATIONS.FindFilesWithPattern is checked first. If it is not implemented or
        # * returns \c STATUS_NOT_IMPLEMENTED, then FindFiles is called, if implemented.
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param FillFindData Callback that has to be called with PWIN32_FIND_DATAW that contain file information.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see FindFilesWithPattern
        # */
        # LPCWSTR FileName,
        #     PFillFindData FillFindData,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('FindFiles', FIND_FILES),

        # /**
        # * \brief FindFilesWithPattern Dokan API callback
        # *
        # * Same as \ref DOKAN_OPERATIONS.FindFiles but with a search pattern.\n
        # * The search pattern is a Windows MS-DOS-style expression. See \ref DokanIsNameInExpression .
        # *
        # * \param PathName Path requested by the Kernel on the FileSystem.
        # * \param SearchPattern Search pattern.
        # * \param FillFindData Callback that has to be called with PWIN32_FIND_DATAW that contains file information.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see FindFiles
        # * \see DokanIsNameInExpression
        # */
        # LPCWSTR PathName,
        #     LPCWSTR SearchPattern,
        #     PFillFindData FillFindData,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('FindFilesWithPattern', FIND_FILES_WITH_PATTERN),

        # /**
        # * \brief SetFileAttributes Dokan API callback
        # *
        # * Set file attributes on a specific file
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param FileAttributes FileAttributes to set on file.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # */
        # LPCWSTR FileName,
        #     DWORD FileAttributes,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('SetFileAttributes', SET_FILE_ATTRIBUTES),

        # /**
        # * \brief SetFileTime Dokan API callback
        # *
        # * Set file attributes on a specific file
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param CreationTime Creation FILETIME.
        # * \param LastAccessTime LastAccess FILETIME.
        # * \param LastWriteTime LastWrite FILETIME.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # */
        # LPCWSTR FileName,
        #     CONST FILETIME *CreationTime,
        #     CONST FILETIME *LastAccessTime,
        #     CONST FILETIME *LastWriteTime,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('SetFileTime', SET_FILE_TIME),

        # /**
        # * \brief DeleteFile Dokan API callback
        # *
        # * Check if it is possible to delete a file.
        # *
        # * DeleteFile will also be called with DOKAN_FILE_INFO.DeleteOnClose set to \c FALSE
        # * to notify the driver when the file is no longer requested to be deleted.
        # *
        # * The file in DeleteFile should not be deleted, but instead the file
        # * must be checked as to whether or not it can be deleted,
        # * and \c STATUS_SUCCESS should be returned (when it can be deleted) or
        # * appropriate error codes, such as \c STATUS_ACCESS_DENIED or
        # * \c STATUS_OBJECT_NAME_NOT_FOUND, should be returned.
        # *
        # * When \c STATUS_SUCCESS is returned, a Cleanup call is received afterwards with
        # * DOKAN_FILE_INFO.DeleteOnClose set to \c TRUE. Only then must the closing file
        # * be deleted.
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see DeleteDirectory
        # * \see Cleanup
        # */
        # LPCWSTR FileName,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('DeleteFile', DELETE_FILE),

        # /**
        # * \brief DeleteDirectory Dokan API callback
        # *
        # * Check if it is possible to delete a directory.
        # *
        # * DeleteDirectory will also be called with DOKAN_FILE_INFO.DeleteOnClose set to \c FALSE
        # * to notify the driver when the file is no longer requested to be deleted.
        # *
        # * The Directory in DeleteDirectory should not be deleted, but instead
        # * must be checked as to whether or not it can be deleted,
        # * and \c STATUS_SUCCESS should be returned (when it can be deleted) or
        # * appropriate error codes, such as \c STATUS_ACCESS_DENIED,
        # * \c STATUS_OBJECT_PATH_NOT_FOUND, or \c STATUS_DIRECTORY_NOT_EMPTY, should
        # * be returned.
        # *
        # * When \c STATUS_SUCCESS is returned, a Cleanup call is received afterwards with
        # * DOKAN_FILE_INFO.DeleteOnClose set to \c TRUE. Only then must the closing file
        # * be deleted.
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or \c NTSTATUS appropriate to the request result.
        # * \ref DeleteFile
        # * \ref Cleanup
        # */
        # LPCWSTR FileName,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('DeleteDirectory', DELETE_DIRECTORY),

        # /**
        # * \brief MoveFile Dokan API callback
        # *
        # * Move a file or directory to a new destination
        # *
        # * \param FileName Path for the file to be moved.
        # * \param NewFileName Path for the new location of the file.
        # * \param ReplaceIfExisting If destination already exists, can it be replaced?
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # */
        # LPCWSTR FileName,
        #     LPCWSTR NewFileName,
        #     BOOL ReplaceIfExisting,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('MoveFile', MOVE_FILE),

        # /**
        # * \brief SetEndOfFile Dokan API callback
        # *
        # * SetEndOfFile is used to truncate or extend a file (physical file size).
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param ByteOffset File length to set.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # */
        # LPCWSTR FileName,
        #     LONGLONG ByteOffset,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('SetEndOfFile', SET_END_OF_FILE),

        # /**
        # * \brief SetAllocationSize Dokan API callback
        # *
        # * SetAllocationSize is used to truncate or extend a file.
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param AllocSize File length to set.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # */
        # LPCWSTR FileName,
        #     LONGLONG AllocSize,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('SetAllocationSize', SET_ALLOCATION_SIZE),

        # /**
        # * \brief LockFile Dokan API callback
        # *
        # * Lock file at a specific offset and data length.
        # * This is only used if \ref DOKAN_OPTION_FILELOCK_USER_MODE is enabled.
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param ByteOffset Offset from where the lock has to be continued.
        # * \param Length Data length to lock.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see UnlockFile
        # */
        # LPCWSTR FileName,
        #     LONGLONG ByteOffset,
        #     LONGLONG Length,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('LockFile', LOCK_FILE),

        # /**
        # * \brief UnlockFile Dokan API callback
        # *
        # * Unlock file at a specific offset and data length.
        # * This is only used if \ref DOKAN_OPTION_FILELOCK_USER_MODE is enabled.
        # *
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param ByteOffset Offset from where the lock has to be continued.
        # * \param Length Data length to lock.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see LockFile
        # */
        # LPCWSTR FileName,
        #     LONGLONG ByteOffset,
        #     LONGLONG Length,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('UnlockFile', UNLOCK_FILE),

        # /**
        # * \brief GetDiskFreeSpace Dokan API callback
        # *
        # * Retrieves information about the amount of space that is available on a disk volume.
        # * It consits of the total amount of space, the total amount of free space, and
        # * the total amount of free space available to the user that is associated with the calling thread.
        # *
        # * Neither GetDiskFreeSpace nor \ref GetVolumeInformation
        # * save the  DOKAN_FILE_INFO.Context.
        # * Before these methods are called, \ref ZwCreateFile may not be called.
        # * (ditto \ref CloseFile and \ref Cleanup)
        # *
        # * \param FreeBytesAvailable Amount of available space.
        # * \param TotalNumberOfBytes Total size of storage space
        # * \param TotalNumberOfFreeBytes Amount of free space
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or \c NTSTATUS appropriate to the request result.
        # * \see <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa364937(v=vs.85).aspx">
        # GetDiskFreeSpaceEx function (MSDN)</a>
        # * \see GetVolumeInformation
        # */
        # PULONGLONG FreeBytesAvailable,
        #     PULONGLONG TotalNumberOfBytes,
        #     PULONGLONG TotalNumberOfFreeBytes,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('GetDiskFreeSpace', GET_DISK_FREE_SPACE),

        # /**
        # * \brief GetVolumeInformation Dokan API callback
        # *
        # * Retrieves information about the file system and volume associated with the specified root directory.
        # *
        # * Neither GetVolumeInformation nor GetDiskFreeSpace
        # * save the \ref DOKAN_FILE_INFO#Context.
        # * Before these methods are called, \ref ZwCreateFile may not be called.
        # * (ditto \ref CloseFile and \ref Cleanup)
        # *
        # * VolumeName length can be anything that fit in the provided buffer.
        # * But some Windows component expect it to be no longer than 32 characters
        # * that why it is recommended to set a value under this limit.
        # *
        # * FileSystemName could be anything up to 10 characters.
        # * But Windows check few feature availability based on file system name.
        # * For this, it is recommended to set NTFS or FAT here.
        # *
        # * \c FILE_READ_ONLY_VOLUME is automatically added to the
        # * FileSystemFlags if \ref DOKAN_OPTION_WRITE_PROTECT was
        # * specified in DOKAN_OPTIONS when the volume was mounted.
        # *
        # * \param VolumeNameBuffer A pointer to a buffer that receives the name of a specified volume.
        # * \param VolumeNameSize The length of a volume name buffer.
        # * \param VolumeSerialNumber A pointer to a variable that receives the volume serial number.
        # * \param MaximumComponentLength A pointer to a variable that receives the maximum length.
        # * \param FileSystemFlags A pointer to a variable that receives flags associated with
        # the specified file system.
        # * \param FileSystemNameBuffer A pointer to a buffer that receives the name of the file system.
        # * \param FileSystemNameSize The length of the file system name buffer.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa364993(v=vs.85).aspx">
        # GetVolumeInformation function (MSDN)</a>
        # * \see GetDiskFreeSpace
        # */
        # LPWSTR VolumeNameBuffer,
        #     DWORD VolumeNameSize,
        #     LPDWORD VolumeSerialNumber,
        #     LPDWORD MaximumComponentLength,
        #     LPDWORD FileSystemFlags,
        #     LPWSTR FileSystemNameBuffer,
        #     DWORD FileSystemNameSize,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('GetVolumeInformation', GET_VOLUME_INFORMATION),

        # /**
        # * \brief Mounted Dokan API callback
        # *
        # * Called when Dokan successfully mounts the volume.
        # *
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see Unmounted
        # */
        # PDOKAN_FILE_INFO DokanFileInfo
        ('Mounted', MOUNTED),

        # /**
        # * \brief Unmounted Dokan API callback
        # *
        # * Called when Dokan is unmounting the volume.
        # *
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or \c NTSTATUS appropriate to the request result.
        # * \see Mounted
        # */
        # PDOKAN_FILE_INFO DokanFileInfo
        ('Unmounted', UNMOUNTED),

        # /**
        # * \brief GetFileSecurity Dokan API callback
        # *
        # * Get specified information about the security of a file or directory.
        # *
        # * Return \c STATUS_NOT_IMPLEMENTED to let dokan library build a sddl of
        # the current process user with authenticate user rights for context menu.
        # * Return \c STATUS_BUFFER_OVERFLOW if buffer size is too small.
        # *
        # * \since Supported since version 0.6.0. The version must be specified in \ref DOKAN_OPTIONS.Version.
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param SecurityInformation A SECURITY_INFORMATION value that identifies
        # the security information being requested.
        # * \param SecurityDescriptor A pointer to a buffer that receives a copy of the
        # security descriptor of the requested file.
        # * \param BufferLength Specifies the size, in bytes, of the buffer.
        # * \param LengthNeeded A pointer to the variable that receives the number of bytes
        # necessary to store the complete security descriptor.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see SetFileSecurity
        # * \see <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa446639(v=vs.85).aspx">
        # GetFileSecurity function (MSDN)</a>
        # */
        # LPCWSTR FileName,
        #     PSECURITY_INFORMATION SecurityInformation,
        #     PSECURITY_DESCRIPTOR SecurityDescriptor,
        #     ULONG BufferLength,
        #     PULONG LengthNeeded,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('GetFileSecurity', GET_FILE_SECURITY),

        # /**
        # * \brief SetFileSecurity Dokan API callback
        # *
        # * Sets the security of a file or directory object.
        # *
        # * \since Supported since version 0.6.0. The version must be specified in \ref DOKAN_OPTIONS.Version.
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param SecurityInformation Structure that identifies the contents of the security
        # descriptor pointed by \a SecurityDescriptor param.
        # * \param SecurityDescriptor A pointer to a SECURITY_DESCRIPTOR structure.
        # * \param BufferLength Specifies the size, in bytes, of the buffer.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # * \see GetFileSecurity
        # * \see <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa379577(v=vs.85).aspx">
        # SetFileSecurity function (MSDN)</a>
        # */
        # LPCWSTR FileName,
        #     PSECURITY_INFORMATION SecurityInformation,
        #     PSECURITY_DESCRIPTOR SecurityDescriptor,
        #     ULONG BufferLength,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('SetFileSecurity', SET_FILE_SECURITY),

        # /**
        # * \brief FindStreams Dokan API callback
        # *
        # * Retrieve all NTFS Streams informations on the file.
        # * This is only called if \ref DOKAN_OPTION_ALT_STREAM is enabled.
        # *
        # * \since Supported since version 0.8.0. The version must be specified in \ref DOKAN_OPTIONS.Version.
        # * \param FileName File path requested by the Kernel on the FileSystem.
        # * \param FillFindStreamData Callback that has to be called with
        # PWIN32_FIND_STREAM_DATA that contain stream information.
        # * \param DokanFileInfo Information about the file or directory.
        # * \return \c STATUS_SUCCESS on success or NTSTATUS appropriate to the request result.
        # */
        # LPCWSTR FileName,
        #     PFillFindStreamData FillFindStreamData,
        #     PDOKAN_FILE_INFO DokanFileInfo
        ('FindStreams', FIND_STREAMS)
    ]


DOKAN_OPERATIONS = _DOKAN_OPERATIONS
PDOKAN_OPERATIONS = POINTER(_DOKAN_OPERATIONS)

# // clang-format on
#
# /**
#  * \defgroup DokanMainResult DokanMainResult
#  * \brief \ref DokanMain returns error codes
#  */
# /** @{ */

# /** Dokan mount succeed. */
DOKAN_SUCCESS = 0

# /** Dokan mount error. */
DOKAN_ERROR = -1

# /** Dokan mount failed - Bad drive letter. */
DOKAN_DRIVE_LETTER_ERROR = -2

# /** Dokan mount failed - Can't install driver.  */
DOKAN_DRIVER_INSTALL_ERROR = -3

# /** Dokan mount failed - Driver answer that something is wrong. */
DOKAN_START_ERROR = -4

# /**
#  * Dokan mount failed.
#  * Can't assign a drive letter or mount point.
#  * Probably already used by another volume.
#  */
DOKAN_MOUNT_ERROR = -5

# /**
#  * Dokan mount failed.
#  * Mount point is invalid.
#  */
DOKAN_MOUNT_POINT_ERROR = -6

# /**
#  * Dokan mount failed.
#  * Requested an incompatible version.
#  */
DOKAN_VERSION_ERROR = -7
#
# /** @} */
#
# /**
#  * \defgroup Dokan Dokan
#  */
# /** @{ */
#
# /**
#  * \brief Mount a new Dokan Volume.
#  *
#  * This function block until the device is unmounted.
#  * If the mount fails, it will directly return a \ref DokanMainResult error.
#  *
#  * \param DokanOptions a \ref DOKAN_OPTIONS that describe the mount.
#  * \param DokanOperations Instance of \ref DOKAN_OPERATIONS that will be called for each request made by the kernel.
#  * \return \ref DokanMainResult status.
#  */
_DokanMain = dokan1.DokanMain
_DokanMain.restype = INT


def DokanMain(DokanOptions, DokanOperations):
    return _DokanMain(
        ctypes.byref(DokanOptions),
        ctypes.byref(DokanOperations)
    )


#
# /**
#  * \brief Unmount a Dokan device from a driver letter.
#  *
#  * \param DriveLetter Dokan driver letter to unmount.
#  * \return \c TRUE if device was unmounted or \c FALSE in case of failure or device not found.
#  */
_DokanUnmount = dokan1.DokanUnmount
_DokanUnmount.restype = BOOL


def DokanUnmount(DriveLetter):
    DriveLetter = WCHAR(DriveLetter)
    return _DokanUnmount(DriveLetter)


#
# /**
#  * \brief Unmount a Dokan device from a mount point
#  *
#  * \param MountPoint Mount point to unmount ("Z", "Z:", "Z:\", "Z:\MyMountPoint").
#  * \return \c TRUE if device was unmounted or \c FALSE in case of failure or device not found.
#  */
_DokanRemoveMountPoint = dokan1.DokanRemoveMountPoint
_DokanRemoveMountPoint.restype = BOOL


def DokanRemoveMountPoint(MountPoint):
    MountPoint = LPCWSTR(MountPoint)
    return DokanRemoveMountPoint(MountPoint)


#
# /**
#  * \brief Checks whether Name matches Expression
#  *
#  * Behave like \c FsRtlIsNameInExpression routine from
#  <a href="https://msdn.microsoft.com/en-us/library/ff546850(v=VS.85).aspx">Microsoft</a>\n
#  * \c * (asterisk) Matches zero or more characters.\n
#  * <tt>?</tt> (question mark) Matches a single character.\n
#  * \c DOS_DOT (\c " quotation mark) Matches either a period or zero characters beyond the name string.\n
#  * \c DOS_QM (\c > greater than) Matches any single character or, upon encountering a period or end
#  *        of name string, advances the expression to the end of the set of
#  *        contiguous DOS_QMs.\n
#  * \c DOS_STAR (\c < less than) Matches zero or more characters until encountering and matching
#  *          the final \c . in the name.
#  *
#  * \param Expression Expression can contain any of the above characters.
#  * \param Name Name to check
#  * \param IgnoreCase Case sensitive or not
#  * \return result if name matches the expression
#  */
_DokanIsNameInExpression = dokan1.DokanIsNameInExpression
_DokanIsNameInExpression.restype = BOOL


def DokanIsNameInExpression(Expression, Name, IgnoreCase):
    Expression = LPCWSTR(Expression)
    Name = LPCWSTR(Name)
    IgnoreCase = BOOL(IgnoreCase)

    return _DokanIsNameInExpression(Expression, Name, IgnoreCase)


#
# /**
#  * \brief Get the version of Dokan.
#  * The returned ULONG is the version number without the dots.
#  * \return The version of Dokan
#  */
_DokanVersion = dokan1.DokanVersion
_DokanVersion.restype = ULONG


def DokanVersion():
    return _DokanVersion().value


#
# /**
#  * \brief Get the version of the Dokan driver.
#  * The returned ULONG is the version number without the dots.
#  * \return The version of Dokan driver.
#  */
_DokanDriverVersion = dokan1.DokanDriverVersion
_DokanDriverVersion.restype = ULONG


def DokanDriverVersion():
    return _DokanDriverVersion().value


#
# /**
#  * \brief Extends the timeout of the current IO operation in driver.
#  *
#  * \param Timeout Extended time in milliseconds requested.
#  * \param DokanFileInfo \ref DOKAN_FILE_INFO of the operation to extend.
#  * \return If the operation was successful.
#  */
_DokanResetTimeout = dokan1.DokanResetTimeout
_DokanResetTimeout.restype = BOOL


def DokanResetTimeout(Timeout, DokanFileInfo):
    Timeout = ULONG(Timeout)
    DokanFileInfo = DOKAN_FILE_INFO(DokanFileInfo)
    _DokanResetTimeout(
        Timeout,
        ctypes.byref(DokanFileInfo)
    )


#
# /**
#  * \brief Get the handle to Access Token.
#  *
#  * This method needs be called in
#  <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa363858(v=vs.85).aspx">
#  CreateFile</a> callback.
#  * The caller must call
#  <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/ms724211(v=vs.85).aspx">CloseHandle</a>
#  * for the returned handle.
#  *
#  * \param DokanFileInfo \ref DOKAN_FILE_INFO of the operation to extend.
#  * \return A handle to the account token for the user on whose behalf the code is running.
#  */
_DokanOpenRequestorToken = dokan1.DokanOpenRequestorToken
_DokanOpenRequestorToken.restype = HANDLE


def DokanOpenRequestorToken(DokanFileInfo):
    return _DokanOpenRequestorToken(
        DokanFileInfo
    )


#
# /**
#  * \brief Get active Dokan mount points.
#  *
#  * Returned array need to be released by calling \ref DokanReleaseMountPointList
#  *
#  * \param uncOnly Get only instances that have UNC Name.
#  * \param nbRead Number of instances successfully retrieved.
#  * \return Allocate array of DOKAN_CONTROL.
#  */
_DokanGetMountPointList = dokan1.DokanGetMountPointList
_DokanGetMountPointList.restype = PDOKAN_CONTROL


def DokanGetMountPointList(uncOnly):
    uncOnly = BOOL(uncOnly)
    nbRead = ULONG(0)

    control_array = _DokanGetMountPointList(
        uncOnly,
        ctypes.byref(nbRead)
    )

    res = []

    for i in range(nbRead.value):
        control_point = control_array[i]
        control_point.Type
        control_point.MountPoint
        control_point.UNCName
        control_point.DeviceName
        control_point.VolumeDeviceObject
        control_point.SessionId
        control_point.MountOptions
        res += [[control[i]]]

    DokanReleaseMountPointList(control_array)


#
# /**
#  * \brief Release Mount point list resources from \ref DokanGetMountPointList.
#  *
#  * After \ref DokanGetMountPointList call you will receive a dynamically allocated array of DOKAN_CONTROL.
#  * This array needs to be released when no longer needed by calling this function.
#  *
#  * \param list Allocated array of DOKAN_CONTROL from \ref DokanGetMountPointList.
#  * \return Nothing.
#  */
_DokanReleaseMountPointList = dokan1.DokanReleaseMountPointList
_DokanReleaseMountPointList.restype = VOID


def DokanReleaseMountPointList(list_):
    return _DokanReleaseMountPointList(
        ctypes.byref(list_)
    )


#
# /**
#  * \brief Convert \ref DOKAN_OPERATIONS.ZwCreateFile parameters to
#  <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa363858(v=vs.85).aspx">CreateFile</a> parameters.
#  *
#  * Dokan Kernel forward the DesiredAccess directly from the IRP_MJ_CREATE.
#  * This DesiredAccess has been converted from generic rights (user CreateFile request)
#  to standard rights and will be converted back here.
#  * https://msdn.microsoft.com/windows/hardware/drivers/ifs/access-mask
#  *
#  * \param DesiredAccess DesiredAccess from \ref DOKAN_OPERATIONS.ZwCreateFile.
#  * \param FileAttributes FileAttributes from \ref DOKAN_OPERATIONS.ZwCreateFile.
#  * \param CreateOptions CreateOptions from \ref DOKAN_OPERATIONS.ZwCreateFile.
#  * \param CreateDisposition CreateDisposition from \ref DOKAN_OPERATIONS.ZwCreateFile.
#  * \param outDesiredAccess New
#  <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa363858(v=vs.85).aspx">
#  CreateFile</a> dwDesiredAccess.
#  * \param outFileAttributesAndFlags New
#  <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa363858(v=vs.85).aspx">
#  CreateFile</a> dwFlagsAndAttributes.
#  * \param outCreationDisposition New
#  <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa363858(v=vs.85).aspx">
#  CreateFile</a> dwCreationDisposition.
#  * \see <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/aa363858(v=vs.85).aspx">
#  CreateFile function (MSDN)</a>
#  */
_DokanMapKernelToUserCreateFileFlags = dokan1.DokanMapKernelToUserCreateFileFlags
_DokanMapKernelToUserCreateFileFlags.restype = VOID


def DokanMapKernelToUserCreateFileFlags(
    DesiredAccess,
    FileAttributes,
    CreateOptions,
    CreateDisposition,
):
    outDesiredAccess = ACCESS_MASK(0)
    outFileAttributesAndFlags = DWORD(0)
    outCreationDisposition = DWORD(0)
    _DokanMapKernelToUserCreateFileFlags(
        DesiredAccess,
        FileAttributes,
        CreateOptions,
        CreateDisposition,
        ctypes.byref(outDesiredAccess),
        ctypes.byref(outFileAttributesAndFlags),
        ctypes.byref(outCreationDisposition)
    )
    return (
        outDesiredAccess.value,
        outFileAttributesAndFlags.value,
        outCreationDisposition.value
    )


#
# /**
#  * \defgroup DokanNotify Dokan Notify
#  * \brief Dokan User FS file-change notification
#  *
#  * The application implementing the user file system can notify
#  * the Dokan kernel driver of external file- and directory-changes.
#  *
#  * For example, the mirror application can notify the driver about
#  * changes made in the mirrored directory so that those changes will
#  * be automatically reflected in the implemented mirror file system.
#  *
#  * This requires the FilePath passed to the respective DokanNotify*-functions
#  * to include the absolute path of the changed file including the drive-letter
#  * and the path to the mount point, e.g. "C:\Dokan\ChangedFile.txt".
#  *
#  * These functions SHOULD NOT be called from within the implemented
#  * file system and thus be independent of any Dokan file system operation.
#  * @{
#  */
#
# /**
#  * \brief Notify dokan that a file or a directory has been created.
#  *
#  * \param FilePath Absolute path to the file or directory, including the mount-point of the file system.
#  * \param IsDirectory Indicates if the path is a directory.
#  * \return \c TRUE if notification succeeded.
#  */
_DokanNotifyCreate = dokan1.DokanNotifyCreate
_DokanNotifyCreate.restype = BOOL


def DokanNotifyCreate(FilePath,  IsDirectory):
    FilePath = LPCWSTR(FilePath)
    IsDirectory = BOOL(IsDirectory)

    return _DokanNotifyCreate(
        FilePath,
        IsDirectory
    )


#
# /**
#  * \brief Notify dokan that a file or a directory has been deleted.
#  *
#  * \param FilePath Absolute path to the file or directory, including the mount-point of the file system.
#  * \param IsDirectory Indicates if the path was a directory.
#  * \return \c TRUE if notification succeeded.
#  */
_DokanNotifyDelete = dokan1.DokanNotifyDelete
_DokanNotifyDelete.restype = BOOL


def DokanNotifyDelete(FilePath,  IsDirectory):
    FilePath = LPCWSTR(FilePath)
    IsDirectory = BOOL(IsDirectory)

    return _DokanNotifyDelete(
        FilePath,
        IsDirectory
    )


#
# /**
#  * \brief Notify dokan that file or directory attributes have changed.
#  *
#  * \param FilePath Absolute path to the file or directory, including the mount-point of the file system.
#  * \return \c TRUE if notification succeeded.
#  */
_DokanNotifyUpdate = dokan1.DokanNotifyUpdate
_DokanNotifyUpdate.restype = BOOL


def DokanNotifyUpdate(FilePath):
    FilePath = LPCWSTR(FilePath)

    return _DokanNotifyUpdate(FilePath)


#
# /**
#  * \brief Notify dokan that file or directory extended attributes have changed.
#  *
#  * \param FilePath Absolute path to the file or directory, including the mount-point of the file system.
#  * \return \c TRUE if notification succeeded.
#  */
_DokanNotifyXAttrUpdate = dokan1.DokanNotifyXAttrUpdate
_DokanNotifyXAttrUpdate.restype = BOOL


def DokanNotifyXAttrUpdate(FilePath):
    FilePath = LPCWSTR(FilePath)

    return _DokanNotifyXAttrUpdate(FilePath)


#
# /**
#  * \brief Notify dokan that a file or a directory has been renamed. This method
#  *  supports in-place rename for file/directory within the same parent.
#  *
#  * \param OldPath Old, absolute path to the file or directory, including the mount-point of the file system.
#  * \param NewPath New, absolute path to the file or directory, including the mount-point of the file system.
#  * \param IsDirectory Indicates if the path is a directory.
#  * \param IsInSameDirectory Indicates if the file or directory have the same parent directory.
#  * \return \c TRUE if notification succeeded.
#  */
_DokanNotifyRename = dokan1.DokanNotifyRename
_DokanNotifyRename.restype = BOOL


def DokanNotifyRename(OldPath,  NewPath, IsDirectory, IsInSameDirectory):

    OldPath = LPCWSTR(OldPath)
    NewPath = LPCWSTR(NewPath)
    IsDirectory = BOOL(IsDirectory)
    IsInSameDirectory = BOOL(IsInSameDirectory)

    return _DokanNotifyRename(
        OldPath,
        NewPath,
        IsDirectory,
        IsInSameDirectory
    )


#
# /**@}*/
#
# /**
#  * \brief Convert WIN32 error to NTSTATUS
#  *
#  * https://support.microsoft.com/en-us/kb/113996
#  *
#  * \param Error Win32 Error to convert
#  * \return NTSTATUS associate to the ERROR.
#  */
_DokanNtStatusFromWin32 = dokan1.DokanNtStatusFromWin32
_DokanNtStatusFromWin32.restype = NTSTATUS


def DokanNtStatusFromWin32(Error):
    Error = DWORD(Error)

    return _DokanNtStatusFromWin32(Error)

#
# /** @} */
#
# #ifdef __cplusplus
# }
# #endif
#
# #endif // DOKAN_H_
