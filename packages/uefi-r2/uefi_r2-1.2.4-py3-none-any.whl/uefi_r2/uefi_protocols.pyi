from typing import Any, Dict
from uefi_r2.uefi_types import UefiGuid as UefiGuid

PROTOCOLS_GUIDS: Any
GUID_FROM_VALUE: Dict[str, UefiGuid]
GUID_FROM_BYTES: Dict[bytes, UefiGuid]
