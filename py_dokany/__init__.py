import threading
import ctypes
from typing import Union

from . import dokan_h as _dokan_h
from . import constants as _constants


class Options(_dokan_h.DOKAN_OPTIONS):
    _global_context_index = 1

    def __init__(self):
        super(Options, self).__init__()
        self.GlobalContext = Options._global_context_index
        Options._global_context_index += 1

        self.timeout = 15000
        self.mount_drive_for_current_session = True
        self.enable_notification_api = True
        self.enable_fcb_garbage_collection = True
        self.case_sensitive = True
        self.version = _dokan_h.DOKAN_VERSION

    @property
    def version(self):
        """
        Version of the Dokan features requested without dots (version "123" is equal to Dokan version 1.2.3).
        """
        return self.Version

    @version.setter
    def version(self, value):
        # noinspection PyAttributeOutsideInit
        self.Version = value

    @property
    def thread_count(self):
        """
        Number of threads to be used by Dokan library internally.

        More threads will handle more events at the same time.
        """
        return self.ThreadCount

    @thread_count.setter
    def thread_count(self, value):
        # noinspection PyAttributeOutsideInit
        self.ThreadCount = value

    @property
    def mount_point(self):
        """
        Mount point.

        It can be a driver letter like "M:\" or a folder path "C:\mount\dokan" on a NTFS partition.
        """
        return self.MountPoint

    @mount_point.setter
    def mount_point(self, value):
        # noinspection PyAttributeOutsideInit
        self.MountPoint = value

    @property
    def network_unc_name(self):
        if self.is_network_drive:
            return self.UNCName

        return None

    @network_unc_name.setter
    def network_unc_name(self, value):
        if self.is_network_drive:
            # noinspection PyAttributeOutsideInit
            self.UNCName = value
        else:
            raise ValueError('drive is not set as a network drive')

    @property
    def timeout(self):
        """
        Max timeout in milliseconds of each request before Dokan gives up to wait events to complete.

        A timeout request is a sign that the userland implementation is no longer
        able to properly manage requests in time. The driver will therefore unmount
        the device when a timeout trigger in order to keep the system stable.

        The default timeout value is 15 seconds.
        """
        return self.Timeout

    @timeout.setter
    def timeout(self, value):
        self.Timeout = value

    @property
    def sector_size(self):
        """
        Sector Size of the volume.

        This will affect the displayed file size.
        """
        return self.SectorSize

    @sector_size.setter
    def sector_size(self, value):
        # noinspection PyAttributeOutsideInit
        self.SectorSize = value

    @property
    def allocation_unit_size(self):
        """
        Allocation Unit Size of the volume.

        This will affect the displayed file size.
        """
        return self.AllocationUnitSize

    @allocation_unit_size.setter
    def allocation_unit_size(self, value):
        # noinspection PyAttributeOutsideInit
        self.AllocationUnitSize = value

    @property
    def enable_debug(self):
        """
        Enable ouput debug messages
        """
        return self.Options | _dokan_h.DOKAN_OPTION_DEBUG == self.Options

    @enable_debug.setter
    def enable_debug(self, value):
        if value == self.enable_debug:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_DEBUG
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_DEBUG

    @property
    def use_stderr_for_debug(self):
        """
        Enable ouput debug message to stderr
        """
        return self.Options | _dokan_h.DOKAN_OPTION_STDERR == self.Options

    @use_stderr_for_debug.setter
    def use_stderr_for_debug(self, value):
        if value == self.use_stderr_for_debug:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_STDERR
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_STDERR

    @property
    def use_stream_names(self):
        """
        Enable the use of alternate stream path names

        <file-name>:<stream-name>
        If this is not specified then the driver will fail any attempt to access a path with a colon.
        """
        return self.Options | _dokan_h.DOKAN_OPTION_ALT_STREAM == self.Options

    @use_stream_names.setter
    def use_stream_names(self, value):
        if value == self.use_stream_names:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_ALT_STREAM
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_ALT_STREAM

    @property
    def write_protect_drive(self):
        """
        Enable mount drive as write-protected
        """
        return self.Options | _dokan_h.DOKAN_OPTION_WRITE_PROTECT == self.Options

    @write_protect_drive.setter
    def write_protect_drive(self, value):
        if value == self.write_protect_drive:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_WRITE_PROTECT
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_WRITE_PROTECT

    @property
    def is_network_drive(self):
        """
        Use network drive - Dokan network provider needs to be installed
        """
        return self.Options | _dokan_h.DOKAN_OPTION_NETWORK == self.Options

    @is_network_drive.setter
    def is_network_drive(self, value):
        if value == self.is_network_drive:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_NETWORK
            if self.is_removable_drive:
                self.Options ^= _dokan_h.DOKAN_OPTION_REMOVABLE
        else:
            # noinspection PyAttributeOutsideInit
            self.UNCName = ''
            self.Options ^= _dokan_h.DOKAN_OPTION_NETWORK
            if self.enable_unmount_network_drive:
                self.Options ^= _dokan_h.DOKAN_OPTION_ENABLE_UNMOUNT_NETWORK_DRIVE

    @property
    def is_removable_drive(self):
        """
        Use removable drive

        Be aware that on some environments, the userland application will be denied
        to communicate with the drive which will result in a unwanted unmount.
        see <a href="https://github.com/dokan-dev/dokany/issues/843">Issue #843</a>
        """
        return self.Options | _dokan_h.DOKAN_OPTION_REMOVABLE == self.Options

    @is_removable_drive.setter
    def is_removable_drive(self, value):
        if value == self.is_removable_drive:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_REMOVABLE
            if self.is_network_drive:
                self.Options ^= _dokan_h.DOKAN_OPTION_NETWORK
            if self.enable_unmount_network_drive:
                self.Options ^= _dokan_h.DOKAN_OPTION_ENABLE_UNMOUNT_NETWORK_DRIVE

            # noinspection PyAttributeOutsideInit
            self.UNCName = ''
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_REMOVABLE

    @property
    def use_mount_manager(self):
        """
        Use mount manager
        """
        return self.Options | _dokan_h.DOKAN_OPTION_MOUNT_MANAGER == self.Options

    @use_mount_manager.setter
    def use_mount_manager(self, value):
        if value == self.use_mount_manager:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_MOUNT_MANAGER
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_MOUNT_MANAGER

    @property
    def mount_drive_for_current_session(self):
        """
        Mount the drive on current session only
        """
        return self.Options | _dokan_h.DOKAN_OPTION_CURRENT_SESSION == self.Options

    @mount_drive_for_current_session.setter
    def mount_drive_for_current_session(self, value):
        if value == self.mount_drive_for_current_session:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_CURRENT_SESSION
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_CURRENT_SESSION

    @property
    def use_managed_file_locks(self):
        """
        Have Dokan manage file locking and unlocking.

        If this is set to False the application will be responsible for
        handling the locking and unlocking of files.
        Enable Lockfile/Unlockfile operations. Otherwise Dokan will take care of it
        """
        return self.Options | _dokan_h.DOKAN_OPTION_FILELOCK_USER_MODE != self.Options

    @use_managed_file_locks.setter
    def use_managed_file_locks(self, value):
        if value == self.use_managed_file_locks:
            return

        if value:
            self.Options ^= _dokan_h.DOKAN_OPTION_FILELOCK_USER_MODE
        else:
            self.Options |= _dokan_h.DOKAN_OPTION_FILELOCK_USER_MODE

    @property
    def enable_notification_api(self):
        """
        Whether DokanNotifyXXX functions should be enabled

        Enabled requires tracking special handles while the file system is mounted.
        Disabled some functions will not be available.
        """
        return self.Options | _dokan_h.DOKAN_OPTION_ENABLE_NOTIFICATION_API == self.Options

    @enable_notification_api.setter
    def enable_notification_api(self, value):
        if value == self.enable_notification_api:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_ENABLE_NOTIFICATION_API
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_ENABLE_NOTIFICATION_API

    @property
    def disable_oplocks(self):
        """
        Disable oplock support on the volume.

        Regular range locks are enabled regardless.
        """
        return self.Options | _dokan_h.DOKAN_OPTION_DISABLE_OPLOCKS == self.Options

    @disable_oplocks.setter
    def disable_oplocks(self, value):
        if value == self.disable_oplocks:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_DISABLE_OPLOCKS
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_DISABLE_OPLOCKS

    @property
    def enable_fcb_garbage_collection(self):
        """
        The advantage of the FCB GC approach is that it prevents filter drivers (Anti-virus)
        from exponentially slowing down procedures like zip file extraction due to
        repeatedly rebuilding state that they attach to the FCB header.
        """
        return self.Options | _dokan_h.DOKAN_OPTION_ENABLE_FCB_GARBAGE_COLLECTION == self.Options

    @enable_fcb_garbage_collection.setter
    def enable_fcb_garbage_collection(self, value):
        if value == self.enable_fcb_garbage_collection:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_ENABLE_FCB_GARBAGE_COLLECTION
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_ENABLE_FCB_GARBAGE_COLLECTION

    @property
    def is_case_sensitive(self):
        """
        Enable Case sensitive path.

        By default all path are case insensitive.
        For case sensitive: \\dir\\File & \\diR\\file are different files
        but for case insensitive they are the same.
        """
        return self.Options | _dokan_h.DOKAN_OPTION_CASE_SENSITIVE == self.Options

    @is_case_sensitive.setter
    def is_case_sensitive(self, value):
        if value == self.is_case_sensitive:
            return

        if value:
            self.Options |= _dokan_h.DOKAN_OPTION_CASE_SENSITIVE
        else:
            self.Options ^= _dokan_h.DOKAN_OPTION_CASE_SENSITIVE

    @property
    def enable_unmount_network_drive(self):
        """
        Allows unmounting of network drive via explorer
        """
        return self.Options | _dokan_h.DOKAN_OPTION_ENABLE_UNMOUNT_NETWORK_DRIVE == self.Options

    @enable_unmount_network_drive.setter
    def enable_unmount_network_drive(self, value):
        if value == self.enable_unmount_network_drive:
            return

        if self.is_network_drive:
            if value:
                self.Options |= _dokan_h.DOKAN_OPTION_ENABLE_UNMOUNT_NETWORK_DRIVE
            else:
                self.Options ^= _dokan_h.DOKAN_OPTION_ENABLE_UNMOUNT_NETWORK_DRIVE
        else:
            raise ValueError('drive must be set as a network drive to use this option.')

    # noinspection PyArgumentList
    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in Options.__dict__:
            obj = Options.__dict__[item]
            if isinstance(obj, property):
                return obj.fget(self)

        elif item in _dokan_h.DOKAN_OPTIONS.__dict__:
            obj = _dokan_h.DOKAN_OPTIONS.__dict__[item]
            if isinstance(obj, property):
                return obj.fget(self)

        return super(Options, self).__getattr__(item)

    # noinspection PyArgumentList
    def __setattr__(self, key, value):
        if key in Options.__dict__:
            obj = Options.__dict__[key]
            if isinstance(obj, property):
                obj.fset(self, value)
                return

        elif key in _dokan_h.DOKAN_OPTIONS.__dict__:
            obj = _dokan_h.DOKAN_OPTIONS.__dict__[key]
            if isinstance(obj, property):
                obj.fset(self, value)
                return

        try:
            super(Options, self).__setattr__(key, value)
        except:
            self.__dict__[key] = value


class CreateDispositionFlags(int):

    @property
    def create_always(self) -> bool:
        """
        Creates a new file, always.

        If the specified file exists and is writable, the function overwrites the file, the function succeeds,
        and last-error code is set to ERROR_ALREADY_EXISTS (183).

        If the specified file does not exist and is a valid path, a new file is created, the function succeeds,
        and the last-error code is set to zero.
        """
        return self | _constants.CREATE_ALWAYS == self

    @property
    def create_new(self) -> bool:
        """
        Creates a new file, only if it does not already exist.

        If the specified file exists, the function fails and the last-error code is set to ERROR_FILE_EXISTS (80).

        If the specified file does not exist and is a valid path to a writable location, a new file is created.
        """
        return self | _constants.CREATE_NEW == self

    @property
    def open_always(self) -> bool:
        """
        Opens a file, always.

        If the specified file exists, the function succeeds and the last-error code is
        set to ERROR_ALREADY_EXISTS (183).

        If the specified file does not exist and is a valid path to a writable location,
        the function creates a file and the last-error code is set to zero."""

        return self | _constants.OPEN_ALWAYS == self

    @property
    def open_existing(self) -> bool:
        """
        Opens a file or device, only if it exists.

        If the specified file or device does not exist, the function fails and the
        last-error code is set to ERROR_FILE_NOT_FOUND (2).
        """
        return self | _constants.OPEN_EXISTING == self

    @property
    def truncate_existing(self) -> bool:
        """
        Opens a file and truncates it so that its size is zero bytes, only if it exists.

        If the specified file does not exist, the function fails and the last-error
        code is set to ERROR_FILE_NOT_FOUND (2).

        The calling process must open the file with the GENERIC_WRITE bit set as
        part of the dwDesiredAccess parameter.
        """
        return self | _constants.TRUNCATE_EXISTING == self


class AccessMask(int):
    """
    User access rights.

    This is a wrapper around ``int`` for the purpose of adding properties
    that handle all of the bit wise operations that need to be performed
    to determine what the users privlages are.

    This is the base class that is subclassed by FileAccessPermissions and DirectoryAccessPermissions

    The properties located in this class are common to all subclasses of this class.
    """

    @property
    def generic_read(self) -> bool:
        """
        The right to read the information maintained by the object.
        """
        return self | _constants.GENERIC_READ == self

    @property
    def generic_write(self) -> bool:
        """
        The right to write the information maintained by the object.
        """
        return self | _constants.GENERIC_WRITE == self

    @property
    def generic_execute(self) -> bool:
        """
        The right to execute or alternatively look into the object.
        """
        return self | _constants.GENERIC_EXECUTE == self

    @property
    def generic_all(self) -> bool:
        """
        The right to read, write, and execute the object.
        """
        return self | _constants.GENERIC_ALL == self

    @property
    def maximum_allowed(self) -> bool:
        """
        I do not know what this is for.
        """
        return self & (1 << 25) > 0

    @property
    def access_system_security(self) -> bool:
        """
        The right to access system security.
        """
        return self & (1 << 24) > 0

    @property
    def synchronize(self) -> bool:
        """
        The right to wait on the given object.

        NOTE: Assuming that this is a valid concept for the object.
        """
        return self | _constants.SYNCHRONIZE == self

    @property
    def write_owner(self) -> bool:
        """
        The right to modify the owner SID of the object.

        Recall that owners always have the right to modify the object.
        """
        return self | _constants.WRITE_OWNER == self

    @property
    def write_dac(self) -> bool:
        """
        The right to modify the control (security) information for the object.
        """
        return self | _constants.WRITE_DAC == self

    @property
    def read_control(self) -> bool:
        """
        The right to read the control (security) information for the object.
        """
        return self | _constants.READ_CONTROL == self

    @property
    def delete(self) -> bool:
        """
        The right to delete the particular object.
        """
        return self | _constants.DELETE == self

    @property
    def read_extended_attributes(self) -> bool:
        """
        The right to read the extended attributes.
        """
        return self | _constants.FILE_READ_EA == self

    @property
    def write_extended_attributes(self) -> bool:
        """
        The right to modify the extended attributes.
        """
        return self | _constants.FILE_WRITE_EA == self

    @property
    def read_attributes(self) -> bool:
        """
        The right to read the attributes.
        """
        return self | _constants.FILE_READ_ATTRIBUTES == self

    @property
    def write_attributes(self) -> bool:
        """
        The right to modify the attributes.
        """
        return self | _constants.FILE_WRITE_ATTRIBUTES == self

    @property
    def is_directory(self) -> bool:
        """
        Is this a directory object.
        """
        return isinstance(self, DirectoryAccessPermissions)


class FileAccessPermissions(AccessMask):

    @property
    def read_data(self) -> bool:
        """
        The right to read data from the given file.
        """
        return self | _constants.FILE_READ_DATA == self

    @property
    def write_data(self) -> bool:
        """
        The right to write data to the given file.

        NOTE: Within the existing range of the file.
        """
        return self | _constants.FILE_WRITE_DATA == self

    @property
    def append_data(self) -> bool:
        """
        The right to extend the given file.
        """
        return self | _constants.FILE_APPEND_DATA == self

    @property
    def execute(self) -> bool:
        """
        The right to locally execute the given file.

        Executing a file stored on a remote share requires read permission,
        since the file is read from the server, but executed on the client.
        """
        return self | _constants.FILE_EXECUTE == self


class DirectoryAccessPermissions(AccessMask):

    @property
    def list_directory(self) -> bool:
        """
        The right to list the contents of the directory.
        """
        return self | _constants.FILE_LIST_DIRECTORY == self

    @property
    def add_file(self) -> bool:
        """
        The right to create a new file within the directory.
        """
        return self | _constants.FILE_ADD_FILE == self

    @property
    def add_subdirectory(self) -> bool:
        """
        The right to create a new directory (subdirectory) within the directory.
        """
        return self | _constants.FILE_ADD_SUBDIRECTORY == self

    @property
    def traverse(self) -> bool:
        """
        The right to access objects within the directory.

        The `traverse` access right is different than the `list_directory` access right.
        Holding the `list_directory` access right allows an entity to obtain a list of the
        contents of a directory, while the `traverse` access right gives an entity the right
        to access the object. A caller without the `list_directory` access right could open
        a file that it knew already existed, but would not be able to obtain a list of the
        contents of the directory.
        """
        return self | _constants.FILE_TRAVERSE == self

    @property
    def delete_child(self) -> bool:
        """
        The right to delete a file or directory within the current directory.
        """
        return self | _constants.FILE_DELETE_CHILD == self


class FileSystemFlags(int):

    @property
    def supports_block_ref_counting(self) -> bool:
        """
        The specified volume supports sharing logical clusters between files on the same volume.

        The file system reallocates on writes to shared clusters. Indicates that
        FSCTL_DUPLICATE_EXTENTS_TO_FILE is a supported operation.
        """
        return self | _constants.FILE_SUPPORTS_BLOCK_REFCOUNTING == self

    @supports_block_ref_counting.setter
    def supports_block_ref_counting(self, value: bool):
        if self.supports_block_ref_counting != value:
            if value:
                self |= _constants.FILE_SUPPORTS_BLOCK_REFCOUNTING
            else:
                self ^= _constants.FILE_SUPPORTS_BLOCK_REFCOUNTING

    @property
    def volume_quotas(self) -> bool:
        """
        The specified volume supports disk quotas.
        """
        return self | _constants.FILE_VOLUME_QUOTAS == self

    @volume_quotas.setter
    def volume_quotas(self, value: bool):
        if self.volume_quotas != value:
            if value:
                self |= _constants.FILE_VOLUME_QUOTAS
            else:
                self ^= _constants.FILE_VOLUME_QUOTAS

    @property
    def is_compressed(self) -> bool:
        """
        The specified volume is a compressed volume, for example, a DoubleSpace volume.
        """
        return self | _constants.FILE_VOLUME_IS_COMPRESSED == self

    @is_compressed.setter
    def is_compressed(self, value: bool):
        if self.is_compressed != value:
            if value:
                self |= _constants.FILE_VOLUME_IS_COMPRESSED
            else:
                self ^= _constants.FILE_VOLUME_IS_COMPRESSED

    @property
    def supports_usn_journal(self) -> bool:
        """
        The specified volume supports update sequence number (USN) journals.
        """
        return self | _constants.FILE_SUPPORTS_USN_JOURNAL == self

    @supports_usn_journal.setter
    def supports_usn_journal(self, value: bool):
        if self.supports_usn_journal != value:
            if value:
                self |= _constants.FILE_SUPPORTS_USN_JOURNAL
            else:
                self ^= _constants.FILE_SUPPORTS_USN_JOURNAL

    @property
    def unicode_on_disk(self) -> bool:
        """
        The specified volume supports Unicode in file names as they appear on disk.
        """
        return self | _constants.FILE_UNICODE_ON_DISK == self

    @unicode_on_disk.setter
    def unicode_on_disk(self, value: bool):
        if self.unicode_on_disk != value:
            if value:
                self |= _constants.FILE_UNICODE_ON_DISK
            else:
                self ^= _constants.FILE_UNICODE_ON_DISK

    @property
    def supports_transactions(self) -> bool:
        """
        The specified volume supports transactions.
        """
        return self | _constants.FILE_SUPPORTS_TRANSACTIONS == self

    @supports_transactions.setter
    def supports_transactions(self, value: bool):
        if self.supports_transactions != value:
            if value:
                self |= _constants.FILE_SUPPORTS_TRANSACTIONS
            else:
                self ^= _constants.FILE_SUPPORTS_TRANSACTIONS

    @property
    def supports_sparse_files(self) -> bool:
        """
        The specified volume supports sparse files.
        """
        return self | _constants.FILE_SUPPORTS_SPARSE_FILES == self

    @supports_sparse_files.setter
    def supports_sparse_files(self, value: bool):
        if self.supports_sparse_files != value:
            if value:
                self |= _constants.FILE_SUPPORTS_SPARSE_FILES
            else:
                self ^= _constants.FILE_SUPPORTS_SPARSE_FILES

    @property
    def supports_reparse_points(self) -> bool:
        """
        The specified volume supports reparse points.
        """
        return self | _constants.FILE_SUPPORTS_REPARSE_POINTS == self

    @supports_reparse_points.setter
    def supports_reparse_points(self, value: bool):
        if self.supports_reparse_points != value:
            if value:
                self |= _constants.FILE_SUPPORTS_REPARSE_POINTS
            else:
                self ^= _constants.FILE_SUPPORTS_REPARSE_POINTS

    @property
    def supports_open_file_by_id(self) -> bool:
        """
        The file system supports open by FileID.
        """
        return self | _constants.FILE_SUPPORTS_OPEN_BY_FILE_ID == self

    @supports_open_file_by_id.setter
    def supports_open_file_by_id(self, value: bool):
        if self.supports_open_file_by_id != value:
            if value:
                self |= _constants.FILE_SUPPORTS_OPEN_BY_FILE_ID
            else:
                self ^= _constants.FILE_SUPPORTS_OPEN_BY_FILE_ID

    @property
    def supports_object_ids(self) -> bool:
        """
        The specified volume supports object identifiers.
        """
        return self | _constants.FILE_SUPPORTS_OBJECT_IDS == self

    @supports_object_ids.setter
    def supports_object_ids(self, value: bool):
        if self.supports_object_ids != value:
            if value:
                self |= _constants.FILE_SUPPORTS_OBJECT_IDS
            else:
                self ^= _constants.FILE_SUPPORTS_OBJECT_IDS

    @property
    def supports_hard_links(self) -> bool:
        """
        The specified volume supports hard links.
        """
        return self | _constants.FILE_SUPPORTS_HARD_LINKS == self

    @supports_hard_links.setter
    def supports_hard_links(self, value: bool):
        if self.supports_hard_links != value:
            if value:
                self |= _constants.FILE_SUPPORTS_HARD_LINKS
            else:
                self ^= _constants.FILE_SUPPORTS_HARD_LINKS

    @property
    def supports_extended_attributes(self) -> bool:
        """
        The specified volume supports extended attributes.

        An extended attribute is a piece of application-specific metadata that an application
        can associate with a file and is not part of the file's data.

        Windows Server 2008, Windows Vista, Windows Server 2003 and Windows XP:
        This value is not supported until Windows Server 2008 R2 and Windows 7.
        """
        return self | _constants.FILE_SUPPORTS_EXTENDED_ATTRIBUTES == self

    @supports_extended_attributes.setter
    def supports_extended_attributes(self, value: bool):
        if self.supports_extended_attributes != value:
            if value:
                self |= _constants.FILE_SUPPORTS_EXTENDED_ATTRIBUTES
            else:
                self ^= _constants.FILE_SUPPORTS_EXTENDED_ATTRIBUTES

    @property
    def supports_encryption(self) -> bool:
        """
        The specified volume supports the Encrypted File System (EFS).
        """
        return self | _constants.FILE_SUPPORTS_ENCRYPTION == self

    @supports_encryption.setter
    def supports_encryption(self, value: bool):
        if self.supports_encryption != value:
            if value:
                self |= _constants.FILE_SUPPORTS_ENCRYPTION
            else:
                self ^= _constants.FILE_SUPPORTS_ENCRYPTION

    @property
    def sequential_write_once(self) -> bool:
        """
        The specified volume supports a single sequential write.
        """
        return self | _constants.FILE_SEQUENTIAL_WRITE_ONCE == self

    @sequential_write_once.setter
    def sequential_write_once(self, value: bool):
        if self.sequential_write_once != value:
            if value:
                self |= _constants.FILE_SEQUENTIAL_WRITE_ONCE
            else:
                self ^= _constants.FILE_SEQUENTIAL_WRITE_ONCE

    @property
    def read_only(self) -> bool:
        """
        The specified volume is read-only.
        """
        return self | _constants.FILE_READ_ONLY_VOLUME == self

    @read_only.setter
    def read_only(self, value: bool):
        if self.read_only != value:
            if value:
                self |= _constants.FILE_READ_ONLY_VOLUME
            else:
                self ^= _constants.FILE_READ_ONLY_VOLUME

    @property
    def persistent_acls(self) -> bool:
        """
        The specified volume preserves and enforces access control lists (ACL).

        For example, the NTFS file system preserves and enforces ACLs, and the FAT file system does not.
        """
        return self | _constants.FILE_PERSISTENT_ACLS == self

    @persistent_acls.setter
    def persistent_acls(self, value: bool):
        if self.persistent_acls != value:
            if value:
                self |= _constants.FILE_PERSISTENT_ACLS
            else:
                self ^= _constants.FILE_PERSISTENT_ACLS

    @property
    def named_streams(self) -> bool:
        """
        The specified volume supports named streams.
        """
        return self | _constants.FILE_NAMED_STREAMS == self

    @named_streams.setter
    def named_streams(self, value: bool):
        if self.named_streams != value:
            if value:
                self |= _constants.FILE_NAMED_STREAMS
            else:
                self ^= _constants.FILE_NAMED_STREAMS

    @property
    def file_compression(self) -> bool:
        """
        The specified volume supports file-based compression.
        """
        return self | _constants.FILE_FILE_COMPRESSION == self

    @file_compression.setter
    def file_compression(self, value: bool):
        if self.file_compression != value:
            if value:
                self |= _constants.FILE_FILE_COMPRESSION
            else:
                self ^= _constants.FILE_FILE_COMPRESSION

    @property
    def dax_volume(self) -> bool:
        """
        The specified volume is a direct access (DAX) volume.
        """
        return self | _constants.FILE_DAX_VOLUME == self

    @dax_volume.setter
    def dax_volume(self, value: bool):
        if self.dax_volume != value:
            if value:
                self |= _constants.FILE_DAX_VOLUME
            else:
                self ^= _constants.FILE_DAX_VOLUME

    @property
    def case_preserved_names(self) -> bool:
        """
        The specified volume supports preserved case of file names when it places a name on disk.
        """
        return self | _constants.FILE_CASE_PRESERVED_NAMES == self

    @case_preserved_names.setter
    def case_preserved_names(self, value: bool):
        if self.case_preserved_names != value:
            if value:
                self |= _constants.FILE_CASE_PRESERVED_NAMES
            else:
                self ^= _constants.FILE_CASE_PRESERVED_NAMES

    @property
    def case_sensitive_search(self) -> bool:
        """
        The specified volume supports case-sensitive file names.
        """
        return self | _constants.FILE_CASE_SENSITIVE_SEARCH == self

    @case_sensitive_search.setter
    def case_sensitive_search(self, value: bool):
        if self.case_sensitive_search != value:
            if value:
                self |= _constants.FILE_CASE_SENSITIVE_SEARCH
            else:
                self ^= _constants.FILE_CASE_SENSITIVE_SEARCH


class Flags(int):

    @property
    def backup_symantics(self) -> bool:
        """
        The file is being opened or created for a backup or restore operation.

        The system ensures that the calling process overrides file security checks when
        the process has SE_BACKUP_NAME and SE_RESTORE_NAME privileges.

        You must set this flag to obtain a handle to a directory. A directory handle can
        be passed to some functions instead of a file handle.
        """
        return self | _constants.FILE_FLAG_BACKUP_SEMANTICS == self

    @property
    def delete_on_close(self) -> bool:
        """
        The file is to be deleted immediately after all of its handles are closed.

        This includes the specified handle and any other open or duplicated handles.
        If there are existing open handles to a file, the call fails unless they were all
        opened with the FILE_SHARE_DELETE share mode.

        Subsequent open requests for the file fail, unless the FILE_SHARE_DELETE
        share mode is specified.
        """
        return self | _constants.FILE_FLAG_DELETE_ON_CLOSE == self

    @property
    def no_buffering(self) -> bool:
        """
        The file or device is being opened with no system caching for data reads and writes.

        This flag does not affect hard disk caching or memory mapped files.
        There are strict requirements for successfully working with files opened with
        CreateFile using the `no_buffering` flag.
        """
        return self | _constants.FILE_FLAG_NO_BUFFERING == self

    @property
    def open_no_recall(self) -> bool:
        """
        The file data is requested, but it should continue to be located in remote storage.

        It should not be transported back to local storage.
        This flag is for use by remote storage systems.
        """
        return self | _constants.FILE_FLAG_OPEN_NO_RECALL == self

    @property
    def open_reparse_point(self) -> bool:
        """
        Normal reparse point processing will not occur.

        CreateFile will attempt to open the reparse point.
        When a file is opened, a file handle is returned, whether or not the filter that
        controls the reparse point is operational.

        This flag cannot be used with the CREATE_ALWAYS flag.
        If the file is not a reparse point, then this flag is ignored.
        """
        return self | _constants.FILE_FLAG_OPEN_REPARSE_POINT == self

    @property
    def overlapped(self) -> bool:
        """
        The file or device is being opened or created for asynchronous I/O.

        When subsequent I/O operations are completed on this handle, the event specified
        in the OVERLAPPED structure will be set to the signaled state.

        If this flag is specified, the file can be used for simultaneous read and write operations.
        If this flag is not specified, then I/O operations are serialized, even if the calls to the
        read and write functions specify an OVERLAPPED structure.
        """
        return self | _constants.FILE_FLAG_OVERLAPPED == self

    @property
    def posix_symantics(self) -> bool:
        """
        Access will occur according to POSIX rules.

        This includes allowing multiple files with names, differing only in case,
        for file systems that support that naming. Use care when using this option,
        because files created with this flag may not be accessible by applications
        that are written for MS-DOS or 16-bit Windows.
        """
        return self | _constants.FILE_FLAG_POSIX_SEMANTICS == self

    @property
    def random_access(self) -> bool:
        """
        Access is intended to be random.

        The system can use this as a hint to optimize file caching.
        This flag has no effect if the file system does not support cached I/O and `no_buffering`.
        """
        return self | _constants.FILE_FLAG_RANDOM_ACCESS == self

    @property
    def session_aware(self) -> bool:
        """
        The file or device is being opened with session awareness.

        If this flag is not specified, then per-session devices (such as a device
        using RemoteFX USB Redirection) cannot be opened by processes running in session 0.
        This flag has no effect for callers not in session 0. This flag is supported only
        on server editions of Windows.

        This flag is not supported before Windows Server 2012.
        """
        return self | _constants.FILE_FLAG_SESSION_AWARE == self

    @property
    def sequential_scan(self) -> bool:
        """
        Access is intended to be sequential from beginning to end.

        The system can use this as a hint to optimize file caching.
        This flag should not be used if read-behind (that is, reverse scans) will be used.
        This flag has no effect if the file system does not support cached I/O and `no_buffering`."""
        return self | _constants.FILE_FLAG_SEQUENTIAL_SCAN == self

    @property
    def write_through(self) -> bool:
        """
        Write operations will not go through any intermediate cache, they will go directly to disk.
        """
        return self | _constants.FILE_FLAG_WRITE_THROUGH == self


class SecurityFlags(int):

    @property
    def anonymous(self) -> bool:
        """
        Impersonates a client at the Anonymous impersonation level.
        """
        return self | _constants.SECURITY_ANONYMOUS == self

    @property
    def context_tracking(self) -> bool:
        """
        The security tracking mode is dynamic.

        If this flag is not specified, the security tracking mode is static.
        """
        return self | _constants.SECURITY_CONTEXT_TRACKING == self

    @property
    def deligation(self) -> bool:
        """
        Impersonates a client at the Delegation impersonation level.
        """
        
        return self | _constants.SECURITY_DELEGATION == self

    @property
    def effective_only(self) -> bool:
        """
        Only the enabled aspects of the client's security context are available to the server.

        If you do not specify this flag, all aspects of the client's security context
        are available. This allows the client to limit the groups and  privileges that
        a server can use while impersonating the client.
        """
        return self | _constants.SECURITY_EFFECTIVE_ONLY == self

    @property
    def identification(self) -> bool:
        """
        Impersonates a client at the Identification impersonation level.
        """
        return self | _constants.SECURITY_IDENTIFICATION == self

    @property
    def impersonation(self) -> bool:
        """
        Impersonate a client at the impersonation level.

        This is the default behavior if no other flags are specified.
        along with the SECURITY_SQOS_PRESENT flag.
        """
        return self | _constants.SECURITY_IMPERSONATION == self


class Attributes(int):

    @property
    def archive(self) -> bool:
        """
        The file should be archived.

        Applications use this attribute to mark files for backup or removal.
        """
        return self | _constants.FILE_ATTRIBUTE_ARCHIVE == self

    @archive.setter
    def archive(self, value: bool):
        if self.archive != value:
            if value:
                self |= _constants.FILE_ATTRIBUTE_ARCHIVE
            else:
                self ^= _constants.FILE_ATTRIBUTE_ARCHIVE

    @property
    def encrypted(self) -> bool:
        """
        The file or directory is encrypted.

        For a file, this means that all data in the file is encrypted.
        For a directory, this means that encryption is the default for newly created files
        and subdirectories.

        This flag has no effect if `system` is also specified.
        This flag is not supported on Home, Home Premium, Starter, or ARM editions of Windows.
        """
        return self | _constants.FILE_ATTRIBUTE_ENCRYPTED == self

    @encrypted.setter
    def encrypted(self, value: bool):
        if self.encrypted != value:
            if value:
                self |= _constants.FILE_ATTRIBUTE_ENCRYPTED
            else:
                self ^= _constants.FILE_ATTRIBUTE_ENCRYPTED

    @property
    def hidden(self) -> bool:
        """
        The file is hidden.

        Do not include it in an ordinary directory listing.
        """
        return self | _constants.FILE_ATTRIBUTE_HIDDEN == self

    @hidden.setter
    def hidden(self, value: bool):
        if self.hidden != value:
            if value:
                self |= _constants.FILE_ATTRIBUTE_HIDDEN
            else:
                self ^= _constants.FILE_ATTRIBUTE_HIDDEN

    @property
    def normal(self) -> bool:
        """
        The file does not have other attributes set.

        This attribute is valid only if used alone.
        """
        return self | _constants.FILE_ATTRIBUTE_NORMAL == self

    @normal.setter
    def normal(self, value: bool):
        if self.normal != value:
            if value:
                self |= _constants.FILE_ATTRIBUTE_NORMAL
            else:
                self ^= _constants.FILE_ATTRIBUTE_NORMAL

    @property
    def offline(self) -> bool:
        """
        The data of a file is not immediately available.

        This attribute indicates that file data is physically moved to offline storage.
        This attribute is used by Remote Storage, the hierarchical storage management
        software. Applications should not arbitrarily change this attribute.
        """
        return self | _constants.FILE_ATTRIBUTE_OFFLINE == self

    @offline.setter
    def offline(self, value: bool):
        if self.offline != value:
            if value:
                self |= _constants.FILE_ATTRIBUTE_OFFLINE
            else:
                self ^= _constants.FILE_ATTRIBUTE_OFFLINE

    @property
    def read_only(self) -> bool:
        """
        The file is read only.

        Applications can read the file, but cannot write to or delete it.
        """
        return self | _constants.FILE_ATTRIBUTE_READONLY == self

    @read_only.setter
    def read_only(self, value: bool):
        if self.read_only != value:
            if value:
                self |= _constants.FILE_ATTRIBUTE_READONLY
            else:
                self ^= _constants.FILE_ATTRIBUTE_READONLY

    @property
    def system(self) -> bool:
        """
        The file is part of or used exclusively by an operating system.
        """
        return self | _constants.FILE_ATTRIBUTE_SYSTEM == self

    @system.setter
    def system(self, value: bool):
        if self.system != value:
            if value:
                self |= _constants.FILE_ATTRIBUTE_SYSTEM
            else:
                self ^= _constants.FILE_ATTRIBUTE_SYSTEM

    @property
    def temporary(self) -> bool:
        """
        The file is being used for temporary storage.
        """
        return self | _constants.FILE_ATTRIBUTE_TEMPORARY == self

    @temporary.setter
    def temporary(self, value: bool):
        if self.temporary != value:
            if value:
                self |= _constants.FILE_ATTRIBUTE_TEMPORARY
            else:
                self ^= _constants.FILE_ATTRIBUTE_TEMPORARY


class ShareAccessFlags(int):

    @property
    def delete(self) -> bool:
        """
        Enables subsequent open operations on a file or device to request delete access.

        Otherwise, other processes cannot open the file or device if they request delete access.

        If this flag is not specified, but the file or device has been opened for delete access,
        the function fails.

        Note: Delete access allows both delete and rename operations.
        """
        return self | _constants.FILE_SHARE_DELETE == self

    @property
    def read(self) -> bool:
        """
        Enables subsequent open operations on a file or device to request read access.

        Otherwise, other processes cannot open the file or device if they request read access.

        If this flag is not specified, but the file or device has been opened for read access,
        the function fails.
        """
        return self | _constants.FILE_SHARE_READ == self

    @property
    def write(self) -> bool:
        """
        Enables subsequent open operations on a file or device to request write access.

        Otherwise, other processes cannot open the file or device if they request write access.

        If this flag is not specified, but the file or device has been opened for write access
        or has a file mapping with write access, the function fails.
        """
        return self | _constants.FILE_SHARE_WRITE == self


class DokanFileInfoBase(object):

    def __init__(self, dokan_file_info):
        self._dokan_file_info = dokan_file_info

    @property
    def context(self) -> int:
        """
        Integer value to track reference to an object.

        internal reference that will help the implementation understand the request context of the event.
        """
        return self._dokan_file_info.contents.Context

    @context.setter
    def context(self, value: int):
        self._dokan_file_info.contents.Context = value

    @property
    def process_id(self) -> int:
        """
        Process ID for the thread that originally requested a given I/O operation
        """
        return self._dokan_file_info.contents.ProcessId.value

    @property
    def is_directory(self) -> bool:
        """
        Is this a directory request
        """
        return bool(self._dokan_file_info.contents.IsDirectory)

    @property
    def delete_on_close(self) -> bool:
        """
        Flag if the file has to be deleted during cleanup event.
        """
        return bool(self._dokan_file_info.contents.DeleteOnClose)

    @property
    def paging_io(self) -> bool:
        """
        Read or write is paging IO.
        """
        return bool(self._dokan_file_info.contents.PagingIo)

    @property
    def synchronous_io(self) -> bool:
        """
        Read or write is synchronous IO.
        """
        return bool(self._dokan_file_info.contents.SynchronousIo)

    @property
    def no_cache(self) -> bool:
        """
        Read or write directly from data source without cache
        """
        return bool(self._dokan_file_info.contents.Nocache)

    @property
    def write_to_end_of_file(self) -> bool:
        """
        Write to the current end of file instead of using the Offset parameter.
        """
        return bool(self._dokan_file_info.contents.WriteToEndOfFile)


class RequestBase(DokanFileInfoBase):

    def __init__(self, filename, dokan_file_info):
        self._filename = filename
        DokanFileInfoBase.__init__(self, dokan_file_info)

    @property
    def filename(self) -> str:
        return self._filename


class CleanupRequest(RequestBase):
    pass


class CloseFileRequest(RequestBase):
    pass


class FlushFileBuffersRequest(RequestBase):
    pass


class DeleteFileRequest(RequestBase):
    pass


class DeleteDirectoryRequest(RequestBase):
    pass


class MountedRequest(DokanFileInfoBase):
    pass


class UnmountedRequest(DokanFileInfoBase):
    pass


class CreateFileRequest(RequestBase):

    def __init__(
            self,
            filename,
            security_context,
            desired_access,
            file_attr_flags,
            share_access,
            create_disposition,
            dokan_file_info
    ):
        RequestBase.__init__(self, filename, dokan_file_info)
        self._security_context = security_context
        self._desired_access = desired_access
        self._file_attr_flags = file_attr_flags
        self._share_access = share_access
        self._create_disposition = create_disposition

    @property
    def share_access(self) -> ShareAccessFlags:
        return ShareAccessFlags(self._share_access)

    @property
    def create_disposition(self) -> CreateDispositionFlags:
        return CreateDispositionFlags(self._create_disposition)

    @property
    def attributes(self) -> Attributes:
        return Attributes(self._file_attr_flags)

    @property
    def security_flags(self) -> SecurityFlags:
        return SecurityFlags(self._file_attr_flags)

    @property
    def flags(self) -> Flags:
        return Flags(self._file_attr_flags)

    @property
    def permissions(self) -> Union[FileAccessPermissions, DirectoryAccessPermissions]:
        if self.is_directory:
            return DirectoryAccessPermissions(self._desired_access)

        return FileAccessPermissions(self._desired_access)


class ReadFileRequest(RequestBase):
    def __init__(self, filename, start_byte, stop_byte, dokan_file_info):
        self._start_byte = start_byte
        self._stop_byte = stop_byte
        self._data = bytearray()

        RequestBase.__init__(self, filename, dokan_file_info)

    @property
    def start_byte(self) -> int:
        return self._start_byte

    @property
    def stop_byte(self) -> int:
        return self._stop_byte

    def data(self, value: Union[bytearray, bytes]):
        if isinstance(value, (list, tuple)):
            try:
                value = bytearray(value)
            except:
                raise ValueError(
                    'data type need to be a bytearray or a data type '
                    'that can be converted into a byte array'
                )
        elif isinstance(value, (str, bytes)):
            value = bytearray(value, encoding='utf-8')
        else:
            raise ValueError(
                'data type need to be a bytearray or a data type '
                'that can be converted into a byte array'
            )

        if len(value) < self.stop_byte - self.start_byte:
            raise ValueError('To many bytes have been read')

        self._data = value

    data = property(fset=data)


class WriteFileRequest(RequestBase):
    def __init__(self, filename, data, offset, num_bytes, dokan_file_info):
        self._offset = offset
        self._num_bytes = num_bytes
        self._num_bytes_written = 0
        self._data = data
        RequestBase.__init__(self, filename, dokan_file_info)

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def num_bytes(self) -> int:
        return self._num_bytes

    def num_bytes_written(self, value: int):
        if value > self.num_bytes:
            raise ValueError('to many bytes written')

        self._num_bytes_written = value

    num_bytes_written = property(fset=num_bytes_written)

    @property
    def data(self) -> bytearray:
        return self._data


class FileInformationRequest(RequestBase):

    def __init__(self, file_name, file_info, dokan_file_info):

        RequestBase.__init__(self, file_name, dokan_file_info)
        self._last_access_time = 0
        self._creation_time = 0
        self._last_write_time = 0
        self._number_of_links = 0
        self._file_index = 0
        self._file_size = 0
        self._attributes = Attributes(0)

    @property
    def attributes(self) -> Attributes:
        return self._attributes

    def creation_time(self, value: int):
        self._creation_time = int(value)

    creation_time = property(fset=creation_time)

    def last_access_time(self, value: int):
        self._last_access_time = int(value)

    last_access_time = property(fset=last_access_time)

    def last_write_time(self, value: int):
        self._last_write_time = int(value)

    last_write_time = property(fset=last_write_time)

    def file_size(self, value: int):
        self._file_size = int(value)


    file_size = property(fset=file_size)

    def number_of_links(self, value: int):
        self._number_of_links == value

    number_of_links = property(fset=number_of_links)

    def file_index(self, value: int):
        self._file_index = value

    file_index = property(fset=file_index)
287.28
27,590,320
class FileAttributesRequest(RequestBase):
    def __init__(self, file_name, file_attributes, dokan_file_info):
        RequestBase.__init__(self, file_name, dokan_file_info)
        self._file_attributes = file_attributes

    @property
    def attributes(self) -> Attributes:
        return Attributes(self._file_attributes)


class FileTimeRequest(RequestBase):
    def __init__(self, file_name, creation_time, last_access_time, last_write_time, dokan_file_info):
        RequestBase.__init__(self, file_name, dokan_file_info)
        self._creation_time = creation_time
        self._last_access_time = last_access_time
        self._last_write_time = last_write_time

    @property
    def creation_time(self) -> int:
        ct = self._creation_time.contents
        dt_high = ct.dwHighDateTime.value
        dt_low = ct.dwLowDateTime.value
        return dt_high << 32 | dt_low

    @property
    def last_access_time(self) -> int:
        lat = self._last_access_time.contents
        dt_high = lat.dwHighDateTime.value
        dt_low = lat.dwLowDateTime.value
        return dt_high << 32 | dt_low

    @property
    def last_write_time(self) -> int:
        lwt = self._last_write_time.contents
        dt_high = lwt.dwHighDateTime.value
        dt_low = lwt.dwLowDateTime.value
        return dt_high << 32 | dt_low


class MoveFileRequest(RequestBase):

    def __init__(self, file_name, new_file_name, replace_if_existing, dokan_file_info):
        RequestBase.__init__(self, file_name, dokan_file_info)
        self._new_file_name = new_file_name
        self._replace_if_existing = replace_if_existing

    @property
    def new_file_name(self) -> str:
        return self._new_file_name

    @property
    def replace_if_existing(self) -> bool:
        return self._replace_if_existing


class EndOfFileRequest(RequestBase):

    def __init__(self, file_name, offset, dokan_file_info):
        RequestBase.__init__(self, file_name, dokan_file_info)
        self._offset = offset

    @property
    def offset(self) -> int:
        return self._offset


class AllocationSizeRequest(RequestBase):

    def __init__(self, file_name, allocation_size, dokan_file_info):
        RequestBase.__init__(self, file_name, dokan_file_info)
        self._allocation_size = allocation_size

    @property
    def allocation_size(self) -> int:
        return self._allocation_size


class LockFileRequest(RequestBase):

    def __init__(self, file_name, offset, length, dokan_file_info):
        RequestBase.__init__(self, file_name, dokan_file_info)
        self._offset = offset
        self._length = length

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def length(self) -> int:
        return self._length


class UnlockFileRequest(RequestBase):

    def __init__(self, file_name, offset, length, dokan_file_info):
        RequestBase.__init__(self, file_name, dokan_file_info)
        self._offset = offset
        self._length = length

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def length(self) -> int:
        return self._length


class DiskFreeSpaceRequest(DokanFileInfoBase):

    def __init__(
        self,
        free_bytes_available,
        total_number_of_bytes,
        total_number_of_free_bytes,
        dokan_file_info
    ):
        DokanFileInfoBase.__init__(self, dokan_file_info)
        self._free_bytes_available = free_bytes_available
        self._total_number_of_bytes = total_number_of_bytes
        self._total_number_of_free_bytes = total_number_of_free_bytes

    def free_bytes_available(self, value: int):
        self._free_bytes_available.contents.value = value

    free_bytes_available = property(fset=free_bytes_available)

    def total_number_of_bytes(self, value: int):
        self._total_number_of_bytes.contents.value = value

    total_number_of_bytes = property(fset=total_number_of_bytes)

    def total_number_of_free_bytes(self, value: int):
        self._total_number_of_free_bytes.contents.value = value

    total_number_of_free_bytes = property(fset=total_number_of_free_bytes)


class VolumeInformationRequest(DokanFileInfoBase):

    def __init__(
            self,
            volume_name_size,
            volume_serial_number,
            maximum_component_length,
            file_system_flags,
            file_system_name_size,
            dokan_file_info
    ):
        DokanFileInfoBase.__init__(self, dokan_file_info)
        self._volume_name_size = volume_name_size
        self._volume_serial_number = volume_serial_number
        self._maximum_component_length = maximum_component_length
        self._file_system_flags = file_system_flags
        self._file_system_name_size = file_system_name_size

        self._volume_name = ''
        self._file_system_name = ''

    @property
    def volume_name(self) -> str:
        return self._volume_name

    @volume_name.setter
    def volume_name(self, value: str):
        if len(value) > self.volume_name_size:
            raise ValueError('volume name is to long')

        self._volume_name = value

    @property
    def file_system_name(self) -> str:
        return self._volume_name

    @file_system_name.setter
    def file_system_name(self, value: str):
        if len(value) > self.file_system_name_size:
            raise ValueError('volume name is to long')

        self._file_system_name = value

    @property
    def volume_name_size(self) -> int:
        return self._volume_name_size

    def volume_serial_number(self, value: int):
        self._volume_serial_number.contents.value = value

    volume_serial_number = property(fset=volume_serial_number)

    def maximum_component_length(self, value: int):
        self._maximum_component_length.contents.value = value

    maximum_component_length = property(fset=maximum_component_length)

    @property
    def file_system_name_size(self) -> int:
        return self._file_system_name_size


class SetFileSecurityRequest(RequestBase):

    def __init__(self, file_name, security_information, security_descriptors, dokan_file_info):
        RequestBase.__init__(self, file_name, dokan_file_info)
        self._security_information = security_information
        self._security_descriptors = security_descriptors

    @property
    def security_information(self):
        return self._security_information

    @property
    def security_descriptors(self):
        return self._security_descriptors[:]


class GetFileSecurityRequest(RequestBase):
    def __init__(self, file_name, security_information, num_descriptors, dokan_file_info):
        RequestBase.__init__(self, file_name, dokan_file_info)
        self._security_information = security_information
        self._security_descriptors = []
        self._num_descriptors = num_descriptors

    @property
    def security_information(self):
        return self._security_information.contents.value

    @security_information.setter
    def security_information(self, value):
        self._security_information.contents = value

    @property
    def num_descriptors(self):
        return self._num_descriptors

    @property
    def security_descriptors(self):
        return self._security_descriptors

    @security_descriptors.setter
    def security_descriptors(self, value):
        if len(value) > self._num_descriptors:
            raise ValueError('to many security descriptors')

        self.security_descriptors = value



class DokanError(Exception):
    msg = 'Unknown Error'

    def __str__(self):
        return self.msg


class AlreadyMountedError(DokanError):
    msg = 'Drive is already mounted.'


class DriveLetterError(DokanError):
    msg = 'Bad drive letter.'


class DriverInstallError(DokanError):
    msg = 'Can\'t install driver.'


class StartError(DokanError):
    msg = 'Driver answer that something is wrong.'


class MountError(DokanError):
    msg = 'Can\'t assign a drive letter or mount point. Probably already used by another volume.'


class MountPointError(DokanError):
    msg = 'Mount point is invalid.'


class VersionError(DokanError):
    msg = 'Requested an incompatible version.'


class Drive(object):
    """
    The main entry point to the library.

    I have dome my best at making this library as simple to use as possible
    while also keeping as much flexability as possible. I am going to cover
    how to use some of the components below because it would be repitive if
    I added it to each of the components.


    The first thing I want to cover is how an application is going to know
    if a request from the operation system is being made.

    There are several methods in this class that are designed to be used as
    decorators, these methods can also be used as methods if needed. They
    can be used in a dynamic nature or they can be used statically. I will
    cover examples on both.

    These methods covered are:

    * :py:meth:`Drive.create_file`
    * :py:meth:`Drive.read_file`
    * :py:meth:`Drive.cleanup`
    * :py:meth:`Drive.close_file`
    * :py:meth:`Drive.write_file`
    * :py:meth:`Drive.flush_file_buffers`
    * :py:meth:`Drive.file_information`
    * :py:meth:`Drive.file_attributes`
    * :py:meth:`Drive.delete_file`
    * :py:meth:`Drive.file_time`
    * :py:meth:`Drive.delete_directory`
    * :py:meth:`Drive.move_file`
    * :py:meth:`Drive.end_of_file`
    * :py:meth:`Drive.allocation_size`
    * :py:meth:`Drive.lock_file`
    * :py:meth:`Drive.unlock_file`
    * :py:meth:`Drive.get_file_security`
    * :py:meth:`Drive.set_file_security`
    * :py:meth:`Drive.find_files`
    * :py:meth:`Drive.find_files_with_pattern`
    * :py:meth:`Drive.find_streams`



    When using any of the methods above they can be used as if you would a normal
    function/method or as a decorator.

    When the OS wants to perform an operation on the drive there needs to be a way to
    relay that to the application for the application to carry out. The methods handle
    registering the callbacks. The description of the scope of the operation that needs
    to be carried out is available in the documentation for that method. I am only
    covering the information that is universal to all of them here, which is use.


    You can specify a callback function for each file and directory that is available
    and/or you can register a "default" callback. It will be eaier if I explain how
    the process works.

    When an operation needs to be carried out by the OS this library will check to see if
    there is a callback registred for that specific file or directory the operation needs
    to be carried out on. If there is one available that is used, if there is no one
    available then the library checks for a default callback. If there is a default callback
    available that is used, if not then :py:data:`STATUS_NOT_IMPLEMENTED` is returned.

    The below code is how to register a specific file/directory to a callback function,
    this is how you would do it statically.

    ..code-block::

        import dokan

        options = dokan.Options
        drive = dokan.Drive(options)

        @drive.create_file('./some/path/some.file')
        def create_file_some_path_some_file(request):
            pass


    The code below shows how to register a default callback, this should
    always be done statically and should only be done once for each
    :py:class:`Drive` instance.

    ..code-block::

        import dokan

        options = dokan.Options
        drive = dokan.Drive(options)

        @drive.create_file
        def default_create_file_callback(request):
            pass


    if you want to dynamically register callbacks for each of the files/directories
    in a drive the example below shows how.

    ..code-block::
        import dokan

        FILES_DIRECTORIES = (
            '/level1'
            '/level1/file1.txt'
            '/level1/file2.txt'
            '/level1/level2'
            '/level1/level2/file1.txt'
        )

        options = dokan.Options
        drive = dokan.Drive(options)

        @drive.create_file
        def default_create_file_callback(request):
            pass

        for path in FILES_DIRECTORIES:
            if 'level2' in path:
                @drive.create_file(path)
                def create_file_callback(request):
                    pass


    This is going to call the `create_file_callback` function if operations
    need to be performed on `'/level1/level2'` or `'/level1/level2/file1.txt'`
    and it will call `default_create_file_callback` for all of the other
    files and folders.

    Now using the methods as methods instead of decorators. There is really only a
    single use case for this and that would be when you have a path specific function
    that handles a few paths but not all the paths on the drive. So instead of creating
    an new function on each iteration like i did in the example above it can be done this
    way.

    ..code-block::

        import dokan

        FILES_DIRECTORIES = (
            '/level1'
            '/level1/file1.txt'
            '/level1/file2.txt'
            '/level1/level2'
            '/level1/level2/file1.txt'
        )

        options = dokan.Options
        drive = dokan.Drive(options)

        @drive.create_file
        def default_create_file_callback(request):
            pass

        def create_file_callback(request):
            pass

        for path in FILES_DIRECTORIES:
            if 'level2' in path:
                drive.create_file(path)(create_file_callback)


    You have the ability to change any of teh callbacks at any time. I put
    into place a series of thread locks that allow the object that stores the
    callbacks to be altered without having 2 threads accessing it at the same time.

    If you want to remove a callback use the following code as an example how to.

    ..code-block::

        import dokan

        options = dokan.Options
        drive = dokan.Drive(options)

        @drive.create_file('./some/path/some.file')
        def create_file_some_path_some_file(request):
            pass

        drive.create_file('./some/path/some.file')


    and if you want to change the callback.

    ..code-block::

        import dokan

        options = dokan.Options
        drive = dokan.Drive(options)

        @drive.create_file('./some/path/some.file')
        def create_file_some_path_some_file(request):
            pass

        @drive.create_file('./some/path/some.file')
        def new_create_file_some_path_some_file(request):
            pass


    calling the method as a method and supplying the path will cause the library to remove any
    existing callback. If a function is supplied or the method is used as a decorator the old callback
    will be removed and the new one added.


    There are also these methods available that can only be supplied a single callback.

    * :py:meth:`Drive.free_disk_space`
    * :py:meth:`Drive.volume_information`
    * :py:meth:`Drive.mounted`
    * :py:meth:`Drive.unmounted`

    You do not have a "path" option these so they would be used in a manner like setting a default callback.

    """

    @staticmethod
    def __register_callback(container_lock, container, path):
        if path in container:
            with container_lock:
                del container[path]

        def wrapper(func):
            with container_lock:
                container[path] = func

            return func

        return wrapper

    def create_file(self, path):
        """
        Registers a callback for open and create operations on a file or directory.

        The callback is passed a :py:class:`CreateFileRequest` instance
        see :py:class:Drive for further details on how to use this method.
        """
        if callable(path):
            self.__default_create_file_callback = path
            return path

        res = self.__register_callback(
            self.__create_file_lock,
            self.__create_file_callbacks,
            path
        )
        return res

    def read_file(self, path):
        """
        Registers a callback for read operations on a file or directory.

        The callback is passed a :py:class:`ReadFileRequest` instance
        see :py:class:Drive for further details on how to use this method.
        """
        if callable(path):
            self.__default_read_file_callback = path
            return path

        res = self.__register_callback(
            self.__read_file_lock,
            self.__read_file_callbacks,
            path
        )
        return res

    def cleanup(self, path):
        """
        Registers a callback for cleanup operations on a file or directory.

        This is so an application can close any open handles.

        The callback is passed a :py:class:`CleanupRequest` instance
        see :py:class:Drive for further details on how to use this method.
        """
        if callable(path):
            self.__default_cleanup_callback = path
            return path

        res = self.__register_callback(
            self.__cleanup_lock,
            self.__cleanup_callbacks,
            path
        )
        return res

    def close_file(self, path):
        """
        Registers a callback for closing operations on a file.

        This is so an application knowns when to close an open file.
        The callback is passed a :py:class:`CloseFileRequest` instance
        see :py:class:Drive for further details on how to use this method.
        """
        if callable(path):
            self.__default_close_file_callback = path
            return path

        res = self.__register_callback(
            self.__close_file_lock,
            self.__close_file_callbacks,
            path
        )
        return res

    def write_file(self, path):
        """
        Registers a callback for write operations on a file.

        The callback is passed a :py:class:`WriteFileRequest` instance
        see :py:class:Drive for further details on how to use this method.
        """
        if callable(path):
            self.__default_write_file_callback = path
            return path

        res = self.__register_callback(
            self.__write_file_lock,
            self.__write_file_callbacks,
            path
        )
        return res

    def flush_file_buffers(self, path):
        """
        Registers a callback for flushing file buffers.

        When writing to a file if the OS wants to ensire the file has
        actually been written to.

        The callback is passed a :py:class:`FlushFileBuffersRequest` instance
        see :py:class:Drive for further details on how to use this method.
        """
        if callable(path):
            self.__default_flush_file_buffers_callback = path
            return path

        res = self.__register_callback(
            self.__flush_file_buffers_lock,
            self.__flush_file_buffers_callbacks,
            path
        )
        return res

    def file_information(self, path):
        """
        Registers a callback for the OS requesting information about a file or directory.

        The callback is passed a :py:class:`FileInformationRequest` instance
        see :py:class:Drive for further details on how to use this method.

        """
        if callable(path):
            self.__default_file_information_callback = path
            return path

        res = self.__register_callback(
            self.__file_information_lock,
            self.__file_information_callbacks,
            path
        )
        return res

    def file_attributes(self, path):
        """FileAttributesRequest"""
        if callable(path):
            self.__default_file_attributes_callback = path
            return path

        res = self.__register_callback(
            self.__file_attributes_lock,
            self.__file_attributes_callbacks,
            path
        )
        return res

    def file_time(self, path):
        """        FileTimeRequest

        """
        if callable(path):
            self.__default_file_time_callback = path
            return path

        res = self.__register_callback(
            self.__file_time_lock,
            self.__file_time_callbacks,
            path
        )
        return res

    def delete_file(self, path):
        """DeleteFileRequest"""
        if callable(path):
            self.__default_delete_file_callback = path
            return path

        res = self.__register_callback(
            self.__delete_file_lock,
            self.__delete_file_callbacks,
            path
        )
        return res

    def delete_directory(self, path):
        """DeleteDirectoryRequest"""
        if callable(path):
            self.__default_delete_directory_callback = path
            return path

        res = self.__register_callback(
            self.__delete_directory_lock,
            self.__delete_directory_callbacks,
            path
        )
        return res

    def move_file(self, path):
        """MoveFileRequest"""
        if callable(path):
            self.__default_move_file_callback = path
            return path

        res = self.__register_callback(
            self.__move_file_lock,
            self.__move_file_callbacks,
            path
        )
        return res

    def end_of_file(self, path):
        """EndOfFileRequest"""
        if callable(path):
            self.__default_end_of_file_callback = path
            return path

        res = self.__register_callback(
            self.__end_of_file_lock,
            self.__end_of_file_callbacks,
            path
        )
        return res

    def allocation_size(self, path):
        """AllocationSizeRequest"""
        if callable(path):
            self.__default_allocation_size_callback = path
            return path

        res = self.__register_callback(
            self.__allocation_size_lock,
            self.__allocation_size_callbacks,
            path
        )
        return res

    def lock_file(self, path):
        """LockFileRequest"""
        if callable(path):
            self.__default_lock_file_callback = path
            return path

        res = self.__register_callback(
            self.__lock_file_lock,
            self.__lock_file_callbacks,
            path
        )
        return res

    def unlock_file(self, path):
        """UnlockFileRequest"""
        if callable(path):
            self.__default_unlock_file_callback = path
            return path

        res = self.__register_callback(
            self.__unlock_file_lock,
            self.__unlock_file_callbacks,
            path
        )
        return res

    def get_file_security(self, path):
        """GetFileSecurityRequest"""
        if callable(path):
            self.__default_get_file_security_callback = path
            return path

        res = self.__register_callback(
            self.__get_file_security_lock,
            self.__get_file_security_callbacks,
            path
        )
        return res

    def set_file_security(self, path):
        """SetFileSecurityRequest"""
        if callable(path):
            self.__default_set_file_security_callback = path
            return path

        res = self.__register_callback(
            self.__set_file_security_lock,
            self.__set_file_security_callbacks,
            path
        )
        return res

    def find_files(self, path):
        if callable(path):
            self.__default_find_files_callback = path
            return path

        res = self.__register_callback(
            self.__find_files_lock,
            self.__find_files_callbacks,
            path
        )
        return res

    def find_files_with_pattern(self, path):
        if callable(path):
            self.__default_find_files_with_pattern_callback = path
            return path

        res = self.__register_callback(
            self.__find_files_with_pattern_lock,
            self.__find_files_with_pattern_callbacks,
            path
        )
        return res

    def find_streams(self, path):

        if callable(path):
            self.__default_find_streams_callback = path
            return path

        res = self.__register_callback(
            self.__find_streams_lock,
            self.__find_streams_callbacks,
            path
        )
        return res

    def free_disk_space(self, func):
        """GetDiskFreeSpaceRequest"""
        self.__free_disk_space_callback = func
        return func

    def volume_information(self, func):
        """GetVolumeInformationRequest"""
        self.__volume_information_callback = func
        return func

    def mounted(self, func):
        """MountedRequest"""
        self.__mounted_callback = func
        return func

    def unmounted(self, func):
        """UnmountedRequest"""
        self.__unmounted_callback = func
        return func

    def __init__(self, options):
        self.options = options

        self.__create_file_callbacks = {}
        self.__default_create_file_callback = None
        self.__create_file_lock = threading.Lock()

        self.__read_file_callbacks = {}
        self.__default_read_file_callback = None
        self.__read_file_lock = threading.Lock()

        self.__cleanup_callbacks = {}
        self.__default_cleanup_callback = None
        self.__cleanup_lock = threading.Lock()

        self.__close_file_callbacks = {}
        self.__default_close_file_callback = None
        self.__close_file_lock = threading.Lock()

        self.__write_file_callbacks = {}
        self.__default_write_file_callback = None
        self.__write_file_lock = threading.Lock()

        self.__flush_file_buffers_callbacks = {}
        self.__default_flush_file_buffers_callback = None
        self.__flush_file_buffers_lock = threading.Lock()

        self.__file_information_callbacks = {}
        self.__default_file_information_callback = None
        self.__file_information_lock = threading.Lock()

        self.__file_attributes_callbacks = {}
        self.__default_file_attributes_callback = None
        self.__file_attributes_lock = threading.Lock()

        self.__file_time_callbacks = {}
        self.__default_file_time_callback = None
        self.__file_time_lock = threading.Lock()

        self.__delete_file_callbacks = {}
        self.__default_delete_file_callback = None
        self.__delete_file_lock = threading.Lock()

        self.__delete_directory_callbacks = {}
        self.__default_delete_directory_callback = None
        self.__delete_directory_lock = threading.Lock()

        self.__move_file_callbacks = {}
        self.__default_move_file_callback = None
        self.__move_file_lock = threading.Lock()

        self.__end_of_file_callbacks = {}
        self.__default_end_of_file_callback = None
        self.__end_of_file_lock = threading.Lock()

        self.__allocation_size_callbacks = {}
        self.__default_allocation_size_callback = None
        self.__allocation_size_lock = threading.Lock()

        self.__lock_file_callbacks = {}
        self.__default_lock_file_callback = None
        self.__lock_file_lock = threading.Lock()

        self.__unlock_file_callbacks = {}
        self.__default_unlock_file_callback = None
        self.__unlock_file_lock = threading.Lock()

        self.__get_file_security_callbacks = {}
        self.__default_get_file_security_callback = None
        self.__get_file_security_lock = threading.Lock()

        self.__set_file_security_callbacks = {}
        self.__default_set_file_security_callback = None
        self.__set_file_security_lock = threading.Lock()

        self.__find_files_callbacks = {}
        self.__default_find_files_callback = None
        self.__find_files_lock = threading.Lock()

        self.__find_streams_callbacks = {}
        self.__default_find_streams_callback = None
        self.__find_streams_lock = threading.Lock()

        self.__find_files_with_pattern_callbacks = {}
        self.__default_find_files_with_pattern_callback = None
        self.__find_files_with_pattern_lock = threading.Lock()

        self.__free_disk_space_callback = None
        self.__volume_information_callback = None
        self.__mounted_callback = None
        self.__unmounted_callback = None
        self._thread = None

        self._is_mounted = False

    @property
    def is_mounted(self):
        return self._is_mounted

    def notify_create(self, path, is_directory):
        """
        Notify dokan that a file or a directory has been created.
        """
        return _dokan_h.DokanNotifyCreate(path, is_directory)

    def notify_delete(self, path, is_directory):
        """
        Notify dokan that a file or a directory has been deleted.
        """
        return _dokan_h.DokanNotifyDelete(path, is_directory)

    def notify_update(self, path):
        """
        Notify dokan that file or directory attributes have changed.
        """
        return _dokan_h.DokanNotifyUpdate(path)

    def notify_attribute_update(self, path):
        """
        Notify dokan that file or directory extended attributes have changed.
        """
        return _dokan_h.DokanNotifyXAttrUpdate(path)

    def notify_rename(self, old_path, new_path, is_directory, in_same_directory):
        """
        Notify dokan that a file or a directory has been renamed.

        This method supports in-place rename for file/directory within the same parent.
        """
        return _dokan_h.DokanNotifyRename(
            old_path,
            new_path,
            is_directory,
            in_same_directory
        )

    def __ZwCreateFile(
        self,
        FileName,
        SecurityContext,
        DesiredAccess,
        FileAttributes,
        ShareAccess,
        CreateDisposition,
        CreateOptions,
        DokanFileInfo
    ):

        (
            desired_access,
            file_attr_flags,
            create_disposition
        ) = _dokan_h.DokanMapKernelToUserCreateFileFlags(
            DesiredAccess,
            FileAttributes,
            CreateOptions,
            CreateDisposition
        )

        request = CreateFileRequest(
            FileName,
            SecurityContext,
            desired_access,
            file_attr_flags,
            ShareAccess,
            create_disposition,
            DokanFileInfo
        )
        # if path points to a file but DokanFileInfo.IsDirectory is set to
        # True return STATUS_NOT_A_DIRECTORY
        # if STATUS_OBJECT_NAME_COLLISION

        with self.__create_file_lock:
            callback = self.__create_file_callbacks.get(
                FileName,
                self.__default_create_file_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __Cleanup(
        self,
        FileName,
        DokanFileInfo
    ):
        request = CleanupRequest(
            FileName,
            DokanFileInfo
        )

        with self.__cleanup_lock:
            callback = self.__cleanup_callbacks.get(
                FileName,
                self.__default_cleanup_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __CloseFile(
        self,
        FileName,
        DokanFileInfo
    ):
        request = CloseFileRequest(
            FileName,
            DokanFileInfo
        )

        with self.__close_file_lock:
            callback = self.__close_file_callbacks.get(
                FileName,
                self.__default_close_file_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __ReadFile(
        self,
        FileName,
        Buffer,
        BufferLength,
        ReadLength,
        Offset,
        DokanFileInfo
    ):
        request = ReadFileRequest(
            FileName,
            Offset,
            Offset + BufferLength,
            DokanFileInfo
        )

        with self.__read_file_lock:
            callback = self.__read_file_callbacks.get(
                FileName,
                self.__default_read_file_callback
            )

        if callback is not None:
            res = callback(request)

            if res == STATUS_SUCCESS:
                data = request._data
                data_len = len(data)
                ReadLength.contents = _dokan_h.DWORD(data_len)
                data_buf = (ctypes.c_byte * data_len)(*data)
                ctypes.memmove(
                    ctypes.addressof(Buffer),
                    data_buf,
                    ctypes.sizeof(data_buf)
                )

            return res

        return STATUS_NOT_IMPLEMENTED

    def __WriteFile(
        self,
        FileName,
        Buffer,
        NumberOfBytesToWrite,
        NumberOfBytesWritten,
        Offset,
        DokanFileInfo
    ):
        buf = ctypes.POINTER(
            ctypes.c_byte * NumberOfBytesToWrite.value
        )
        buf_2 = ctypes.cast(Buffer, buf)

        data = []
        for i in range(NumberOfBytesToWrite.value):
            data += [buf_2.contents[i]]

        data = bytearray(data)

        request = WriteFileRequest(
            FileName,
            data,
            Offset.value,
            NumberOfBytesToWrite.value,
            DokanFileInfo
        )

        with self.__write_file_lock:
            callback = self.__write_file_callbacks.get(
                FileName,
                self.__default_write_file_callback
            )

        if callback is not None:
            res = callback(request)

            if res == STATUS_SUCCESS:
                NumberOfBytesWritten.contents.value = request._num_bytes_written

            return res

        return STATUS_NOT_IMPLEMENTED

    def __FlushFileBuffers(
        self,
        FileName,
        DokanFileInfo
    ):
        request = FlushFileBuffersRequest(
            FileName,
            DokanFileInfo
        )

        with self.__flush_file_buffers_lock:
            callback = self.__flush_file_buffers_callbacks.get(
                FileName,
                self.__default_flush_file_buffers_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __GetFileInformation(
        self,
        FileName,
        FileInformation,
        DokanFileInfo
    ):
        request = FileInformationRequest(
            FileName,
            FileInformation,
            DokanFileInfo
        )

        with self.__file_information_lock:
            callback = self.__file_information_callbacks.get(
                FileName,
                self.__default_file_information_callback
            )

        if callback is not None:
            res = callback(request)

            file_info = _dokan_h.BY_HANDLE_FILE_INFORMATION()
            dt_high = request._last_access_time >> 32
            dt_low = request._last_access_time & 0xFFFFFFFF
            lat = file_info.ftLastAccessTime

            lat.dwHighDateTime = dt_high
            lat.dwLowDateTime = dt_low

            dt_high = request._last_write_time >> 32
            dt_low = request._last_write_time & 0xFFFFFFFF
            lwt = file_info.ftLastWriteTime

            lwt.dwHighDateTime = dt_high
            lwt.dwLowDateTime = dt_low

            dt_high = request._creation_time >> 32
            dt_low = request._creation_time & 0xFFFFFFFF
            ct = file_info.ftCreationTime

            ct.dwHighDateTime = dt_high
            ct.dwLowDateTime = dt_low

            file_info.dwFileAttributes = request.attributes

            fs_high = request._file_size >> 32
            fs_low = request._file_size & 0xFFFFFFFF

            file_info.nFileSizeHigh = fs_high
            file_info.nFileSizeLow = fs_low

            file_info.nNumberOfLinks = request._number_of_links

            fi_high = request._file_index >> 32
            fi_low = request._file_index & 0xFFFFFFFF

            file_info.nFileIndexHigh = fi_high
            file_info.nFileIndexLow = fi_low
            FileInformation.contents = file_info

            return res

        return STATUS_NOT_IMPLEMENTED

    def __SetFileAttributes(
        self,
        FileName,
        FileAttributes,
        DokanFileInfo
    ):
        request = FileAttributesRequest(
            FileName,
            FileAttributes,
            DokanFileInfo
        )

        with self.__file_attributes_lock:
            callback = self.__file_attributes_callbacks.get(
                FileName,
                self.__default_file_attributes_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __SetFileTime(
        self,
        FileName,
        CreationTime,
        LastAccessTime,
        LastWriteTime,
        DokanFileInfo
    ):
        request = FileTimeRequest(
            FileName,
            CreationTime,
            LastAccessTime,
            LastWriteTime,
            DokanFileInfo
        )

        with self.__file_time_lock:
            callback = self.__file_time_callbacks.get(
                FileName,
                self.__default_file_time_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __DeleteFile(
        self,
        FileName,
        DokanFileInfo
    ):

        request = DeleteFileRequest(
            FileName,
            DokanFileInfo
        )

        with self.__delete_file_lock:
            callback = self.__delete_file_callbacks.get(
                FileName,
                self.__default_delete_file_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __DeleteDirectory(
        self,
        FileName,
        DokanFileInfo
    ):
        request = DeleteDirectoryRequest(
            FileName,
            DokanFileInfo
        )

        with self.__delete_directory_lock:
            callback = self.__delete_directory_callbacks.get(
                FileName,
                self.__default_delete_directory_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __MoveFile(
        self,
        FileName,
        NewFileName,
        ReplaceIfExisting,
        DokanFileInfo
    ):

        request = MoveFileRequest(
            FileName,
            NewFileName,
            bool(ReplaceIfExisting),
            DokanFileInfo
        )

        with self.__move_file_lock:
            callback = self.__move_file_callbacks.get(
                FileName,
                self.__default_move_file_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __SetEndOfFile(
        self,
        FileName,
        ByteOffset,
        DokanFileInfo
    ):
        request = EndOfFileRequest(
            FileName,
            ByteOffset.value,
            DokanFileInfo
        )

        with self.__end_of_file_lock:
            callback = self.__end_of_file_callbacks.get(
                FileName,
                self.__default_end_of_file_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __SetAllocationSize(
        self,
        FileName,
        AllocSize,
        DokanFileInfo
    ):
        request = AllocationSizeRequest(
            FileName,
            AllocSize.value,
            DokanFileInfo
        )

        with self.__allocation_size_lock:
            callback = self.__allocation_size_callbacks.get(
                FileName,
                self.__default_allocation_size_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __LockFile(
        self,
        FileName,
        ByteOffset,
        Length,
        DokanFileInfo
    ):
        request = LockFileRequest(
            FileName,
            ByteOffset.value,
            Length.value,
            DokanFileInfo
        )

        with self.__lock_file_lock:
            callback = self.__lock_file_callbacks.get(
                FileName,
                self.__default_lock_file_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __UnlockFile(
        self,
        FileName,
        ByteOffset,
        Length,
        DokanFileInfo
    ):
        request = UnlockFileRequest(
            FileName,
            ByteOffset.value,
            Length.value,
            DokanFileInfo
        )

        with self.__unlock_file_lock:
            callback = self.__unlock_file_callbacks.get(
                FileName,
                self.__default_unlock_file_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __GetDiskFreeSpace(
        self,
        FreeBytesAvailable,
        TotalNumberOfBytes,
        TotalNumberOfFreeBytes,
        DokanFileInfo
    ):

        request = DiskFreeSpaceRequest(
            FreeBytesAvailable,
            TotalNumberOfBytes,
            TotalNumberOfFreeBytes,
            DokanFileInfo
        )

        if self.__free_disk_space_callback is not None:
            res = self.__free_disk_space_callback(request)

            return res

        return STATUS_NOT_IMPLEMENTED

    def __GetVolumeInformation(
        self,
        VolumeNameBuffer,
        VolumeNameSize,
        VolumeSerialNumber,
        MaximumComponentLength,
        FileSystemFlags_,
        FileSystemNameBuffer,
        FileSystemNameSize,
        DokanFileInfo
    ):
        request = VolumeInformationRequest(
            VolumeNameSize,
            VolumeSerialNumber,
            MaximumComponentLength,
            FileSystemFlags_,
            FileSystemNameSize,
            DokanFileInfo
        )

        if self.__volume_information_callback is not None:
            res = self.__volume_information_callback(request)
            if res == STATUS_SUCCESS:
                volume_name = request.volume_name
                file_system_name = request.file_system_name
                vn_len = len(volume_name) + 1
                fsn_len = len(file_system_name) + 1

                volume_name = bytearray(volume_name, encoding='utf-8')
                volume_name += bytearray([0x0] * (33 - vn_len))

                volume_name = (_dokan_h.CHAR * 33)(*volume_name)
                ctypes.memmove(
                    ctypes.addressof(VolumeNameBuffer),
                    volume_name,
                    ctypes.sizeof(volume_name)
                )

                file_system_name = bytearray(file_system_name, encoding='utf-8')
                file_system_name += bytearray([0x0] * (11 - fsn_len))

                file_system_name = (_dokan_h.CHAR * 11)(*file_system_name)
                ctypes.memmove(
                    ctypes.addressof(FileSystemNameBuffer),
                    file_system_name,
                    ctypes.sizeof(file_system_name)
                )

                print(VolumeNameBuffer)
                print(FileSystemNameBuffer)

            return res
        return STATUS_NOT_IMPLEMENTED

    def __Mounted(self, DokanFileInfo):
        request = MountedRequest(DokanFileInfo)
        if self.__mounted_callback is not None:
            res = self.__mounted_callback(request)
            if res == STATUS_SUCCESS:
                self._is_mounted = True

            return res

        self._is_mounted = True
        return STATUS_SUCCESS

    def __Unmounted(self, DokanFileInfo):
        request = UnmountedRequest(DokanFileInfo)
        if self.__unmounted_callback is not None:
            res = self.__unmounted_callback(request)

            if res == STATUS_SUCCESS:
                self._is_mounted = False

            return res

        self._is_mounted = False
        return STATUS_SUCCESS

    def __GetFileSecurity(
        self,
        FileName,
        SecurityInformation,
        SecurityDescriptor,
        BufferLength,
        LengthNeeded,
        DokanFileInfo
    ):

        num_descriptors = BufferLength // ctypes.sizeof(_dokan_h.SECURITY_DESCRIPTOR)

        request = GetFileSecurityRequest(
            FileName,
            SecurityInformation,
            num_descriptors,
            DokanFileInfo
        )

        with self.__get_file_security_lock:
            callback = self.__get_file_security_callbacks.get(
                FileName,
                self.__default_get_file_security_callback
            )

        if callback is not None:
            res = callback(request)

            if res == STATUS_SUCCESS:
                for i, descriptor in enumerate(request.security_descriptors):
                    SecurityDescriptor.contents[i] = descriptor

                LengthNeeded.contents = _dokan_h.ULONG(
                    len(request.security_descriptors) *
                    ctypes.sizeof(_dokan_h.SECURITY_DESCRIPTOR)
                )

            return res

        return STATUS_NOT_IMPLEMENTED

    def __SetFileSecurity(
        self,
        FileName,
        SecurityInformation,
        SecurityDescriptor,
        BufferLength,
        DokanFileInfo
    ):

        security_descriptors = []
        for i in range(ctypes.sizeof(_dokan_h.SECURITY_DESCRIPTOR) // BufferLength.value):
            security_descriptors += [SecurityDescriptor.contents[i]]

        request = SetFileSecurityRequest(
            FileName,
            SecurityInformation,
            security_descriptors,
            DokanFileInfo
        )

        with self.__set_file_security_lock:
            callback = self.__set_file_security_callbacks.get(
                FileName,
                self.__default_set_file_security_callback
            )

        if callback is not None:
            return callback(request)

        return STATUS_NOT_IMPLEMENTED

    def __FindFiles(
            self,
            FileName,
            FillFindData,
            DokanFileInfo
    ):

        return STATUS_NOT_IMPLEMENTED

    def __FindFilesWithPattern(
            self,
            PathName,
            SearchPattern,
            FillFindData,
            DokanFileInfo
    ):

        return STATUS_NOT_IMPLEMENTED

    def __FindStreams(
            self,
            FileName,
            FillFindStreamData,
            DokanFileInfo
    ):
        return STATUS_NOT_IMPLEMENTED

    def mount(self, block=True):
        if self._thread is not None:
            raise AlreadyMountedError

        operations = _dokan_h.DOKAN_OPERATIONS()
        operations.ZwCreateFile = _dokan_h.ZW_CREATE_FILE(self.__ZwCreateFile)
        operations.Cleanup = _dokan_h.CLEANUP(self.__Cleanup)
        operations.CloseFile = _dokan_h.CLOSE_FILE(self.__CloseFile)
        operations.ReadFile = _dokan_h.READ_FILE(self.__ReadFile)
        operations.WriteFile = _dokan_h.WRITE_FILE(self.__WriteFile)
        operations.FlushFileBuffers = _dokan_h.FLUSH_FILE_BUFFERS(self.__FlushFileBuffers)
        operations.GetFileInformation = _dokan_h.GET_FILE_INFORMATION(self.__GetFileInformation)
        operations.FindFiles = _dokan_h.FIND_FILES(self.__FindFiles)
        operations.FindFilesWithPattern = _dokan_h.FIND_FILES_WITH_PATTERN(self.__FindFilesWithPattern)
        operations.SetFileAttributes = _dokan_h.SET_FILE_ATTRIBUTES(self.__SetFileAttributes)
        operations.SetFileTime = _dokan_h.SET_FILE_TIME(self.__SetFileTime)
        operations.DeleteFile = _dokan_h.DELETE_FILE(self.__DeleteFile)
        operations.DeleteDirectory = _dokan_h.DELETE_DIRECTORY(self.__DeleteDirectory)
        operations.MoveFile = _dokan_h.MOVE_FILE(self.__MoveFile)
        operations.SetEndOfFile = _dokan_h.SET_END_OF_FILE(self.__SetEndOfFile)
        operations.SetAllocationSize = _dokan_h.SET_ALLOCATION_SIZE(self.__SetAllocationSize)
        operations.LockFile = _dokan_h.LOCK_FILE(self.__LockFile)
        operations.UnlockFile = _dokan_h.UNLOCK_FILE(self.__UnlockFile)
        operations.GetDiskFreeSpace = _dokan_h.GET_DISK_FREE_SPACE(self.__GetDiskFreeSpace)
        operations.GetVolumeInformation = _dokan_h.GET_VOLUME_INFORMATION(self.__GetVolumeInformation)
        operations.Mounted = _dokan_h.MOUNTED(self.__Mounted)
        operations.Unmounted = _dokan_h.UNMOUNTED(self.__Unmounted)
        operations.GetFileSecurity = _dokan_h.GET_FILE_SECURITY(self.__GetFileSecurity)
        operations.SetFileSecurity = _dokan_h.SET_FILE_SECURITY(self.__SetFileSecurity)
        operations.FindStreams = _dokan_h.FIND_STREAMS(self.__FindStreams)

        res = [None]
        wait_event = threading.Event()

        def _do():
            result = _dokan_h.DokanMain(self.options, operations)
            if result == _dokan_h.DOKAN_ERROR:
                res[0] = DokanError
                wait_event.set()
            elif result == _dokan_h.DOKAN_DRIVE_LETTER_ERROR:
                res[0] = DriveLetterError
                wait_event.set()
            elif result == _dokan_h.DOKAN_DRIVER_INSTALL_ERROR:
                res[0] = DriverInstallError
                wait_event.set()
            elif result == _dokan_h.DOKAN_START_ERROR:
                res[0] = StartError
                wait_event.set()
            elif result == _dokan_h.DOKAN_MOUNT_ERROR:
                res[0] = MountError
                wait_event.set()
            elif result == _dokan_h.DOKAN_MOUNT_POINT_ERROR:
                res[0] = MountPointError
                wait_event.set()
            elif result == _dokan_h.DOKAN_VERSION_ERROR:
                res[0] = VersionError
                wait_event.set()

            self._thread = None

        if block:
            _do()
        else:
            self._thread = threading.Thread(target=_do)
            self._thread.daemon = True
            self._thread.start()
            wait_event.wait(2.0)

        if wait_event.is_set():
            raise res[0]
