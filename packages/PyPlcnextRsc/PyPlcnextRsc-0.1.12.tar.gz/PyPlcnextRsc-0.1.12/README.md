# PyPLCnextRsc

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Web](https://img.shields.io/badge/PLCnext-Website-blue.svg)](https://www.phoenixcontact.com/plcnext)
[![Community](https://img.shields.io/badge/PLCnext-Community-blue.svg)](https://www.plcnext-community.net)

**PyPLCnextRsc** is a simple ,yet elegant, RSC client library.

PyPLCnextRsc allows you to use RSC service extremely easily:

```python
from PyPlcnextRsc import *
from PyPlcnextRsc.Arp.Plc.Domain.Services import IPlcManagerService, PlcStartKind

if __name__ == "__main__":
    with Device('192.168.1.10', secureInfoSupplier=GUISupplierExample) as device:
        plc_manager_service = IPlcManagerService(device)  # Get PlcManagerService
        plc_manager_service.Stop()
        plc_manager_service.Start(PlcStartKind.Cold)
```

-----

## Resources

- [Documentation](https://pyplcnextrsc.readthedocs.io/) comprehensive documentation, tutorials, and examples.

**Recommended to build docs using Python 3.9**

## Environment

This module can be used **Remotely** ( PC,Server,Raspberry Pi ... ) or **Locally** ( on PLCnext device )

Requires: **Python>=3.7.6**

---

## Installing PyPLCnextRsc

```console
$ pip install -U PyPlcnextRsc
```
**Note** current the Pypi is only for test purpose , developers or users should always get latest version
at https://gitlab.phoenixcontact.com/SongYantao/pyplcnextrsc

## How to generate the latest doc ?

```console
$ pip install sphinx>=4.0.2
$ pip install sphinx_rtd_theme==0.5.1
$ cd docs
$ make html  

(for zh_CN version : python -m sphinx -T -E -b html -d build_zh_CN/doctrees -D language=zh_CH ./source build_zh_CN/html )
```


