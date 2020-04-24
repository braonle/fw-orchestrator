from ipaddress import IPv4Address, IPv4Network, ip_address
from enum import Enum

from engine.config import *


class ReturnCode(Enum):
    SUCCESS = 0
    OBJECT_NOT_FOUND = -1
    INVALID_FIELDS = -2


class FwObject:
    name: str
    origin_addr: IPv4Address
    port: int
    raw_config: str
    username: str
    password: str
    secret: str

    def __init__(self, origin_address: str, port: int = None, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        self.origin_addr = ip_address(origin_address)
        self.port = port
        self.name = obj_name
        self.username = username
        self.password = password
        self.secret = secret

    def fetch_config(self) -> ReturnCode:
        pass


class HostObject(FwObject):
    ip_addr: IPv4Address

    def __init__(self, origin_address: str, port: int = None,
                  obj_name: str = None, ip_addr: IPv4Address = None,
                  username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        super().__init__(origin_address, port, obj_name, username, password, secret)
        self.ip_addr = ip_addr


class NetworkObject(FwObject):
    prefix: IPv4Network

    def __init__(self, origin_address: str, port: int = None,
                  obj_name: str = None, prefix: IPv4Network = None,
                  username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        super().__init__(origin_address, port, obj_name, username, password, secret)
        self.prefix = prefix


class FqdnObject(FwObject):
    fqdn: str

    def __init__(self, origin_address: str, port: int = None,
                  obj_name: str = None, fqdn: str = None,
                  username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        super().__init__(origin_address, port, obj_name, username, password, secret)
        self.fqdn = fqdn


class AddrRangeObject(FwObject):
    first_addr: IPv4Address
    last_addr: IPv4Address

    def __init__(self, origin_address: str, port: int = None,
                  obj_name: str = None, first: IPv4Address = None, last: IPv4Address = None,
                  username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        super().__init__(origin_address, port, obj_name, username, password, secret)
        self.first_addr = first
        self.last_addr = last
