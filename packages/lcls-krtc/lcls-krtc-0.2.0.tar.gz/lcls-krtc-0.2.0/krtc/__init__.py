from . import _version
from .krtc import KerberosTicket

__version__ = _version.get_versions()['version']

__all__ = ["KerberosTicket"]
