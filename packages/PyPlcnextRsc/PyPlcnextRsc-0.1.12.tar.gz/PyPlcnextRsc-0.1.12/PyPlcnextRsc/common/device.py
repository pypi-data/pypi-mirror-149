# Copyright (c) 2021 Phoenix Contact. All rights reserved.
# Licensed under the MIT. See LICENSE file in the project root for full license information.
import warnings
from inspect import signature
from typing import Callable, Tuple, Optional
from PyPlcnextRsc.common.transport import RscClient

__all__ = ["ExtraConfigure", "Device", "GUISupplierExample", "ConsoleSupplierExample"]

_LOGO_ = """

             ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄       ▄  ▄▄▄▄▄▄▄▄▄▄▄ 
            ▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌▐░▌     ▐░▌▐░░░░░░░░░░░▌
            ▐░█▀▀▀▀▀▀▀█░▌▐░▌          ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀▀▀  ▐░▌   ▐░▌  ▀▀▀▀█░█▀▀▀▀ 
            ▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌▐░▌    ▐░▌▐░▌            ▐░▌ ▐░▌       ▐░▌     
            ▐░█▄▄▄▄▄▄▄█░▌▐░▌          ▐░▌          ▐░▌ ▐░▌   ▐░▌▐░█▄▄▄▄▄▄▄▄▄    ▐░▐░▌        ▐░▌     
            ▐░░░░░░░░░░░▌▐░▌          ▐░▌          ▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌    ▐░▌         ▐░▌     
            ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌          ▐░▌          ▐░▌   ▐░▌ ▐░▌▐░█▀▀▀▀▀▀▀▀▀    ▐░▌░▌        ▐░▌     
            ▐░▌          ▐░▌          ▐░▌          ▐░▌    ▐░▌▐░▌▐░▌            ▐░▌ ▐░▌       ▐░▌     
            ▐░▌          ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌     ▐░▐░▌▐░█▄▄▄▄▄▄▄▄▄  ▐░▌   ▐░▌      ▐░▌     
            ▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌▐░░░░░░░░░░░▌▐░▌     ▐░▌     ▐░▌     
             ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀       ▀       ▀      

██████╗ ██╗  ██╗ ██████╗ ███████╗███╗   ██╗██╗██╗  ██╗ ██████╗ ██████╗ ███╗   ██╗████████╗ █████╗  ██████╗████████╗
██╔══██╗██║  ██║██╔═══██╗██╔════╝████╗  ██║██║╚██╗██╔╝██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔════╝╚══██╔══╝
██████╔╝███████║██║   ██║█████╗  ██╔██╗ ██║██║ ╚███╔╝ ██║     ██║   ██║██╔██╗ ██║   ██║   ███████║██║        ██║   
██╔═══╝ ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║██║ ██╔██╗ ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██║██║        ██║   
██║     ██║  ██║╚██████╔╝███████╗██║ ╚████║██║██╔╝ ██╗╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╗   ██║   
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═╝                                                                                                     
"""

"""

Comprehensive documentation, tutorials, and examples:

        https://pyplcnextrsc.readthedocs.io/

"""


class _ConnectInfo:
    def __init__(self, ip: str, user: str = None, passwd: str = None, port: int = 41100, secureInfoSupplier: Callable[[Optional[dict]], Tuple[str, str]] = None):
        if user is None and passwd is not None:
            raise ValueError("Must provide user name")
        if user is not None and secureInfoSupplier is not None:
            raise ValueError("Only provide one method to provide secure info, not both !")
        if user:
            warnings.warn("Directly supply username and password is deprecated for security reasons, Use secureInfoSupplier instead !", DeprecationWarning, stacklevel=3)

        self._isNotificationNeeded = False
        if secureInfoSupplier:
            param_count = len(signature(secureInfoSupplier).parameters)
            if param_count == 1:
                self._isNotificationNeeded = True
            elif param_count != 0:
                raise TypeError("secureInfoSupplier should have zero or one param !")

        self._user_name = user
        self._password = passwd
        self._ip_address = ip
        self._port = port
        self._supplier = secureInfoSupplier

    def getSecureInfo(self, notification=None):
        if self._user_name == self._password is None:
            if not notification:
                security_info = self._supplier()
            else:
                security_info = self._supplier(notification)
        else:
            security_info = self._user_name, self._password
        if type(security_info) != tuple:
            raise ValueError(f"secureInfoSupplier must return tuple with username and password,but is {type(security_info)}")
        if len(security_info) != 2:
            raise ValueError(f"secureInfoSupplier must return tuple with 2 item,but is {len(security_info)}")
        for item in security_info:
            if type(item) != str:
                raise ValueError(f"secureInfoSupplier must return tuple with str type,but {type(item)} is in tuple")
        return security_info

    def isAuthenticationProvided(self):
        if self._user_name == self._password is None:
            return self._supplier is not None
        else:
            return self._password is not None

    def isNotificationNeeded(self):
        return self._isNotificationNeeded

    def getAddr(self):
        return self._ip_address, self._port


class ExtraConfigure:
    """
    Additional configure for RscClient

    + timeout   -   default is 10s

    + useTls  -   default is True

    + keepAlive_ms  -   default is 30000ms

    """

    def __init__(self):
        self.timeout = 10
        self.useTls = True
        self.keepAlive_ms = 30000


class Device:
    """
    PLCnext Device Object ,this is the main object for end-user.

    In order to get any RSC service , this object must be created and connect (log-in) successfully.

    .. warning::
            Always use *secureInfoSupplier* to supply security information instead of use 'user' and 'passwd' argument

    Usage:

        Typical way : using with-block for auto connect and dispose , and use *secureInfoSupplier* to provide secure login-information.

        .. code:: python

            from PyPlcnextRsc import Device, GUISupplierExample

            if __name__ == "__main__":
                with Device('192.168.1.10', secureInfoSupplier=GUISupplierExample) as device:
                    ...

    :param ip: the IP address of the target PLCnext for connecting
    :type ip: str
    :param user: user name for login if user authentication is enabled. (deprecated ,use secureInfoSupplier instead)
    :type user: str
    :param port: socket port of target , default is set to *41100*
    :type port: int
    :param passwd: passwd for login if user authentication is enabled. (deprecated ,use secureInfoSupplier instead)
    :type passwd: str
    :param config: additional setting for this client , such as switch of *TLS* and socket time-out
    :type config: :py:class:`~PyPlcnextRsc.device.ExtraConfigure`
    :param secureInfoSupplier: a callback function for getting secure info.
                            the function's signature can have no or only one argument,
                            if one argument is in signature,then during login period the details about
                            target (such as serial number ,firmware-version) will be passed by the argument

                            .. note::

                                The function will not be called if **user-authentication** is *disabled* on target PLCnext

    :type secureInfoSupplier: Callable[[Optional[dict]],Tuple[str,str]]

    :raises: #TODO
    """

    def __init__(self,
                 ip: str,
                 user: str = None,  # deprecated
                 passwd: str = None,  # deprecated
                 port: int = 41100,
                 config: ExtraConfigure = None,
                 secureInfoSupplier: Callable[
                     [
                         Optional[dict]  # Param is optional , is function signature has one parameter , then the detail information for connection will be feed in
                     ],
                     Tuple[
                         str,  # Username
                         str  # Passwd
                     ]
                 ] = None,
                 ):
        self._connectInfo = _ConnectInfo(ip, user, passwd, port, secureInfoSupplier)
        self._configure = config if config else ExtraConfigure()
        self._rscClient = RscClient(self._connectInfo, self._configure)
        warnings.warn("CURRENT ONLY FOR INTERNAL TEST USE !!!", FutureWarning, stacklevel=2)

    def connect(self):
        self._rscClient.connect()
        return self

    def dispose(self):
        if hasattr(self, "_rscClient"):  # in case that exception occur while construct Device
            self._rscClient.dispose()

    def getConnectInfo(self):
        return self._connectInfo

    def getConfigure(self):
        return self._configure

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()

        return False

    def __del__(self):
        self.dispose()


def ConsoleSupplierExample(detail):
    """
    A simple console interface for authentication login based on getpass module

    .. note::

        This will not be called if user-authentication is disabled.

        If is running by PyCharm , the ``getpass module``'s behavior is changed,
        the password will be echoed.
        This will not happen if you run this directly through python

    """
    import sys, getpass
    from io import StringIO
    def write(msg, flush=False):
        sys.stdout.write(msg)
        if flush:
            sys.stdout.flush()

    sio = StringIO(detail["Notification"])
    max_line_size = 0
    for line in sio.readlines():
        if len(line) > max_line_size:
            max_line_size = len(line)
    center = round(max_line_size / 2)
    write("***  SECURE DEVICE LOGIN  ***".center(max_line_size, '*') + "\n")
    write(detail["Notification"])
    write("-" * max_line_size + "\n")
    write("Device serial number  :  ".rjust(center) + detail["General.SerialNumber"] + '\n')
    write("Controller article name  :  ".rjust(center) + detail["General.ArticleName"] + '\n')
    write("Firmware version  :  ".rjust(center) + detail["General.Firmware.Version"] + '\n')
    write("-" * max_line_size + "\n")
    write("Username[admin]:", True)
    line = sys.stdin.readline()
    if " " in line:
        raise ValueError("should not contain space")
    if line in ('\n', '\r\n'):
        user_name = "admin"
    else:
        if line.endswith("\r\n"):
            line = line[0:-2]
        if line.endswith("\n"):
            line = line[0:-1]
        user_name = line

    if "sitecustomize" in sys.modules:
        # fix getpass for PyCharm
        import warnings
        print("Maybe this program is running in IDE (such as Pycharm), the behavior of 'getpass' is now changed", file=sys.stderr)
        getpass.getpass = getpass.fallback_getpass
        if hasattr(getpass, 'GetPassWarning'):
            warnings.simplefilter("ignore", category=getpass.GetPassWarning)
    return user_name, getpass.getpass(f"{user_name}@{detail['Address'][0]}'s password :")


def GUISupplierExample(detail):
    """
    A simple GUI for authentication login based on tkinter

    .. note::

        This GUI will not be called if user-authentication is disabled.

    """
    try:
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        raise ImportError(
            "Your Python doesn't have tkinter for GUI, this is usually happen on Linux, use 'sudo apt-get install python3-tk'"
        )
    GUISupplierExample.user = ""
    GUISupplierExample.password = ""
    WIDTH_INNER = 400
    WIDTH = 420
    HEIGHT = 500
    top = tk.Tk()
    top.title("***  SECURE DEVICE LOGIN  ***")
    top.resizable(False, False)
    screenwidth = top.winfo_screenwidth()
    screenheight = top.winfo_screenheight()
    top.geometry(f"{WIDTH}x{HEIGHT}+{int((screenwidth - WIDTH) / 2)}+{int((screenheight - HEIGHT) / 2)}")
    _frame = tk.Frame(top)
    _frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.NSEW)
    _DeviceInfoFrame = tk.LabelFrame(top, height=100, width=WIDTH_INNER, text="Device Info")
    _DeviceInfoFrame.grid_propagate(0)
    _DeviceInfoFrame.grid(row=0, column=0, padx=10, pady=5)
    tk.Label(_DeviceInfoFrame, text="Device serial number: " + detail["General.SerialNumber"]).grid(row=0, column=0, sticky=tk.W)
    tk.Label(_DeviceInfoFrame, text="Controller article name: " + detail["General.ArticleName"]).grid(row=1, column=0, sticky=tk.W)
    tk.Label(_DeviceInfoFrame, text="Firmware version: " + detail["General.Firmware.Version"]).grid(row=2, column=0, sticky=tk.W)
    _AuthenticationFrame = tk.LabelFrame(top, height=80, width=WIDTH_INNER, text="Authentication")
    _AuthenticationFrame.grid_propagate(0)
    _AuthenticationFrame.grid(row=1, column=0, padx=10, pady=5)
    tk.Label(_AuthenticationFrame, anchor=tk.W, text="Username:  ").grid(row=0, column=0, sticky=tk.W)
    userNameEntry = tk.Entry(_AuthenticationFrame, width=12)
    userNameEntry.grid(row=0, column=1, sticky=tk.W)
    userNameEntry.insert(0, "admin")
    tk.Label(_AuthenticationFrame, anchor=tk.W, text="Password:  ").grid(row=1, column=0, sticky=tk.W)
    passEntry = tk.Entry(_AuthenticationFrame, show="*", width=12)
    passEntry.grid(row=1, column=1, sticky=tk.W)

    def login_btn():
        GUISupplierExample.user = userNameEntry.get()
        GUISupplierExample.password = passEntry.get()
        top.quit()
        top.destroy()

    passEntry.bind("<Return>", lambda _: login_btn())
    userNameEntry.bind("<Return>", lambda _: login_btn())
    passEntry.focus_force()
    ttk.Button(_AuthenticationFrame, text="LOGIN", command=login_btn).grid(row=1, column=2, padx=50, pady=2)
    _NotificationFrame = tk.LabelFrame(top, height=280, width=WIDTH_INNER, text="Notification")
    _NotificationFrame.grid_propagate(0)
    _NotificationFrame.grid(row=2, column=0, padx=10, pady=5)
    tk.Label(_NotificationFrame, text=detail["Notification"], justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
    top.mainloop()
    return GUISupplierExample.user, GUISupplierExample.password
