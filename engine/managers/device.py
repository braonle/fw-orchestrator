from enum import Enum
from ipaddress import IPv4Address, ip_address


class DeviceTypes(Enum):
    ASA = 1
    FTD = 2


class Device:
    type: DeviceTypes
    ip_addr: IPv4Address

    def __init__(self, type: DeviceTypes, address: str):
        self.ip_addr = ip_address(address)
        self.type = type