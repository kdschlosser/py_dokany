import os
import sys

from .windows_api import (
    SecurityAnonymous,
    SecurityIdentification,
    SecurityImpersonation,
    SecurityDelegation
)

base_path = os.path.dirname(__file__)
codes_path = os.path.join(base_path, 'codes.db')


class CodeWrapper(int):
    _str = ''

    def __call__(self, *args, **kwargs):
        return self

    @property
    def exception(self) -> "CodeException":
        return Codes.make_exception(self)

    @property
    def name(self):
        return self._str.rsplit('(', 1)[-1].replace(')', '')

    @property
    def hex(self):
        return self._str.split('(')[-2].replace(')', '')

    def __str__(self):
        return self._str


class CodeException(Exception):
    code: CodeWrapper

    def __str__(self):
        return str(self.code)

    def __call__(self, *args, **kwargs):
        return self


class Codes(object):
    """
    This collects the NTSTATUS and HRESULT codes that can be used with Dokany.
    There are a large number of them 1241 total and each code being 32 bit
    along with any documentation quite a bit of ram would be consumed if all
    of them were loaded into memory. Thre is no need to have the codes loaded
    that you are not going to use.
    """

    def __init__(self):
        mod = sys.modules[__name__]

        self.__name__ = mod.__dict__['__name__']
        self.__doc__ = mod.__dict__['__doc__']
        self.__loader__ = mod.__dict__['__loader__']
        self.__package__ = mod.__dict__['__package__']
        self.__spec__ = mod.__dict__['__spec__']
        self.__file__ = mod.__dict__['__file__']
        self.__cached__ = mod.__dict__['__cached__']
        self.__original_module__ = mod

        # noinspection PyTypeChecker
        sys.modules[__name__] = self

        for key, value in mod.__dict__.items():
            if key.isupper() and not key.startswith('_'):
                setattr(self, key, value)

    def add_code(self, name: str, value: int, docstring: str) -> CodeWrapper:
        if name in self:
            return getattr(self, name)

        desc = docstring.capitalize().replace('\n', '*&^NL^&*')
        val = '0x' + hex(value)[2:].upper().zfill(8)
        line = name + ' -- ' + val + ' -- ' + desc
        with open(codes_path, 'a') as f:
            f.write('\n' + line)

        desc += '({1})({0})'.format(name, val)
        namespace = {
            '__name__': name,
            '_str': desc
        }
        cls = type(name, (CodeWrapper,), namespace)
        val = cls(value)

        return val

    @staticmethod
    def make_exception(code: CodeWrapper) -> CodeException:
        namespace = {
            '__name__': code.name,
            'code': code
        }

        return type(code.name, (CodeException,), namespace)()

    def __contains__(self, item):
        # noinspection PyArgumentEqualDefault
        with open(codes_path, 'r') as f:
            line = f.readline()
            last_pos = f.tell()
            while not line.startswith(item):
                line = f.readline()
                if f.tell() == last_pos:
                    break
                last_pos = f.tell()

        return line.startswith(item)

    @property
    def all_codes(self):
        return list(self.__iter__())

    def __iter__(self):
        # noinspection PyArgumentEqualDefault
        with open(codes_path, 'r') as f:
            for line in f.readlines():
                name, value, desc = [item.strip() for item in line.split('--')]
                desc = desc.replace('*&^NL^&*', '\n').capitalize()
                desc += '({1})({0})'.format(name, value)
                namespace = {
                    '__name__': name,
                    '_str': desc
                }
                cls = type(name, (CodeWrapper,), namespace)
                val = cls(int(value, 16))
                yield val

    def __getattr__(self, item) -> CodeWrapper:
        if item in self.__dict__:
            return self.__dict__[item]

        # noinspection PyArgumentEqualDefault
        with open(codes_path, 'r') as f:
            line = f.readline()
            last_pos = f.tell()
            while not line.startswith(item):
                line = f.readline()
                if f.tell() == last_pos:
                    break
                last_pos = f.tell()

            if line.startswith(item):
                value, desc = [item.strip() for item in line.split('--')][1:]
                desc = desc.replace('*&^NL^&*', '\n').capitalize()
                desc += '({1})({0})'.format(item, value)
                namespace = {
                    '__name__': item,
                    '_str': desc
                }
                cls = type(item, (CodeWrapper,), namespace)
                val = cls(int(value, 16))

                self.__dict__[item] = val

                return val
        raise AttributeError('The code {0} is not in the database.'.format(item))


#: The starting point is zero or the beginning of the file.
FILE_BEGIN = 0x00000000

#:  The starting point is the current value of the file pointer.
FILE_CURRENT = 0x00000001

#: The starting point is the current end-of-file position.
FILE_END = 0x00000002

#: The privilege is enabled.
SE_PRIVILEGE_ENABLED = 0x00000002

#: The privilege is enabled by default.
SE_PRIVILEGE_ENABLED_BY_DEFAULT = 0x00000001

#: The privilege was used to gain access to an object or service.
#: This flag is used to identify the relevant privileges in a set passed by a client
#: application that may contain unnecessary privileges.
SE_PRIVILEGE_USED_FOR_ACCESS = 0x80000000

#: The privilege is removed from the list of privileges in the token.
#: The other privileges in the list are reordered to remain contiguous.
#: SE_PRIVILEGE_REMOVED supersedes SE_PRIVILEGE_ENABLED.
#: Because the privilege has been removed from the token, attempts to reenable the
#: privilege result in the warning ERROR_NOT_ALL_ASSIGNED as if the privilege had
#: never existed. Attempting to remove a privilege that does not exist in the token
#: results in ERROR_NOT_ALL_ASSIGNED being returned. Privilege checks for removed
#: privileges result in STATUS_PRIVILEGE_NOT_HELD. Failed privilege check auditing
#: occurs as normal.
SE_PRIVILEGE_REMOVED = 0x00000004

#: Access System Security Right
ACCESS_SYSTEM_SECURITY = 0x01000000

#: The owner identifier of the object is being referenced.
OWNER_SECURITY_INFORMATION = 0x00000001

#: The primary group identifier of the object is being referenced.
GROUP_SECURITY_INFORMATION = 0x00000002

#: The DACL of the object is being referenced.
DACL_SECURITY_INFORMATION = 0x00000004

#: The SACL of the object is being referenced.
SACL_SECURITY_INFORMATION = 0x00000008

#: The mandatory integrity label is being referenced.
LABEL_SECURITY_INFORMATION = 0x00000010

#: A SYSTEM_RESOURCE_ATTRIBUTE_ACE (section 2.4.4.15) is being referenced.
ATTRIBUTE_SECURITY_INFORMATION = 0x00000020

#: A SYSTEM_SCOPED_POLICY_ID_ACE (section 2.4.4.16) is being referenced.
SCOPE_SECURITY_INFORMATION = 0x00000040

#: Reserved.
PROCESS_TRUST_LABEL_SECURITY_INFORMATION = 0x00000080

#: The security descriptor is being accessed for use in a backup operation.
BACKUP_SECURITY_INFORMATION = 0x00010000

#: The DACL cannot inherit ACEs.
PROTECTED_DACL_SECURITY_INFORMATION = 0x80000000

#: The SACL cannot inherit ACEs.
PROTECTED_SACL_SECURITY_INFORMATION = 0x40000000

#: The DACL inherits ACEs from the parent object.
UNPROTECTED_DACL_SECURITY_INFORMATION = 0x20000000

#: The SACL inherits access control entries (ACEs) from the parent object.
UNPROTECTED_SACL_SECURITY_INFORMATION = 0x10000000

# used in the DOKAN_OPERATIONS.ZwCreateFile callback.
# these flags are what get set  to the DesiredAccess parameter

#: Read data from a file.
FILE_READ_DATA = 0x00000001

#: Read the attributes of a file or directory
FILE_READ_ATTRIBUTES = 0x00000080

#: Read the extended attributes (EAs) of a file or directory
#: This flag is irrelevant for device and intermediate drivers.
FILE_READ_EA = 0x00000008

#: Write data to a file.
FILE_WRITE_DATA = 0x00000002

#: Write the attributes of a file or directory.
FILE_WRITE_ATTRIBUTES = 0x00000100

#: Change the extended attributes (EAs) of a file or directory.
#: This flag is irrelevant for device and intermediate drivers.
FILE_WRITE_EA = 0x00000010

#: Append data to a file.
FILE_APPEND_DATA = 0x00000004

#: Use system paging I/O to read data from a file into memory.
#: This flag is irrelevant for device and intermediate drivers.
FILE_EXECUTE = 0x00000020

#: List the files in a directory.
FILE_LIST_DIRECTORY = 0x00000001

#: Traverse a directory, in other words, include the directory in the path of a file.
FILE_TRAVERSE = 0x00000020


# dunno about these just yet
#: Add a dile to a directory
FILE_ADD_FILE = 0x00000002

#: Add a directory to a directory
FILE_ADD_SUBDIRECTORY = 0x00000004

#: Delete a file or directory that is a child
FILE_DELETE_CHILD = 0x00000040


# used in the DOKAN_OPERATIONS.ZwCreateFile callback.
# these flags are what get set  to the ShareAccess parameter

#: Read the file
FILE_SHARE_READ = 0x00000001

#: Write the file
FILE_SHARE_WRITE = 0x00000002

#: Delete the file
FILE_SHARE_DELETE = 0x00000004

FILE_SHARE_VALID_FLAGS = 0x00000007


# used in the DOKAN_OPERATIONS.ZwCreateFile callback.
# these flags are what get set  to the FileAttributes parameter

#: This value is reserved for system use.
FILE_ATTRIBUTE_DEVICE = 0x00000040

#: This value is reserved for system use.
FILE_ATTRIBUTE_VIRTUAL = 0x00010000

#: A file or directory that is an archive file or directory. Applications typically
#: use this attribute to mark files for backup or removal .
FILE_ATTRIBUTE_ARCHIVE = 0x00000020

#: A file or directory that is compressed. For a file, all of the data in the file
#: is compressed. For a directory, compression is the default for newly created
#: files and subdirectories.
FILE_ATTRIBUTE_COMPRESSED = 0x00000800

#: The handle that identifies a directory.
FILE_ATTRIBUTE_DIRECTORY = 0x00000010

#: A file or directory that is encrypted. For a file, all data streams in the file are
#: encrypted. For a directory, encryption is the default for newly created files and
#: subdirectories.
FILE_ATTRIBUTE_ENCRYPTED = 0x00004000

#: The file or directory is hidden. It is not included in an ordinary directory listing.
FILE_ATTRIBUTE_HIDDEN = 0x00000002

#: The directory or user data stream is configured with integrity
#: (only supported on ReFS volumes). It is not included in an ordinary directory listing.
#: The integrity setting persists with the file if it's renamed. If a file is copied the
#: destination file will have integrity set if either the source file or destination
#: directory have integrity set.
#: Windows Server 2008 R2, Windows 7, Windows Server 2008, Windows Vista,
#: Windows Server 2003 and Windows XP: This flag is not supported until
#: Windows Server 2012.
FILE_ATTRIBUTE_INTEGRITY_STREAM = 0x00008000

#: A file that does not have other attributes set. This attribute is valid only when used alone.
FILE_ATTRIBUTE_NORMAL = 0x00000080

#: The file or directory is not to be indexed by the content indexing service.
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 0x00002000

#: The user data stream not to be read by the background data integrity scanner
#: (AKA scrubber). When set on a directory it only provides inheritance.
#: This flag is only supported on Storage Spaces and ReFS volumes. It is not
#: included in an ordinary directory listing.
#: Windows Server 2008 R2, Windows 7, Windows Server 2008, Windows Vista,
#: Windows Server 2003 and Windows XP: This flag is not supported until
#: Windows 8 and Windows Server 2012.
FILE_ATTRIBUTE_NO_SCRUB_DATA = 0x00020000

#: The data of a file is not available immediately. This attribute indicates that the
#: file data is physically moved to offline storage. This attribute is used by Remote
#: Storage, which is the hierarchical storage management software. Applications should
#: not arbitrarily change this attribute.
FILE_ATTRIBUTE_OFFLINE = 0x00001000

#: A file that is read-only. Applications can read the file, but cannot write to it
#: or delete it. This attribute is not honored on directories. For more information,
#: see You cannot view or change the Read-only or the System attributes of folders
#: in Windows Server 2003, in Windows XP, in Windows Vista or in Windows 7.
FILE_ATTRIBUTE_READONLY = 0x00000001

#: When this attribute is set, it means that the file or directory is not fully present
#: locally. For a file that means that not all of its data is on local storage
#: (e.g. it may be sparse with some data still in remote storage). For a directory it
#: means that some of the directory contents are being virtualized from another location.
#: Reading the file / enumerating the directory will be more expensive than normal,
#: e.g. it will cause at least some of the file/directory content to be fetched from
#: a remote store. Only kernel-mode callers can set this bit.
FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x00400000

#: This attribute only appears in directory enumeration classes
#: (FILE_DIRECTORY_INFORMATION, FILE_BOTH_DIR_INFORMATION, etc.).
#: When this attribute is set, it means that the file or directory has no physical
#: representation on the local system; the item is virtual. Opening the item will be
#: more expensive than normal, e.g. it will cause at least some of it to be fetched
#: from a remote store.
FILE_ATTRIBUTE_RECALL_ON_OPEN = 0x00040000

#: A file or directory that has an associated reparse point, or a file that is a symbolic link.
FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400

#: A file that is a sparse file.
FILE_ATTRIBUTE_SPARSE_FILE = 0x00000200

#: A file or directory that the operating system uses a part of, or uses exclusively.
FILE_ATTRIBUTE_SYSTEM = 0x00000004

#: A file that is being used for temporary storage. File systems avoid writing data back to mass
#: storage if sufficient cache memory is available, because typically, an application deletes a
#: temporary file after the handle is closed. In that scenario, the system can entirely avoid
#: writing the data. Otherwise, the data is written after the handle is closed.
FILE_ATTRIBUTE_TEMPORARY = 0x00000100

# used in the DOKAN_OPERATIONS.ZwCreateFile callback.
# these flags are what get set to the CreateDisposition parameter

#: Replace a file if it exists, create it if it doesn't.
FILE_SUPERSEDE = 0x00000000

#: Open the file if it exists, return an error if it doesn't.
FILE_OPEN = 0x00000001

#: Return an error if the file exists, create the file if it doesn't.
FILE_CREATE = 0x00000002

#: Open the file if it exists, create the file if it doesn't.
FILE_OPEN_IF = 0x00000003

#: Open the file and overwrite it if it exists, return an error if it doesn't.
FILE_OVERWRITE = 0x00000004

#: Open the file and overwrite it if it exists, create the file if it doesn't.
FILE_OVERWRITE_IF = 0x00000005


# used in the DOKAN_OPERATIONS.ZwCreateFile callback.
# these flags are what get set to the CreateOptions parameter

#: The file is a directory.
#: Compatible CreateOptions flags are:
#:   FILE_SYNCHRONOUS_IO_ALERT,
#:   FILE_SYNCHRONOUS_IO_NONALERT,
#:   FILE_WRITE_THROUGH,
#:   FILE_OPEN_FOR_BACKUP_INTENT,
#:   FILE_OPEN_BY_FILE_ID.
#:
#: The CreateDisposition parameter must be set to one of the following:
#:   FILE_CREATE,
#:   FILE_OPEN,
#:   FILE_OPEN_IF
FILE_DIRECTORY_FILE = 0x00000001

#: The file is not a directory.
#: The file object to open can represent a data file; a logical, virtual, or physical device; or a volume.
FILE_NON_DIRECTORY_FILE = 0x00000040

#: System services, file-system drivers, and drivers that write data to the file must actually
#: transfer the data to the file before any requested write operation is considered complete.
FILE_WRITE_THROUGH = 0x00000002

#: All access to the file will be sequential.
FILE_SEQUENTIAL_ONLY = 0x00000004

#: Access to the file can be random, so no sequential read-ahead operations should be
#: performed by file-system drivers or by the system.
FILE_RANDOM_ACCESS = 0x00000800

#: The file cannot be cached or buffered in a driver's internal buffers.
#: This flag is incompatible with the DesiredAccess parameter's FILE_APPEND_DATA flag.
FILE_NO_INTERMEDIATE_BUFFERING = 0x00000008

#: All operations on the file are performed synchronously.
#: Any wait on behalf of the caller is subject to premature termination from alerts.
#: This flag also causes the I/O system to maintain the file-position pointer.
#: If this flag is set, the SYNCHRONIZE flag must be set in the DesiredAccess parameter.
FILE_SYNCHRONOUS_IO_ALERT = 0x00000010

#: All operations on the file are performed synchronously.
#: Waits in the system that synchronize I/O queuing and completion are not subject to alerts.
#: This flag also causes the I/O system to maintain the file-position context. If this flag is set,
#: the SYNCHRONIZE flag must be set in the DesiredAccess parameter.
FILE_SYNCHRONOUS_IO_NONALERT = 0x00000020

#: Create a tree connection for this file in order to open it over the network.
#: This flag is not used by device and intermediate drivers.
FILE_CREATE_TREE_CONNECTION = 0x00000080

#: Complete this operation immediately with an alternate success code of
#: STATUS_OPLOCK_BREAK_IN_PROGRESS if the target file is oplocked, rather than
#: blocking the caller's thread. If the file is oplocked, another caller already
#: has access to the file. This flag is not used by device and intermediate drivers.
FILE_COMPLETE_IF_OPLOCKED = 0x00000100

#: If the extended attributes (EAs) for an existing file being opened indicate that
#: the caller must understand EAs to properly interpret the file, NtCreateFile should
#: return an error.
#: This flag is irrelevant for device and intermediate drivers.
FILE_NO_EA_KNOWLEDGE = 0x00000200

#: Open a file with a reparse point and bypass normal reparse point processing for the file.
#: For more information, see the following Remarks section.
FILE_OPEN_REPARSE_POINT = 0x00200000

#: The system deletes the file when the last handle to the file is passed to NtClose.
#: If this flag is set, the DELETE flag must be set in the DesiredAccess parameter.
FILE_DELETE_ON_CLOSE = 0x00001000

#: The file name that is specified by the ObjectAttributes parameter includes a binary
#: 8-byte or 16-byte file reference number or object ID for the file, depending on the
#: file system as shown below. Optionally, a device name followed by a backslash character
#: may proceed these binary values.
#: For example, a device name will have the following format.
#:
#: \??\C:\FileID\device\HardDiskVolume1\ObjectID
#:
#: where FileID is 8 bytes and ObjectID is 16 bytes
#:
#: On NTFS, this can be a 8-byte or 16-byte reference number or object ID.
#: A 16-byte reference number is the same as an 8-byte number padded with zeros.
#:
#: On ReFS, this can be an 8-byte or 16-byte reference number.
#: A 16-byte number is not related to an 8-byte number. Object IDs are not supported.
#:
#: The FAT, ExFAT, UDFS, and CDFS file systems do not support this flag.
#:
#: This number is assigned by and specific to the particular file system.
#:
#: Note: Because the filename field will partly contain a binary blob,
#:       it is incorrect to assume that this is a valid Unicode string, and
#:       more importantly may not be a null terminated string.
FILE_OPEN_BY_FILE_ID = 0x00002000


#: The file is being opened for backup intent.
#: Therefore, the system should check for certain access rights and grant the caller
#: the appropriate access to the file—before checking the DesiredAccess parameter
#: against the file's security descriptor. This flag not used by device and
#: intermediate drivers.
FILE_OPEN_FOR_BACKUP_INTENT = 0x00004000

#: This flag allows an application to request a Filter opportunistic lock (oplock)
#: to prevent other applications from getting share violations. If there are already
#: open handles, the create request will fail with STATUS_OPLOCK_NOT_GRANTED. F
#: or more information, see the following Remarks section.
FILE_RESERVE_OPFILTER = 0x00100000

#: The file is being opened and an opportunistic lock (oplock) on the file is being
#: requested as a single atomic operation. The file system checks for oplocks before
#: it performs the create operation, and will fail the create with a return code of
#: STATUS_CANNOT_BREAK_OPLOCK if the result would be to break an existing oplock.
#:
#: Note: The FILE_OPEN_REQUIRING_OPLOCK flag is available in Windows 7, Windows
#:       Server 2008 R2 and later Windows operating systems.
FILE_OPEN_REQUIRING_OPLOCK = 0x00010000

#: The client opening the file or device is session aware and per session access is validated if necessary.
FILE_SESSION_AWARE = 0x00040000

#: Creates a new file, always.
#: If the specified file exists and is writable, the function overwrites the file.
#: If the file is overwritten then STATUS_OBJECT_NAME_COLLISION needs to be returned.
#:
#: If the specified file does not exist and is a valid path, a new file is created.
#: If the file is created STATUS_SUCCESS needs to be returned.
CREATE_ALWAYS = 0x00000002

#: Creates a new file, only if it does not already exist.
#: If the specified file exists return ERROR_FILE_EXISTS.
#:
#: If the specified file does not exist and is a valid path to a writable location.
#: If the file is created STATUS_SUCCESS needs to be returned.
CREATE_NEW = 0x00000001

#: Opens a file, always.
#: If the specified file exists STATUS_OBJECT_NAME_COLLISION needs to be returned.
#:
#: If the specified file does not exist and is a valid path to a writable location
#: If the file is created STATUS_SUCCESS needs to be returned.
OPEN_ALWAYS = 0x00000004

#: Opens a file or directory, only if it exists.
#: If the specified file or directory does not exist ERROR_FILE_NOT_FOUND needs to be returned.
#: If the specified file is a file and is_directory returns True STATUS_NOT_A_DIRECTORY must be returned.
#: If the file exists and has been opened STATUS_SUCCESS needs to be returned.
OPEN_EXISTING = 0x00000003

#: Opens a file and truncates it so that its size is zero bytes, only if it exists.
#: If the specified file does not exist ERROR_FILE_NOT_FOUND needs to be returned.
#:
#: NOTE: The calling process must open the file with the GENERIC_WRITE bit set as
#: part of the desired access parameter.
TRUNCATE_EXISTING = 0x00000005

# DesiredAccess
#: The caller can perform normal read operations on the object.
GENERIC_READ = 0x80000000

#: The caller can perform normal write operations on the object.
GENERIC_WRITE = 0x40000000

#: The caller can execute the object.
#: Note: This generally only makes sense for certain kinds of objects, such as file objects and section objects.
GENERIC_EXECUTE = 0x20000000

#: The caller can perform all normal operations on the object.
GENERIC_ALL = 0x10000000

#: The caller can delete the object.
DELETE = 0x00010000

#: The caller can read the access control list (ACL) and ownership information for the file.
READ_CONTROL = 0x00020000

#: The caller can change the discretionary access control list (DACL) information for the object.
WRITE_DAC = 0x00040000

#: The caller can change the ownership information for the file.
WRITE_OWNER = 0x00080000


#: Write operations will not go through any intermediate cache, they will go directly to disk.
FILE_FLAG_WRITE_THROUGH = 0x80000000

#: The file or device is being opened or created for asynchronous I/O.
#: When subsequent I/O operations are completed on this handle, the event specified in the
#: OVERLAPPED structure will be set to the signaled state.
#: If this flag is specified, the file can be used for simultaneous read and write operations.
#: If this flag is not specified, then I/O operations are serialized, even if the calls to
#: the read and write functions specify an OVERLAPPED structure.
FILE_FLAG_OVERLAPPED = 0x40000000

#: The file or device is being opened with no system caching for data reads and writes.
#: This flag does not affect hard disk caching or memory mapped files.
#: There are strict requirements for successfully working with files opened with CreateFile
#: using the FILE_FLAG_NO_BUFFERING flag, for details see File Buffering.
FILE_FLAG_NO_BUFFERING = 0x20000000

#: Access is intended to be random. The system can use this as a hint to optimize file caching.
#: This flag has no effect if the file system does not support cached I/O and FILE_FLAG_NO_BUFFERING.
FILE_FLAG_RANDOM_ACCESS = 0x10000000

#: Access is intended to be sequential from beginning to end.
#: The system can use this as a hint to optimize file caching.
#: This flag should not be used if read-behind (that is, reverse scans) will be used.
#: This flag has no effect if the file system does not support cached I/O and FILE_FLAG_NO_BUFFERING.
FILE_FLAG_SEQUENTIAL_SCAN = 0x08000000

#: The file is to be deleted immediately after all of its handles are closed, which includes
#: the specified handle and any other open or duplicated handles.
#: If there are existing open handles to a file, the call fails unless they were all opened
#: with the FILE_SHARE_DELETE share mode.
#: Subsequent open requests for the file fail, unless the FILE_SHARE_DELETE share mode is specified.
FILE_FLAG_DELETE_ON_CLOSE = 0x04000000

#: The file is being opened or created for a backup or restore operation.
#: The system ensures that the calling process overrides file security checks when the process
#: has SE_BACKUP_NAME and SE_RESTORE_NAME privileges.
#: You must set this flag to obtain a handle to a directory. A directory handle can be passed
#: to some functions instead of a file handle.
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000

#: Access will occur according to POSIX rules.
#: This includes allowing multiple files with names, differing only in case, for file systems
#: that support that naming. Use care when using this option, because files created with this
#: flag may not be accessible by applications that are written for MS-DOS or 16-bit Windows.
FILE_FLAG_POSIX_SEMANTICS = 0x01000000

#: The file or device is being opened with session awareness.
#: If this flag is not specified, then per-session devices (such as a device using RemoteFX
#: USB Redirection) cannot be opened by processes running in session 0. This flag has no
#: effect for callers not in session 0. This flag is supported only on server editions of Windows.
#: Windows Server 2008 R2 and Windows Server 2008:  This flag is not supported before Windows Server 2012.
FILE_FLAG_SESSION_AWARE = 0x00800000

#: Normal reparse point processing will not occur; CreateFile will attempt to open the reparse point.
#: When a file is opened, a file handle is returned, whether or not the filter that controls the
#: reparse point is operational.
#: This flag cannot be used with the CREATE_ALWAYS flag.
#: If the file is not a reparse point, then this flag is ignored.
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000

#: The file data is requested, but it should continue to be located in remote storage.
#: It should not be transported back to local storage.
#: This flag is for use by remote storage systems.
FILE_FLAG_OPEN_NO_RECALL = 0x00100000

#: If you attempt to create multiple instances of a pipe with this flag, creation
#: of the first instance succeeds, but creation of the next instance fails
#: with ERROR_ACCESS_DENIED.
FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000

#: Impersonate the client at the Anonymous impersonation level.
SECURITY_ANONYMOUS = SecurityAnonymous << 16

#: Impersonate the client at the Identification impersonation level.
SECURITY_IDENTIFICATION = SecurityIdentification << 16

#: Impersonate the client at the Impersonation impersonation level.
SECURITY_IMPERSONATION = SecurityImpersonation << 16

#: Impersonate the client at the Delegation impersonation level.
SECURITY_DELEGATION = SecurityDelegation << 16

#: The security tracking mode is dynamic. If this flag is not specified, the
#: security tracking mode is static.
SECURITY_CONTEXT_TRACKING = 0x00040000

#: Only the enabled aspects of the client security context are available to the server.
#: If you do not specify this flag, all aspects of the client security context are available.
#: This allows the client to limit the groups and privileges that a server can use while
#: impersonating the client.
SECURITY_EFFECTIVE_ONLY = 0x00080000

SECURITY_SQOS_PRESENT = 0x00100000

#: The file system supports case-sensitive file names.
FILE_CASE_SENSITIVE_SEARCH = 0x00000001

#: The file system preserves the case of file names when it places a name on disk.
FILE_CASE_PRESERVED_NAMES = 0x00000002

#: The specified volume is a direct access (DAX) volume.
FILE_DAX_VOLUME = 0x20000000

#: The file system supports file-based compression.
#: This flag is incompatible with the FILE_VOLUME_IS_COMPRESSED flag.
#: This flag does not affect how data is transferred over the network.
FILE_FILE_COMPRESSION = 0x00000010

#: The file system supports named data streams for a file.
FILE_NAMED_STREAMS = 0x00040000

#: The file system preserves and enforces access control lists (ACLs).
FILE_PERSISTENT_ACLS = 0x00000008

#: The specified volume is read-only.
FILE_READ_ONLY_VOLUME = 0x00080000

#: The specified volume can be written to one time only.
#: The write must be performed in sequential order.
FILE_SEQUENTIAL_WRITE_ONCE = 0x00100000

#: On a successful cleanup operation, the file system returns information that
#: describes additional actions taken during cleanup, such as deleting the file.
#: File system filters can examine this information in their post-cleanup callback.
FILE_RETURNS_CLEANUP_RESULT_INFO = 0x00000200

#: The file system supports POSIX-style delete and rename operations.
FILE_SUPPORTS_POSIX_UNLINK_RENAME = 0x00000400

#: The file system supports remote storage.
FILE_SUPPORTS_REMOTE_STORAGE = 0x00000100

#: The file system supports encryption.
FILE_SUPPORTS_ENCRYPTION = 0x00020000

#: The file system supports extended attributes (EAs).
FILE_SUPPORTS_EXTENDED_ATTRIBUTES = 0x00800000

#: The file system supports direct links to other devices and partitions.
FILE_SUPPORTS_HARD_LINKS = 0x00400000

#: The file system supports object identifiers.
FILE_SUPPORTS_OBJECT_IDS = 0x00010000

#: The file system supports open by file ID.
FILE_SUPPORTS_OPEN_BY_FILE_ID = 0x01000000

#: The file system supports reparse points.
FILE_SUPPORTS_REPARSE_POINTS = 0x00000080

#: The file system supports sparse files.
FILE_SUPPORTS_SPARSE_FILES = 0x00000040

#: The file system supports transaction processing.
FILE_SUPPORTS_TRANSACTIONS = 0x00200000

#: The file system supports update sequence number (USN) journals.
FILE_SUPPORTS_USN_JOURNAL = 0x02000000

#: The file system supports Unicode in file names.
FILE_UNICODE_ON_DISK = 0x00000004

#: The specified volume is a compressed volume.
#: This flag is incompatible with the FILE_FILE_COMPRESSION flag.
#: This does not affect how data is transferred over the network.
FILE_VOLUME_IS_COMPRESSED = 0x00008000

#: The file system supports per-user quotas.
FILE_VOLUME_QUOTAS = 0x00000020

#: The file system supports block cloning, that is, sharing logical
#: clusters between files on the same volume. The file system reallocates
#: on writes to shared clusters.
FILE_SUPPORTS_BLOCK_REFCOUNTING = 0x08000000

#: The file system supports integrity streams.
FILE_SUPPORTS_INTEGRITY_STREAMS = 0x04000000

#: The file system tracks whether each cluster of a file contains valid data
#: (either from explicit file writes or automatic zeros) or invalid data
#: (has not yet been written to or zeroed). File systems that use sparse valid
#: data length (VDL) do not store a valid data length and do not require that
#: valid data be contiguous within a file.
FILE_SUPPORTS_SPARSE_VDL = 0x10000000

#: The file system supports ghosting.
FILE_SUPPORTS_GHOSTING = 0x40000000

#: The caller can perform a wait operation on the object.
SYNCHRONIZE = 0x00100000

#: Combines DELETE, READ_CONTROL, WRITE_DAC, WRITE_OWNER, and SYNCHRONIZE access.
STANDARD_RIGHTS_ALL = (
    DELETE |
    READ_CONTROL |
    WRITE_DAC |
    WRITE_OWNER |
    SYNCHRONIZE
)

#: Currently defined to equal READ_CONTROL.
STANDARD_RIGHTS_EXECUTE = READ_CONTROL

#: Currently defined to equal READ_CONTROL.
STANDARD_RIGHTS_READ = READ_CONTROL

#: Combines DELETE, READ_CONTROL, WRITE_DAC, and WRITE_OWNER access.
STANDARD_RIGHTS_REQUIRED = (
    DELETE |
    READ_CONTROL |
    WRITE_DAC |
    WRITE_OWNER
)

#: Currently defined to equal READ_CONTROL.
STANDARD_RIGHTS_WRITE = READ_CONTROL

#: Required to attach a primary token to a process.
TOKEN_ASSIGN_PRIMARY = 0x0001

#: Required to duplicate an access token.
TOKEN_DUPLICATE = 0x0002

#: Required to query the source of an access token.
TOKEN_QUERY_SOURCE = 0x0010

#: Required to enable or disable the privileges in an access token.
TOKEN_ADJUST_PRIVILEGES = 0x00000020

#: Required to attach an impersonation access token to a process.
TOKEN_IMPERSONATE = 0x00000004

#: Required to query an access token.
TOKEN_QUERY = 0x00000008

#: Required to adjust the attributes of the groups in an access token.
TOKEN_ADJUST_GROUPS = 0x0040

#: Required to change the default owner, primary group, or DACL of an access token.
TOKEN_ADJUST_DEFAULT = 0x0080

#: Required to adjust the session ID of an access token. The SE_TCB_NAME privilege is required.
TOKEN_ADJUST_SESSIONID = 0x0100
TOKEN_ALL_ACCESS_P = (
    STANDARD_RIGHTS_REQUIRED |
    TOKEN_ASSIGN_PRIMARY |
    TOKEN_DUPLICATE |
    TOKEN_IMPERSONATE |
    TOKEN_QUERY |
    TOKEN_QUERY_SOURCE |
    TOKEN_ADJUST_PRIVILEGES |
    TOKEN_ADJUST_GROUPS |
    TOKEN_ADJUST_DEFAULT
)

#: Combines STANDARD_RIGHTS_EXECUTE and TOKEN_IMPERSONATE.
TOKEN_EXECUTE = (
    STANDARD_RIGHTS_EXECUTE |
    TOKEN_IMPERSONATE
)

#: Combines STANDARD_RIGHTS_READ and TOKEN_QUERY.
TOKEN_READ = (
    STANDARD_RIGHTS_READ |
    TOKEN_QUERY
)


#: Combines STANDARD_RIGHTS_WRITE, TOKEN_ADJUST_PRIVILEGES, TOKEN_ADJUST_GROUPS, and TOKEN_ADJUST_DEFAULT.
TOKEN_WRITE = (
    STANDARD_RIGHTS_WRITE |
    TOKEN_ADJUST_PRIVILEGES |
    TOKEN_ADJUST_GROUPS |
    TOKEN_ADJUST_DEFAULT
)


def TEXT(quote):
    return quote


SE_SECURITY_NAME = TEXT("SeSecurityPrivilege")


_codes = Codes()


if __name__ == '__main__':
    print(_codes.TOKEN_ADJUST_GROUPS)
    cde = _codes.STG_E_CSS_KEY_NOT_PRESENT
    print(cde)
    print(cde.hex)
    print(cde.name)
    print(int(cde))
    print()
    print()
    exc = _codes.make_exception(cde)
    raise exc


if 'ONLY_FOR_IDE_INTELLISENSE_AND_AUTOCOMPLETION' in os.environ:
    # This never actually runs and there for does not take up any ram,
    # it is only here for the sole purpose of having intellisense and
    # autocomplete function properly in your IDE

    EPT_NT_CANT_CREATE = CodeWrapper(0xC002004C)
    EPT_NT_CANT_PERFORM_OP = CodeWrapper(0xC0020035)
    EPT_NT_INVALID_ENTRY = CodeWrapper(0xC0020034)
    EPT_NT_NOT_REGISTERED = CodeWrapper(0xC0020036)
    RPC_NT_ADDRESS_ERROR = CodeWrapper(0xC0020045)
    RPC_NT_ALREADY_LISTENING = CodeWrapper(0xC002000E)
    RPC_NT_ALREADY_REGISTERED = CodeWrapper(0xC002000C)
    RPC_NT_BAD_STUB_DATA = CodeWrapper(0xC003000C)
    RPC_NT_BINDING_HAS_NO_AUTH = CodeWrapper(0xC002002F)
    RPC_NT_BINDING_INCOMPLETE = CodeWrapper(0xC0020051)
    RPC_NT_BYTE_COUNT_TOO_SMALL = CodeWrapper(0xC003000B)
    RPC_NT_CALL_CANCELLED = CodeWrapper(0xC0020050)
    RPC_NT_CALL_FAILED = CodeWrapper(0xC002001B)
    RPC_NT_CALL_FAILED_DNE = CodeWrapper(0xC002001C)
    RPC_NT_CALL_IN_PROGRESS = CodeWrapper(0xC0020049)
    RPC_NT_CANNOT_SUPPORT = CodeWrapper(0xC0020041)
    RPC_NT_CANT_CREATE_ENDPOINT = CodeWrapper(0xC0020015)
    RPC_NT_COMM_FAILURE = CodeWrapper(0xC0020052)
    RPC_NT_DUPLICATE_ENDPOINT = CodeWrapper(0xC0020029)
    RPC_NT_ENTRY_ALREADY_EXISTS = CodeWrapper(0xC002003D)
    RPC_NT_ENTRY_NOT_FOUND = CodeWrapper(0xC002003E)
    RPC_NT_ENUM_VALUE_OUT_OF_RANGE = CodeWrapper(0xC003000A)
    RPC_NT_FP_DIV_ZERO = CodeWrapper(0xC0020046)
    RPC_NT_FP_OVERFLOW = CodeWrapper(0xC0020048)
    RPC_NT_FP_UNDERFLOW = CodeWrapper(0xC0020047)
    RPC_NT_GROUP_MEMBER_NOT_FOUND = CodeWrapper(0xC002004B)
    RPC_NT_INCOMPLETE_NAME = CodeWrapper(0xC0020038)
    RPC_NT_INTERFACE_NOT_FOUND = CodeWrapper(0xC002003C)
    RPC_NT_INTERNAL_ERROR = CodeWrapper(0xC0020043)
    RPC_NT_INVALID_ASYNC_CALL = CodeWrapper(0xC0020063)
    RPC_NT_INVALID_ASYNC_HANDLE = CodeWrapper(0xC0020062)
    RPC_NT_INVALID_AUTH_IDENTITY = CodeWrapper(0xC0020032)
    RPC_NT_INVALID_BOUND = CodeWrapper(0xC0020023)
    RPC_NT_INVALID_ENDPOINT_FORMAT = CodeWrapper(0xC0020007)
    RPC_NT_INVALID_ES_ACTION = CodeWrapper(0xC0030059)
    RPC_NT_INVALID_NAF_ID = CodeWrapper(0xC0020040)
    RPC_NT_INVALID_NAME_SYNTAX = CodeWrapper(0xC0020025)
    RPC_NT_INVALID_NETWORK_OPTIONS = CodeWrapper(0xC0020019)
    RPC_NT_INVALID_NET_ADDR = CodeWrapper(0xC0020008)
    RPC_NT_INVALID_OBJECT = CodeWrapper(0xC002004D)
    RPC_NT_INVALID_PIPE_OBJECT = CodeWrapper(0xC003005C)
    RPC_NT_INVALID_PIPE_OPERATION = CodeWrapper(0xC003005D)
    RPC_NT_INVALID_RPC_PROTSEQ = CodeWrapper(0xC0020005)
    RPC_NT_INVALID_STRING_BINDING = CodeWrapper(0xC0020001)
    RPC_NT_INVALID_STRING_UUID = CodeWrapper(0xC0020006)
    RPC_NT_INVALID_TAG = CodeWrapper(0xC0020022)
    RPC_NT_INVALID_TIMEOUT = CodeWrapper(0xC002000A)
    RPC_NT_INVALID_VERS_OPTION = CodeWrapper(0xC0020039)
    RPC_NT_MAX_CALLS_TOO_SMALL = CodeWrapper(0xC002002B)
    RPC_NT_NAME_SERVICE_UNAVAILABLE = CodeWrapper(0xC002003F)
    RPC_NT_NOTHING_TO_EXPORT = CodeWrapper(0xC0020037)
    RPC_NT_NOT_ALL_OBJS_UNEXPORTED = CodeWrapper(0xC002003B)
    RPC_NT_NOT_CANCELLED = CodeWrapper(0xC0020058)
    RPC_NT_NOT_LISTENING = CodeWrapper(0xC0020010)
    RPC_NT_NOT_RPC_ERROR = CodeWrapper(0xC0020055)
    RPC_NT_NO_BINDINGS = CodeWrapper(0xC0020013)
    RPC_NT_NO_CALL_ACTIVE = CodeWrapper(0xC002001A)
    RPC_NT_NO_CONTEXT_AVAILABLE = CodeWrapper(0xC0020042)
    RPC_NT_NO_ENDPOINT_FOUND = CodeWrapper(0xC0020009)
    RPC_NT_NO_ENTRY_NAME = CodeWrapper(0xC0020024)
    RPC_NT_NO_INTERFACES = CodeWrapper(0xC002004F)
    RPC_NT_NO_MORE_BINDINGS = CodeWrapper(0xC002004A)
    RPC_NT_NO_MORE_ENTRIES = CodeWrapper(0xC0030001)
    RPC_NT_NO_MORE_MEMBERS = CodeWrapper(0xC002003A)
    RPC_NT_NO_PRINC_NAME = CodeWrapper(0xC0020054)
    RPC_NT_NO_PROTSEQS = CodeWrapper(0xC0020014)
    RPC_NT_NO_PROTSEQS_REGISTERED = CodeWrapper(0xC002000F)
    RPC_NT_NULL_REF_POINTER = CodeWrapper(0xC0030009)
    RPC_NT_OBJECT_NOT_FOUND = CodeWrapper(0xC002000B)
    RPC_NT_OUT_OF_RESOURCES = CodeWrapper(0xC0020016)
    RPC_NT_PIPE_CLOSED = CodeWrapper(0xC003005F)
    RPC_NT_PIPE_DISCIPLINE_ERROR = CodeWrapper(0xC0030060)
    RPC_NT_PIPE_EMPTY = CodeWrapper(0xC0030061)
    RPC_NT_PROCNUM_OUT_OF_RANGE = CodeWrapper(0xC002002E)
    RPC_NT_PROTOCOL_ERROR = CodeWrapper(0xC002001D)
    RPC_NT_PROTSEQ_NOT_FOUND = CodeWrapper(0xC002002D)
    RPC_NT_PROTSEQ_NOT_SUPPORTED = CodeWrapper(0xC0020004)
    RPC_NT_SEC_PKG_ERROR = CodeWrapper(0xC0020057)
    RPC_NT_SEND_INCOMPLETE = CodeWrapper(0x400200AF)
    RPC_NT_SERVER_TOO_BUSY = CodeWrapper(0xC0020018)
    RPC_NT_SERVER_UNAVAILABLE = CodeWrapper(0xC0020017)
    RPC_NT_SS_CANNOT_GET_CALL_HANDLE = CodeWrapper(0xC0030008)
    RPC_NT_SS_CHAR_TRANS_OPEN_FAIL = CodeWrapper(0xC0030002)
    RPC_NT_SS_CHAR_TRANS_SHORT_FILE = CodeWrapper(0xC0030003)
    RPC_NT_SS_CONTEXT_DAMAGED = CodeWrapper(0xC0030006)
    RPC_NT_SS_HANDLES_MISMATCH = CodeWrapper(0xC0030007)
    RPC_NT_STRING_TOO_LONG = CodeWrapper(0xC002002C)
    RPC_NT_TYPE_ALREADY_REGISTERED = CodeWrapper(0xC002000D)
    RPC_NT_UNKNOWN_AUTHN_LEVEL = CodeWrapper(0xC0020031)
    RPC_NT_UNKNOWN_AUTHN_SERVICE = CodeWrapper(0xC0020030)
    RPC_NT_UNKNOWN_AUTHN_TYPE = CodeWrapper(0xC002002A)
    RPC_NT_UNKNOWN_AUTHZ_SERVICE = CodeWrapper(0xC0020033)
    RPC_NT_UNKNOWN_IF = CodeWrapper(0xC0020012)
    RPC_NT_UNKNOWN_MGR_TYPE = CodeWrapper(0xC0020011)
    RPC_NT_UNSUPPORTED_AUTHN_LEVEL = CodeWrapper(0xC0020053)
    RPC_NT_UNSUPPORTED_NAME_SYNTAX = CodeWrapper(0xC0020026)
    RPC_NT_UNSUPPORTED_TRANS_SYN = CodeWrapper(0xC002001F)
    RPC_NT_UNSUPPORTED_TYPE = CodeWrapper(0xC0020021)
    RPC_NT_UUID_LOCAL_ONLY = CodeWrapper(0x40020056)
    RPC_NT_UUID_NO_ADDRESS = CodeWrapper(0xC0020028)
    RPC_NT_WRONG_ES_VERSION = CodeWrapper(0xC003005A)
    RPC_NT_WRONG_KIND_OF_BINDING = CodeWrapper(0xC0020002)
    RPC_NT_WRONG_PIPE_VERSION = CodeWrapper(0xC003005E)
    RPC_NT_WRONG_STUB_VERSION = CodeWrapper(0xC003005B)
    RPC_NT_ZERO_DIVIDE = CodeWrapper(0xC0020044)
    SEC_E_CONTEXT_EXPIRED = CodeWrapper(0x80090317)
    SEC_E_DECRYPT_FAILURE = CodeWrapper(0x80090330)
    SEC_E_ENCRYPT_FAILURE = CodeWrapper(0x80090329)
    SEC_E_WRONG_PRINCIPAL = CodeWrapper(0x80090322)
    STATUS_ACCESS_DENIED = CodeWrapper(0xC0000022)
    STATUS_ACCESS_DISABLED_BY_POLICY_OTHER = CodeWrapper(0xC0000364)
    STATUS_ACCESS_VIOLATION = CodeWrapper(0xC0000005)
    STATUS_ACCOUNT_DISABLED = CodeWrapper(0xC0000072)
    STATUS_ACCOUNT_EXPIRED = CodeWrapper(0xC0000193)
    STATUS_ACCOUNT_LOCKED_OUT = CodeWrapper(0xC0000234)
    STATUS_ACCOUNT_RESTRICTION = CodeWrapper(0xC000006E)
    STATUS_ADAPTER_HARDWARE_ERROR = CodeWrapper(0xC00000C2)
    STATUS_ADDRESS_ALREADY_ASSOCIATED = CodeWrapper(0xC0000238)
    STATUS_ADDRESS_NOT_ASSOCIATED = CodeWrapper(0xC0000239)
    STATUS_ALIAS_EXISTS = CodeWrapper(0xC0000154)
    STATUS_ALLOTTED_SPACE_EXCEEDED = CodeWrapper(0xC0000099)
    STATUS_ALREADY_DISCONNECTED = CodeWrapper(0x80000025)
    STATUS_AUDITING_DISABLED = CodeWrapper(0xC0000356)
    STATUS_BAD_BINDINGS = CodeWrapper(0xC000035B)
    STATUS_BAD_DESCRIPTOR_FORMAT = CodeWrapper(0xC00000E7)
    STATUS_BAD_DEVICE_TYPE = CodeWrapper(0xC00000CB)
    STATUS_BAD_IMPERSONATION_LEVEL = CodeWrapper(0xC00000A5)
    STATUS_BAD_INHERITANCE_ACL = CodeWrapper(0xC000007D)
    STATUS_BAD_LOGON_SESSION_STATE = CodeWrapper(0xC0000104)
    STATUS_BAD_NETWORK_NAME = CodeWrapper(0xC00000CC)
    STATUS_BAD_NETWORK_PATH = CodeWrapper(0xC00000BE)
    STATUS_BAD_REMOTE_ADAPTER = CodeWrapper(0xC00000C5)
    STATUS_BAD_TOKEN_TYPE = CodeWrapper(0xC00000A8)
    STATUS_BAD_VALIDATION_CLASS = CodeWrapper(0xC00000A7)
    STATUS_BEGINNING_OF_MEDIA = CodeWrapper(0x8000001F)
    STATUS_BUFFER_OVERFLOW = CodeWrapper(0x80000005)
    STATUS_BUFFER_TOO_SMALL = CodeWrapper(0xC0000023)
    STATUS_BUS_RESET = CodeWrapper(0x8000001D)
    STATUS_CANCELLED = CodeWrapper(0xC0000120)
    STATUS_CANNOT_IMPERSONATE = CodeWrapper(0xC000010D)
    STATUS_CANNOT_MAKE = CodeWrapper(0xC00002EA)
    STATUS_CANT_ACCESS_DOMAIN_INFO = CodeWrapper(0xC00000DA)
    STATUS_CANT_DISABLE_MANDATORY = CodeWrapper(0xC000005D)
    STATUS_CANT_OPEN_ANONYMOUS = CodeWrapper(0xC00000A6)
    STATUS_CHILD_MUST_BE_VOLATILE = CodeWrapper(0xC0000181)
    STATUS_CLEANER_CARTRIDGE_INSTALLED = CodeWrapper(0x80000027)
    STATUS_CLUSTER_INVALID_NETWORK = CodeWrapper(0xC0130010)
    STATUS_CLUSTER_INVALID_NETWORK_PROVIDER = CodeWrapper(0xC013000B)
    STATUS_CLUSTER_INVALID_NODE = CodeWrapper(0xC0130001)
    STATUS_CLUSTER_INVALID_REQUEST = CodeWrapper(0xC013000A)
    STATUS_CLUSTER_JOIN_IN_PROGRESS = CodeWrapper(0xC0130003)
    STATUS_CLUSTER_JOIN_NOT_IN_PROGRESS = CodeWrapper(0xC013000F)
    STATUS_CLUSTER_LOCAL_NODE_NOT_FOUND = CodeWrapper(0xC0130005)
    STATUS_CLUSTER_NETINTERFACE_EXISTS = CodeWrapper(0xC0130008)
    STATUS_CLUSTER_NETINTERFACE_NOT_FOUND = CodeWrapper(0xC0130009)
    STATUS_CLUSTER_NETWORK_ALREADY_OFFLINE = CodeWrapper(0x80130004)
    STATUS_CLUSTER_NETWORK_ALREADY_ONLINE = CodeWrapper(0x80130003)
    STATUS_CLUSTER_NETWORK_EXISTS = CodeWrapper(0xC0130006)
    STATUS_CLUSTER_NETWORK_NOT_FOUND = CodeWrapper(0xC0130007)
    STATUS_CLUSTER_NETWORK_NOT_INTERNAL = CodeWrapper(0xC0130016)
    STATUS_CLUSTER_NODE_ALREADY_DOWN = CodeWrapper(0x80130002)
    STATUS_CLUSTER_NODE_ALREADY_MEMBER = CodeWrapper(0x80130005)
    STATUS_CLUSTER_NODE_ALREADY_UP = CodeWrapper(0x80130001)
    STATUS_CLUSTER_NODE_DOWN = CodeWrapper(0xC013000C)
    STATUS_CLUSTER_NODE_EXISTS = CodeWrapper(0xC0130002)
    STATUS_CLUSTER_NODE_NOT_FOUND = CodeWrapper(0xC0130004)
    STATUS_CLUSTER_NODE_NOT_MEMBER = CodeWrapper(0xC013000E)
    STATUS_CLUSTER_NODE_NOT_PAUSED = CodeWrapper(0xC0130014)
    STATUS_CLUSTER_NODE_PAUSED = CodeWrapper(0xC0130013)
    STATUS_CLUSTER_NODE_UNREACHABLE = CodeWrapper(0xC013000D)
    STATUS_CLUSTER_NODE_UP = CodeWrapper(0xC0130012)
    STATUS_CLUSTER_NO_SECURITY_CONTEXT = CodeWrapper(0xC0130015)
    STATUS_COMMITMENT_LIMIT = CodeWrapper(0xC000012D)
    STATUS_CONNECTION_ABORTED = CodeWrapper(0xC0000241)
    STATUS_CONNECTION_ACTIVE = CodeWrapper(0xC000023B)
    STATUS_CONNECTION_COUNT_LIMIT = CodeWrapper(0xC0000246)
    STATUS_CONNECTION_INVALID = CodeWrapper(0xC000023A)
    STATUS_CONNECTION_IN_USE = CodeWrapper(0xC0000108)
    STATUS_CONNECTION_REFUSED = CodeWrapper(0xC0000236)
    STATUS_COPY_PROTECTION_FAILURE = CodeWrapper(0xC0000305)
    STATUS_CRC_ERROR = CodeWrapper(0xC000003F)
    STATUS_CRYPTO_SYSTEM_INVALID = CodeWrapper(0xC00002F3)
    STATUS_CSS_AUTHENTICATION_FAILURE = CodeWrapper(0xC0000306)
    STATUS_CSS_KEY_NOT_ESTABLISHED = CodeWrapper(0xC0000308)
    STATUS_CSS_KEY_NOT_PRESENT = CodeWrapper(0xC0000307)
    STATUS_CSS_REGION_MISMATCH = CodeWrapper(0xC000030A)
    STATUS_CSS_RESETS_EXHAUSTED = CodeWrapper(0xC000030B)
    STATUS_CSS_SCRAMBLED_SECTOR = CodeWrapper(0xC0000309)
    STATUS_CTX_BAD_VIDEO_MODE = CodeWrapper(0xC00A0018)
    STATUS_CTX_CLIENT_LICENSE_IN_USE = CodeWrapper(0xC00A0034)
    STATUS_CTX_CLIENT_LICENSE_NOT_SET = CodeWrapper(0xC00A0033)
    STATUS_CTX_CLIENT_QUERY_TIMEOUT = CodeWrapper(0xC00A0026)
    STATUS_CTX_CLOSE_PENDING = CodeWrapper(0xC00A0006)
    STATUS_CTX_CONSOLE_CONNECT = CodeWrapper(0xC00A0028)
    STATUS_CTX_CONSOLE_DISCONNECT = CodeWrapper(0xC00A0027)
    STATUS_CTX_GRAPHICS_INVALID = CodeWrapper(0xC00A0022)
    STATUS_CTX_INVALID_MODEMNAME = CodeWrapper(0xC00A0009)
    STATUS_CTX_INVALID_PD = CodeWrapper(0xC00A0002)
    STATUS_CTX_INVALID_WD = CodeWrapper(0xC00A002E)
    STATUS_CTX_LICENSE_CLIENT_INVALID = CodeWrapper(0xC00A0012)
    STATUS_CTX_LICENSE_EXPIRED = CodeWrapper(0xC00A0014)
    STATUS_CTX_LICENSE_NOT_AVAILABLE = CodeWrapper(0xC00A0013)
    STATUS_CTX_MODEM_INF_NOT_FOUND = CodeWrapper(0xC00A0008)
    STATUS_CTX_MODEM_RESPONSE_BUSY = CodeWrapper(0xC00A000E)
    STATUS_CTX_MODEM_RESPONSE_NO_CARRIER = CodeWrapper(0xC00A000C)
    STATUS_CTX_MODEM_RESPONSE_NO_DIALTONE = CodeWrapper(0xC00A000D)
    STATUS_CTX_MODEM_RESPONSE_TIMEOUT = CodeWrapper(0xC00A000B)
    STATUS_CTX_MODEM_RESPONSE_VOICE = CodeWrapper(0xC00A000F)
    STATUS_CTX_NOT_CONSOLE = CodeWrapper(0xC00A0024)
    STATUS_CTX_NO_OUTBUF = CodeWrapper(0xC00A0007)
    STATUS_CTX_PD_NOT_FOUND = CodeWrapper(0xC00A0003)
    STATUS_CTX_RESPONSE_ERROR = CodeWrapper(0xC00A000A)
    STATUS_CTX_SHADOW_DENIED = CodeWrapper(0xC00A002A)
    STATUS_CTX_SHADOW_DISABLED = CodeWrapper(0xC00A0031)
    STATUS_CTX_SHADOW_ENDED_BY_MODE_CHANGE = CodeWrapper(0xC00A0035)
    STATUS_CTX_SHADOW_INVALID = CodeWrapper(0xC00A0030)
    STATUS_CTX_SHADOW_NOT_RUNNING = CodeWrapper(0xC00A0036)
    STATUS_CTX_TD_ERROR = CodeWrapper(0xC00A0010)
    STATUS_CTX_WD_NOT_FOUND = CodeWrapper(0xC00A002F)
    STATUS_CTX_WINSTATION_ACCESS_DENIED = CodeWrapper(0xC00A002B)
    STATUS_CTX_WINSTATION_BUSY = CodeWrapper(0xC00A0017)
    STATUS_CTX_WINSTATION_NAME_COLLISION = CodeWrapper(0xC00A0016)
    STATUS_CTX_WINSTATION_NAME_INVALID = CodeWrapper(0xC00A0001)
    STATUS_CTX_WINSTATION_NOT_FOUND = CodeWrapper(0xC00A0015)
    STATUS_CURRENT_DOMAIN_NOT_ALLOWED = CodeWrapper(0xC00002E9)
    STATUS_DESTINATION_ELEMENT_FULL = CodeWrapper(0xC0000284)
    STATUS_DEVICE_BUSY = CodeWrapper(0x80000011)
    STATUS_DEVICE_DOES_NOT_EXIST = CodeWrapper(0xC00000C0)
    STATUS_DEVICE_DOOR_OPEN = CodeWrapper(0x80000289)
    STATUS_DEVICE_NOT_CONNECTED = CodeWrapper(0xC000009D)
    STATUS_DEVICE_NOT_PARTITIONED = CodeWrapper(0xC0000174)
    STATUS_DEVICE_NOT_READY = CodeWrapper(0xC00000A3)
    STATUS_DEVICE_PAPER_EMPTY = CodeWrapper(0x8000000E)
    STATUS_DEVICE_REMOVED = CodeWrapper(0xC00002B6)
    STATUS_DEVICE_REQUIRES_CLEANING = CodeWrapper(0x80000288)
    STATUS_DFS_UNAVAILABLE = CodeWrapper(0xC000026D)
    STATUS_DIRECTORY_NOT_EMPTY = CodeWrapper(0xC0000101)
    STATUS_DIRECTORY_SERVICE_REQUIRED = CodeWrapper(0xC00002B1)
    STATUS_DISK_CORRUPT_ERROR = CodeWrapper(0xC0000032)
    STATUS_DISK_FULL = CodeWrapper(0xC000007F)
    STATUS_DISK_OPERATION_FAILED = CodeWrapper(0xC000016A)
    STATUS_DISK_RECALIBRATE_FAILED = CodeWrapper(0xC0000169)
    STATUS_DISK_RESET_FAILED = CodeWrapper(0xC000016B)
    STATUS_DLL_INIT_FAILED = CodeWrapper(0xC0000142)
    STATUS_DLL_NOT_FOUND = CodeWrapper(0xC0000135)
    STATUS_DOMAIN_CONTROLLER_NOT_FOUND = CodeWrapper(0xC0000233)
    STATUS_DOMAIN_EXISTS = CodeWrapper(0xC00000E0)
    STATUS_DOMAIN_LIMIT_EXCEEDED = CodeWrapper(0xC00000E1)
    STATUS_DOMAIN_TRUST_INCONSISTENT = CodeWrapper(0xC000019B)
    STATUS_DOWNGRADE_DETECTED = CodeWrapper(0xC0000388)
    STATUS_DRIVER_BLOCKED = CodeWrapper(0xC000036C)
    STATUS_DRIVER_UNABLE_TO_LOAD = CodeWrapper(0xC000026C)
    STATUS_DS_ADMIN_LIMIT_EXCEEDED = CodeWrapper(0xC00002C1)
    STATUS_DS_AG_CANT_HAVE_UNIVERSAL_MEMBER = CodeWrapper(0xC0000358)
    STATUS_DS_ATTRIBUTE_OR_VALUE_EXISTS = CodeWrapper(0xC00002A4)
    STATUS_DS_ATTRIBUTE_TYPE_UNDEFINED = CodeWrapper(0xC00002A3)
    STATUS_DS_BUSY = CodeWrapper(0xC00002A5)
    STATUS_DS_CANT_MOD_OBJ_CLASS = CodeWrapper(0xC00002AE)
    STATUS_DS_CANT_MOD_PRIMARYGROUPID = CodeWrapper(0xC00002D0)
    STATUS_DS_CANT_ON_NON_LEAF = CodeWrapper(0xC00002AC)
    STATUS_DS_CANT_ON_RDN = CodeWrapper(0xC00002AD)
    STATUS_DS_CANT_START = CodeWrapper(0xC00002E1)
    STATUS_DS_CROSS_DOM_MOVE_FAILED = CodeWrapper(0xC00002AF)
    STATUS_DS_GC_NOT_AVAILABLE = CodeWrapper(0xC00002B0)
    STATUS_DS_GC_REQUIRED = CodeWrapper(0xC00002E4)
    STATUS_DS_GLOBAL_CANT_HAVE_CROSSDOMAIN_MEMBER = CodeWrapper(0xC00002DA)
    STATUS_DS_GLOBAL_CANT_HAVE_LOCAL_MEMBER = CodeWrapper(0xC00002D7)
    STATUS_DS_GLOBAL_CANT_HAVE_UNIVERSAL_MEMBER = CodeWrapper(0xC00002D8)
    STATUS_DS_HAVE_PRIMARY_MEMBERS = CodeWrapper(0xC00002DC)
    STATUS_DS_INCORRECT_ROLE_OWNER = CodeWrapper(0xC00002A9)
    STATUS_DS_INIT_FAILURE = CodeWrapper(0xC00002E2)
    STATUS_DS_INIT_FAILURE_CONSOLE = CodeWrapper(0xC00002EC)
    STATUS_DS_INVALID_ATTRIBUTE_SYNTAX = CodeWrapper(0xC00002A2)
    STATUS_DS_INVALID_GROUP_TYPE = CodeWrapper(0xC00002D4)
    STATUS_DS_LOCAL_CANT_HAVE_CROSSDOMAIN_LOCAL_MEMBER = CodeWrapper(0xC00002DB)
    STATUS_DS_LOCAL_MEMBER_OF_LOCAL_ONLY = CodeWrapper(0xC00002E5)
    STATUS_DS_MACHINE_ACCOUNT_QUOTA_EXCEEDED = CodeWrapper(0xC00002E7)
    STATUS_DS_MEMBERSHIP_EVALUATED_LOCALLY = CodeWrapper(0x00000121)
    STATUS_DS_NO_ATTRIBUTE_OR_VALUE = CodeWrapper(0xC00002A1)
    STATUS_DS_NO_FPO_IN_UNIVERSAL_GROUPS = CodeWrapper(0xC00002E6)
    STATUS_DS_NO_MORE_RIDS = CodeWrapper(0xC00002A8)
    STATUS_DS_NO_NEST_GLOBALGROUP_IN_MIXEDDOMAIN = CodeWrapper(0xC00002D5)
    STATUS_DS_NO_NEST_LOCALGROUP_IN_MIXEDDOMAIN = CodeWrapper(0xC00002D6)
    STATUS_DS_NO_RIDS_ALLOCATED = CodeWrapper(0xC00002A7)
    STATUS_DS_OBJ_CLASS_VIOLATION = CodeWrapper(0xC00002AB)
    STATUS_DS_RIDMGR_INIT_ERROR = CodeWrapper(0xC00002AA)
    STATUS_DS_SAM_INIT_FAILURE = CodeWrapper(0xC00002CB)
    STATUS_DS_SAM_INIT_FAILURE_CONSOLE = CodeWrapper(0xC00002ED)
    STATUS_DS_SENSITIVE_GROUP_VIOLATION = CodeWrapper(0xC00002CD)
    STATUS_DS_SHUTTING_DOWN = CodeWrapper(0x40000370)
    STATUS_DS_UNAVAILABLE = CodeWrapper(0xC00002A6)
    STATUS_DS_UNIVERSAL_CANT_HAVE_LOCAL_MEMBER = CodeWrapper(0xC00002D9)
    STATUS_DUPLICATE_NAME = CodeWrapper(0xC00000BD)
    STATUS_EAS_NOT_SUPPORTED = CodeWrapper(0xC000004F)
    STATUS_EA_LIST_INCONSISTENT = CodeWrapper(0x80000014)
    STATUS_EFS_ALG_BLOB_TOO_BIG = CodeWrapper(0xC0000352)
    STATUS_END_OF_FILE = CodeWrapper(0xC0000011)
    STATUS_END_OF_MEDIA = CodeWrapper(0x8000001E)
    STATUS_EOM_OVERFLOW = CodeWrapper(0xC0000177)
    STATUS_EVENTLOG_CANT_START = CodeWrapper(0xC000018F)
    STATUS_EVENTLOG_FILE_CHANGED = CodeWrapper(0xC0000197)
    STATUS_EVENTLOG_FILE_CORRUPT = CodeWrapper(0xC000018E)
    STATUS_FILEMARK_DETECTED = CodeWrapper(0x8000001B)
    STATUS_FILES_OPEN = CodeWrapper(0xC0000107)
    STATUS_FILE_CORRUPT_ERROR = CodeWrapper(0xC0000102)
    STATUS_FILE_ENCRYPTED = CodeWrapper(0xC0000293)
    STATUS_FILE_INVALID = CodeWrapper(0xC0000098)
    STATUS_FILE_IS_OFFLINE = CodeWrapper(0xC0000267)
    STATUS_FILE_NOT_ENCRYPTED = CodeWrapper(0xC0000291)
    STATUS_FLOPPY_BAD_REGISTERS = CodeWrapper(0xC0000168)
    STATUS_FLOPPY_ID_MARK_NOT_FOUND = CodeWrapper(0xC0000165)
    STATUS_FLOPPY_UNKNOWN_ERROR = CodeWrapper(0xC0000167)
    STATUS_FLOPPY_WRONG_CYLINDER = CodeWrapper(0xC0000166)
    STATUS_FULLSCREEN_MODE = CodeWrapper(0xC0000159)
    STATUS_GENERIC_NOT_MAPPED = CodeWrapper(0xC00000E6)
    STATUS_GRACEFUL_DISCONNECT = CodeWrapper(0xC0000237)
    STATUS_GROUP_EXISTS = CodeWrapper(0xC0000065)
    STATUS_HOST_DOWN = CodeWrapper(0xC0000350)
    STATUS_HOST_UNREACHABLE = CodeWrapper(0xC000023D)
    STATUS_ILLEGAL_ELEMENT_ADDRESS = CodeWrapper(0xC0000285)
    STATUS_ILL_FORMED_PASSWORD = CodeWrapper(0xC000006B)
    STATUS_IMAGE_ALREADY_LOADED = CodeWrapper(0xC000010E)
    STATUS_INFO_LENGTH_MISMATCH = CodeWrapper(0xC0000004)
    STATUS_INSUFFICIENT_RESOURCES = CodeWrapper(0xC000009A)
    STATUS_INSUFF_SERVER_RESOURCES = CodeWrapper(0xC0000205)
    STATUS_INTEGER_OVERFLOW = CodeWrapper(0xC0000095)
    STATUS_INTERNAL_DB_CORRUPTION = CodeWrapper(0xC00000E4)
    STATUS_INTERNAL_DB_ERROR = CodeWrapper(0xC0000158)
    STATUS_INTERNAL_ERROR = CodeWrapper(0xC00000E5)
    STATUS_INVALID_ACCOUNT_NAME = CodeWrapper(0xC0000062)
    STATUS_INVALID_ACL = CodeWrapper(0xC0000077)
    STATUS_INVALID_ADDRESS_COMPONENT = CodeWrapper(0xC0000207)
    STATUS_INVALID_BLOCK_LENGTH = CodeWrapper(0xC0000173)
    STATUS_INVALID_COMPUTER_NAME = CodeWrapper(0xC0000122)
    STATUS_INVALID_DEVICE_STATE = CodeWrapper(0xC0000184)
    STATUS_INVALID_DOMAIN_ROLE = CodeWrapper(0xC00000DE)
    STATUS_INVALID_DOMAIN_STATE = CodeWrapper(0xC00000DD)
    STATUS_INVALID_EA_NAME = CodeWrapper(0x80000013)
    STATUS_INVALID_GROUP_ATTRIBUTES = CodeWrapper(0xC00000A4)
    STATUS_INVALID_HANDLE = CodeWrapper(0xC0000008)
    STATUS_INVALID_ID_AUTHORITY = CodeWrapper(0xC0000084)
    STATUS_INVALID_IMAGE_FORMAT = CodeWrapper(0xC000007B)
    STATUS_INVALID_IMPORT_OF_NON_DLL = CodeWrapper(0xC000036F)
    STATUS_INVALID_LEVEL = CodeWrapper(0xC0000148)
    STATUS_INVALID_LOGON_HOURS = CodeWrapper(0xC000006F)
    STATUS_INVALID_LOGON_TYPE = CodeWrapper(0xC000010B)
    STATUS_INVALID_MEMBER = CodeWrapper(0xC000017B)
    STATUS_INVALID_NETWORK_RESPONSE = CodeWrapper(0xC00000C3)
    STATUS_INVALID_OPLOCK_PROTOCOL = CodeWrapper(0xC00000E3)
    STATUS_INVALID_OWNER = CodeWrapper(0xC000005A)
    STATUS_INVALID_PARAMETER = CodeWrapper(0xC000000D)
    STATUS_INVALID_PIPE_STATE = CodeWrapper(0xC00000AD)
    STATUS_INVALID_PRIMARY_GROUP = CodeWrapper(0xC000005B)
    STATUS_INVALID_SECURITY_DESCR = CodeWrapper(0xC0000079)
    STATUS_INVALID_SERVER_STATE = CodeWrapper(0xC00000DC)
    STATUS_INVALID_SID = CodeWrapper(0xC0000078)
    STATUS_INVALID_SUB_AUTHORITY = CodeWrapper(0xC0000076)
    STATUS_INVALID_USER_BUFFER = CodeWrapper(0xC00000E8)
    STATUS_INVALID_VOLUME_LABEL = CodeWrapper(0xC0000086)
    STATUS_INVALID_WORKSTATION = CodeWrapper(0xC0000070)
    STATUS_IN_PAGE_ERROR = CodeWrapper(0xC0000006)
    STATUS_IO_DEVICE_ERROR = CodeWrapper(0xC0000185)
    STATUS_IO_REPARSE_DATA_INVALID = CodeWrapper(0xC0000278)
    STATUS_IO_REPARSE_TAG_INVALID = CodeWrapper(0xC0000276)
    STATUS_IO_REPARSE_TAG_MISMATCH = CodeWrapper(0xC0000277)
    STATUS_IO_REPARSE_TAG_NOT_HANDLED = CodeWrapper(0xC0000279)
    STATUS_IO_TIMEOUT = CodeWrapper(0xC00000B5)
    STATUS_ISSUING_CA_UNTRUSTED = CodeWrapper(0xC000038A)
    STATUS_JOURNAL_DELETE_IN_PROGRESS = CodeWrapper(0xC00002B7)
    STATUS_JOURNAL_ENTRY_DELETED = CodeWrapper(0xC00002CF)
    STATUS_JOURNAL_NOT_ACTIVE = CodeWrapper(0xC00002B8)
    STATUS_KDC_INVALID_REQUEST = CodeWrapper(0xC00002FB)
    STATUS_KDC_UNABLE_TO_REFER = CodeWrapper(0xC00002FC)
    STATUS_KDC_UNKNOWN_ETYPE = CodeWrapper(0xC00002FD)
    STATUS_KEY_DELETED = CodeWrapper(0xC000017C)
    STATUS_KEY_HAS_CHILDREN = CodeWrapper(0xC0000180)
    STATUS_LAST_ADMIN = CodeWrapper(0xC0000069)
    STATUS_LICENSE_QUOTA_EXCEEDED = CodeWrapper(0xC0000259)
    STATUS_LM_CROSS_ENCRYPTION_REQUIRED = CodeWrapper(0xC000017F)
    STATUS_LOCAL_USER_SESSION_KEY = CodeWrapper(0x40000006)
    STATUS_LOCK_NOT_GRANTED = CodeWrapper(0xC0000055)
    STATUS_LOGIN_TIME_RESTRICTION = CodeWrapper(0xC0000247)
    STATUS_LOGIN_WKSTA_RESTRICTION = CodeWrapper(0xC0000248)
    STATUS_LOGON_FAILURE = CodeWrapper(0xC000006D)
    STATUS_LOGON_NOT_GRANTED = CodeWrapper(0xC0000155)
    STATUS_LOGON_SESSION_COLLISION = CodeWrapper(0xC0000105)
    STATUS_LOGON_SESSION_EXISTS = CodeWrapper(0xC00000EE)
    STATUS_LOGON_TYPE_NOT_GRANTED = CodeWrapper(0xC000015B)
    STATUS_LOG_FILE_FULL = CodeWrapper(0xC0000188)
    STATUS_LUIDS_EXHAUSTED = CodeWrapper(0xC0000075)
    STATUS_MAGAZINE_NOT_PRESENT = CodeWrapper(0xC0000286)
    STATUS_MAPPED_ALIGNMENT = CodeWrapper(0xC0000220)
    STATUS_MAX_REFERRALS_EXCEEDED = CodeWrapper(0xC00002F4)
    STATUS_MEDIA_CHANGED = CodeWrapper(0x8000001C)
    STATUS_MEDIA_WRITE_PROTECTED = CodeWrapper(0xC00000A2)
    STATUS_MEMBERS_PRIMARY_GROUP = CodeWrapper(0xC0000127)
    STATUS_MEMBER_IN_ALIAS = CodeWrapper(0xC0000153)
    STATUS_MEMBER_IN_GROUP = CodeWrapper(0xC0000067)
    STATUS_MEMBER_NOT_IN_ALIAS = CodeWrapper(0xC0000152)
    STATUS_MEMBER_NOT_IN_GROUP = CodeWrapper(0xC0000068)
    STATUS_MEMORY_NOT_ALLOCATED = CodeWrapper(0xC00000A0)
    STATUS_MESSAGE_NOT_FOUND = CodeWrapper(0xC0000109)
    STATUS_MFT_TOO_FRAGMENTED = CodeWrapper(0xC0000304)
    STATUS_MUST_BE_KDC = CodeWrapper(0xC00002F5)
    STATUS_MUTUAL_AUTHENTICATION_FAILED = CodeWrapper(0xC00002C3)
    STATUS_NAME_TOO_LONG = CodeWrapper(0xC0000106)
    STATUS_NETLOGON_NOT_STARTED = CodeWrapper(0xC0000192)
    STATUS_NETWORK_ACCESS_DENIED = CodeWrapper(0xC00000CA)
    STATUS_NETWORK_BUSY = CodeWrapper(0xC00000BF)
    STATUS_NETWORK_CREDENTIAL_CONFLICT = CodeWrapper(0xC0000195)
    STATUS_NETWORK_NAME_DELETED = CodeWrapper(0xC00000C9)
    STATUS_NETWORK_UNREACHABLE = CodeWrapper(0xC000023C)
    STATUS_NET_WRITE_FAULT = CodeWrapper(0xC00000D2)
    STATUS_NOLOGON_INTERDOMAIN_TRUST_ACCOUNT = CodeWrapper(0xC0000198)
    STATUS_NOLOGON_SERVER_TRUST_ACCOUNT = CodeWrapper(0xC000019A)
    STATUS_NOLOGON_WORKSTATION_TRUST_ACCOUNT = CodeWrapper(0xC0000199)
    STATUS_NONEXISTENT_SECTOR = CodeWrapper(0xC0000015)
    STATUS_NONE_MAPPED = CodeWrapper(0xC0000073)
    STATUS_NOTIFY_ENUM_DIR = CodeWrapper(0x0000010C)
    STATUS_NOT_ALL_ASSIGNED = CodeWrapper(0x00000106)
    STATUS_NOT_A_DIRECTORY = CodeWrapper(0xC0000103)
    STATUS_NOT_A_REPARSE_POINT = CodeWrapper(0xC0000275)
    STATUS_NOT_EXPORT_FORMAT = CodeWrapper(0xC0000292)
    STATUS_NOT_FOUND = CodeWrapper(0xC0000225)
    STATUS_NOT_IMPLEMENTED = CodeWrapper(0xC0000002)
    STATUS_NOT_LOCKED = CodeWrapper(0xC000002A)
    STATUS_NOT_LOGON_PROCESS = CodeWrapper(0xC00000ED)
    STATUS_NOT_REGISTRY_FILE = CodeWrapper(0xC000015C)
    STATUS_NOT_SAME_DEVICE = CodeWrapper(0xC00000D4)
    STATUS_NOT_SUPPORTED = CodeWrapper(0xC00000BB)
    STATUS_NOT_SUPPORTED_ON_SBS = CodeWrapper(0xC0000300)
    STATUS_NO_BROWSER_SERVERS_FOUND = CodeWrapper(0xC000021C)
    STATUS_NO_DATA_DETECTED = CodeWrapper(0x80000022)
    STATUS_NO_IMPERSONATION_TOKEN = CodeWrapper(0xC000005C)
    STATUS_NO_INHERITANCE = CodeWrapper(0x8000000B)
    STATUS_NO_IP_ADDRESSES = CodeWrapper(0xC00002F1)
    STATUS_NO_KERB_KEY = CodeWrapper(0xC0000322)
    STATUS_NO_LDT = CodeWrapper(0xC0000117)
    STATUS_NO_LOGON_SERVERS = CodeWrapper(0xC000005E)
    STATUS_NO_LOG_SPACE = CodeWrapper(0xC000017D)
    STATUS_NO_MATCH = CodeWrapper(0xC0000272)
    STATUS_NO_MEDIA = CodeWrapper(0xC0000178)
    STATUS_NO_MEMORY = CodeWrapper(0xC0000017)
    STATUS_NO_MORE_ENTRIES = CodeWrapper(0x8000001A)
    STATUS_NO_MORE_FILES = CodeWrapper(0x80000006)
    STATUS_NO_PA_DATA = CodeWrapper(0xC00002F8)
    STATUS_NO_QUOTAS_FOR_ACCOUNT = CodeWrapper(0x0000010D)
    STATUS_NO_SECURITY_ON_OBJECT = CodeWrapper(0xC00000D7)
    STATUS_NO_SPOOL_SPACE = CodeWrapper(0xC00000C7)
    STATUS_NO_SUCH_ALIAS = CodeWrapper(0xC0000151)
    STATUS_NO_SUCH_DOMAIN = CodeWrapper(0xC00000DF)
    STATUS_NO_SUCH_GROUP = CodeWrapper(0xC0000066)
    STATUS_NO_SUCH_LOGON_SESSION = CodeWrapper(0xC000005F)
    STATUS_NO_SUCH_MEMBER = CodeWrapper(0xC000017A)
    STATUS_NO_SUCH_PACKAGE = CodeWrapper(0xC00000FE)
    STATUS_NO_SUCH_PRIVILEGE = CodeWrapper(0xC0000060)
    STATUS_NO_SUCH_USER = CodeWrapper(0xC0000064)
    STATUS_NO_TGT_REPLY = CodeWrapper(0xC00002EF)
    STATUS_NO_TOKEN = CodeWrapper(0xC000007C)
    STATUS_NO_TRACKING_SERVICE = CodeWrapper(0xC000029F)
    STATUS_NO_TRUST_LSA_SECRET = CodeWrapper(0xC000018A)
    STATUS_NO_TRUST_SAM_ACCOUNT = CodeWrapper(0xC000018B)
    STATUS_NO_USER_SESSION_KEY = CodeWrapper(0xC0000202)
    STATUS_NT_CROSS_ENCRYPTION_REQUIRED = CodeWrapper(0xC000015D)
    STATUS_NULL_LM_PASSWORD = CodeWrapper(0x4000000D)
    STATUS_OBJECT_NAME_COLLISION = CodeWrapper(0xC0000035)
    STATUS_OBJECT_NAME_INVALID = CodeWrapper(0xC0000033)
    STATUS_OBJECT_NAME_NOT_FOUND = CodeWrapper(0xC0000034)
    STATUS_OBJECT_PATH_INVALID = CodeWrapper(0xC0000039)
    STATUS_OBJECT_PATH_NOT_FOUND = CodeWrapper(0xC000003A)
    STATUS_ONLY_IF_CONNECTED = CodeWrapper(0xC00002CC)
    STATUS_OPLOCK_NOT_GRANTED = CodeWrapper(0xC00000E2)
    STATUS_ORDINAL_NOT_FOUND = CodeWrapper(0xC0000138)
    STATUS_PAGEFILE_QUOTA = CodeWrapper(0xC0000007)
    STATUS_PARTIAL_COPY = CodeWrapper(0x8000000D)
    STATUS_PARTITION_FAILURE = CodeWrapper(0xC0000172)
    STATUS_PASSWORD_EXPIRED = CodeWrapper(0xC0000071)
    STATUS_PASSWORD_MUST_CHANGE = CodeWrapper(0xC0000224)
    STATUS_PASSWORD_RESTRICTION = CodeWrapper(0xC000006C)
    STATUS_PENDING = CodeWrapper(0x00000103)
    STATUS_PIPE_BROKEN = CodeWrapper(0xC000014B)
    STATUS_PIPE_BUSY = CodeWrapper(0xC00000AE)
    STATUS_PIPE_CONNECTED = CodeWrapper(0xC00000B2)
    STATUS_PIPE_DISCONNECTED = CodeWrapper(0xC00000B0)
    STATUS_PIPE_EMPTY = CodeWrapper(0xC00000D9)
    STATUS_PIPE_LISTENING = CodeWrapper(0xC00000B3)
    STATUS_PKINIT_CLIENT_FAILURE = CodeWrapper(0xC000038C)
    STATUS_PKINIT_FAILURE = CodeWrapper(0xC0000320)
    STATUS_PKINIT_NAME_MISMATCH = CodeWrapper(0xC00002F9)
    STATUS_PLUGPLAY_NO_DEVICE = CodeWrapper(0xC000025E)
    STATUS_POLICY_OBJECT_NOT_FOUND = CodeWrapper(0xC000029A)
    STATUS_POLICY_ONLY_IN_DS = CodeWrapper(0xC000029B)
    STATUS_PORT_UNREACHABLE = CodeWrapper(0xC000023F)
    STATUS_POSSIBLE_DEADLOCK = CodeWrapper(0xC0000194)
    STATUS_PRENT4_MACHINE_ACCOUNT = CodeWrapper(0xC0000357)
    STATUS_PRINT_CANCELLED = CodeWrapper(0xC00000C8)
    STATUS_PRINT_QUEUE_FULL = CodeWrapper(0xC00000C6)
    STATUS_PRIVILEGE_NOT_HELD = CodeWrapper(0xC0000061)
    STATUS_PROCEDURE_NOT_FOUND = CodeWrapper(0xC000007A)
    STATUS_PROPSET_NOT_FOUND = CodeWrapper(0xC0000230)
    STATUS_PROTOCOL_UNREACHABLE = CodeWrapper(0xC000023E)
    STATUS_QUOTA_EXCEEDED = CodeWrapper(0xC0000044)
    STATUS_REDIRECTOR_PAUSED = CodeWrapper(0xC00000D1)
    STATUS_REGISTRY_CORRUPT = CodeWrapper(0xC000014C)
    STATUS_REGISTRY_IO_FAILED = CodeWrapper(0xC000014D)
    STATUS_REGISTRY_RECOVERED = CodeWrapper(0x40000009)
    STATUS_REG_NAT_CONSUMPTION = CodeWrapper(0xC00002C9)
    STATUS_REINITIALIZATION_NEEDED = CodeWrapper(0xC0000287)
    STATUS_REMOTE_NOT_LISTENING = CodeWrapper(0xC00000BC)
    STATUS_REMOTE_SESSION_LIMIT = CodeWrapper(0xC0000196)
    STATUS_REMOTE_STORAGE_MEDIA_ERROR = CodeWrapper(0xC000029E)
    STATUS_REMOTE_STORAGE_NOT_ACTIVE = CodeWrapper(0xC000029D)
    STATUS_REPARSE_ATTRIBUTE_CONFLICT = CodeWrapper(0xC00002B2)
    STATUS_REPARSE_POINT_NOT_RESOLVED = CodeWrapper(0xC0000280)
    STATUS_REQUEST_ABORTED = CodeWrapper(0xC0000240)
    STATUS_REQUEST_NOT_ACCEPTED = CodeWrapper(0xC00000D0)
    STATUS_RESOURCE_DATA_NOT_FOUND = CodeWrapper(0xC0000089)
    STATUS_RESOURCE_LANG_NOT_FOUND = CodeWrapper(0xC0000204)
    STATUS_RESOURCE_NAME_NOT_FOUND = CodeWrapper(0xC000008B)
    STATUS_RESOURCE_NOT_OWNED = CodeWrapper(0xC0000264)
    STATUS_RESOURCE_TYPE_NOT_FOUND = CodeWrapper(0xC000008A)
    STATUS_RETRY = CodeWrapper(0xC000022D)
    STATUS_REVISION_MISMATCH = CodeWrapper(0xC0000059)
    STATUS_REVOCATION_OFFLINE_C = CodeWrapper(0xC000038B)
    STATUS_RXACT_COMMIT_FAILURE = CodeWrapper(0xC000011D)
    STATUS_RXACT_INVALID_STATE = CodeWrapper(0xC000011C)
    STATUS_SAM_INIT_FAILURE = CodeWrapper(0xC00002E3)
    STATUS_SAM_NEED_BOOTKEY_FLOPPY = CodeWrapper(0xC00002E0)
    STATUS_SAM_NEED_BOOTKEY_PASSWORD = CodeWrapper(0xC00002DF)
    STATUS_SECRET_TOO_LONG = CodeWrapper(0xC0000157)
    STATUS_SECTION_NOT_EXTENDED = CodeWrapper(0xC0000087)
    STATUS_SEMAPHORE_LIMIT_EXCEEDED = CodeWrapper(0xC0000047)
    STATUS_SERIAL_COUNTER_TIMEOUT = CodeWrapper(0x4000000C)
    STATUS_SERIAL_MORE_WRITES = CodeWrapper(0x40000008)
    STATUS_SERIAL_NO_DEVICE_INITED = CodeWrapper(0xC0000150)
    STATUS_SERVER_DISABLED = CodeWrapper(0xC0000080)
    STATUS_SERVER_NOT_DISABLED = CodeWrapper(0xC0000081)
    STATUS_SERVER_SHUTDOWN_IN_PROGRESS = CodeWrapper(0xC00002FF)
    STATUS_SETMARK_DETECTED = CodeWrapper(0x80000021)
    STATUS_SHARED_IRQ_BUSY = CodeWrapper(0xC000016C)
    STATUS_SHARED_POLICY = CodeWrapper(0xC0000299)
    STATUS_SHARING_PAUSED = CodeWrapper(0xC00000CF)
    STATUS_SHARING_VIOLATION = CodeWrapper(0xC0000043)
    STATUS_SHUTDOWN_IN_PROGRESS = CodeWrapper(0xC00002FE)
    STATUS_SMARTCARD_CARD_BLOCKED = CodeWrapper(0xC0000381)
    STATUS_SMARTCARD_CARD_NOT_AUTHENTICATED = CodeWrapper(0xC0000382)
    STATUS_SMARTCARD_CERT_EXPIRED = CodeWrapper(0xC000038D)
    STATUS_SMARTCARD_CERT_REVOKED = CodeWrapper(0xC0000389)
    STATUS_SMARTCARD_IO_ERROR = CodeWrapper(0xC0000387)
    STATUS_SMARTCARD_LOGON_REQUIRED = CodeWrapper(0xC00002FA)
    STATUS_SMARTCARD_NO_CARD = CodeWrapper(0xC0000383)
    STATUS_SMARTCARD_NO_CERTIFICATE = CodeWrapper(0xC0000385)
    STATUS_SMARTCARD_NO_KEYSET = CodeWrapper(0xC0000386)
    STATUS_SMARTCARD_NO_KEY_CONTAINER = CodeWrapper(0xC0000384)
    STATUS_SMARTCARD_SUBSYSTEM_FAILURE = CodeWrapper(0xC0000321)
    STATUS_SMARTCARD_WRONG_PIN = CodeWrapper(0xC0000380)
    STATUS_SOME_NOT_MAPPED = CodeWrapper(0x00000107)
    STATUS_SOURCE_ELEMENT_EMPTY = CodeWrapper(0xC0000283)
    STATUS_SPECIAL_ACCOUNT = CodeWrapper(0xC0000124)
    STATUS_SPECIAL_GROUP = CodeWrapper(0xC0000125)
    STATUS_SPECIAL_USER = CodeWrapper(0xC0000126)
    STATUS_STACK_OVERFLOW = CodeWrapper(0xC00000FD)
    STATUS_STRONG_CRYPTO_NOT_SUPPORTED = CodeWrapper(0xC00002F6)
    STATUS_SUCCESS = CodeWrapper(0x00EF00C8)
    STATUS_SUSPEND_COUNT_EXCEEDED = CodeWrapper(0xC000004A)
    STATUS_SXS_ACTIVATION_CONTEXT_DISABLED = CodeWrapper(0xC0150007)
    STATUS_SXS_ASSEMBLY_NOT_FOUND = CodeWrapper(0xC0150004)
    STATUS_SXS_CANT_GEN_ACTCTX = CodeWrapper(0xC0150002)
    STATUS_SXS_INVALID_ACTCTXDATA_FORMAT = CodeWrapper(0xC0150003)
    STATUS_SXS_KEY_NOT_FOUND = CodeWrapper(0xC0150008)
    STATUS_SXS_MANIFEST_FORMAT_ERROR = CodeWrapper(0xC0150005)
    STATUS_SXS_MANIFEST_PARSE_ERROR = CodeWrapper(0xC0150006)
    STATUS_SXS_PROCESS_DEFAULT_ALREADY_SET = CodeWrapper(0xC015000E)
    STATUS_SXS_SECTION_NOT_FOUND = CodeWrapper(0xC0150001)
    STATUS_SXS_THREAD_QUERIES_DISABLED = CodeWrapper(0xC015000B)
    STATUS_SXS_WRONG_SECTION_TYPE = CodeWrapper(0xC015000A)
    STATUS_TIME_DIFFERENCE_AT_DC = CodeWrapper(0xC0000133)
    STATUS_TOKEN_ALREADY_IN_USE = CodeWrapper(0xC000012B)
    STATUS_TOO_MANY_COMMANDS = CodeWrapper(0xC00000C1)
    STATUS_TOO_MANY_CONTEXT_IDS = CodeWrapper(0xC000015A)
    STATUS_TOO_MANY_LINKS = CodeWrapper(0xC0000265)
    STATUS_TOO_MANY_LUIDS_REQUESTED = CodeWrapper(0xC0000074)
    STATUS_TOO_MANY_NAMES = CodeWrapper(0xC00000CD)
    STATUS_TOO_MANY_OPENED_FILES = CodeWrapper(0xC000011F)
    STATUS_TOO_MANY_PRINCIPALS = CodeWrapper(0xC00002F7)
    STATUS_TOO_MANY_SECRETS = CodeWrapper(0xC0000156)
    STATUS_TOO_MANY_SESSIONS = CodeWrapper(0xC00000CE)
    STATUS_TOO_MANY_SIDS = CodeWrapper(0xC000017E)
    STATUS_TRANSPORT_FULL = CodeWrapper(0xC00002CA)
    STATUS_TRUSTED_DOMAIN_FAILURE = CodeWrapper(0xC000018C)
    STATUS_TRUSTED_RELATIONSHIP_FAILURE = CodeWrapper(0xC000018D)
    STATUS_TRUST_FAILURE = CodeWrapper(0xC0000190)
    STATUS_UNABLE_TO_LOCK_MEDIA = CodeWrapper(0xC0000175)
    STATUS_UNABLE_TO_UNLOAD_MEDIA = CodeWrapper(0xC0000176)
    STATUS_UNEXPECTED_NETWORK_ERROR = CodeWrapper(0xC00000C4)
    STATUS_UNFINISHED_CONTEXT_DELETED = CodeWrapper(0xC00002EE)
    STATUS_UNKNOWN_REVISION = CodeWrapper(0xC0000058)
    STATUS_UNMAPPABLE_CHARACTER = CodeWrapper(0xC0000162)
    STATUS_UNRECOGNIZED_MEDIA = CodeWrapper(0xC0000014)
    STATUS_UNRECOGNIZED_VOLUME = CodeWrapper(0xC000014F)
    STATUS_UNSUCCESSFUL = CodeWrapper(0xC0000001)
    STATUS_UNSUPPORTED_PREAUTH = CodeWrapper(0xC0000351)
    STATUS_USER_EXISTS = CodeWrapper(0xC0000063)
    STATUS_USER_MAPPED_FILE = CodeWrapper(0xC0000243)
    STATUS_VARIABLE_NOT_FOUND = CodeWrapper(0xC0000100)
    STATUS_VIRTUAL_CIRCUIT_CLOSED = CodeWrapper(0xC00000D6)
    STATUS_WMI_ALREADY_DISABLED = CodeWrapper(0xC0000302)
    STATUS_WMI_ALREADY_ENABLED = CodeWrapper(0xC0000303)
    STATUS_WMI_GUID_DISCONNECTED = CodeWrapper(0xC0000301)
    STATUS_WMI_GUID_NOT_FOUND = CodeWrapper(0xC0000295)
    STATUS_WMI_INSTANCE_NOT_FOUND = CodeWrapper(0xC0000296)
    STATUS_WMI_ITEMID_NOT_FOUND = CodeWrapper(0xC0000297)
    STATUS_WMI_READ_ONLY = CodeWrapper(0xC00002C6)
    STATUS_WMI_SET_FAILURE = CodeWrapper(0xC00002C7)
    STATUS_WMI_TRY_AGAIN = CodeWrapper(0xC0000298)
    STATUS_WORKING_SET_QUOTA = CodeWrapper(0xC00000A1)
    STATUS_WRONG_CREDENTIAL_HANDLE = CodeWrapper(0xC00002F2)
    STATUS_WRONG_PASSWORD = CodeWrapper(0xC000006A)
    STATUS_WRONG_VOLUME = CodeWrapper(0xC0000012)
    EPT_S_CANT_CREATE = CodeWrapper(0x8007076B)
    EPT_S_CANT_PERFORM_OP = CodeWrapper(0x800706D8)
    EPT_S_INVALID_ENTRY = CodeWrapper(0x800706D7)
    EPT_S_NOT_REGISTERED = CodeWrapper(0x800706D9)
    ERROR_ACCESS_DENIED = CodeWrapper(0x80070005)
    ERROR_ACCESS_DISABLED_BY_POLICY = CodeWrapper(0x800704EC)
    ERROR_ACCOUNT_DISABLED = CodeWrapper(0x80070533)
    ERROR_ACCOUNT_EXPIRED = CodeWrapper(0x80070701)
    ERROR_ACCOUNT_LOCKED_OUT = CodeWrapper(0x80070775)
    ERROR_ACCOUNT_RESTRICTION = CodeWrapper(0x8007052F)
    ERROR_ACTIVE_CONNECTIONS = CodeWrapper(0x80070962)
    ERROR_ADAP_HDW_ERR = CodeWrapper(0x80070039)
    ERROR_ADDRESS_ALREADY_ASSOCIATED = CodeWrapper(0x800704CB)
    ERROR_ADDRESS_NOT_ASSOCIATED = CodeWrapper(0x800704CC)
    ERROR_ALIAS_EXISTS = CodeWrapper(0x80070563)
    ERROR_ALLOTTED_SPACE_EXCEEDED = CodeWrapper(0x80070540)
    ERROR_ALREADY_EXISTS = CodeWrapper(0x800700B7)
    ERROR_ARITHMETIC_OVERFLOW = CodeWrapper(0x80070216)
    ERROR_AUDITING_DISABLED = CodeWrapper(0xC0090001)
    ERROR_BADDB = CodeWrapper(0x800703F1)
    ERROR_BAD_COMMAND = CodeWrapper(0x80070016)
    ERROR_BAD_DESCRIPTOR_FORMAT = CodeWrapper(0x80070551)
    ERROR_BAD_DEV_TYPE = CodeWrapper(0x80070042)
    ERROR_BAD_DRIVER = CodeWrapper(0x80070077)
    ERROR_BAD_EXE_FORMAT = CodeWrapper(0x800700C1)
    ERROR_BAD_IMPERSONATION_LEVEL = CodeWrapper(0x80070542)
    ERROR_BAD_INHERITANCE_ACL = CodeWrapper(0x8007053C)
    ERROR_BAD_LENGTH = CodeWrapper(0x80070018)
    ERROR_BAD_LOGON_SESSION_STATE = CodeWrapper(0x80070555)
    ERROR_BAD_NETPATH = CodeWrapper(0x80070035)
    ERROR_BAD_NET_NAME = CodeWrapper(0x80070043)
    ERROR_BAD_NET_RESP = CodeWrapper(0x8007003A)
    ERROR_BAD_PATHNAME = CodeWrapper(0x800700A1)
    ERROR_BAD_PIPE = CodeWrapper(0x800700E6)
    ERROR_BAD_REM_ADAP = CodeWrapper(0x8007003C)
    ERROR_BAD_TOKEN_TYPE = CodeWrapper(0x80070545)
    ERROR_BAD_VALIDATION_CLASS = CodeWrapper(0x80070544)
    ERROR_BEGINNING_OF_MEDIA = CodeWrapper(0x8007044E)
    ERROR_BROKEN_PIPE = CodeWrapper(0x8007006D)
    ERROR_BUSY = CodeWrapper(0x8007008E)
    ERROR_BUS_RESET = CodeWrapper(0x80070457)
    ERROR_CANNOT_IMPERSONATE = CodeWrapper(0x80070558)
    ERROR_CANNOT_MAKE = CodeWrapper(0x80070052)
    ERROR_CANT_ACCESS_DOMAIN_INFO = CodeWrapper(0x80070547)
    ERROR_CANT_ACCESS_FILE = CodeWrapper(0x80070780)
    ERROR_CANT_DISABLE_MANDATORY = CodeWrapper(0x8007051E)
    ERROR_CANT_OPEN_ANONYMOUS = CodeWrapper(0x80070543)
    ERROR_CANT_RESOLVE_FILENAME = CodeWrapper(0x80070781)
    ERROR_CHILD_MUST_BE_VOLATILE = CodeWrapper(0x800703FD)
    ERROR_CLEANER_CARTRIDGE_INSTALLED = CodeWrapper(0x800710F4)
    ERROR_CLUSTER_INVALID_NETWORK = CodeWrapper(0x800713B9)
    ERROR_CLUSTER_INVALID_NETWORK_PROVIDER = CodeWrapper(0x800713B9)
    ERROR_CLUSTER_INVALID_NODE = CodeWrapper(0x800713AF)
    ERROR_CLUSTER_INVALID_REQUEST = CodeWrapper(0x800713B8)
    ERROR_CLUSTER_JOIN_IN_PROGRESS = CodeWrapper(0x800713B1)
    ERROR_CLUSTER_JOIN_NOT_IN_PROGRESS = CodeWrapper(0x800713BD)
    ERROR_CLUSTER_LOCAL_NODE_NOT_FOUND = CodeWrapper(0x800713B3)
    ERROR_CLUSTER_NETINTERFACE_EXISTS = CodeWrapper(0x800713B6)
    ERROR_CLUSTER_NETINTERFACE_NOT_FOUND = CodeWrapper(0x800713B7)
    ERROR_CLUSTER_NETWORK_ALREADY_OFFLINE = CodeWrapper(0x800713C8)
    ERROR_CLUSTER_NETWORK_ALREADY_ONLINE = CodeWrapper(0x800713C7)
    ERROR_CLUSTER_NETWORK_EXISTS = CodeWrapper(0x800713B4)
    ERROR_CLUSTER_NETWORK_NOT_FOUND = CodeWrapper(0x800713B5)
    ERROR_CLUSTER_NETWORK_NOT_INTERNAL = CodeWrapper(0x800713C4)
    ERROR_CLUSTER_NODE_ALREADY_DOWN = CodeWrapper(0x800713C6)
    ERROR_CLUSTER_NODE_ALREADY_MEMBER = CodeWrapper(0x800713C9)
    ERROR_CLUSTER_NODE_ALREADY_UP = CodeWrapper(0x800713C5)
    ERROR_CLUSTER_NODE_DOWN = CodeWrapper(0x800713BA)
    ERROR_CLUSTER_NODE_EXISTS = CodeWrapper(0x800713B0)
    ERROR_CLUSTER_NODE_NOT_FOUND = CodeWrapper(0x800713B2)
    ERROR_CLUSTER_NODE_NOT_MEMBER = CodeWrapper(0x800713BC)
    ERROR_CLUSTER_NODE_NOT_PAUSED = CodeWrapper(0x800713C2)
    ERROR_CLUSTER_NODE_PAUSED = CodeWrapper(0x800713CE)
    ERROR_CLUSTER_NODE_UNREACHABLE = CodeWrapper(0x800713BB)
    ERROR_CLUSTER_NODE_UP = CodeWrapper(0x800713C0)
    ERROR_CLUSTER_NO_SECURITY_CONTEXT = CodeWrapper(0x800713C3)
    ERROR_COMMITMENT_LIMIT = CodeWrapper(0x800705AF)
    ERROR_CONNECTION_ABORTED = CodeWrapper(0x800704D4)
    ERROR_CONNECTION_ACTIVE = CodeWrapper(0x800704CE)
    ERROR_CONNECTION_COUNT_LIMIT = CodeWrapper(0x800704D6)
    ERROR_CONNECTION_INVALID = CodeWrapper(0x800704CD)
    ERROR_CONNECTION_REFUSED = CodeWrapper(0x800704C9)
    ERROR_CONNECTION_UNAVAIL = CodeWrapper(0x800704B1)
    ERROR_CONTEXT_EXPIRED = CodeWrapper(0x8007078B)
    ERROR_COUNTER_TIMEOUT = CodeWrapper(0x80070461)
    ERROR_CRC = CodeWrapper(0x80070017)
    ERROR_CTX_BAD_VIDEO_MODE = CodeWrapper(0x80071B71)
    ERROR_CTX_CLIENT_LICENSE_IN_USE = CodeWrapper(0x80071B8C)
    ERROR_CTX_CLIENT_LICENSE_NOT_SET = CodeWrapper(0x80071B8D)
    ERROR_CTX_CLIENT_QUERY_TIMEOUT = CodeWrapper(0x80071B80)
    ERROR_CTX_CLOSE_PENDING = CodeWrapper(0x80071B5F)
    ERROR_CTX_CONSOLE_CONNECT = CodeWrapper(0x80071B82)
    ERROR_CTX_CONSOLE_DISCONNECT = CodeWrapper(0x80071B81)
    ERROR_CTX_GRAPHICS_INVALID = CodeWrapper(0x80071B7B)
    ERROR_CTX_INVALID_MODEMNAME = CodeWrapper(0x80071B62)
    ERROR_CTX_INVALID_PD = CodeWrapper(0x80071B5A)
    ERROR_CTX_INVALID_WD = CodeWrapper(0x80071B89)
    ERROR_CTX_LICENSE_CLIENT_INVALID = CodeWrapper(0x80071B8F)
    ERROR_CTX_LICENSE_EXPIRED = CodeWrapper(0x80071B90)
    ERROR_CTX_LICENSE_NOT_AVAILABLE = CodeWrapper(0x80071B8E)
    ERROR_CTX_MODEM_INF_NOT_FOUND = CodeWrapper(0x80071B61)
    ERROR_CTX_MODEM_RESPONSE_BUSY = CodeWrapper(0x80071B67)
    ERROR_CTX_MODEM_RESPONSE_ERROR = CodeWrapper(0x80071B63)
    ERROR_CTX_MODEM_RESPONSE_NO_CARRIER = CodeWrapper(0x80071B65)
    ERROR_CTX_MODEM_RESPONSE_NO_DIALTONE = CodeWrapper(0x80071B66)
    ERROR_CTX_MODEM_RESPONSE_TIMEOUT = CodeWrapper(0x80071B64)
    ERROR_CTX_MODEM_RESPONSE_VOICE = CodeWrapper(0x80071B68)
    ERROR_CTX_NOT_CONSOLE = CodeWrapper(0x80071B7E)
    ERROR_CTX_NO_OUTBUF = CodeWrapper(0x80071B60)
    ERROR_CTX_PD_NOT_FOUND = CodeWrapper(0x80071B5B)
    ERROR_CTX_SHADOW_DENIED = CodeWrapper(0x80071B84)
    ERROR_CTX_SHADOW_DISABLED = CodeWrapper(0x80071B8B)
    ERROR_CTX_SHADOW_ENDED_BY_MODE_CHANGE = CodeWrapper(0x80071B92)
    ERROR_CTX_SHADOW_INVALID = CodeWrapper(0x80071B8A)
    ERROR_CTX_SHADOW_NOT_RUNNING = CodeWrapper(0x80071B91)
    ERROR_CTX_TD_ERROR = CodeWrapper(0x80071B69)
    ERROR_CTX_WD_NOT_FOUND = CodeWrapper(0x80071B5C)
    ERROR_CTX_WINSTATION_ACCESS_DENIED = CodeWrapper(0x80071B85)
    ERROR_CTX_WINSTATION_ALREADY_EXISTS = CodeWrapper(0x80071B6F)
    ERROR_CTX_WINSTATION_BUSY = CodeWrapper(0x80071B70)
    ERROR_CTX_WINSTATION_NAME_INVALID = CodeWrapper(0x80071B59)
    ERROR_CTX_WINSTATION_NOT_FOUND = CodeWrapper(0x80071B6E)
    ERROR_CURRENT_DOMAIN_NOT_ALLOWED = CodeWrapper(0x80070577)
    ERROR_DECRYPTION_FAILED = CodeWrapper(0x80071771)
    ERROR_DESTINATION_ELEMENT_FULL = CodeWrapper(0x80070489)
    ERROR_DEVICE_DOOR_OPEN = CodeWrapper(0x8007048E)
    ERROR_DEVICE_IN_USE = CodeWrapper(0x80070964)
    ERROR_DEVICE_NOT_CONNECTED = CodeWrapper(0x8007048F)
    ERROR_DEVICE_NOT_PARTITIONED = CodeWrapper(0x80070453)
    ERROR_DEVICE_REINITIALIZATION_NEEDED = CodeWrapper(0x8007048C)
    ERROR_DEVICE_REMOVED = CodeWrapper(0x80070651)
    ERROR_DEVICE_REQUIRES_CLEANING = CodeWrapper(0x8007048D)
    ERROR_DEV_NOT_EXIST = CodeWrapper(0x80070037)
    ERROR_DIRECTORY = CodeWrapper(0x8007010B)
    ERROR_DIR_NOT_EMPTY = CodeWrapper(0x80070091)
    ERROR_DISK_CORRUPT = CodeWrapper(0x80070571)
    ERROR_DISK_FULL = CodeWrapper(0x80070070)
    ERROR_DISK_OPERATION_FAILED = CodeWrapper(0x80070467)
    ERROR_DISK_RECALIBRATE_FAILED = CodeWrapper(0x80070466)
    ERROR_DISK_RESET_FAILED = CodeWrapper(0x80070468)
    ERROR_DISK_TOO_FRAGMENTED = CodeWrapper(0x8007012E)
    ERROR_DLL_INIT_FAILED = CodeWrapper(0x80070270)
    ERROR_DOMAIN_CONTROLLER_NOT_FOUND = CodeWrapper(0x80070774)
    ERROR_DOMAIN_EXISTS = CodeWrapper(0x8007054C)
    ERROR_DOMAIN_LIMIT_EXCEEDED = CodeWrapper(0x8007054D)
    ERROR_DOMAIN_TRUST_INCONSISTENT = CodeWrapper(0x80070712)
    ERROR_DOWNGRADE_DETECTED = CodeWrapper(0x800704F1)
    ERROR_DRIVER_BLOCKED = CodeWrapper(0x800704FB)
    ERROR_DS_ADMIN_LIMIT_EXCEEDED = CodeWrapper(0x80072024)
    ERROR_DS_AG_CANT_HAVE_UNIVERSAL_MEMBER = CodeWrapper(0x80072182)
    ERROR_DS_ATTRIBUTE_OR_VALUE_EXISTS = CodeWrapper(0x8007200D)
    ERROR_DS_ATTRIBUTE_TYPE_UNDEFINED = CodeWrapper(0x8007200C)
    ERROR_DS_BUSY = CodeWrapper(0x8007200E)
    ERROR_DS_CANT_MOD_OBJ_CLASS = CodeWrapper(0x80072017)
    ERROR_DS_CANT_MOD_PRIMARYGROUPID = CodeWrapper(0x8007213A)
    ERROR_DS_CANT_ON_NON_LEAF = CodeWrapper(0x80072015)
    ERROR_DS_CANT_ON_RDN = CodeWrapper(0x80072016)
    ERROR_DS_CANT_START = CodeWrapper(0x80072153)
    ERROR_DS_CROSS_DOM_MOVE_ERROR = CodeWrapper(0x80072018)
    ERROR_DS_DS_REQUIRED = CodeWrapper(0x8007211E)
    ERROR_DS_GC_NOT_AVAILABLE = CodeWrapper(0x80072019)
    ERROR_DS_GC_REQUIRED = CodeWrapper(0x80072163)
    ERROR_DS_GLOBAL_CANT_HAVE_CROSSDOMAIN_MEMBER = CodeWrapper(0x80072147)
    ERROR_DS_GLOBAL_CANT_HAVE_LOCAL_MEMBER = CodeWrapper(0x80072144)
    ERROR_DS_GLOBAL_CANT_HAVE_UNIVERSAL_MEMBER = CodeWrapper(0x80072145)
    ERROR_DS_HAVE_PRIMARY_MEMBERS = CodeWrapper(0x80072149)
    ERROR_DS_INCORRECT_ROLE_OWNER = CodeWrapper(0x80072012)
    ERROR_DS_INIT_FAILURE = CodeWrapper(0x80072154)
    ERROR_DS_INIT_FAILURE_CONSOLE = CodeWrapper(0x80072171)
    ERROR_DS_INVALID_ATTRIBUTE_SYNTAX = CodeWrapper(0x8007200B)
    ERROR_DS_INVALID_GROUP_TYPE = CodeWrapper(0x80072141)
    ERROR_DS_LOCAL_CANT_HAVE_CROSSDOMAIN_LOCAL_MEMBER = CodeWrapper(0x80072148)
    ERROR_DS_LOCAL_MEMBER_OF_LOCAL_ONLY = CodeWrapper(0x80072164)
    ERROR_DS_MACHINE_ACCOUNT_CREATED_PRENT4 = CodeWrapper(0x8007217C)
    ERROR_DS_MACHINE_ACCOUNT_QUOTA_EXCEEDED = CodeWrapper(0x8007216D)
    ERROR_DS_MEMBERSHIP_EVALUATED_LOCALLY = CodeWrapper(0x80072009)
    ERROR_DS_NO_ATTRIBUTE_OR_VALUE = CodeWrapper(0x8007200A)
    ERROR_DS_NO_FPO_IN_UNIVERSAL_GROUPS = CodeWrapper(0x80072165)
    ERROR_DS_NO_MORE_RIDS = CodeWrapper(0x80072011)
    ERROR_DS_NO_NEST_GLOBALGROUP_IN_MIXEDDOMAIN = CodeWrapper(0x80072142)
    ERROR_DS_NO_NEST_LOCALGROUP_IN_MIXEDDOMAIN = CodeWrapper(0x80072143)
    ERROR_DS_NO_RIDS_ALLOCATED = CodeWrapper(0x80072010)
    ERROR_DS_OBJ_CLASS_VIOLATION = CodeWrapper(0x80072014)
    ERROR_DS_RIDMGR_INIT_ERROR = CodeWrapper(0x80072013)
    ERROR_DS_SAM_INIT_FAILURE = CodeWrapper(0x80072138)
    ERROR_DS_SAM_INIT_FAILURE_CONSOLE = CodeWrapper(0x80072172)
    ERROR_DS_SAM_NEED_BOOTKEY_FLOPPY = CodeWrapper(0x80072152)
    ERROR_DS_SAM_NEED_BOOTKEY_PASSWORD = CodeWrapper(0x80072151)
    ERROR_DS_SENSITIVE_GROUP_VIOLATION = CodeWrapper(0x80072139)
    ERROR_DS_SHUTTING_DOWN = CodeWrapper(0x800720AC)
    ERROR_DS_UNAVAILABLE = CodeWrapper(0x8007200F)
    ERROR_DS_UNIVERSAL_CANT_HAVE_LOCAL_MEMBER = CodeWrapper(0x80072146)
    ERROR_DUP_NAME = CodeWrapper(0x80070034)
    ERROR_EAS_NOT_SUPPORTED = CodeWrapper(0x8007011A)
    ERROR_EA_LIST_INCONSISTENT = CodeWrapper(0x800700FF)
    ERROR_EFS_ALG_BLOB_TOO_BIG = CodeWrapper(0x8007177D)
    ERROR_ENCRYPTION_FAILED = CodeWrapper(0x80071770)
    ERROR_END_OF_MEDIA = CodeWrapper(0x8007044C)
    ERROR_ENVVAR_NOT_FOUND = CodeWrapper(0x800700CB)
    ERROR_EOM_OVERFLOW = CodeWrapper(0x80070469)
    ERROR_EVENTLOG_CANT_START = CodeWrapper(0x800705DD)
    ERROR_EVENTLOG_FILE_CHANGED = CodeWrapper(0x800705DF)
    ERROR_EVENTLOG_FILE_CORRUPT = CodeWrapper(0x800705DC)
    ERROR_FILEMARK_DETECTED = CodeWrapper(0x8007044D)
    ERROR_FILENAME_EXCED_RANGE = CodeWrapper(0x800700CE)
    ERROR_FILE_CORRUPT = CodeWrapper(0x80070570)
    ERROR_FILE_ENCRYPTED = CodeWrapper(0x80071772)
    ERROR_FILE_EXISTS = CodeWrapper(0x80070050)
    ERROR_FILE_INVALID = CodeWrapper(0x800703EE)
    ERROR_FILE_NOT_ENCRYPTED = CodeWrapper(0x80071777)
    ERROR_FILE_NOT_FOUND = CodeWrapper(0x80070002)
    ERROR_FILE_OFFLINE = CodeWrapper(0x800710FE)
    ERROR_FLOPPY_BAD_REGISTERS = CodeWrapper(0x80070465)
    ERROR_FLOPPY_ID_MARK_NOT_FOUND = CodeWrapper(0x80070462)
    ERROR_FLOPPY_UNKNOWN_ERROR = CodeWrapper(0x80070464)
    ERROR_FLOPPY_WRONG_CYLINDER = CodeWrapper(0x80070463)
    ERROR_FULLSCREEN_MODE = CodeWrapper(0x800703EF)
    ERROR_GENERIC_NOT_MAPPED = CodeWrapper(0x80070550)
    ERROR_GEN_FAILURE = CodeWrapper(0x8007001F)
    ERROR_GRACEFUL_DISCONNECT = CodeWrapper(0x800704CA)
    ERROR_GROUP_EXISTS = CodeWrapper(0x80070526)
    ERROR_HANDLE_EOF = CodeWrapper(0x80070026)
    ERROR_HOST_DOWN = CodeWrapper(0x800704E8)
    ERROR_HOST_UNREACHABLE = CodeWrapper(0x800704D0)
    ERROR_ILLEGAL_ELEMENT_ADDRESS = CodeWrapper(0x8007048A)
    ERROR_ILL_FORMED_PASSWORD = CodeWrapper(0x8007052C)
    ERROR_INSUFFICIENT_BUFFER = CodeWrapper(0x8007007A)
    ERROR_INTERNAL_DB_CORRUPTION = CodeWrapper(0x8007054E)
    ERROR_INTERNAL_DB_ERROR = CodeWrapper(0x80070567)
    ERROR_INTERNAL_ERROR = CodeWrapper(0x8007054F)
    ERROR_INVALID_ACCOUNT_NAME = CodeWrapper(0x80070523)
    ERROR_INVALID_ACL = CodeWrapper(0x80070538)
    ERROR_INVALID_ADDRESS = CodeWrapper(0x800701E7)
    ERROR_INVALID_BLOCK_LENGTH = CodeWrapper(0x80070452)
    ERROR_INVALID_COMPUTERNAME = CodeWrapper(0x800704BA)
    ERROR_INVALID_DOMAIN_ROLE = CodeWrapper(0x8007054A)
    ERROR_INVALID_DOMAIN_STATE = CodeWrapper(0x80070549)
    ERROR_INVALID_EA_NAME = CodeWrapper(0x800700FE)
    ERROR_INVALID_FUNCTION = CodeWrapper(0x80070001)
    ERROR_INVALID_GROUP_ATTRIBUTES = CodeWrapper(0x80070541)
    ERROR_INVALID_HANDLE = CodeWrapper(0x80070006)
    ERROR_INVALID_ID_AUTHORITY = CodeWrapper(0x8007053F)
    ERROR_INVALID_IMPORT_OF_NON_DLL = CodeWrapper(0x800704FC)
    ERROR_INVALID_LEVEL = CodeWrapper(0x8007007C)
    ERROR_INVALID_LOGON_HOURS = CodeWrapper(0x80070530)
    ERROR_INVALID_LOGON_TYPE = CodeWrapper(0x80070557)
    ERROR_INVALID_MEMBER = CodeWrapper(0x8007056C)
    ERROR_INVALID_NAME = CodeWrapper(0x8007007B)
    ERROR_INVALID_NETNAME = CodeWrapper(0x800704BE)
    ERROR_INVALID_OPLOCK_PROTOCOL = CodeWrapper(0x8007012D)
    ERROR_INVALID_ORDINAL = CodeWrapper(0x800700B6)
    ERROR_INVALID_OWNER = CodeWrapper(0x8007051B)
    ERROR_INVALID_PARAMETER = CodeWrapper(0x80070057)
    ERROR_INVALID_PASSWORD = CodeWrapper(0x80070056)
    ERROR_INVALID_PRIMARY_GROUP = CodeWrapper(0x8007051C)
    ERROR_INVALID_REPARSE_DATA = CodeWrapper(0x80071128)
    ERROR_INVALID_SECURITY_DESCR = CodeWrapper(0x8007053A)
    ERROR_INVALID_SERVER_STATE = CodeWrapper(0x80070548)
    ERROR_INVALID_SID = CodeWrapper(0x80070539)
    ERROR_INVALID_SUB_AUTHORITY = CodeWrapper(0x80070537)
    ERROR_INVALID_THREAD_ID = CodeWrapper(0x800705A4)
    ERROR_INVALID_USER_BUFFER = CodeWrapper(0x800706F8)
    ERROR_INVALID_WORKSTATION = CodeWrapper(0x80070531)
    ERROR_IO_DEVICE = CodeWrapper(0x8007045D)
    ERROR_IO_PENDING = CodeWrapper(0x800703E5)
    ERROR_IRQ_BUSY = CodeWrapper(0x8007045F)
    ERROR_JOURNAL_DELETE_IN_PROGRESS = CodeWrapper(0x8007049A)
    ERROR_JOURNAL_ENTRY_DELETED = CodeWrapper(0x8007049D)
    ERROR_JOURNAL_NOT_ACTIVE = CodeWrapper(0x8007049B)
    ERROR_KEY_DELETED = CodeWrapper(0x800703FA)
    ERROR_KEY_HAS_CHILDREN = CodeWrapper(0x800703FC)
    ERROR_LABEL_TOO_LONG = CodeWrapper(0x8007009A)
    ERROR_LAST_ADMIN = CodeWrapper(0x8007052A)
    ERROR_LICENSE_QUOTA_EXCEEDED = CodeWrapper(0x80070573)
    ERROR_LM_CROSS_ENCRYPTION_REQUIRED = CodeWrapper(0x8007056E)
    ERROR_LOCAL_USER_SESSION_KEY = CodeWrapper(0x80070517)
    ERROR_LOCK_VIOLATION = CodeWrapper(0x80070021)
    ERROR_LOGIN_TIME_RESTRICTION = CodeWrapper(0x800704D7)
    ERROR_LOGIN_WKSTA_RESTRICTION = CodeWrapper(0x800704D8)
    ERROR_LOGON_FAILURE = CodeWrapper(0x8007052E)
    ERROR_LOGON_NOT_GRANTED = CodeWrapper(0x80070564)
    ERROR_LOGON_SESSION_COLLISION = CodeWrapper(0x80070556)
    ERROR_LOGON_SESSION_EXISTS = CodeWrapper(0x80070553)
    ERROR_LOGON_TYPE_NOT_GRANTED = CodeWrapper(0x80070569)
    ERROR_LOG_FILE_FULL = CodeWrapper(0x800705DE)
    ERROR_LUIDS_EXHAUSTED = CodeWrapper(0x80070536)
    ERROR_MAGAZINE_NOT_PRESENT = CodeWrapper(0x8007048B)
    ERROR_MAPPED_ALIGNMENT = CodeWrapper(0x8007046C)
    ERROR_MEDIA_CHANGED = CodeWrapper(0x80070456)
    ERROR_MEMBERS_PRIMARY_GROUP = CodeWrapper(0x8007055E)
    ERROR_MEMBER_IN_ALIAS = CodeWrapper(0x80070562)
    ERROR_MEMBER_IN_GROUP = CodeWrapper(0x80070528)
    ERROR_MEMBER_NOT_IN_ALIAS = CodeWrapper(0x80070561)
    ERROR_MEMBER_NOT_IN_GROUP = CodeWrapper(0x80070529)
    ERROR_MOD_NOT_FOUND = CodeWrapper(0x8007007E)
    ERROR_MORE_DATA = CodeWrapper(0x800700EA)
    ERROR_MORE_WRITES = CodeWrapper(0x80070460)
    ERROR_MR_MID_NOT_FOUND = CodeWrapper(0x8007013D)
    ERROR_MUTUAL_AUTH_FAILED = CodeWrapper(0x80070575)
    ERROR_NETLOGON_NOT_STARTED = CodeWrapper(0x80070700)
    ERROR_NETNAME_DELETED = CodeWrapper(0x80070040)
    ERROR_NETWORK_ACCESS_DENIED = CodeWrapper(0x80070041)
    ERROR_NETWORK_BUSY = CodeWrapper(0x80070036)
    ERROR_NETWORK_UNREACHABLE = CodeWrapper(0x800704CF)
    ERROR_NET_WRITE_FAULT = CodeWrapper(0x80070058)
    ERROR_NOACCESS = CodeWrapper(0x800703E6)
    ERROR_NOLOGON_INTERDOMAIN_TRUST_ACCOUNT = CodeWrapper(0x8007070F)
    ERROR_NOLOGON_SERVER_TRUST_ACCOUNT = CodeWrapper(0x80070711)
    ERROR_NOLOGON_WORKSTATION_TRUST_ACCOUNT = CodeWrapper(0x80070710)
    ERROR_NONE_MAPPED = CodeWrapper(0x80070534)
    ERROR_NOTIFY_ENUM_DIR = CodeWrapper(0x800703FE)
    ERROR_NOT_ALL_ASSIGNED = CodeWrapper(0x80070514)
    ERROR_NOT_A_REPARSE_POINT = CodeWrapper(0x80071126)
    ERROR_NOT_ENOUGH_MEMORY = CodeWrapper(0x80070008)
    ERROR_NOT_ENOUGH_QUOTA = CodeWrapper(0x80070718)
    ERROR_NOT_ENOUGH_SERVER_MEMORY = CodeWrapper(0x8007046A)
    ERROR_NOT_EXPORT_FORMAT = CodeWrapper(0x80071778)
    ERROR_NOT_FOUND = CodeWrapper(0x80070490)
    ERROR_NOT_LOCKED = CodeWrapper(0x8007009E)
    ERROR_NOT_LOGON_PROCESS = CodeWrapper(0x80070552)
    ERROR_NOT_OWNER = CodeWrapper(0x80070120)
    ERROR_NOT_READY = CodeWrapper(0x80070015)
    ERROR_NOT_REGISTRY_FILE = CodeWrapper(0x800703F9)
    ERROR_NOT_SAME_DEVICE = CodeWrapper(0x80070011)
    ERROR_NOT_SUPPORTED = CodeWrapper(0x80070032)
    ERROR_NOT_SUPPORTED_ON_SBS = CodeWrapper(0x800704E6)
    ERROR_NO_BROWSER_SERVERS_FOUND = CodeWrapper(0x800717E6)
    ERROR_NO_DATA = CodeWrapper(0x800700E8)
    ERROR_NO_DATA_DETECTED = CodeWrapper(0x80070450)
    ERROR_NO_IMPERSONATION_TOKEN = CodeWrapper(0x8007051D)
    ERROR_NO_INHERITANCE = CodeWrapper(0x8007056F)
    ERROR_NO_LOGON_SERVERS = CodeWrapper(0x8007051F)
    ERROR_NO_LOG_SPACE = CodeWrapper(0x800703FB)
    ERROR_NO_MATCH = CodeWrapper(0x80070491)
    ERROR_NO_MEDIA_IN_DRIVE = CodeWrapper(0x80070458)
    ERROR_NO_MORE_FILES = CodeWrapper(0x80070012)
    ERROR_NO_MORE_ITEMS = CodeWrapper(0x80070103)
    ERROR_NO_QUOTAS_FOR_ACCOUNT = CodeWrapper(0x80070516)
    ERROR_NO_SECURITY_ON_OBJECT = CodeWrapper(0x80070546)
    ERROR_NO_SPOOL_SPACE = CodeWrapper(0x8007003E)
    ERROR_NO_SUCH_ALIAS = CodeWrapper(0x80070560)
    ERROR_NO_SUCH_DOMAIN = CodeWrapper(0x8007054B)
    ERROR_NO_SUCH_GROUP = CodeWrapper(0x80070527)
    ERROR_NO_SUCH_LOGON_SESSION = CodeWrapper(0x80070520)
    ERROR_NO_SUCH_MEMBER = CodeWrapper(0x8007056B)
    ERROR_NO_SUCH_PACKAGE = CodeWrapper(0x80070554)
    ERROR_NO_SUCH_PRIVILEGE = CodeWrapper(0x80070521)
    ERROR_NO_SUCH_USER = CodeWrapper(0x80070525)
    ERROR_NO_SYSTEM_RESOURCES = CodeWrapper(0x800705AA)
    ERROR_NO_TOKEN = CodeWrapper(0x800703F0)
    ERROR_NO_TRACKING_SERVICE = CodeWrapper(0x80070494)
    ERROR_NO_TRUST_LSA_SECRET = CodeWrapper(0x800706FA)
    ERROR_NO_TRUST_SAM_ACCOUNT = CodeWrapper(0x800706FB)
    ERROR_NO_UNICODE_TRANSLATION = CodeWrapper(0x80070459)
    ERROR_NO_USER_SESSION_KEY = CodeWrapper(0x80070572)
    ERROR_NT_CROSS_ENCRYPTION_REQUIRED = CodeWrapper(0x8007056A)
    ERROR_NULL_LM_PASSWORD = CodeWrapper(0x80070518)
    ERROR_ONLY_IF_CONNECTED = CodeWrapper(0x800704E3)
    ERROR_OPEN_FILES = CodeWrapper(0x80070961)
    ERROR_OPERATION_ABORTED = CodeWrapper(0x800703E3)
    ERROR_OPLOCK_NOT_GRANTED = CodeWrapper(0x8007012C)
    ERROR_OUTOFMEMORY = CodeWrapper(0x8007000E)
    ERROR_OUT_OF_PAPER = CodeWrapper(0x8007001C)
    ERROR_PAGEFILE_QUOTA = CodeWrapper(0x80070237)
    ERROR_PARTIAL_COPY = CodeWrapper(0x8007012B)
    ERROR_PARTITION_FAILURE = CodeWrapper(0x80070451)
    ERROR_PASSWORD_EXPIRED = CodeWrapper(0x80070532)
    ERROR_PASSWORD_MUST_CHANGE = CodeWrapper(0x80070773)
    ERROR_PASSWORD_RESTRICTION = CodeWrapper(0x8007052D)
    ERROR_PATH_NOT_FOUND = CodeWrapper(0x80070003)
    ERROR_PIPE_BUSY = CodeWrapper(0x800700E7)
    ERROR_PIPE_CONNECTED = CodeWrapper(0x80070217)
    ERROR_PIPE_LISTENING = CodeWrapper(0x80070218)
    ERROR_PIPE_NOT_CONNECTED = CodeWrapper(0x800700E9)
    ERROR_PKINIT_FAILURE = CodeWrapper(0x800704EF)
    ERROR_POLICY_OBJECT_NOT_FOUND = CodeWrapper(0x8007201B)
    ERROR_POLICY_ONLY_IN_DS = CodeWrapper(0x8007201C)
    ERROR_PORT_UNREACHABLE = CodeWrapper(0x800704D2)
    ERROR_POSSIBLE_DEADLOCK = CodeWrapper(0x8007046B)
    ERROR_PRINTQ_FULL = CodeWrapper(0x8007003D)
    ERROR_PRINT_CANCELLED = CodeWrapper(0x8007003F)
    ERROR_PRIVILEGE_NOT_HELD = CodeWrapper(0x80070522)
    ERROR_PROC_NOT_FOUND = CodeWrapper(0x8007007F)
    ERROR_PROTOCOL_UNREACHABLE = CodeWrapper(0x800704D1)
    ERROR_REDIR_PAUSED = CodeWrapper(0x80070048)
    ERROR_REGISTRY_IO_FAILED = CodeWrapper(0x800703F8)
    ERROR_REGISTRY_RECOVERED = CodeWrapper(0x800703F6)
    ERROR_REG_NAT_CONSUMPTION = CodeWrapper(0x800704ED)
    ERROR_REMOTE_SESSION_LIMIT_EXCEEDED = CodeWrapper(0x800704C4)
    ERROR_REMOTE_STORAGE_MEDIA_ERROR = CodeWrapper(0x80071100)
    ERROR_REMOTE_STORAGE_NOT_ACTIVE = CodeWrapper(0x800710FF)
    ERROR_REM_NOT_LIST = CodeWrapper(0x80070033)
    ERROR_REPARSE_ATTRIBUTE_CONFLICT = CodeWrapper(0x80071127)
    ERROR_REPARSE_TAG_INVALID = CodeWrapper(0x80071129)
    ERROR_REPARSE_TAG_MISMATCH = CodeWrapper(0x8007112A)
    ERROR_REQUEST_ABORTED = CodeWrapper(0x800704D3)
    ERROR_REQ_NOT_ACCEP = CodeWrapper(0x80070047)
    ERROR_RESOURCE_DATA_NOT_FOUND = CodeWrapper(0x80070714)
    ERROR_RESOURCE_LANG_NOT_FOUND = CodeWrapper(0x80070717)
    ERROR_RESOURCE_NAME_NOT_FOUND = CodeWrapper(0x80070716)
    ERROR_RESOURCE_TYPE_NOT_FOUND = CodeWrapper(0x80070715)
    ERROR_RETRY = CodeWrapper(0x800704D5)
    ERROR_REVISION_MISMATCH = CodeWrapper(0x8007051A)
    ERROR_RXACT_COMMIT_FAILURE = CodeWrapper(0x8007055A)
    ERROR_RXACT_INVALID_STATE = CodeWrapper(0x80070559)
    ERROR_SAM_INIT_FAILURE = CodeWrapper(0x8007215D)
    ERROR_SECRET_TOO_LONG = CodeWrapper(0x80070566)
    ERROR_SECTOR_NOT_FOUND = CodeWrapper(0x8007001B)
    ERROR_SEM_TIMEOUT = CodeWrapper(0x80070079)
    ERROR_SERIAL_NO_DEVICE = CodeWrapper(0x8007045E)
    ERROR_SERVER_DISABLED = CodeWrapper(0x8007053D)
    ERROR_SERVER_NOT_DISABLED = CodeWrapper(0x8007053E)
    ERROR_SERVER_SHUTDOWN_IN_PROGRESS = CodeWrapper(0x800704E7)
    ERROR_SERVICE_ALREADY_RUNNING = CodeWrapper(0x80070420)
    ERROR_SERVICE_DISABLED = CodeWrapper(0x80070422)
    ERROR_SESSION_CREDENTIAL_CONFLICT = CodeWrapper(0x800704C3)
    ERROR_SETMARK_DETECTED = CodeWrapper(0x8007044F)
    ERROR_SET_NOT_FOUND = CodeWrapper(0x80070492)
    ERROR_SHARED_POLICY = CodeWrapper(0x8007201A)
    ERROR_SHARING_PAUSED = CodeWrapper(0x80070046)
    ERROR_SHARING_VIOLATION = CodeWrapper(0x80070020)
    ERROR_SHUTDOWN_IN_PROGRESS = CodeWrapper(0x8007045B)
    ERROR_SIGNAL_REFUSED = CodeWrapper(0x8007009C)
    ERROR_SMARTCARD_SUBSYSTEM_FAILURE = CodeWrapper(0x800704F0)
    ERROR_SOME_NOT_MAPPED = CodeWrapper(0x80070515)
    ERROR_SOURCE_ELEMENT_EMPTY = CodeWrapper(0x80070488)
    ERROR_SPECIAL_ACCOUNT = CodeWrapper(0x8007055B)
    ERROR_SPECIAL_GROUP = CodeWrapper(0x8007055C)
    ERROR_SPECIAL_USER = CodeWrapper(0x8007055D)
    ERROR_STACK_OVERFLOW = CodeWrapper(0x80070257)
    ERROR_SWAPERROR = CodeWrapper(0x800703E7)
    ERROR_SXS_ACTIVATION_CONTEXT_DISABLED = CodeWrapper(0x800736B6)
    ERROR_SXS_ASSEMBLY_NOT_FOUND = CodeWrapper(0x800736B3)
    ERROR_SXS_CANT_GEN_ACTCTX = CodeWrapper(0x800736B1)
    ERROR_SXS_INVALID_ACTCTXDATA_FORMAT = CodeWrapper(0x800736B2)
    ERROR_SXS_KEY_NOT_FOUND = CodeWrapper(0x800736B7)
    ERROR_SXS_MANIFEST_FORMAT_ERROR = CodeWrapper(0x800736B4)
    ERROR_SXS_MANIFEST_PARSE_ERROR = CodeWrapper(0x800736B5)
    ERROR_SXS_PROCESS_DEFAULT_ALREADY_SET = CodeWrapper(0x800736BB)
    ERROR_SXS_SECTION_NOT_FOUND = CodeWrapper(0x800736B0)
    ERROR_SXS_THREAD_QUERIES_DISABLED = CodeWrapper(0x800736BA)
    ERROR_SXS_WRONG_SECTION_TYPE = CodeWrapper(0x800736B9)
    ERROR_TIME_SKEW = CodeWrapper(0x80070576)
    ERROR_TOKEN_ALREADY_IN_USE = CodeWrapper(0x8007055F)
    ERROR_TOO_MANY_CMDS = CodeWrapper(0x80070038)
    ERROR_TOO_MANY_CONTEXT_IDS = CodeWrapper(0x80070568)
    ERROR_TOO_MANY_LINKS = CodeWrapper(0x80070476)
    ERROR_TOO_MANY_LUIDS_REQUESTED = CodeWrapper(0x80070535)
    ERROR_TOO_MANY_NAMES = CodeWrapper(0x80070044)
    ERROR_TOO_MANY_OPEN_FILES = CodeWrapper(0x80070004)
    ERROR_TOO_MANY_POSTS = CodeWrapper(0x8007012A)
    ERROR_TOO_MANY_SECRETS = CodeWrapper(0x80070565)
    ERROR_TOO_MANY_SESS = CodeWrapper(0x80070045)
    ERROR_TOO_MANY_SIDS = CodeWrapper(0x8007056D)
    ERROR_TRANSPORT_FULL = CodeWrapper(0x800710E8)
    ERROR_TRUSTED_DOMAIN_FAILURE = CodeWrapper(0x800706FC)
    ERROR_TRUSTED_RELATIONSHIP_FAILURE = CodeWrapper(0x800706FD)
    ERROR_TRUST_FAILURE = CodeWrapper(0x800706FE)
    ERROR_UNABLE_TO_LOCK_MEDIA = CodeWrapper(0x80070454)
    ERROR_UNABLE_TO_UNLOAD_MEDIA = CodeWrapper(0x80070455)
    ERROR_UNEXP_NET_ERR = CodeWrapper(0x8007003B)
    ERROR_UNKNOWN_REVISION = CodeWrapper(0x80070519)
    ERROR_UNRECOGNIZED_MEDIA = CodeWrapper(0x800706F9)
    ERROR_UNRECOGNIZED_VOLUME = CodeWrapper(0x800703ED)
    ERROR_USER_EXISTS = CodeWrapper(0x80070524)
    ERROR_USER_MAPPED_FILE = CodeWrapper(0x800704C8)
    ERROR_VC_DISCONNECTED = CodeWrapper(0x800700F0)
    ERROR_WMI_ALREADY_DISABLED = CodeWrapper(0x80071074)
    ERROR_WMI_ALREADY_ENABLED = CodeWrapper(0x8007106E)
    ERROR_WMI_GUID_DISCONNECTED = CodeWrapper(0x8007106F)
    ERROR_WMI_GUID_NOT_FOUND = CodeWrapper(0x80071068)
    ERROR_WMI_INSTANCE_NOT_FOUND = CodeWrapper(0x80071069)
    ERROR_WMI_ITEMID_NOT_FOUND = CodeWrapper(0x8007106A)
    ERROR_WMI_READ_ONLY = CodeWrapper(0x80071075)
    ERROR_WMI_SET_FAILURE = CodeWrapper(0x80071076)
    ERROR_WMI_TRY_AGAIN = CodeWrapper(0x8007106B)
    ERROR_WORKING_SET_QUOTA = CodeWrapper(0x800705AD)
    ERROR_WRITE_PROTECT = CodeWrapper(0x80070013)
    ERROR_WRONG_DISK = CodeWrapper(0x80070022)
    ERROR_WRONG_TARGET_NAME = CodeWrapper(0x80070574)
    NO_ERROR = CodeWrapper(0xC00D0FD0)
    NTE_BAD_KEYSET = CodeWrapper(0x80090016)
    NTE_NO_KEY = CodeWrapper(0x8009000D)
    RPC_S_ADDRESS_ERROR = CodeWrapper(0x800706E8)
    RPC_S_ALREADY_LISTENING = CodeWrapper(0x800706B1)
    RPC_S_ALREADY_REGISTERED = CodeWrapper(0x800706AF)
    RPC_S_BINDING_HAS_NO_AUTH = CodeWrapper(0x800706D2)
    RPC_S_BINDING_INCOMPLETE = CodeWrapper(0x8007071B)
    RPC_S_CALL_CANCELLED = CodeWrapper(0x8007071A)
    RPC_S_CALL_FAILED = CodeWrapper(0x800706BE)
    RPC_S_CALL_FAILED_DNE = CodeWrapper(0x800706BF)
    RPC_S_CALL_IN_PROGRESS = CodeWrapper(0x800706FF)
    RPC_S_CANNOT_SUPPORT = CodeWrapper(0x800706E4)
    RPC_S_CANT_CREATE_ENDPOINT = CodeWrapper(0x800706B8)
    RPC_S_COMM_FAILURE = CodeWrapper(0x8007071C)
    RPC_S_DUPLICATE_ENDPOINT = CodeWrapper(0x800706CC)
    RPC_S_ENTRY_ALREADY_EXISTS = CodeWrapper(0x800706E0)
    RPC_S_ENTRY_NOT_FOUND = CodeWrapper(0x800706E1)
    RPC_S_FP_DIV_ZERO = CodeWrapper(0x800706E9)
    RPC_S_FP_OVERFLOW = CodeWrapper(0x800706EB)
    RPC_S_FP_UNDERFLOW = CodeWrapper(0x800706EA)
    RPC_S_GROUP_MEMBER_NOT_FOUND = CodeWrapper(0x8007076A)
    RPC_S_INCOMPLETE_NAME = CodeWrapper(0x800706DB)
    RPC_S_INTERFACE_NOT_FOUND = CodeWrapper(0x800706DF)
    RPC_S_INTERNAL_ERROR = CodeWrapper(0x800706E6)
    RPC_S_INVALID_ASYNC_CALL = CodeWrapper(0x8007077B)
    RPC_S_INVALID_ASYNC_HANDLE = CodeWrapper(0x8007077A)
    RPC_S_INVALID_AUTH_IDENTITY = CodeWrapper(0x800706D5)
    RPC_S_INVALID_BOUND = CodeWrapper(0x800706C6)
    RPC_S_INVALID_ENDPOINT_FORMAT = CodeWrapper(0x800706AA)
    RPC_S_INVALID_NAF_ID = CodeWrapper(0x800706E3)
    RPC_S_INVALID_NAME_SYNTAX = CodeWrapper(0x800706C8)
    RPC_S_INVALID_NETWORK_OPTIONS = CodeWrapper(0x800706BC)
    RPC_S_INVALID_NET_ADDR = CodeWrapper(0x800706AB)
    RPC_S_INVALID_OBJECT = CodeWrapper(0x8007076C)
    RPC_S_INVALID_RPC_PROTSEQ = CodeWrapper(0x800706A8)
    RPC_S_INVALID_STRING_BINDING = CodeWrapper(0x800706A4)
    RPC_S_INVALID_STRING_UUID = CodeWrapper(0x800706A9)
    RPC_S_INVALID_TAG = CodeWrapper(0x800706C5)
    RPC_S_INVALID_TIMEOUT = CodeWrapper(0x800706AD)
    RPC_S_INVALID_VERS_OPTION = CodeWrapper(0x800706DC)
    RPC_S_MAX_CALLS_TOO_SMALL = CodeWrapper(0x800706CE)
    RPC_S_NAME_SERVICE_UNAVAILABLE = CodeWrapper(0x800706E2)
    RPC_S_NOTHING_TO_EXPORT = CodeWrapper(0x800706DA)
    RPC_S_NOT_ALL_OBJS_UNEXPORTED = CodeWrapper(0x800706DE)
    RPC_S_NOT_CANCELLED = CodeWrapper(0x80070722)
    RPC_S_NOT_LISTENING = CodeWrapper(0x800706B3)
    RPC_S_NOT_RPC_ERROR = CodeWrapper(0x8007071F)
    RPC_S_NO_BINDINGS = CodeWrapper(0x800706B6)
    RPC_S_NO_CALL_ACTIVE = CodeWrapper(0x800706BD)
    RPC_S_NO_CONTEXT_AVAILABLE = CodeWrapper(0x800706E5)
    RPC_S_NO_ENDPOINT_FOUND = CodeWrapper(0x800706AC)
    RPC_S_NO_ENTRY_NAME = CodeWrapper(0x800706C7)
    RPC_S_NO_INTERFACES = CodeWrapper(0x80070719)
    RPC_S_NO_MORE_BINDINGS = CodeWrapper(0x8007070E)
    RPC_S_NO_MORE_MEMBERS = CodeWrapper(0x800706DD)
    RPC_S_NO_PRINC_NAME = CodeWrapper(0x8007071E)
    RPC_S_NO_PROTSEQS = CodeWrapper(0x800706B2)
    RPC_S_NO_PROTSEQS_REGISTERED = CodeWrapper(0x800706B2)
    RPC_S_OBJECT_NOT_FOUND = CodeWrapper(0x800706AE)
    RPC_S_OUT_OF_RESOURCES = CodeWrapper(0x800706B9)
    RPC_S_PROCNUM_OUT_OF_RANGE = CodeWrapper(0x800706D1)
    RPC_S_PROTOCOL_ERROR = CodeWrapper(0x800706C0)
    RPC_S_PROTSEQ_NOT_FOUND = CodeWrapper(0x800706D0)
    RPC_S_PROTSEQ_NOT_SUPPORTED = CodeWrapper(0x800706A7)
    RPC_S_SEC_PKG_ERROR = CodeWrapper(0x80070721)
    RPC_S_SEND_INCOMPLETE = CodeWrapper(0x80070779)
    RPC_S_SERVER_TOO_BUSY = CodeWrapper(0x800706BB)
    RPC_S_SERVER_UNAVAILABLE = CodeWrapper(0x800706BA)
    RPC_S_STRING_TOO_LONG = CodeWrapper(0x800706CF)
    RPC_S_TYPE_ALREADY_REGISTERED = CodeWrapper(0x800706B0)
    RPC_S_UNKNOWN_AUTHN_LEVEL = CodeWrapper(0x800706D4)
    RPC_S_UNKNOWN_AUTHN_SERVICE = CodeWrapper(0x800706D3)
    RPC_S_UNKNOWN_AUTHN_TYPE = CodeWrapper(0x800706CD)
    RPC_S_UNKNOWN_AUTHZ_SERVICE = CodeWrapper(0x800706D6)
    RPC_S_UNKNOWN_IF = CodeWrapper(0x800706B5)
    RPC_S_UNKNOWN_MGR_TYPE = CodeWrapper(0x800706B4)
    RPC_S_UNSUPPORTED_AUTHN_LEVEL = CodeWrapper(0x8007071D)
    RPC_S_UNSUPPORTED_NAME_SYNTAX = CodeWrapper(0x800706C9)
    RPC_S_UNSUPPORTED_TRANS_SYN = CodeWrapper(0x800706C2)
    RPC_S_UNSUPPORTED_TYPE = CodeWrapper(0x800706C4)
    RPC_S_UUID_LOCAL_ONLY = CodeWrapper(0x80070720)
    RPC_S_UUID_NO_ADDRESS = CodeWrapper(0x800706CB)
    RPC_S_WRONG_KIND_OF_BINDING = CodeWrapper(0x800706A5)
    RPC_S_ZERO_DIVIDE = CodeWrapper(0x800706E7)
    RPC_X_BAD_STUB_DATA = CodeWrapper(0x800706F7)
    RPC_X_BYTE_COUNT_TOO_SMALL = CodeWrapper(0x800706F6)
    RPC_X_ENUM_VALUE_OUT_OF_RANGE = CodeWrapper(0x800706F5)
    RPC_X_INVALID_ES_ACTION = CodeWrapper(0x80070723)
    RPC_X_INVALID_PIPE_OBJECT = CodeWrapper(0x80070726)
    RPC_X_NO_MORE_ENTRIES = CodeWrapper(0x800706EC)
    RPC_X_NULL_REF_POINTER = CodeWrapper(0x800706F4)
    RPC_X_PIPE_CLOSED = CodeWrapper(0x8007077C)
    RPC_X_PIPE_DISCIPLINE_ERROR = CodeWrapper(0x8007077D)
    RPC_X_PIPE_EMPTY = CodeWrapper(0x8007077E)
    RPC_X_SS_CANNOT_GET_CALL_HANDLE = CodeWrapper(0x800706F3)
    RPC_X_SS_CHAR_TRANS_OPEN_FAIL = CodeWrapper(0x800706ED)
    RPC_X_SS_CHAR_TRANS_SHORT_FILE = CodeWrapper(0x800706EE)
    RPC_X_SS_CONTEXT_DAMAGED = CodeWrapper(0x800706F1)
    RPC_X_SS_HANDLES_MISMATCH = CodeWrapper(0x800706F2)
    RPC_X_WRONG_ES_VERSION = CodeWrapper(0x80070724)
    RPC_X_WRONG_PIPE_VERSION = CodeWrapper(0x80070728)
    RPC_X_WRONG_STUB_VERSION = CodeWrapper(0x80070725)
    SCARD_E_COMM_DATA_LOST = CodeWrapper(0x8010002F)
    SCARD_E_NO_SMARTCARD = CodeWrapper(0x8010000C)
    SCARD_E_NO_SUCH_CERTIFICATE = CodeWrapper(0x8010002C)
    SCARD_W_CARD_NOT_AUTHENTICATED = CodeWrapper(0x8010006F)
    SCARD_W_CHV_BLOCKED = CodeWrapper(0x8010006C)
    SCARD_W_WRONG_CHV = CodeWrapper(0x8010006B)
    SEC_E_BAD_BINDINGS = CodeWrapper(0x80090346)
    SEC_E_CRYPTO_SYSTEM_INVALID = CodeWrapper(0x80090337)
    SEC_E_ISSUING_CA_UNTRUSTED = CodeWrapper(0x80090352)
    SEC_E_KDC_INVALID_REQUEST = CodeWrapper(0x80090340)
    SEC_E_KDC_UNABLE_TO_REFER = CodeWrapper(0x80090341)
    SEC_E_KDC_UNKNOWN_ETYPE = CodeWrapper(0x80090342)
    SEC_E_MAX_REFERRALS_EXCEEDED = CodeWrapper(0x80090338)
    SEC_E_MUST_BE_KDC = CodeWrapper(0x80090339)
    SEC_E_NO_IP_ADDRESSES = CodeWrapper(0x80090335)
    SEC_E_NO_KERB_KEY = CodeWrapper(0x80090348)
    SEC_E_NO_PA_DATA = CodeWrapper(0x8009033C)
    SEC_E_NO_TGT_REPLY = CodeWrapper(0x80090334)
    SEC_E_PKINIT_CLIENT_FAILURE = CodeWrapper(0x80090354)
    SEC_E_PKINIT_NAME_MISMATCH = CodeWrapper(0x8009033D)
    SEC_E_REVOCATION_OFFLINE_C = CodeWrapper(0x80090353)
    SEC_E_SMARTCARD_CERT_EXPIRED = CodeWrapper(0x80090355)
    SEC_E_SMARTCARD_CERT_REVOKED = CodeWrapper(0x80090351)
    SEC_E_SMARTCARD_LOGON_REQUIRED = CodeWrapper(0x8009033E)
    SEC_E_STRONG_CRYPTO_NOT_SUPPORTED = CodeWrapper(0x8009033A)
    SEC_E_TOO_MANY_PRINCIPALS = CodeWrapper(0x8009033B)
    SEC_E_UNFINISHED_CONTEXT_DELETED = CodeWrapper(0x80090333)
    SEC_E_UNSUPPORTED_PREAUTH = CodeWrapper(0x80090343)
    SEC_E_WRONG_CREDENTIAL_HANDLE = CodeWrapper(0x80090336)
    STATUS_DUPLICATE_OBJECTID = CodeWrapper(0xC000022A)
    STATUS_OBJECTID_EXISTS = CodeWrapper(0xC000022B)
    STG_E_CSS_AUTHENTICATION_FAILURE = CodeWrapper(0x80030306)
    STG_E_CSS_KEY_NOT_ESTABLISHED = CodeWrapper(0x80030308)
    STG_E_CSS_KEY_NOT_PRESENT = CodeWrapper(0x80030307)
    STG_E_CSS_REGION_MISMATCH = CodeWrapper(0x8003030A)
    STG_E_CSS_SCRAMBLED_SECTOR = CodeWrapper(0x80030309)
    STG_E_RESETS_EXHAUSTED = CodeWrapper(0x8003030B)
    STG_E_STATUS_COPY_PROTECTION_FAILURE = CodeWrapper(0x80030305)
    ERROR_SUCCESS = CodeWrapper(0x00000000)
    INVALID_FILE_ATTRIBUTES = CodeWrapper(-0x00000001)
    INVALID_HANDLE_VALUE = CodeWrapper(-0x00000001)
    INVALID_FILE_SIZE = CodeWrapper(-0x00000001)

    # noinspection PyUnusedLocal
    def make_exception(code: CodeWrapper) -> CodeException:
        pass

    # noinspection PyUnusedLocal
    def add_code(name: str, value: int, docstring: str) -> CodeWrapper:
        pass

    all_codes: list
