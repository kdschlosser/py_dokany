
from .dokan_h import ENUM


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

#: The caller can perform a wait operation on the object.
SYNCHRONIZE = 0x00100000

#: Standard specific rights that correspond to GENERIC_ALL. This includes DELETE, but not SYNCHRONIZE.
STANDARD_RIGHTS_REQUIRED = 0x000F0000

#: Standard specific rights that correspond to GENERIC_READ
STANDARD_RIGHTS_READ = READ_CONTROL

#: Standard specific rights that correspond to GENERIC_WRITE
STANDARD_RIGHTS_WRITE = READ_CONTROL

#: Standard specific rights that correspond to GENERIC_EXECUTE
STANDARD_RIGHTS_EXECUTE = READ_CONTROL

#: All standard access rights.
STANDARD_RIGHTS_ALL = 0x001F0000

FILE_FLAG_WRITE_THROUGH = 0x80000000
FILE_FLAG_OVERLAPPED = 0x40000000
FILE_FLAG_NO_BUFFERING = 0x20000000
FILE_FLAG_RANDOM_ACCESS = 0x10000000
FILE_FLAG_SEQUENTIAL_SCAN = 0x08000000
FILE_FLAG_DELETE_ON_CLOSE = 0x04000000
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_POSIX_SEMANTICS = 0x01000000
FILE_FLAG_SESSION_AWARE = 0x00800000
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FILE_FLAG_OPEN_NO_RECALL = 0x00100000
FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000


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

SECURITY_ANONYMOUS = SecurityAnonymous << 16
SECURITY_IDENTIFICATION = SecurityIdentification << 16
SECURITY_IMPERSONATION = SecurityImpersonation << 16
SECURITY_DELEGATION = SecurityDelegation << 16

SECURITY_CONTEXT_TRACKING = 0x00040000
SECURITY_EFFECTIVE_ONLY = 0x00080000

SECURITY_SQOS_PRESENT = 0x00100000


FILE_CASE_SENSITIVE_SEARCH = 0x00000001
FILE_CASE_PRESERVED_NAMES = 0x00000002
FILE_DAX_VOLUME = 0x20000000
FILE_FILE_COMPRESSION = 0x00000010
FILE_NAMED_STREAMS = 0x00040000
FILE_PERSISTENT_ACLS = 0x00000008
FILE_READ_ONLY_VOLUME = 0x00080000
FILE_SEQUENTIAL_WRITE_ONCE = 0x00100000
FILE_SUPPORTS_ENCRYPTION = 0x00020000
FILE_SUPPORTS_EXTENDED_ATTRIBUTES = 0x00800000
FILE_SUPPORTS_HARD_LINKS = 0x00400000
FILE_SUPPORTS_OBJECT_IDS = 0x00010000
FILE_SUPPORTS_OPEN_BY_FILE_ID = 0x01000000
FILE_SUPPORTS_REPARSE_POINTS = 0x00000080
FILE_SUPPORTS_SPARSE_FILES = 0x00000040
FILE_SUPPORTS_TRANSACTIONS = 0x00200000
FILE_SUPPORTS_USN_JOURNAL = 0x02000000
FILE_UNICODE_ON_DISK = 0x00000004
FILE_VOLUME_IS_COMPRESSED = 0x00008000
FILE_VOLUME_QUOTAS = 0x00000020
FILE_SUPPORTS_BLOCK_REFCOUNTING = 0x08000000