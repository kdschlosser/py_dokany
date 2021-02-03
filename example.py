#  Dokan : user-mode file system library for Windows

#  Copyright (C) 2020 Google, Inc.
#  Copyright (C) 2015 - 2019 Adrien J. <liryna.stark@gmail.com> and Maxime C. <maxime@islog.com>
#  Copyright (C) 2007 - 2011 Hiroki Asakawa <info@dokan-dev.net>

#  http://dokan-dev.github.io
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from py_dokany.dokan_h import *
from py_dokany.fileinfo_h import *
from py_dokany.constants import *
from py_dokany.windows_api import *
# noinspection PyProtectedMember
from py_dokany.windows_api import _wcsnicmp
# include "../../dokan/dokan.h"
# include "../../dokan/fileinfo.h"
# include <malloc.h>
# include <stdio.h>
# include <stdlib.h>
# include <winbase.h>

import sys

if sys.version_info.major >= 10:
    DOKAN_MAX_PATH = 32768
else:
    DOKAN_MAX_PATH = MAX_PATH

g_UseStdErr: bool
g_DebugMode: bool
g_CaseSensitive: bool
g_HasSeSecurityPrivilege: bool
g_ImpersonateCallerUser: bool


def UNREFERENCED_PARAMETER(_):
    pass


def DbgPrint(format_, *args):
    if g_DebugMode:
        outputString = format_ % args

        if g_UseStdErr:
            sys.stderr.write(outputString)
            sys.stderr.flush()
        else:
            print(outputString.strip())


RootDirectory = (WCHAR * DOKAN_MAX_PATH)("C", ":")
MountPoint = (WCHAR * DOKAN_MAX_PATH)("M", ":", "\\")
UNCName = (WCHAR * DOKAN_MAX_PATH)()


def GetFilePath(filePath, numberOfElements, FileName):
    wcsncpy_s(filePath, numberOfElements, RootDirectory, wcslen(RootDirectory))

    unclen = wcslen(UNCName)

    if unclen > 0 and _wcsnicmp(FileName, UNCName, unclen) == 0:
        if _wcsnicmp(FileName + unclen, ".", 1) != 0:
            wcsncat_s(
                filePath,
                numberOfElements,
                FileName + unclen,
                wcslen(FileName) - unclen
            )
    else:
        wcsncat_s(filePath, numberOfElements, FileName, wcslen(FileName))


def PrintUserName(DokanFileInfo: PDOKAN_FILE_INFO):
    buffer = (UCHAR * 1024)()
    returnLength = DWORD()
    accountName = (WCHAR * 256)()
    domainName = (WCHAR * 256)()
    accountLength = DWORD(ctypes.sizeof(accountName) // ctypes.sizeof(WCHAR))
    domainLength = DWORD(ctypes.sizeof(domainName) // ctypes.sizeof(WCHAR))
    tokenUser = PTOKEN_USER()
    snu = SID_NAME_USE()

    if not g_DebugMode:
        return

    handle = DokanOpenRequestorToken(DokanFileInfo)
    if handle == INVALID_HANDLE_VALUE:
        DbgPrint("  DokanOpenRequestorToken failed\n")
        return

    if not GetTokenInformation(
            handle,
            tokenUser,
            buffer,
            ctypes.sizeof(buffer),
            ctypes.byref(returnLength)
    ):
        DbgPrint("  GetTokenInformaiton failed: %d\n", ctypes.GetLastError())
        CloseHandle(handle)
        return

    CloseHandle(handle)

    tokenUser = ctypes.cast(buffer, PTOKEN_USER)
    # noinspection PyUnresolvedReferences
    if not LookupAccountSid(
            None,
            tokenUser.contents.User.Sid,
            accountName,
            ctypes.byref(accountLength),
            domainName,
            ctypes.byref(domainLength),
            ctypes.byref(snu)
    ):
        DbgPrint("  LookupAccountSid failed: %d\n", ctypes.GetLastError())
        return

    DbgPrint("  AccountName: %s, DomainName: %s\n", accountName, domainName)


def AddSeSecurityNamePrivilege() -> bool:
    token = HANDLE(0)
    DbgPrint("## Attempting to add SE_SECURITY_NAME privilege to process token ##\n")
    luid = LUID()
    if not LookupPrivilegeValue(0, SE_SECURITY_NAME, ctypes.byref(luid)):
        err = ctypes.GetLastError()
        if err != ERROR_SUCCESS:
            DbgPrint("  failed: Unable to lookup privilege value. error = %u\n", err)
            return False

    attr = LUID_AND_ATTRIBUTES()
    attr.Attributes = SE_PRIVILEGE_ENABLED
    attr.Luid = luid

    priv = TOKEN_PRIVILEGES()
    priv.PrivilegeCount = 1
    priv.Privileges[0] = attr

    if not OpenProcessToken(
            HANDLE(GetCurrentProcess()),
            DWORD(TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY),
            ctypes.byref(token)
    ):
        err = ctypes.GetLastError()
        if err != ERROR_SUCCESS:
            DbgPrint("  failed: Unable obtain process token. error = %u\n", err)
            return False

    oldPriv = TOKEN_PRIVILEGES()
    retSize = DWORD()
    AdjustTokenPrivileges(
        token,
        False,
        ctypes.byref(priv),
        ctypes.sizeof(TOKEN_PRIVILEGES),
        ctypes.byref(oldPriv),
        ctypes.byref(retSize)
    )
    err = ctypes.GetLastError()
    if err != ERROR_SUCCESS:
        DbgPrint("  failed: Unable to adjust token privileges: %u\n", err)
        CloseHandle(token)
        return False

    privAlreadyPresent = False
    for i in range(oldPriv.PrivilegeCount):
        if (
                oldPriv.Privileges[i].Luid.HighPart == luid.HighPart and
                oldPriv.Privileges[i].Luid.LowPart == luid.LowPart
        ):
            privAlreadyPresent = True
            break

    if privAlreadyPresent:
        DbgPrint("  success: privilege already present\n")
    else:
        DbgPrint("  success: privilege added\n")

    if token:
        CloseHandle(token)

    return True


def MirrorCheckFlag(val, flag):
    if val & flag:
        DbgPrint("\t" + str(flag) + '\n')


@ZW_CREATE_FILE
def MirrorCreateFile(
        FileName,
        SecurityContext,
        DesiredAccess,
        FileAttributes,
        ShareAccess,
        CreateDisposition,
        CreateOptions,
        DokanFileInfo: PDOKAN_FILE_INFO
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    status_ = STATUS_SUCCESS
    securityAttrib = SECURITY_ATTRIBUTES()
    # userTokenHandle is for Impersonate Caller User Option
    userTokenHandle = HANDLE(INVALID_HANDLE_VALUE)

    securityAttrib.nLength = ctypes.sizeof(securityAttrib)
    securityAttrib.lpSecurityDescriptor = SecurityContext.contents.AccessState.SecurityDescriptor
    securityAttrib.bInheritHandle = False

    (
        genericDesiredAccess,
        fileAttributesAndFlags,
        creationDisposition
    ) = DokanMapKernelToUserCreateFileFlags(
        DesiredAccess,
        FileAttributes,
        CreateOptions,
        CreateDisposition
    )

    DbgPrint("CreateFile : %s\n", filePath.value)

    PrintUserName(DokanFileInfo)

    # /*
    # if (ShareMode == 0 && AccessMode & FILE_WRITE_DATA)
    #         ShareMode = FILE_SHARE_WRITE;
    # else if (ShareMode == 0)
    #         ShareMode = FILE_SHARE_READ;
    # */

    DbgPrint("\tShareMode = 0x%x\n", ShareAccess)

    MirrorCheckFlag(ShareAccess, FILE_SHARE_READ)
    MirrorCheckFlag(ShareAccess, FILE_SHARE_WRITE)
    MirrorCheckFlag(ShareAccess, FILE_SHARE_DELETE)

    DbgPrint("\tDesiredAccess = 0x%x\n", DesiredAccess)

    MirrorCheckFlag(DesiredAccess, GENERIC_READ)
    MirrorCheckFlag(DesiredAccess, GENERIC_WRITE)
    MirrorCheckFlag(DesiredAccess, GENERIC_EXECUTE)

    MirrorCheckFlag(DesiredAccess, DELETE)
    MirrorCheckFlag(DesiredAccess, FILE_READ_DATA)
    MirrorCheckFlag(DesiredAccess, FILE_READ_ATTRIBUTES)
    MirrorCheckFlag(DesiredAccess, FILE_READ_EA)
    MirrorCheckFlag(DesiredAccess, READ_CONTROL)
    MirrorCheckFlag(DesiredAccess, FILE_WRITE_DATA)
    MirrorCheckFlag(DesiredAccess, FILE_WRITE_ATTRIBUTES)
    MirrorCheckFlag(DesiredAccess, FILE_WRITE_EA)
    MirrorCheckFlag(DesiredAccess, FILE_APPEND_DATA)
    MirrorCheckFlag(DesiredAccess, WRITE_DAC)
    MirrorCheckFlag(DesiredAccess, WRITE_OWNER)
    MirrorCheckFlag(DesiredAccess, SYNCHRONIZE)
    MirrorCheckFlag(DesiredAccess, FILE_EXECUTE)
    MirrorCheckFlag(DesiredAccess, STANDARD_RIGHTS_READ)
    MirrorCheckFlag(DesiredAccess, STANDARD_RIGHTS_WRITE)
    MirrorCheckFlag(DesiredAccess, STANDARD_RIGHTS_EXECUTE)

    # When filePath is a directory, needs to change the flag so that the file can
    # be opened.
    fileAttr = GetFileAttributes(filePath)

    if (
            fileAttr != INVALID_FILE_ATTRIBUTES and
            fileAttr & FILE_ATTRIBUTE_DIRECTORY
    ):
        if CreateOptions & FILE_NON_DIRECTORY_FILE:
            DbgPrint("\tCannot open a dir as a file\n")
            return STATUS_FILE_IS_A_DIRECTORY

        DokanFileInfo.contents.IsDirectory = True
        # Needed by FindFirstFile to list files in it
        # TODO: use ReOpenFile in MirrorFindFiles to set share read temporary
        ShareAccess |= FILE_SHARE_READ

    DbgPrint("\tFlagsAndAttributes = 0x%x\n", fileAttributesAndFlags)

    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_ARCHIVE)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_COMPRESSED)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_DEVICE)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_DIRECTORY)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_ENCRYPTED)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_HIDDEN)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_INTEGRITY_STREAM)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_NORMAL)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_NOT_CONTENT_INDEXED)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_NO_SCRUB_DATA)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_OFFLINE)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_READONLY)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_REPARSE_POINT)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_SPARSE_FILE)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_SYSTEM)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_TEMPORARY)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_ATTRIBUTE_VIRTUAL)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_FLAG_WRITE_THROUGH)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_FLAG_OVERLAPPED)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_FLAG_NO_BUFFERING)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_FLAG_RANDOM_ACCESS)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_FLAG_SEQUENTIAL_SCAN)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_FLAG_DELETE_ON_CLOSE)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_FLAG_BACKUP_SEMANTICS)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_FLAG_POSIX_SEMANTICS)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_FLAG_OPEN_REPARSE_POINT)
    MirrorCheckFlag(fileAttributesAndFlags, FILE_FLAG_OPEN_NO_RECALL)
    MirrorCheckFlag(fileAttributesAndFlags, SECURITY_ANONYMOUS)
    MirrorCheckFlag(fileAttributesAndFlags, SECURITY_IDENTIFICATION)
    MirrorCheckFlag(fileAttributesAndFlags, SECURITY_IMPERSONATION)
    MirrorCheckFlag(fileAttributesAndFlags, SECURITY_DELEGATION)
    MirrorCheckFlag(fileAttributesAndFlags, SECURITY_CONTEXT_TRACKING)
    MirrorCheckFlag(fileAttributesAndFlags, SECURITY_EFFECTIVE_ONLY)
    MirrorCheckFlag(fileAttributesAndFlags, SECURITY_SQOS_PRESENT)

    if g_CaseSensitive:
        fileAttributesAndFlags |= FILE_FLAG_POSIX_SEMANTICS

    if creationDisposition == CREATE_NEW:
        DbgPrint("\tCREATE_NEW\n")
    elif creationDisposition == OPEN_ALWAYS:
        DbgPrint("\tOPEN_ALWAYS\n")
    elif creationDisposition == CREATE_ALWAYS:
        DbgPrint("\tCREATE_ALWAYS\n")
    elif creationDisposition == OPEN_EXISTING:
        DbgPrint("\tOPEN_EXISTING\n")
    elif creationDisposition == TRUNCATE_EXISTING:
        DbgPrint("\tTRUNCATE_EXISTING\n")
    else:
        DbgPrint("\tUNKNOWN creationDisposition!\n")

    if g_ImpersonateCallerUser:
        userTokenHandle = DokanOpenRequestorToken(DokanFileInfo)

        if userTokenHandle == INVALID_HANDLE_VALUE:
            DbgPrint("  DokanOpenRequestorToken failed\n")
            # Should we return some error?

    if DokanFileInfo.contents.IsDirectory:
        # It is a create directory request

        if (
                creationDisposition == CREATE_NEW or
                creationDisposition == OPEN_ALWAYS
        ):
            if (
                    g_ImpersonateCallerUser and
                    userTokenHandle != INVALID_HANDLE_VALUE
            ):
                # if g_ImpersonateCallerUser option is on, call the ImpersonateLoggedOnUser function.
                if not ImpersonateLoggedOnUser(userTokenHandle):
                    # handle the error if failed to impersonate
                    DbgPrint("\tImpersonateLoggedOnUser failed.\n")

            # We create folder
            if not CreateDirectory(filePath, ctypes.byref(securityAttrib)):
                error = ctypes.GetLastError()
                # Fail to create folder for OPEN_ALWAYS is not an error
                if (
                        error != ERROR_ALREADY_EXISTS or
                        creationDisposition == CREATE_NEW
                ):
                    DbgPrint("\terror code = %d\n\n", error)
                    status_ = DokanNtStatusFromWin32(error)

            if (
                    g_ImpersonateCallerUser and
                    userTokenHandle != INVALID_HANDLE_VALUE
            ):
                # Clean Up operation for impersonate
                lastError = ctypes.GetLastError()
                if status_ != STATUS_SUCCESS:  # Keep the handle open for CreateFile
                    CloseHandle(userTokenHandle)

                RevertToSelf()
                SetLastError(lastError)

        if status_ == STATUS_SUCCESS:
            # Check first if we're trying to open a file as a directory.
            if (
                    fileAttr != INVALID_FILE_ATTRIBUTES and
                    not fileAttr & FILE_ATTRIBUTE_DIRECTORY and
                    CreateOptions & FILE_DIRECTORY_FILE
            ):
                return STATUS_NOT_A_DIRECTORY

            if (
                    g_ImpersonateCallerUser and
                    userTokenHandle != INVALID_HANDLE_VALUE
            ):
                # if g_ImpersonateCallerUser option is on, call the ImpersonateLoggedOnUser function.
                if not ImpersonateLoggedOnUser(userTokenHandle):
                    # handle the error if failed to impersonate
                    DbgPrint("\tImpersonateLoggedOnUser failed.\n")

            # FILE_FLAG_BACKUP_SEMANTICS is required for opening directory handles
            handle = CreateFile(
                filePath,
                genericDesiredAccess,
                ShareAccess,
                ctypes.byref(securityAttrib, OPEN_EXISTING),
                fileAttributesAndFlags | FILE_FLAG_BACKUP_SEMANTICS,
                None
            )

            if (
                    g_ImpersonateCallerUser and
                    userTokenHandle != INVALID_HANDLE_VALUE
            ):
                # Clean Up operation for impersonate
                lastError = ctypes.GetLastError()
                CloseHandle(userTokenHandle)
                RevertToSelf()
                SetLastError(lastError)

            if handle == INVALID_HANDLE_VALUE:
                error = ctypes.GetLastError()
                DbgPrint("\terror code = %d\n\n", error)
                status_ = DokanNtStatusFromWin32(error)
            else:
                DokanFileInfo.contents.Context = handle  # save the file handle in Context

                # Open succeed but we need to inform the driver
                # that the dir open and not created by returning STATUS_OBJECT_NAME_COLLISION
                if (
                        creationDisposition == OPEN_ALWAYS and
                        fileAttr != INVALID_FILE_ATTRIBUTES
                ):
                    return STATUS_OBJECT_NAME_COLLISION
    else:
        # It is a create file request

        # Cannot overwrite a hidden or system file if flag not set
        if (
                fileAttr != INVALID_FILE_ATTRIBUTES and
                (
                        (
                                not fileAttributesAndFlags & FILE_ATTRIBUTE_HIDDEN and
                                fileAttr & FILE_ATTRIBUTE_HIDDEN
                        ) or
                        (
                                not fileAttributesAndFlags & FILE_ATTRIBUTE_SYSTEM and
                                fileAttr & FILE_ATTRIBUTE_SYSTEM
                        )
                ) and
                (
                        creationDisposition == TRUNCATE_EXISTING or
                        creationDisposition == CREATE_ALWAYS
                )
        ):
            return STATUS_ACCESS_DENIED

        # Cannot delete a read only file
        if (
                (
                        fileAttr != INVALID_FILE_ATTRIBUTES and
                        fileAttr & FILE_ATTRIBUTE_READONLY or
                        fileAttributesAndFlags & FILE_ATTRIBUTE_READONLY
                ) and
                fileAttributesAndFlags & FILE_FLAG_DELETE_ON_CLOSE
        ):
            return STATUS_CANNOT_DELETE

        # Truncate should always be used with write access
        if creationDisposition == TRUNCATE_EXISTING:
            genericDesiredAccess |= GENERIC_WRITE

        if (
                g_ImpersonateCallerUser and
                userTokenHandle != INVALID_HANDLE_VALUE
        ):
            # if g_ImpersonateCallerUser option is on, call the ImpersonateLoggedOnUser function.
            if not ImpersonateLoggedOnUser(userTokenHandle):
                # handle the error if failed to impersonate
                DbgPrint("\tImpersonateLoggedOnUser failed.\n")

        handle = CreateFile(
            filePath,
            genericDesiredAccess,  # GENERIC_READ|GENERIC_WRITE|GENERIC_EXECUTE,
            ShareAccess,
            ctypes.byref(securityAttrib),  # security attribute
            creationDisposition,
            fileAttributesAndFlags,  # |FILE_FLAG_NO_BUFFERING,
            None  # template file handle
        )

        if (
                g_ImpersonateCallerUser and
                userTokenHandle != INVALID_HANDLE_VALUE
        ):
            # Clean Up operation for impersonate
            lastError = ctypes.GetLastError()
            CloseHandle(userTokenHandle)
            RevertToSelf()
            SetLastError(lastError)

        if handle == INVALID_HANDLE_VALUE:
            error = ctypes.GetLastError()
            DbgPrint("\terror code = %d\n\n", error)

            status_ = DokanNtStatusFromWin32(error)
        else:
            # Need to update FileAttributes with previous when Overwrite file
            if (
                    fileAttr != INVALID_FILE_ATTRIBUTES and
                    creationDisposition == TRUNCATE_EXISTING
            ):
                SetFileAttributes(filePath, fileAttributesAndFlags | fileAttr)

            DokanFileInfo.contents.Context = handle  # save the file handle in Context

            if (
                    creationDisposition == OPEN_ALWAYS or
                    creationDisposition == CREATE_ALWAYS
            ):
                error = ctypes.GetLastError()
                if error == ERROR_ALREADY_EXISTS:
                    DbgPrint("\tOpen an already existing file\n")
                    # Open succeed but we need to inform the driver
                    # that the file open and not created by returning STATUS_OBJECT_NAME_COLLISION
                    status_ = STATUS_OBJECT_NAME_COLLISION

    DbgPrint("\n")
    return status_


@CLOSE_FILE
def MirrorCloseFile(
        FileName,
        DokanFileInfo: PDOKAN_FILE_INFO
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    if DokanFileInfo.contents.Context:
        DbgPrint("CloseFile: %s\n", filePath.value)
        DbgPrint("\terror : not cleanuped file\n\n")
        CloseHandle(HANDLE(DokanFileInfo.contents.Context))
        DokanFileInfo.contents.Context = 0
    else:
        DbgPrint("Close: %s\n\n", filePath.value)


@CLEANUP
def MirrorCleanup(
        FileName,
        DokanFileInfo: PDOKAN_FILE_INFO
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    if DokanFileInfo.contents.Context:
        DbgPrint("Cleanup: %s\n\n", filePath.value)
        CloseHandle(HANDLE(DokanFileInfo.contents.Context))
        DokanFileInfo.contents.Context = 0
    else:
        DbgPrint("Cleanup: %s\n\tinvalid handle\n\n", filePath.value)

    if DokanFileInfo.contents.DeleteOnClose:
        # Should already be deleted by CloseHandle
        # if open with FILE_FLAG_DELETE_ON_CLOSE
        DbgPrint("\tDeleteOnClose\n")
        if DokanFileInfo.contents.IsDirectory:
            DbgPrint("  DeleteDirectory ")
            if not RemoveDirectory(filePath):
                DbgPrint("error code = %d\n\n", ctypes.GetLastError())
            else:
                DbgPrint("success\n\n")

        else:
            DbgPrint("  DeleteFile ")
            if DeleteFile(filePath) == 0:
                DbgPrint(" error code = %d\n\n", ctypes.GetLastError())
            else:
                DbgPrint("success\n\n")


@READ_FILE
def MirrorReadFile(
        FileName,
        Buffer,
        BufferLength: DWORD,
        ReadLength: LPDWORD,
        Offset: LONGLONG,
        DokanFileInfo: PDOKAN_FILE_INFO
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    handle = HANDLE(DokanFileInfo.contents.Context)
    offset = ULONG(Offset.value)
    opened = False

    DbgPrint("ReadFile : %s\n", filePath.value)

    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle, cleanuped?\n")
        handle = CreateFile(
            filePath,
            GENERIC_READ,
            FILE_SHARE_READ,
            None,
            OPEN_EXISTING,
            0,
            None
        )
        if handle == INVALID_HANDLE_VALUE:
            error = ctypes.GetLastError()
            DbgPrint("\tCreateFile error : %d\n\n", error)
            return DokanNtStatusFromWin32(error)

        opened = True

    distanceToMove = LARGE_INTEGER()
    distanceToMove.QuadPart = Offset
    if not SetFilePointerEx(handle, distanceToMove, None, FILE_BEGIN):
        error = ctypes.GetLastError()
        DbgPrint("\tseek error, offset = %d\n\n", offset)
        if opened:
            CloseHandle(handle)

        return DokanNtStatusFromWin32(error)

    if not ReadFile(handle, Buffer, BufferLength, ReadLength, None):
        error = ctypes.GetLastError()
        DbgPrint(
            "\tread error = %u, buffer length = %d, read length = %d\n\n",
            error,
            BufferLength,
            ReadLength
        )
        if opened:
            CloseHandle(handle)

        return DokanNtStatusFromWin32(error)

    else:
        DbgPrint(
            "\tByte to read: %d, Byte read %d, offset %d\n\n",
            BufferLength,
            ReadLength,
            offset
        )

    if opened:
        CloseHandle(handle)

    return STATUS_SUCCESS


@WRITE_FILE
def MirrorWriteFile(
        FileName,
        Buffer,
        NumberOfBytesToWrite: DWORD,
        NumberOfBytesWritten: LPDWORD,
        Offset: LONGLONG,
        DokanFileInfo: PDOKAN_FILE_INFO
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    handle = HANDLE(DokanFileInfo.contents.Context)
    opened = False

    DbgPrint(
        "WriteFile : %s, offset %I64d, length %d\n",
        filePath.value,
        Offset.value,
        NumberOfBytesToWrite.value
    )

    # reopen the file
    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle, cleanuped?\n")
        handle = CreateFile(
            filePath,
            GENERIC_WRITE,
            FILE_SHARE_WRITE,
            None,
            OPEN_EXISTING,
            0,
            None
        )

        if handle == INVALID_HANDLE_VALUE:
            error = ctypes.GetLastError()
            DbgPrint("\tCreateFile error : %d\n\n", error)
            return DokanNtStatusFromWin32(error)

        opened = True

    fileSizeHigh = DWORD(0)
    fileSizeLow = GetFileSize(handle, ctypes.byref(fileSizeHigh))

    if fileSizeLow == INVALID_FILE_SIZE:
        error = ctypes.GetLastError()
        DbgPrint("\tcan not get a file size error = %d\n", error)
        if opened:
            CloseHandle(handle)

        return DokanNtStatusFromWin32(error)

    fileSize = ctypes.c_uint64(fileSizeHigh.value << 32 | fileSizeLow.value)

    distanceToMove = LARGE_INTEGER()
    if DokanFileInfo.contents.WriteToEndOfFile:
        z = LARGE_INTEGER()
        z.QuadPart = 0
        if not SetFilePointerEx(handle, z, None, FILE_END):
            error = ctypes.GetLastError()
            DbgPrint("\tseek error, offset = EOF, error = %d\n", error)
            if opened:
                CloseHandle(handle)

            return DokanNtStatusFromWin32(error)
    else:
        # Paging IO cannot write after allocate file size.
        if DokanFileInfo.contents.PagingIo:
            if Offset >= fileSize:
                NumberOfBytesWritten.value = 0
                if opened:
                    CloseHandle(handle)

                return STATUS_SUCCESS

        if Offset.value + NumberOfBytesToWrite.value > fileSize.value:
            bytes_ = fileSize.value - Offset.value
            if bytes_ >> 32:
                NumberOfBytesToWrite.value = bytes_ & 0xFFFFFFFF
            else:
                NumberOfBytesToWrite.contents = DWORD(bytes_)

    if Offset.value > fileSize.value:
        # In the mirror sample helperZeroFileData is not necessary. NTFS will
        # zero a hole.
        # But if user's file system is different from NTFS( or other Windows's
        # file systems ) then  users will have to zero the hole themselves.
        pass

    distanceToMove.QuadPart = Offset
    if not SetFilePointerEx(handle, distanceToMove, None, FILE_BEGIN):
        error = ctypes.GetLastError()
        DbgPrint("\tseek error, offset = %I64d, error = %d\n", Offset.value, error)
        if opened:
            CloseHandle(handle)

        return DokanNtStatusFromWin32(error)

    if not WriteFile(handle, Buffer, NumberOfBytesToWrite, NumberOfBytesWritten, None):
        error = ctypes.GetLastError()
        DbgPrint(
            "\twrite error = %u, buffer length = %d, write length = %d\n",
            error,
            NumberOfBytesToWrite.value,
            NumberOfBytesWritten.value
        )
        if opened:
            CloseHandle(handle)

        return DokanNtStatusFromWin32(error)

    else:
        DbgPrint("\twrite %d, offset %I64d\n\n", NumberOfBytesWritten, Offset.value)

    # close the file when it is reopened
    if opened:
        CloseHandle(handle)

    return STATUS_SUCCESS


@FLUSH_FILE_BUFFERS
def MirrorFlushFileBuffers(FileName, DokanFileInfo):
    handle = HANDLE(DokanFileInfo.contents.Context)
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    DbgPrint("FlushFileBuffers : %s\n", filePath.value)

    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle\n\n")
        return STATUS_SUCCESS

    if FlushFileBuffers(handle):
        return STATUS_SUCCESS
    else:
        error = ctypes.GetLastError()
        DbgPrint("\tflush error code = %d\n", error)
        return DokanNtStatusFromWin32(error)


@GET_FILE_INFORMATION
def MirrorGetFileInformation(
        FileName,
        HandleFileInformation: LPBY_HANDLE_FILE_INFORMATION,
        DokanFileInfo
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    handle = HANDLE(DokanFileInfo.contents.Context)
    opened = False
    file_information = BY_HANDLE_FILE_INFORMATION()

    DbgPrint("GetFileInfo : %s\n", filePath.value)

    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle, cleanuped?\n")
        handle = CreateFile(
            filePath,
            GENERIC_READ,
            FILE_SHARE_READ,
            None,
            OPEN_EXISTING,
            0,
            None
        )
        if handle == INVALID_HANDLE_VALUE:
            error = ctypes.GetLastError()
            DbgPrint("\tCreateFile error : %d\n\n", error)
            return DokanNtStatusFromWin32(error)

        opened = True

    if not GetFileInformationByHandle(handle, HandleFileInformation):
        DbgPrint("\terror code = %d\n", ctypes.GetLastError())

        # FileName is a root directory
        # in this case, FindFirstFile can't get directory information
        if len(FileName) == 1:
            DbgPrint("  root dir\n")
            file_information.dwFileAttributes = GetFileAttributes(filePath)

        else:
            find = WIN32_FIND_DATAW()
            findHandle = FindFirstFile(filePath, ctypes.byref(find))
            if findHandle == INVALID_HANDLE_VALUE:
                error = ctypes.GetLastError()
                DbgPrint("\tFindFirstFile error code = %d\n\n", error)
                if opened:
                    CloseHandle(handle)
                    return DokanNtStatusFromWin32(error)

            file_information.dwFileAttributes = find.dwFileAttributes
            file_information.ftCreationTime = find.ftCreationTime
            file_information.ftLastAccessTime = find.ftLastAccessTime
            file_information.ftLastWriteTime = find.ftLastWriteTime
            file_information.nFileSizeHigh = find.nFileSizeHigh
            file_information.nFileSizeLow = find.nFileSizeLow
            DbgPrint("\tFindFiles OK, file size = %d\n", find.nFileSizeLow)
            FindClose(findHandle)

            HandleFileInformation.contents = file_information
    else:
        DbgPrint("\tGetFileInformationByHandle success, file size = %d\n", HandleFileInformation.contents.nFileSizeLow)

    DbgPrint("FILE ATTRIBUTE  = %d\n", HandleFileInformation.contents.dwFileAttributes)

    if opened:
        CloseHandle(handle)

    return STATUS_SUCCESS


@FIND_FILES
def MirrorFindFiles(
        FileName,
        FillFindData,  # function pointer
        DokanFileInfo
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    findData = WIN32_FIND_DATAW()
    count = 0

    DbgPrint("FindFiles : %s\n", filePath.value)

    fileLen = wcslen(filePath)
    if filePath[fileLen - 1] != '\\':
        fileLen += 1
        filePath[fileLen] = '\\'

    if fileLen + 1 >= DOKAN_MAX_PATH:
        return STATUS_BUFFER_OVERFLOW

    filePath[fileLen] = '*'
    filePath[fileLen + 1] = '\0'

    hFind = FindFirstFile(filePath, ctypes.byref(findData))

    if hFind == INVALID_HANDLE_VALUE:
        error = ctypes.GetLastError()
        DbgPrint("\tinvalid file handle. Error is %u\n\n", error)
        return DokanNtStatusFromWin32(error)

    # Root folder does not have . and .. folder - we remove them
    rootFolder = wcscmp(FileName, "\\") == 0
    while FindNextFile(hFind, ctypes.byref(findData)) != 0:
        if (
                not rootFolder or
                (
                        wcscmp(findData.cFileName, ".") != 0 and
                        wcscmp(findData.cFileName, "..") != 0
                )
        ):
            FillFindData(ctypes.byref(findData), DokanFileInfo)

        count += 1

    error = ctypes.GetLastError()
    FindClose(hFind)

    if error != ERROR_NO_MORE_FILES:
        DbgPrint("\tFindNextFile error. Error is %u\n\n", error)
        return DokanNtStatusFromWin32(error)

    DbgPrint("\tFindFiles return %d entries in %s\n\n", count, filePath.value)

    return STATUS_SUCCESS


@DELETE_FILE
def MirrorDeleteFile(FileName, DokanFileInfo):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    handle = HANDLE(DokanFileInfo.contents.Context)

    DbgPrint("DeleteFile %s - %d\n", filePath.value, DokanFileInfo.contents.DeleteOnClose)
    dwAttrib = GetFileAttributes(filePath)

    if (
            dwAttrib.value != INVALID_FILE_ATTRIBUTES and
            dwAttrib.value & FILE_ATTRIBUTE_DIRECTORY
    ):
        return STATUS_ACCESS_DENIED

    if handle and handle != INVALID_HANDLE_VALUE:
        fdi = FILE_DISPOSITION_INFO()
        fdi.DeleteFile = DokanFileInfo.contents.DeleteOnClose
        if not SetFileInformationByHandle(
                handle,
                FILE_INFORMATION_CLASS.FileDispositionInformation,
                ctypes.byref(fdi),
                ctypes.sizeof(FILE_DISPOSITION_INFO)
        ):
            return DokanNtStatusFromWin32(ctypes.GetLastError())

    return STATUS_SUCCESS


@DELETE_DIRECTORY
def MirrorDeleteDirectory(
        FileName,
        DokanFileInfo
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    # HANDLE	handle = (HANDLE)DokanFileInfo->Context;
    findData = WIN32_FIND_DATAW()

    DbgPrint("DeleteDirectory %s - %d\n", filePath.value, DokanFileInfo.contents.DeleteOnClose)

    if not DokanFileInfo.contents.DeleteOnClose:
        # Dokan notify that the file is requested not to be deleted.
        return STATUS_SUCCESS

    fileLen = wcslen(filePath)

    if filePath[fileLen - 1] != '\\':
        fileLen += 1
        filePath[fileLen] = '\\'

    if fileLen + 1 >= DOKAN_MAX_PATH:
        return STATUS_BUFFER_OVERFLOW

    filePath[fileLen] = '*'
    filePath[fileLen + 1] = '\0'

    hFind = FindFirstFile(filePath, ctypes.byref(findData))

    if hFind == INVALID_HANDLE_VALUE:
        error = ctypes.GetLastError()
        DbgPrint("\tDeleteDirectory error code = %d\n\n", error)
        return DokanNtStatusFromWin32(error)

    while FindNextFile(hFind, ctypes.byref(findData)) != 0:
        if (
                wcscmp(findData.cFileName, "..") != 0 and
                wcscmp(findData.cFileName, ".") != 0
        ):
            FindClose(hFind)
            DbgPrint("\tDirectory is not empty: %s\n", findData.cFileName)
            return STATUS_DIRECTORY_NOT_EMPTY

    error = ctypes.GetLastError()

    FindClose(hFind)

    if error != ERROR_NO_MORE_FILES:
        DbgPrint("\tDeleteDirectory error code = %d\n\n", error)
        return DokanNtStatusFromWin32(error)

    return STATUS_SUCCESS


@MOVE_FILE
def MirrorMoveFile(
        FileName,  # existing file name
        NewFileName,
        ReplaceIfExisting,
        DokanFileInfo
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    newFilePath = (WCHAR * DOKAN_MAX_PATH)()

    if wcslen(NewFileName) and NewFileName[0] != ':':
        GetFilePath(newFilePath, DOKAN_MAX_PATH, NewFileName)

    else:
        # For a stream rename, FileRenameInfo expect the FileName param without the filename
        # like :<stream name>:<stream type>
        wcsncpy_s(newFilePath, DOKAN_MAX_PATH, NewFileName, wcslen(NewFileName))

    DbgPrint("MoveFile %s -> %s\n\n", filePath.value, newFilePath.value)
    handle = HANDLE(DokanFileInfo.contents.Context)
    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle\n\n")
        return STATUS_INVALID_HANDLE

    newFilePathLen = wcslen(newFilePath)

    # the PFILE_RENAME_INFO struct has space for one WCHAR for the name at
    # the end, so that
    # accounts for the null terminator

    bufferSize = DWORD(ctypes.sizeof(FILE_RENAME_INFO) + newFilePathLen * ctypes.sizeof(newFilePath[0]))

    renameInfo = PFILE_RENAME_INFO(ctypes.cdll.msvcrt.malloc(bufferSize))
    if not renameInfo:
        return STATUS_BUFFER_OVERFLOW

    renameInfo.ReplaceIfExists = ReplaceIfExisting

    renameInfo.RootDirectory = None  # hope it is never needed, shouldn't be
    renameInfo.FileNameLength = DWORD(newFilePathLen * ctypes.sizeof(newFilePath[0]))  # they want length in bytes

    wcscpy_s(renameInfo.FileName, newFilePathLen + 1, newFilePath)

    result = SetFileInformationByHandle(handle, FILE_INFORMATION_CLASS.FileRenameInformation, renameInfo, bufferSize)
    if result:
        return STATUS_SUCCESS
    else:
        error = ctypes.GetLastError()
        DbgPrint("\tMoveFile error = %u\n", error)
        return DokanNtStatusFromWin32(error)


@LOCK_FILE
def MirrorLockFile(
        FileName,
        ByteOffset,
        Length,
        DokanFileInfo
):
    offset = LARGE_INTEGER()
    length = LARGE_INTEGER()

    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    DbgPrint("LockFile %s\n", filePath.value)

    handle = HANDLE(DokanFileInfo.contents.Context)
    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle\n\n")
        return STATUS_INVALID_HANDLE

    length.QuadPart = Length.value
    offset.QuadPart = ByteOffset.value

    if not LockFile(
            handle,
            offset.LowPart,
            offset.HighPart,
            length.LowPart,
            length.HighPart
    ):
        error = ctypes.GetLastError()
        DbgPrint("\terror code = %d\n\n", error)
        return DokanNtStatusFromWin32(error)

    DbgPrint("\tsuccess\n\n")
    return STATUS_SUCCESS


@SET_END_OF_FILE
def MirrorSetEndOfFile(
        FileName,
        ByteOffset,
        DokanFileInfo
):
    offset = LARGE_INTEGER()

    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    DbgPrint("SetEndOfFile %s, %I64d\n", filePath.value, ByteOffset.value)

    handle = HANDLE(DokanFileInfo.contents.Context)
    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle\n\n")
        return STATUS_INVALID_HANDLE

    offset.QuadPart = ByteOffset.value
    if not SetFilePointerEx(handle, offset, None, FILE_BEGIN):
        error = ctypes.GetLastError()
        DbgPrint("\tSetFilePointer error: %d, offset = %I64d\n\n", error, ByteOffset.value)
        return DokanNtStatusFromWin32(error)

    if not SetEndOfFile(handle):
        error = ctypes.GetLastError()
        DbgPrint("\tSetEndOfFile error code = %d\n\n", error)
        return DokanNtStatusFromWin32(error)

    return STATUS_SUCCESS


@SET_ALLOCATION_SIZE
def MirrorSetAllocationSize(
        FileName,
        AllocSize,
        DokanFileInfo
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    fileSize = LARGE_INTEGER()

    DbgPrint("SetAllocationSize %s, %I64d\n", filePath.value, AllocSize.value)

    handle = HANDLE(DokanFileInfo.contents.Context)
    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle\n\n")
        return STATUS_INVALID_HANDLE

    if GetFileSizeEx(handle, ctypes.byref(fileSize)):
        if AllocSize < fileSize.QuadPart:
            fileSize.QuadPart = AllocSize
            if not SetFilePointerEx(handle, fileSize, None, FILE_BEGIN):
                error = ctypes.GetLastError()
                DbgPrint("\tSetAllocationSize: SetFilePointer eror: %d, offset = %I64d\n\n", error, AllocSize.value)
                return DokanNtStatusFromWin32(error)

            if not SetEndOfFile(handle):
                error = ctypes.GetLastError()
                DbgPrint("\tSetEndOfFile error code = %d\n\n", error)
                return DokanNtStatusFromWin32(error)
    else:
        error = ctypes.GetLastError()
        DbgPrint("\terror code = %d\n\n", error)
        return DokanNtStatusFromWin32(error)

    return STATUS_SUCCESS


@SET_FILE_ATTRIBUTES
def MirrorSetFileAttributes(
        FileName,
        FileAttributes,
        DokanFileInfo
):
    UNREFERENCED_PARAMETER(DokanFileInfo)
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    DbgPrint("SetFileAttributes %s 0x%x\n", filePath.value, FileAttributes.value)

    if FileAttributes.value != 0:
        if not SetFileAttributes(filePath, FileAttributes):
            error = ctypes.GetLastError()
            DbgPrint("\terror code = %d\n\n", error)
            return DokanNtStatusFromWin32(error)

    else:
        # case FileAttributes == 0 :
        # MS-FSCC 2.6 File Attributes : There is no file attribute with the value 0x00000000
        # because a value of 0x00000000 in the FileAttributes field means that the file
        # attributes for this file MUST NOT be changed when setting basic information for the file
        DbgPrint("Set 0 to FileAttributes means MUST NOT be changed. Didn't call SetFileAttributes function. \n")

    DbgPrint("\n")
    return STATUS_SUCCESS


@SET_FILE_TIME
def MirrorSetFileTime(
        FileName,
        CreationTime: ctypes.POINTER(FILETIME),
        LastAccessTime: ctypes.POINTER(FILETIME),
        LastWriteTime: ctypes.POINTER(FILETIME),
        DokanFileInfo: PDOKAN_FILE_INFO
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    DbgPrint("SetFileTime %s\n", filePath)

    handle = HANDLE(DokanFileInfo.contents.Context)

    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle\n\n")
        return STATUS_INVALID_HANDLE

    if not SetFileTime(
            handle,
            CreationTime,
            LastAccessTime,
            LastWriteTime
    ):
        error = ctypes.GetLastError()
        DbgPrint("\terror code = %d\n\n", error)
        return DokanNtStatusFromWin32(error)

    DbgPrint("\n")
    return STATUS_SUCCESS


@UNLOCK_FILE
def MirrorUnlockFile(
        FileName,
        ByteOffset: LONGLONG,
        Length: LONGLONG,
        DokanFileInfo: PDOKAN_FILE_INFO
):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    length = LARGE_INTEGER()
    offset = LARGE_INTEGER()

    DbgPrint("UnlockFile %s\n", filePath.value)

    handle = HANDLE(DokanFileInfo.contents.Context)
    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle\n\n")
        return STATUS_INVALID_HANDLE

    length.QuadPart = Length.value
    offset.QuadPart = ByteOffset.value

    if not UnlockFile(
            handle,
            offset.LowPart,
            offset.HighPart,
            length.LowPart,
            length.HighPart
    ):
        error = ctypes.GetLastError()
        DbgPrint("\terror code = %d\n\n", error)
        return DokanNtStatusFromWin32(error)

    DbgPrint("\tsuccess\n\n")
    return STATUS_SUCCESS


@GET_FILE_SECURITY
def MirrorGetFileSecurity(
        FileName,
        SecurityInformation: PSECURITY_INFORMATION,
        SecurityDescriptor: PSECURITY_DESCRIPTOR,
        BufferLength: ULONG,
        LengthNeeded: PULONG,
        DokanFileInfo: PDOKAN_FILE_INFO
):
    UNREFERENCED_PARAMETER(DokanFileInfo)
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    DbgPrint("GetFileSecurity %s\n", filePath.value)

    MirrorCheckFlag(SecurityInformation.contents.value, FILE_SHARE_READ)
    MirrorCheckFlag(SecurityInformation.contents.value, OWNER_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, GROUP_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, DACL_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, SACL_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, LABEL_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, ATTRIBUTE_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, SCOPE_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, PROCESS_TRUST_LABEL_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, BACKUP_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, PROTECTED_DACL_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, PROTECTED_SACL_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, UNPROTECTED_DACL_SECURITY_INFORMATION)
    MirrorCheckFlag(SecurityInformation.contents.value, UNPROTECTED_SACL_SECURITY_INFORMATION)

    requestingSaclInfo = (
            (SecurityInformation.contents.value & SACL_SECURITY_INFORMATION) or
            (SecurityInformation.contents.value & BACKUP_SECURITY_INFORMATION)
    )

    if not g_HasSeSecurityPrivilege:
        SecurityInformation.contents = DWORD(SecurityInformation.contents.value & ~SACL_SECURITY_INFORMATION)
        SecurityInformation.contents = DWORD(SecurityInformation.contents.value & ~BACKUP_SECURITY_INFORMATION)

    DbgPrint("  Opening new handle with READ_CONTROL access\n")
    handle = CreateFile(
        filePath,
        READ_CONTROL | (ACCESS_SYSTEM_SECURITY if requestingSaclInfo and g_HasSeSecurityPrivilege else 0),
        FILE_SHARE_WRITE | FILE_SHARE_READ | FILE_SHARE_DELETE,
        None,  # security attribute
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS,  # |FILE_FLAG_NO_BUFFERING,
        None
    )

    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle\n\n")
        error = ctypes.GetLastError()
        return DokanNtStatusFromWin32(error)

    if not GetUserObjectSecurity(
            handle,
            SecurityInformation,
            SecurityDescriptor,
            BufferLength,
            LengthNeeded
    ):
        error = ctypes.GetLastError()
        if error == ERROR_INSUFFICIENT_BUFFER:
            DbgPrint("  GetUserObjectSecurity error: ERROR_INSUFFICIENT_BUFFER\n")
            CloseHandle(handle)
            return STATUS_BUFFER_OVERFLOW
        else:
            DbgPrint("  GetUserObjectSecurity error: %d\n", error)
            CloseHandle(handle)
            return DokanNtStatusFromWin32(error)

    # Ensure the Security Descriptor Length is set
    securityDescriptorLength = GetSecurityDescriptorLength(SecurityDescriptor)
    DbgPrint("  GetUserObjectSecurity return true,  *LengthNeeded = securityDescriptorLength \n")
    LengthNeeded.contents = ULONG(securityDescriptorLength)

    CloseHandle(handle)

    return STATUS_SUCCESS


@SET_FILE_SECURITY
def MirrorSetFileSecurity(
        FileName,
        SecurityInformation: PSECURITY_INFORMATION,
        SecurityDescriptor: PSECURITY_DESCRIPTOR,
        SecurityDescriptorLength: ULONG,
        DokanFileInfo: PDOKAN_FILE_INFO
):
    UNREFERENCED_PARAMETER(SecurityDescriptorLength)
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    DbgPrint("SetFileSecurity %s\n", filePath.value)

    handle = HANDLE(DokanFileInfo.contents.Context)
    if not handle or handle == INVALID_HANDLE_VALUE:
        DbgPrint("\tinvalid handle\n\n")
        return STATUS_INVALID_HANDLE

    if not SetUserObjectSecurity(handle, SecurityInformation, SecurityDescriptor):
        error = ctypes.GetLastError()
        DbgPrint("  SetUserObjectSecurity error: %d\n", error)
        return DokanNtStatusFromWin32(error)

    return STATUS_SUCCESS


@GET_VOLUME_INFORMATION
def MirrorGetVolumeInformation(
        VolumeNameBuffer: LPWSTR,
        VolumeNameSize: DWORD,
        VolumeSerialNumber: LPDWORD,
        MaximumComponentLength: LPDWORD,
        FileSystemFlags: LPDWORD,
        FileSystemNameBuffer: LPWSTR,
        FileSystemNameSize: DWORD,
        DokanFileInfo: PDOKAN_FILE_INFO
):
    UNREFERENCED_PARAMETER(DokanFileInfo)
    volumeRoot = (WCHAR * 4)()
    fsFlags = DWORD(0)
    flags = (
            FILE_SUPPORTS_REMOTE_STORAGE |
            FILE_UNICODE_ON_DISK |
            FILE_PERSISTENT_ACLS |
            FILE_NAMED_STREAMS
    )
    wcscpy_s(VolumeNameBuffer, VolumeNameSize, "DOKAN")

    if VolumeSerialNumber:
        VolumeSerialNumber.contnts = DWORD(0x19831116)
    if MaximumComponentLength:
        MaximumComponentLength.contents = DWORD(255)

    if g_CaseSensitive:
        flags |= FILE_CASE_SENSITIVE_SEARCH | FILE_CASE_PRESERVED_NAMES

    FileSystemFlags.contents = fsFlags
    volumeRoot[0] = RootDirectory[0]
    volumeRoot[1] = ':'
    volumeRoot[2] = '\\'
    volumeRoot[3] = '\0'

    if GetVolumeInformation(
            volumeRoot,
            None,
            0,
            None,
            MaximumComponentLength,
            ctypes.byref(fsFlags),
            FileSystemNameBuffer,
            FileSystemNameSize
    ):
        FileSystemFlags.contents = DWORD(flags | fsFlags.value)

        DbgPrint("GetVolumeInformation: max component length %u\n", MaximumComponentLength.contents.value)

        DbgPrint("GetVolumeInformation: file system name %s\n", FileSystemNameBuffer)

        DbgPrint("GetVolumeInformation: got file system flags 0x%08x, returning 0x%08x\n", fsFlags.value,
                 FileSystemFlags.contents.value)
    else:
        DbgPrint(
            "GetVolumeInformation: unable to query underlying fs, using defaults.  Last error = %u\n",
            ctypes.GetLastError())

        # File system name could be anything up to 10 characters.
        # But Windows check few feature availability based on file system name.
        # For this, it is recommended to set NTFS or FAT here.
        wcscpy_s(FileSystemNameBuffer, FileSystemNameSize, "NTFS")

    return STATUS_SUCCESS


#
# // Uncomment the function and set dokanOperations.GetDiskFreeSpace to personalize disk space
# /*
# static NTSTATUS DOKAN_CALLBACK MirrorDokanGetDiskFreeSpace(
#     PULONGLONG FreeBytesAvailable, PULONGLONG TotalNumberOfBytes,
#     PULONGLONG TotalNumberOfFreeBytes, PDOKAN_FILE_INFO DokanFileInfo) {
#   UNREFERENCED_PARAMETER(DokanFileInfo);
#
#   *FreeBytesAvailable = (ULONGLONG)(512 * 1024 * 1024);
#   *TotalNumberOfBytes = 9223372036854775807;
#   *TotalNumberOfFreeBytes = 9223372036854775807;
#
#   return STATUS_SUCCESS;
# }
# */

@GET_DISK_FREE_SPACE
def MirrorDokanGetDiskFreeSpace(
        FreeBytesAvailable,
        TotalNumberOfBytes,
        TotalNumberOfFreeBytes,
        DokanFileInfo
):
    UNREFERENCED_PARAMETER(DokanFileInfo)
    SectorsPerCluster = DWORD()
    BytesPerSector = DWORD()
    NumberOfFreeClusters = DWORD()
    TotalNumberOfClusters = DWORD()
    DriveLetter = (WCHAR * 3)('C', ':', '\x00')

    if RootDirectory[0] == '\\':  # UNC as Root
        RootPathName = (WCHAR * len(RootDirectory))(*list(RootDirectory))
    else:
        DriveLetter[0] = RootDirectory[0]
        RootPathName = DriveLetter

    GetDiskFreeSpace(
        RootPathName,
        ctypes.byref(SectorsPerCluster),
        ctypes.byref(BytesPerSector),
        ctypes.byref(NumberOfFreeClusters),
        ctypes.byref(TotalNumberOfClusters)
    )
    FreeBytesAvailable.contents = ULONG(
        SectorsPerCluster.value * BytesPerSector.value * NumberOfFreeClusters.value
    )
    TotalNumberOfFreeBytes.contents = ULONG(
        SectorsPerCluster.value * BytesPerSector.value * NumberOfFreeClusters.value
    )
    TotalNumberOfBytes.contents = ULONG(
        SectorsPerCluster.value * BytesPerSector.value * TotalNumberOfClusters.value
    )
    return STATUS_SUCCESS


@FIND_STREAMS
def MirrorFindStreams(FileName, FillFindStreamData, DokanFileInfo):
    filePath = (WCHAR * DOKAN_MAX_PATH)()
    GetFilePath(filePath, DOKAN_MAX_PATH, FileName)

    findData = WIN32_FIND_STREAM_DATA()
    count = 0

    DbgPrint("FindStreams :%s\n", filePath.value)

    hFind = FindFirstStream(
        filePath,
        FILE_STANDARD_INFORMATION.FindStreamInfoStandard,
        ctypes.byref(findData),
        0
    )

    if hFind == INVALID_HANDLE_VALUE:
        error = ctypes.GetLastError()
        DbgPrint("\tinvalid file handle. Error is %u\n\n", error)
        return DokanNtStatusFromWin32(error)

    FillFindStreamData(ctypes.byref(findData), DokanFileInfo)
    count += 1

    while FindNextStream(hFind, ctypes.byref(findData)) != 0:
        FillFindStreamData(ctypes.byref(findData), DokanFileInfo)
        count += 1

    error = ctypes.GetLastError()
    FindClose(hFind)

    if error != ERROR_HANDLE_EOF:
        DbgPrint("\tFindNextStreamW error. Error is %u\n\n", error)
        return DokanNtStatusFromWin32(error)

    DbgPrint("\tFindStreams return %d entries in %s\n\n", count, filePath)

    return STATUS_SUCCESS


@MOUNTED
def MirrorMounted(DokanFileInfo):
    UNREFERENCED_PARAMETER(DokanFileInfo)
    DbgPrint("Mounted\n")
    return STATUS_SUCCESS


@UNMOUNTED
def MirrorUnmounted(DokanFileInfo):
    UNREFERENCED_PARAMETER(DokanFileInfo)
    DbgPrint("Unmounted\n")
    return STATUS_SUCCESS


SetConsoleCtrlHandler = ctypes.windll.kernel32.SetConsoleCtrlHandler
SetConsoleCtrlHandler.restype = BOOL
HandlerRoutine = ctypes.WINFUNCTYPE(BOOL, DWORD)

CTRL_C_EVENT = 0
CTRL_BREAK_EVENT = 1
CTRL_CLOSE_EVENT = 2
CTRL_LOGOFF_EVENT = 5
CTRL_SHUTDOWN_EVENT = 6


@HandlerRoutine
def CtrlHandler(dwCtrlType):
    if dwCtrlType.value in (
            CTRL_C_EVENT,
            CTRL_BREAK_EVENT,
            CTRL_CLOSE_EVENT,
            CTRL_LOGOFF_EVENT,
            CTRL_SHUTDOWN_EVENT
    ):
        SetConsoleCtrlHandler(CtrlHandler, False)
        DokanRemoveMountPoint(MountPoint)
        return True

    return False


g_DebugMode = False
g_UseStdErr = False
g_CaseSensitive = False


def main(*args):
    global g_DebugMode
    global g_UseStdErr
    global g_CaseSensitive
    global g_ImpersonateCallerUser
    global g_HasSeSecurityPrivilege
    global RootDirectory

    import argparse

    parser = argparse.ArgumentParser(
        description='Mirror a local device or folder to secondary device, an NTFS folder or a network device.'
    )

    parser.add_argument('--unmount', action="store_true", default=False, dest="unmount",
                        help='Unmounts a drive.')
    parser.add_argument('--threads', action="store", default=0, dest="threads", type=int,
                        help='Number of threads to be used internally by Dokan library.\r\n'
                             'More threads will handle more event at the same time.')
    parser.add_argument('--debug', action="store_true", default=False, dest="debug",
                        help='Enable debug output to an attached debugger.')
    parser.add_argument('--stderr', action="store_true", default=False, dest="stderr_debug",
                        help='Output debugging data to STDERR.')
    parser.add_argument('--network', action="store_true", default=False, dest="network_drive",
                        help='Show device as network device.')
    parser.add_argument('--removable', action="store_true", default=False, dest="removable",
                        help='Show device as removable media.')
    parser.add_argument('--readonly', action="store_true", default=False, dest="read_only",
                        help='Read only filesystem.')
    parser.add_argument('--case-sensitive', action="store_true", default=False, dest="case_sensitive",
                        help='Case-sensitive file names.')
    parser.add_argument('--mount-manager', action="store_true", default=False, dest="mount_manager",
                        help='Register device to Windows mount manager. \r\n'
                             'This enables advanced Windows features like recycle bin and more.')
    parser.add_argument('--single-session', action="store_true", default=False, dest="single_session",
                        help='Device only visible for current user session.')
    parser.add_argument('--unc-name', action="store", default=None, dest="unc_name",
                        help='UNC name used for network volume.')
    parser.add_argument('--impersonate', action="store_true", default=False, dest="imp_credentials",
                        help='Impersonate Caller User when getting the handle in CreateFile for operations.\r\n'
                             'This option requires administrator right to work properly.')
    parser.add_argument('--alloc-size', action="store", default=4096, type=int, dest="allocation_size",
                        help='Allocation Unit Size of the volume.\r\n'
                             'This will alter the drive size, used space and free space that is displayed.')
    parser.add_argument('--sector-size', action="store", default=32, type=int, dest="sector_size",
                        help='Sector Size of the volume.\r\n'
                             'This will alter the drive size, used space and free space that is displayed.')
    parser.add_argument('--user-locks', action="store_true", default=False, dest="user_locks",
                        help='User mode file lock and unlock.\r\n'
                             'Enable Lockfile/Unlockfile operations. Otherwise Dokan will take care of it.')
    parser.add_argument('--disable-oplocks', action="store_true", default=False, dest="oplocks",
                        help='Disable OpLocks kernel operations. Otherwise Dokan will take care of it.')
    parser.add_argument('--timeout', action="store", default=15000, type=int, dest="timeout",
                        help='(Timeout in Milliseconds.\r\n'
                             'Timeout until a running operation is aborted and the device is unmounted.')
    parser.add_argument('--enable-fcb-gc', action="store_true", default=False, dest="enable_fcb",
                        help='Enabled FCB GC.\r\n'
                             'Might speed up on env with filter drivers (Anti-virus) slowing down the system.')
    parser.add_argument('--network-unmount', action="store_true", default=False, dest="network_unmount",
                        help='Allows unmounting network drive from file explorer')
    parser.add_argument('destination', nargs='+', action="store",
                        help='The Mount point and RootDirectory.\r\n'
                             'Can be M:\\ (drive letter) or empty NTFS folder C:\\mount\\dokan .\r\n '
                             'the source drive is the source to mirror. If --unmount is specified this '
                             'argument can be left out. otherwise it is required.')
    parser.add_argument('source', nargs='+', action="store",
                        help='The directory to mirror contents from.\r\n'
                             'Or empty NTFS folder C:\\mount\\dokan .\r\n '
                             'The source drive is the source to mirror. If --unmount is specified this '
                             'argument can be left out. otherwise it is required.')

    args = parser.parse_args(args)

    args.mount_point = args.destination[0]
    args.root_directory = args.source[0]

    if not args.unmount and not args.root_directory:
        raise RuntimeError(
            'You must supply both the source and destination '
            'directories when you are not unmounting a drive.'
        )

    if args.unmount:
        if args.mount_point not in DokanGetMountPointList(False):
            raise RuntimeError(
                'Unable to locate mapped drive "{0}"'.format(args.mount_point)
            )

        DokanRemoveMountPoint(args.unmount)
        sys.exit(0)

    if not args.network_drive:
        if args.network_unmount:
            args.network_drive = True

        if args.unc_name:
            args.network_drive = True

    if args.mount_manager:
        if args.network_drive:
            raise RuntimeError(
                'You cannot apply the mount manager to a network drive.'
            )
        if args.single_session:
            raise RuntimeError(
                'The mount manager will make all '
                'mounts persistant betwen user changes.'
            )

    if args.stderr_debug:
        args.debug = True

    if args.network_drive and args.removable:
        raise RuntimeError(
            '--network cannot be combined with --removable, '
            'if you do not supply either the drive will be '
            'attached like a hard disk')

    from py_dokany import Options

    options = Options()

    options.mount_point = args.mount_point
    options.thread_count = args.threads
    options.enable_debug = g_DebugMode = args.debug
    options.use_stderr_for_debug = g_UseStdErr = args.stderr_debug
    options.is_network_drive = args.network_drive
    options.is_removable_drive = args.removable
    options.write_protect_drive = args.read_only
    options.is_case_sensitive = g_CaseSensitive = args.case_sensitive
    options.use_mount_manager = args.mount_manager
    options.mount_drive_for_current_session = args.single_session
    # options.network_unc_name = args.unc_name
    options.allocation_unit_size = args.allocation_size
    options.sector_size = args.sector_size
    options.use_managed_file_locks = not args.user_locks
    options.disable_oplocks = not args.oplocks
    options.timeout = args.timeout
    options.enable_fcb_garbage_collection = args.enable_fcb
    options.enable_unmount_network_drive = args.network_unmount
    options.use_stream_names = True

    args.unc_name = '' if args.unc_name is None else args.unc_name

    wcsncpy_s(RootDirectory, DOKAN_MAX_PATH, args.root_directory, wcslen(args.root_directory))
    wcsncpy_s(MountPoint, DOKAN_MAX_PATH, args.mount_point, wcslen(args.mount_point))
    wcsncpy_s(UNCName, DOKAN_MAX_PATH, args.unc_name, wcslen(args.unc_name))

    g_ImpersonateCallerUser = args.imp_credentials

    if not SetConsoleCtrlHandler(CtrlHandler, True):
        print("Control Handler is not set.")

    # Add security name privilege. Required here to handle GetFileSecurity
    # properly.
    g_HasSeSecurityPrivilege = AddSeSecurityNamePrivilege()
    if not g_HasSeSecurityPrivilege:
        print("[Mirror] Failed to add security privilege to process\n"
              "\t=> GetFileSecurity/SetFileSecurity may not work properly\n"
              "\t=> Please restart mirror sample with administrator rights to fix it\n")
        sys.exit(1)

    dokanOperations = DOKAN_OPERATIONS()

    dokanOperations.ZwCreateFile = MirrorCreateFile
    dokanOperations.Cleanup = MirrorCleanup
    dokanOperations.CloseFile = MirrorCloseFile
    dokanOperations.ReadFile = MirrorReadFile
    dokanOperations.WriteFile = MirrorWriteFile
    dokanOperations.FlushFileBuffers = MirrorFlushFileBuffers
    dokanOperations.GetFileInformation = MirrorGetFileInformation
    dokanOperations.FindFiles = MirrorFindFiles
    # dokanOperations.FindFilesWithPattern = NULL;
    dokanOperations.SetFileAttributes = MirrorSetFileAttributes
    dokanOperations.SetFileTime = MirrorSetFileTime
    dokanOperations.DeleteFile = MirrorDeleteFile
    dokanOperations.DeleteDirectory = MirrorDeleteDirectory
    dokanOperations.MoveFile = MirrorMoveFile
    dokanOperations.SetEndOfFile = MirrorSetEndOfFile
    dokanOperations.SetAllocationSize = MirrorSetAllocationSize
    dokanOperations.LockFile = MirrorLockFile
    dokanOperations.UnlockFile = MirrorUnlockFile
    dokanOperations.GetFileSecurity = MirrorGetFileSecurity
    dokanOperations.SetFileSecurity = MirrorSetFileSecurity
    dokanOperations.GetDiskFreeSpace = MirrorDokanGetDiskFreeSpace
    dokanOperations.GetVolumeInformation = MirrorGetVolumeInformation
    dokanOperations.Unmounted = MirrorUnmounted
    dokanOperations.FindStreams = MirrorFindStreams
    dokanOperations.Mounted = MirrorMounted

    status_ = DokanMain(options, dokanOperations)
    if status_ == DOKAN_SUCCESS:
        print("Success")
    elif status_ == DOKAN_ERROR:
        print("Error")
    elif status_ == DOKAN_DRIVE_LETTER_ERROR:
        print("Bad Drive letter")
    elif status_ == DOKAN_DRIVER_INSTALL_ERROR:
        print("Can't install driver")
    elif status_ == DOKAN_START_ERROR:
        print("Driver something wrong")
    elif status_ == DOKAN_MOUNT_ERROR:
        print("Can't assign a drive letter")
    elif status_ == DOKAN_MOUNT_POINT_ERROR:
        print("Mount point error")
    elif status_ == DOKAN_VERSION_ERROR:
        print("Version error")
    else:
        print("Unknown error: %d" % (status_,))

    sys.exit(status_)


if __name__ == '__main__':
    import os

    base_path = os.path.dirname(__file__)
    # main('--unmount', 'R:', '')
    # main('--unmount', 'V:', '')

    if len(sys.argv) == 1:
        main('--impersonate', '--debug', '--enable-fcb-gc', 'X:', base_path)
    else:
        main(sys.argv)
