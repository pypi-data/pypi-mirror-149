# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.common.serviceDefinition.all_needed import *


@MarshalAs(rscType=RscType.Uint8)
class BackupError(RscTpIntEnum):
    """
    Possible error codes for retain rsc services.

    """

    NONE = 0
    """Function call succeeded."""
    UnableToWriteFile = 1
    """Error when writing the backup file, e.g. no permission or out of memory."""
    UnableToReadFile = 2
    """Error when reading the backup file, e.g. no permission."""
    NoRetainData = 3
    """No retain data exists to create a backup."""
    CrcFileMismatch = 4
    """Crc mismatch while reading a the backup file."""
    NoSuchFile = 5
    """No backup file exists."""
    LayoutMismatch = 6
    """The backup data layout does not match the project."""
    InvalidVersion = 7
    """The backup file is not valid."""
    InvalidFile = 8
    """The variable type is not supported.   """
    Unspecified = 255
    """Unspecified error. See log file for more information."""
    UnvalidSubscription = 10


class BackupResult(RscStruct):
    """
    Contains the name and error code of the backup.

    """

    FileName: RscString512
    """Name of the backup file."""

    Error: BackupError
    """Contains the to be written data."""



@RemotingService('Arp.Plc.Retain.Services.IRetainManagerService')
class IRetainManagerService:
    """
    Use this service for the retain backup handling.
    """

    @RemotingMethod(1)
    def GenerateBackupFile(self) -> BackupResult:
        """
        Generates a backup file of the retain data

        Generates a backup file of all configured retain data including a header with several information e.g. version, project name, hw name, fw version, etc.
        The backup file is stored in the configured retain backup path. The name of the backup file is generated from the time of
        creation with the suffix '_USER'. E.g.: 2020_06_02_14_44_23_User

        :return: A result item which contains the created backup file name and an error code.
        :rtype: BackupResult

        """
        pass

    @RemotingMethod(2)
    def PrepareLatestBackupFileForRestoring(self) -> BackupResult:
        """
        Prepares the latest backup file of retain data for restoring for the next plc 'RestoreWarm' start

        Prepares the retain data of the lastest retain backup file based on the name,which is contained in the configured retain backup path and matched to the format defined.
        On the next 'RestoreWarm' start the prepared backup data is used instead of the data from the retain memory.
        The prepared backup will be cleared at each plc start (Cold, Warm, Hot, RestoreWarm), DCG and PlcReset.

        :return: An item which contains the prepared backup file name and an error code.
        :rtype: BackupResult

        """
        pass