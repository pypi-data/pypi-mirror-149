# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.
from PyPlcnextRsc.common.serviceDefinition.all_needed import *

__all__ = [
    "FileSystemError",
    "Permissions",
    "Traits",
    "TraitItem",
    "FileSystemEntry",
    "FileSystemTraitsEntry",
    "SpaceInfo",
    "IFileSystemInfoService",
    "IFileService",
    "IDirectoryService",
]


@MarshalAs(rscType=RscType.Int32)
class FileSystemError(RscTpIntEnum):
    """This enum is used by several file operations."""

    NONE = 0
    """Success"""
    Unknown = 1
    """The error is not listed in this enumeration."""
    InvalidPath = 2
    """The path is invalid."""
    NotExist = 3
    """The path does not exist."""
    AlreadyExists = 4
    """The path already exists."""
    AccessDenied = 5
    """The file is already in use."""
    OutOfSpace = 6
    """There is not enough space on the Device left."""


@MarshalAs(rscType=RscType.Int32)
class Permissions(RscFlag):
    """
    Provides attributes for files and directories.

    """

    NONE = 0
    """NoPerms of posix"""
    OthersExe = 1
    """Execute/search permission, owner"""
    OthersWrite = 2
    """Write permission, owner"""
    OthersRead = 4
    """Read permission, owner"""
    OthersAll = 7
    """Read, Write, execute/search by owner; owner_read | owner_write | owner_exe"""
    GroupExe = 8
    """Execute/search permission, group"""
    GroupWrite = 16
    """Execute/search permission, group"""
    GroupRead = 32
    """Read permission, group"""
    GroupAll = 56
    """Read, Write, execute/search by group; group_read | group_write | group_exe"""
    OwnerExe = 64
    """Read permission, others"""
    OwnerWrite = 128
    """Write permission, others"""
    OwnerRead = 256
    """Execute/search permission, others"""
    OwnerAll = 448
    """Read, Write, execute/search by others; others_read | others_write | others_exe"""
    AllAll = 511
    """owner_all | group_all | others_all"""


@MarshalAs(rscType=RscType.Int32)
class Traits(RscFlag):
    """
    This enum is used by several file Services to specify the file traits to get or set, respectively.

    """
    NONE = 0
    """Not set."""
    Permissions = 1
    """Specifies the file permissions mask as Arp.System.Commons.Services.Io.Permissions mask."""
    LastWriteTime = 2
    """Specifies the time of last Write access or last modified time, respectively as System.DateTime in UTC"""
    Length = 4
    """Specifies the size of the file in bytes as System.Int64."""
    Crc32 = 8
    """Specifies the CRC32 value of the file as System.Int32."""


class TraitItem(RscStruct):
    """
    Specifies a file trait item

    """
    Trait: Traits
    """The file trait of this item."""
    Value: RscVariant
    """The value of the file info trait of this item."""


class FileSystemEntry(RscStruct):
    """
    This struct is used by file operations to reading of the file system entries.

    """

    Path: RscString512
    """The path of the file system entry (file or directory)"""
    IsFile: bool
    """The specified path ia a file."""
    IsDirectory: bool
    """The specified path is a directory."""


class FileSystemTraitsEntry(RscStruct):
    """
    This struct is used by file operations reading file informations from Device.

    """

    Path: RscString512
    """The path of the file."""
    IsFile: bool
    """The specified path ia a file."""
    IsDirectory: bool
    """The specified path ia a directory."""
    Traits: RscTpSequence[TraitItem]
    """The requested file traits of the file."""


class SpaceInfo(RscStruct):
    """
    This struct is used by file operations to reading of the space information.

    """

    Capacity: Uint64
    """Capacity space of the Device."""
    Free: Uint64
    """Free space of the Device."""
    Available: Uint64
    """Available space of the Device."""


@RemotingService('Arp.System.Commons.Services.Io.IFileSystemInfoService')
class IFileSystemInfoService:
    """
    A generic service to retrieve file system infos.

    """

    @RemotingMethod(1)
    def GetSupportedTraits(self) -> Traits:
        """
        Gets the supported traits.

        :return: The supported traits as bitset.
        :rtype: Traits

        """
        pass

    @RemotingMethod(2)
    def GetPermissions(self, path: RscString512) -> RscTpTuple[Permissions, FileSystemError]:
        """
        Gets the permissions of the specified path.

        :param path: The path to get the permissions from.
        :type path: str(max=512)
        :return:

            **tuple with 2 return values :**

            0. The permissions of the specified path.

            1. Result of the action.

        :rtype: tuple[Permissions, FileSystemError]

        """
        pass

    @RemotingMethod(3)
    def AddPermissions(self, path: RscString512, permissions: Permissions) -> FileSystemError:
        """
        Adds the permissions to the specified path.

        :param path: The path to get the permissions from.
        :type path: str(max=512)
        :param permissions: The permissions to add.
        :type permissions: Permissions
        :return: Result of the action.
        :rtype: FileSystemError

        """
        pass

    @RemotingMethod(4)
    def RemovePermissions(self, path: RscString512, permissions: Permissions) -> FileSystemError:
        """
        Removes the permissions of the specified path.

        :param path: The path to get the permissions from.
        :type path: str(max=512)
        :param permissions: The permissions to remove.
        :type permissions: Permissions
        :return: Result of the action.

        """
        pass

    @RemotingMethod(5)
    def GetFileSystemTraitsEntry(self, traits: Traits, path: RscString512) -> \
            RscTpTuple[
                FileSystemTraitsEntry,
                FileSystemError
            ]:
        """
        Gets the file system traits entry of the specified path.

        :param traits: The selection of traits to get.
        :type traits: Traits
        :param path: The path to get the file system traits entry from.
        :type path: str(max=512)
        :return:

            **tuple with 2 return values :**

            0. The file system traits entry of the specified path

            1. Result of the action.

        :rtype: tuple[FileSystemTraitsEntry,FileSystemError]

        """
        pass

    @RemotingMethod(6)
    def GetSpaceInfo(self, path: RscString512) -> RscTpTuple[SpaceInfo, FileSystemError]:
        """
        Gets the space information of the specified path.

        :param path: The path to get the file system traits entry from.
        :type path: str(max=512)
        :return:

            **tuple with 2 return values :**

            0. The space information of the specified path.

            1. Result of the action.

        :rtype: tuple[SpaceInfo, FileSystemError]

        """
        pass

    @RemotingMethod(7)
    def GetRootDirectories(self) -> RscTpTuple[RscString512]:
        """
        Gets a list of all root directories supported by the target.

        :return: A list of all root directories.
        :rtype: tuple[str]

        """
        pass


@RemotingService('Arp.System.Commons.Services.Io.IFileService')
class IFileService:
    """
    Provides common file operations for reading and writing files as well as deleting/moving/copying files on the Device.

    """

    @RemotingMethod(1)
    def Exists(self, path: RscString512) -> bool:
        """
        Checks if the specified file exists.

        :return: true if the file exists, otherwise false
        :rtype: bool

        """
        pass

    @RemotingMethod(2)
    def Write(self,
              filePath: RscString512,
              overwrite: bool,
              traitItems: RscTpSequence[TraitItem],
              data: RscStream) \
            -> FileSystemError:
        """
        Writes the given data to the specified file.

        :param filePath: Path of the file on the target.
        :type filePath: str(max=512)
        :param overwrite: If set to true the destination file is overwritten, if it yet exists, otherwise an error is returned.
        :type overwrite: bool
        :param traitItems: Trait items to set up after writing the file.
        :type traitItems: Sequence[TraitItem]
        :param data: Data to writing into the specified file.
        :type data: RscStream
        :return: Result of the action.
        :rtype: FileSystemError

        """
        pass

    @RemotingMethod(3)
    def Read(self, fileTraits: Traits, filePath: RscString512) -> \
            RscTpTuple[
                RscStream,
                RscTpTuple[TraitItem],
                FileSystemError
            ]:
        """
        Reads the specified file from Device.

        :param fileTraits: Specifies the file traits to Read, if this value is not :py:const:`PyPlcnextRsc.Arp.System.Commons.Services.Io.Traits.NONE`
        :type fileTraits: Traits
        :param filePath: The path of the file to Read
        :type filePath: str(max=512)
        :return:

            **tuple with 3 return values :**

            0. Data Read from the specified file.

            1. Specified trait items Read from the specified file.

            2. Result of the action.

        :rtype: tuple[RscStream,tuple[TraitItem],FileSystemError]

        """
        pass

    @RemotingMethod(4)
    def Delete(self, filePath: RscString512) -> FileSystemError:
        """
        Deletes the specified file.

        :param filePath: The path of the file to delete.
        :type filePath: str(max=512)
        :return: Result of the action.
        :rtype: FileSystemError

        """

    @RemotingMethod(5)
    def Move(self, createDirectory: bool, overwrite: bool, sourceFilePath: RscString512, destinationFilePath: RscString512) -> FileSystemError:
        """
        Moves the specified file.

        :param createDirectory: if set to true the directory of the file is created (recursively), if it does not exists yet.
        :type createDirectory: bool
        :param overwrite: 	if set to true the destination file is overwritten, if it yet exists, otherwise an error is returned.
        :type overwrite: bool
        :param sourceFilePath: The source path of the file to move.
        :type sourceFilePath: str(max=512)
        :param destinationFilePath: The destination path of the file to move.
        :type destinationFilePath: str(max=512)
        :return: Result of the action.
        :rtype: FileSystemError

        """
        pass

    @RemotingMethod(6)
    def Copy(self, createDirectory: bool, overwrite: bool, sourceFilePath: RscString512, destinationFilePath: RscString512) -> FileSystemError:
        """
        Copies the specified files.

        :param createDirectory: if set to true the directory of the file is created (recursively), if it does not exists yet.
        :type createDirectory: bool
        :param overwrite: If set to true the destination file is overwritten, if it yet exists, otherwise an error is returned.
        :type overwrite: bool
        :param sourceFilePath: The source path of the file to copy.
        :type sourceFilePath: str(max=512)
        :param destinationFilePath: The destination path of the file to copy.
        :type destinationFilePath: str(max=512)
        :return: Result of the action.
        :rtype: FileSystemError

        """
        pass


@RemotingService('Arp.System.Commons.Services.Io.IDirectoryService')
class IDirectoryService:
    """Provides common file directory operations."""

    @RemotingMethod(1)
    def Exists(self, path: RscString512) -> bool:
        """
        Checks if the specified directory exists.

        :param path: The path of the directory to check.
        :type path: str(max=512)
        :return: true if the directory exists, otherwise false.
        :rtype: bool

        """
        pass

    @RemotingMethod(2)
    def Create(self, path: RscString512) -> FileSystemError:
        """
        Creates the specified directory.

        :param path: The path of the directory to create.
        :type path: str(max=512)
        :return: Result of the action.
        :rtype: FileSystemError

        """
        pass

    @RemotingMethod(3)
    def Delete(self, path: RscString512) -> FileSystemError:
        """
        Deletes the specified directory and its content.

        :param path: The path of the directory to delete.
        :type path: str(max=512)
        :return: Result of the action.
        :rtype: FileSystemError

        """
        pass

    @RemotingMethod(4)
    def Clear(self, path: RscString512) -> FileSystemError:
        """
        Removes the content of the specified directory, but does not delete the specified directory itself.

        :param path: The path of the directory to clear.
        :type path: str(max=512)
        :return: Result of the action.
        :rtype: FileSystemError


        """
        pass

    @RemotingMethod(5)
    def Move(self, sourcePath: RscString512, destinationPath: RscString512, clear: bool = False) -> FileSystemError:
        """
        Moves the specified directory and its content to the given new location.

        :param sourcePath: The source path of the directory to move.
        :type sourcePath: str(max=512)
        :param destinationPath: The destination path of the directory to move all content to.
        :type destinationPath: str(max=512)
        :param clear:
            If set to true the destination location is cleared first if it yet exists and the operation succeeds anyway while returning true.
            Otherwise, if the destination yet exists, the operations fails and returns false.
        :type clear: bool
        :return: Result of the action.
        :rtype: FileSystemError

        """
        pass

    @RemotingMethod(6)
    def Copy(self, sourcePath: RscString512, destinationPath: RscString512, clear: bool = False) -> FileSystemError:
        """
        Copies the specified directory and its content to the given new location.

        :param sourcePath: The source path of the directory to copy.
        :type sourcePath: str(max=512)
        :param destinationPath: The destination path of the directory to copy all content to.
        :type destinationPath: str(max=512)
        :param clear:
            If set to true the destination location is cleared first if it yet exists and the operation succeeds anyway while returning true.
            Otherwise, if the destination yet exists, the operations fails and returns false.
        :type clear: bool
        :return: Result of the action.
        :rtype: FileSystemError

        """

    @RemotingMethod(7)
    def EnumerateFileSystemEntries(self, path: RscString512, searchPattern: RscString512, recursive: bool) -> RscEnumerator[FileSystemEntry]:
        """
        Enumerates all files and subdirectories of the specified directory.

        :param path: The path of the directory to search in.
        :type path: str(max=512)
        :param searchPattern: The pattern of the files to enumerate.
        :type searchPattern: str(max=512)
        :param recursive: If set to true the files of all subdirectories are liested as well.
        :type recursive: bool
        :return: A file system entry for each found file.
        :rtype: list[FileSystemEntry]

        """
        pass

    @RemotingMethod(8)
    def EnumerateFileSystemTraitsEntries(self, path: RscString512, searchPattern: RscString512, traits: Traits, recursive: bool) -> RscEnumerator[FileSystemTraitsEntry]:
        """
        Enumerates all files and subdirectories of the specified directory.

        :param path: The path of the directory to search in.
        :type path: str(max=512)
        :param searchPattern: The pattern of the files to enumerate.
        :type searchPattern: str(max=512)
        :param traits: The selection of traits to get.
        :type traits: Traits
        :param recursive: if set to true the files of all subdirectories are listed as well.
        :type recursive: bool
        :return: A file system trait entry for each found file.
        :rtype: list[FileSystemTraitsEntry]

        """
        pass
