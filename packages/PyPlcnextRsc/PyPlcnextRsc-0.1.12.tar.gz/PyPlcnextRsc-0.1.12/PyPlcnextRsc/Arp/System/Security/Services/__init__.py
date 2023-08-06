# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.

from PyPlcnextRsc.Arp.System.Commons.Services.Io import FileSystemError
from PyPlcnextRsc.common.serviceDefinition.all_needed import *

__all__ = [
    "FileSystemError",  # Forward
    "AuthenticationError",
    "PasswordChangeError",
    "IPasswordAuthenticationService",
    "IPasswordConfigurationService2",
    "ISecureDeviceInfoService",
    "ISecuritySessionInfoService2",
]


@MarshalAs(rscType=RscType.Int32)
class AuthenticationError(RscTpIntEnum):
    """Defines values indicating success or failure of an attempt to create a security session."""
    NONE = 0
    """A new security session has been established successfully."""
    InvalidCredentials = -1
    """Authentication failed because name and / or password is not correct."""
    PeraltyDelayActive = -2
    """Authentication failed because a penalty delay is currently active."""
    DuplicateSession = -3
    """For this combination of user and rscClient there already exists a session."""
    SessionLimitReached = -4
    """The remote side's capacity does no allow to open more security sessions within this rscClient."""
    TryAgainLater = -5
    """The system is temporarily unable to answer authentication requests."""
    PasswordMustBeChanged = -6
    """The password is correct but it must be changed before a session is created."""


@MarshalAs(rscType=RscType.Int32)
class PasswordChangeError(RscTpIntEnum):
    """Defines values indicating success or failure of an attempt to create a security session."""
    NONE = 0
    """The password has been changed or set as desiged."""
    InvalidCredentials = -1
    """Authentication (during password change) failed because name and / or the (old) password is not correct."""
    PenaltyDelayActive = -2
    """Authentication (during password change) failed because a penalty delay is currently active in example due to too many failed authentication attempts."""
    NotSupportedForThisUser = -3
    """The (sub)system in use for authentication of the user does not support changing or (re)setting a password."""
    InsufficientNewPassword = -4
    """The password does not comply with security policies."""
    TryAgainLater = -5
    """The system is temporarily unable to answer authentication requests."""


@RemotingService(fullName='Arp.System.Security.Services.IPasswordAuthenticationService', serviceProviderName='Arp')
class IPasswordAuthenticationService:
    """
    This service allows a Remoting client to authenticate a user to the gateway (device) and by this start a security session on behalf of her or him.
    With PLCnext Technology authentication happens with usernames. But other kind of devices might not identify individual users but authenticate roles.
    Thus the name parameters given here in this service interface refer to role names or other kinds of identities then.

    """

    # @RemotingMethod(1)
    # def createSession(self,
    #                   username: Annotate[str, Marshal(rscStringEncoding=RscStringEncoding.Utf8, maxStringSize=64)],
    #                   password: Annotate[str, Marshal(rscType=RscType.SecureString, rscStringEncoding=RscStringEncoding.Utf8, maxStringSize=128)],
    #                   securityToken: RscOutParam[[SecurityToken], None],
    #                   penaltyDelayMillis: RscOutParam[[int], None]
    #                   ) -> AuthenticationError: ...

    @RemotingMethod(1)
    def createSession(self,
                      username: RscString64,  # The name of the role or user or other identity in question.
                      password: RscSecureString128,  # The password which is the proof that the client is allowed to act as the user (or role) specified with username.
                      ) -> \
            RscTpTuple[
                SecurityToken,
                int,
                AuthenticationError
            ]:
        """
        Starts a security context for a particular user or role known at the device.
        Every successful call (see return value) to this method creates a security session for a particular user (or role) at the RSC-gateway (device).
        Within the same rscClient a client can create several sessions. Sessions are identified by the securityToken provided by this method.
        But please check the T:Ade.CommonRemoting.IRemotingAdapter whether and how it allows to change the securityToken to use within the rscClient.
        First versions of this interface requires synchronization, so switching security sessions on a per call basis did not make sense for this because it is rather expensive.
        The maximum number of concurrent sessions is limited by the gatway's capacitiy (respectively the device's capacity) and therefore clients shall terminate sessions
        which they do not need any more, :py:func:`PyPlcnextRsc.Arp.System.Security.Services.IPasswordAuthenticationService.closeSession`.
        Sessions are automatically terminated whenever the corresponding Remoting rscClient is closed. Sessions cannot be used across channels.

        :param username: The name of the role or user or other identity in question,With PLCnext Technology the name has to be a username, not a role name.
        :param password: The password which is the proof that the client is allowed to act as the user (or role) specified with username.

                        Please note that the password is sensitive data. The caller must care for keeping it secret.
                        If the method implementation creates copies then it ensures they are erased from memory (i.e. overwritten with zeroes) before destruction and that each
                        copy is destructed at latest when the corresponding security context is closed.
        :return:

            **tuple with 3 return values :**

            0. securityToken - A value identifying the security session.
                The output value is only valid in case that the method has the return value
                :py:const:`PyPlcnextRsc.Arp.System.Security.Services.AuthenticationError.NONE` to indicate success.
                Then and only then a security session has been created which shall be closed by the client with a call to
                :py:func:`PyPlcnextRsc.Arp.System.Security.Services.IPasswordAuthenticationService.closeSession`
                once it is no longer needed. All security sessions which have been opened by the client during a
                Remoting connection are automatically closed whenever the Remoting connection is terminated.
                The value is intended to be passed to the Remoting sink of the communication rscClient, in example with every method call.
                Session context handles shall not be interpreted by the client. The client cannot derive any further meaning
                from the value.One exception: The value 0 (zero) is never returned by this  upon success.
                The value zero always identifies the default security session which is used when no particular security
                session has been established yet,in example right after the Remoting rscClient was established.
                Thus for safety reasons the out parameter securityToken is set to zero whenever this method indicates an error.

            1. penaltyDelayMillis - A timespan expressed in milliseconds for which further authentication attempts are rejected.
                The value is always 0 unless the method returns :py:const:`PyPlcnextRsc.Arp.System.Security.Services.PasswordChangeError.InvalidCredentials`.
                Then it is a positive value. A penalty delay is imposed to slow down brute force attacks.
                The penalty may be valid for a particular user attempting to change a password or to authenticate via
                a particular access path (TCP port, service, ...) or it may be valid for a group or even all users.
                The timespan is just an indication that subsequent authentication attempts may be rejected during this timespan.
                Please note that the accuracy of this value is questionable due to the latency which is introduced with its transmission.

            2. Upon success :py:const:`PyPlcnextRsc.Arp.System.Security.Services.AuthenticationError.NONE` is returned.
                Every other value indicates a failure.

        :rtype: tuple[SecurityToken,int,bool]

        """

    @RemotingMethod(2)
    def closeSession(self,
                     securityToken: SecurityToken
                     ):
        """
        Terminates a security session which was started at the gateway (device) by a former call to :py:class:`~PyPlcnextRsc.Arp.System.Security.Services.IPasswordAuthenticationService.createSession`


        :param securityToken: Security token as formerly returned by a successful session creation. It identifies the session which shall be closed.
        :type securityToken: SecurityToken

        """


@RemotingService(fullName='Arp.System.Security.Services.IPasswordConfigurationService2', serviceProviderName='Arp')
class IPasswordConfigurationService2:
    """
    This service allows to maintain passwords for existing users (password based authentication).

    """

    @RemotingMethod(1)
    def changePassword(self,
                       username: RscString64,  # The new who's password to change.
                       oldPassword: RscSecureString128,  # The old password for verification.
                       newPassword: RscSecureString128,  # The new password to set.
                       ) -> \
            RscTpTuple[
                int,
                PasswordChangeError
            ]:
        """
        This operation changes a password for a user.

        The method can even be called without prior authentication because it verifies the old password before it sets the new password.
        Support for calls without authentication is required to allow users to change their password even if the password has been locked in example because its usage period has expired.
        Systems which enforce password changes before and after password expiration then can allow anybody to call this method to unlock their password prior to the next authentication.

        :param username: The new who's password to change.
        :type username: str(max=64)
        :param oldPassword: The old password for verification.
        :type username: str(max=128)
        :param newPassword: The new password to set.
        :type username: str(max=128)
        :return:

            **tuple with 2 return values :**

            0. penaltyDelayMillis - A timespan expressed in milliseconds for which further authentication attempts are rejected.
                The value is always 0 unless the method returns :py:const:`PyPlcnextRsc.Arp.System.Security.Services.PasswordChangeError.InvalidCredentials`.
                Then it is a positive value. A penalty delay is imposed to slow down brute force attacks.
                The penalty may be valid for a particular user attempting to change a password or to authenticate via
                a particular access path (TCP port, service, ...) or it may be valid for a group or even all users.
                The timespan is just an indication that subsequent authentication attempts may be rejected during this timespan.

            1. Upon success :py:const:`PyPlcnextRsc.Arp.System.Security.Services.PasswordChangeError.NONE` is returned.
                Every other value indicates a failure.

        :rtype: tuple[int,PasswordChangeError]

        """

    @RemotingMethod(2)
    def setPassword(self,
                    username: RscString64,  # The name of the user for whom to override the password.
                    newPassword: RscSecureString128,  # The new password to set.
                    ) -> \
            PasswordChangeError:
        """
        This operation overrides the password for a user with administrative power.
        This operation is an administration function because it allows to change a password for a user without knowing it.
        Thus appropriate access control lists need to be in place and the method must only be callable for users with administrative rights.

        :param username:The name of the user for whom to override the password.
        :type username: str(max=64)
        :param newPassword: The new password to set.
        :type newPassword: str(max=128)

        :return: Upon success :py:const:'PyPlcnextRsc.Arp.System.Security.Services.PasswordChangeError.NONE' is returned.
            Every other value indicates a failure. The :py:const:'PyPlcnextRsc.Arp.System.Security.Services.PasswordChangeError.PenaltyDelayActive` is never returned by this method.
        :rtype: PasswordChangeError

        """
        pass


@RemotingService(fullName='Arp.System.Security.Services.ISecureDeviceInfoService', serviceProviderName='Arp')
class ISecureDeviceInfoService:
    """
    This service provides information about the access control which applies to the device without relation to any session or former authorization.

    """

    @RemotingMethod(1)
    def getSystemUseNotification(self) -> RscTpTuple[RscStream, FileSystemError]:
        """
        Provides a message for display to users before accessing the device that access restrictions apply and what the consequence of ignoring them is.
        The system use notification conventionally is needed due to legal issues. If an attacker has not been warned that he tries to abuse an access restricted device
        then much lower legal consequences he has to expect. So the message is intended for warning about entering an access restricted area (device) and which consequences
        it has if the area is entered without authorization. The message shall be displayed by clients to the user at the time the user establishes a session to the device.

        :return:

            **tuple with 2 return values :**

            0. The system use notification to display to users before they start a session to access the device.
                The message is provided as array of strings which need to be concatenated for display.
                The message is configured by the device owner. Which language it is depends on the owner.
                It is likely that the message contains the notification in several languages.

            1. An error indication whether the message could be provided correctly.

        :rtype: tuple[RscStream,FileSystemError]

        """
        pass


@RemotingService(fullName='Arp.System.Security.Services.ISecuritySessionInfoService2', serviceProviderName='Arp')
class ISecuritySessionInfoService2:
    """
    This service provides information about the access crontol which currently applies to the session and which was established
    for example with :py:class:`~PyPlcnextRsc.Arp.System.Security.Services.IPasswordAuthenticationService`.

    """

    @RemotingMethod(1)
    def getRoleNames(self) -> RscTpTuple[RscString128]:
        """
        Provides the set of roles which determines the kind of access which is granted.
        It is intended for use within error messages which explain why a particular access to the gateway (device) is currently not allowed.
        The role names may be cached for the lifetime of a security session. But a caller must not assume that with the next authentication attempt for the same user the roles will stay the same.

        :return: The names of the roles as they are associated with the current session at the gateway site (device site).
        :rtype: tuple[str]

        """
        pass

    @RemotingMethod(2)
    def isServiceCallAllowed(self,
                             provider: RscString128,
                             service: RscString128,
                             method: RscString128
                             ) -> bool:
        """
        Allows to determine which methods of which services can currently be called by this client within the current security session.
        Please note that the access which is granted depends on the current security context which applies to the session at the server site (device site).
        This is changed if the client authenticates to the server (another time) during the Remoting connection for example by using the :py:class:`PyPlcnextRsc.Arp.System.Security.Services.IPasswordAuthenticationService`.
        Clients may cache and re-use the infomation as long as a correspondig security session is valid.

        :param provider: Must be the name which identifies the provider of the service. The same service may be implemented by different providers.
        :type provider: str(max=128)
        :param service: Must be the name which identifies the service. Conventionally this is the fully qualified name of the C# interface which defines the service.
        :type service: str(max=128)
        :param method: Must be the number of the method.
        :type method: str(max=128)
        :return: A value which indicates whether the service method is allowed to be invoked or not.
        :rtype: bool

        """
        pass

    @RemotingMethod(3)
    def isUserAuthenticationRequired(self) -> bool:
        """
        Defines whether user authentication is required.
        At the device user authentication can be disabled with the effect that anything is allowed.

        :return: If user authentication is required true is returned and then without authentication nothing except authentication is allowed.
        :rtype: bool

        """
        pass

    @RemotingMethod(4)
    def isServiceCallAllowedOld(self,
                                provider: RscString128,
                                service: RscString128,
                                method: int) -> bool:
        """
        Allows to determine which methods of which services can currently be called by this client within the current security session.
        Please note that the access which is granted depends on the current security context which applies to the session at the server site (device site).
        This is changed if the client authenticates to the server (another time) during the Remoting connection for example by using the :py:class:`~PyPlcnextRsc.Arp.System.Security.Services.IPasswordAuthenticationService`.
        Clients may cache and re-use the infomation as long as a correspondig security session is valid.

        :param provider: Must be the name which identifies the provider of the service. The same service may be implemented by different providers.
        :type provider: str(max=128)
        :param service: Must be the name which identifies the service. Conventionally this is the fully qualified name of the C# interface which defines the service.
        :type service: str(max=128)
        :param method: Must be the number of the method.
        :type method: int
        :return: A value which indicates whether the service method is allowed to be invoked or not.
        :rtype: bool

        """
        pass
