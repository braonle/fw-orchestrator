from enum import Enum


class DeviceTypes(Enum):
    ASA = 1
    FTD = 2


class Device:
    type: DeviceTypes
    ip_addr: str

    def __init__(self, type: DeviceTypes, address: str):
        self.ip_addr = address
        self.type = type