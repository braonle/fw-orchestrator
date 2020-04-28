from ipaddress import IPv4Address, IPv4Network, ip_address
from enum import Enum

from engine.config import *


class ReturnCode(Enum):
    SUCCESS = 0
    OBJECT_NOT_FOUND = -1
    INVALID_FIELDS = -2
    NOT_INITIALIZED = -3


class ResultObject:
    obj_name: str
    origin_addr: IPv4Address
    acl_list: list
    dns: bool
    ntp: bool

   # def __str__(self):
     #  return str(self.)
        

class FwObject:
    name: str
    origin_addr: IPv4Address
    username: str
    password: str

    def __init__(self, origin_address: str, obj_name: str = None, username: str = USERNAME, password: str = PASSWORD):
        self.origin_addr = ip_address(origin_address)
        self.name = obj_name
        self.username = username
        self.password = password

    def fetch_config(self) -> ReturnCode:
        pass

    def dns_usage(self) -> bool:
        pass

    def ntp_usage(self) -> bool:
        pass

    def acl_usage(self) -> list:
        pass

    def usage(self) -> ResultObject:
        res = ResultObject()
        res.acl_list = self.acl_usage()
        res.dns = self.dns_usage()
        res.ntp = self.ntp_usage()
        res.obj_name = self.name
        res.origin_addr = self.origin_addr

        return res



class HostObject:
    ip_addr: IPv4Address

    def __init__(self, ip_addr: IPv4Address = None):
        self.ip_addr = ip_addr


class NetworkObject:
    prefix: IPv4Network

    def __init__(self, prefix: IPv4Network = None):
        self.prefix = prefix


class FqdnObject:
    fqdn: str

    def __init__(self, fqdn: str = None):
        self.fqdn = fqdn


class AddrRangeObject:
    first_addr: IPv4Address
    last_addr: IPv4Address

    def __init__(self, first: IPv4Address = None, last: IPv4Address = None):
        self.first_addr = first
        self.last_addr = last
