#
#	Copyright (c) 2020 Cisco and/or its affiliates.
#
#	This software is licensed to you under the terms of the Cisco Sample
#	Code License, Version 1.1 (the "License"). You may obtain a copy of the
#	License at
#
#		       https://developer.cisco.com/docs/licenses
#
#	All use of the material herein must be in accordance with the terms of
#	the License. All rights not expressly granted by the License are
#	reserved. Unless required by applicable law or agreed to separately in
#	writing, software distributed under the License is distributed on an "AS
#	IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#	or implied.
#

from ipaddress import IPv4Address, IPv4Network, ip_address
from enum import Enum
from typing import List

from engine.config import *


class ReturnCode(Enum):
    SUCCESS = 0
    OBJECT_NOT_FOUND = -1
    INVALID_FIELDS = -2
    NOT_INITIALIZED = -3


class AclEntry:
    acl_name: str
    hit_count: int

    def __str__(self):
        return self.acl_name + " hit " + str(self.hit_count)


class ResultObject:
    obj_name: str
    origin_addr: IPv4Address
    acl_list: List[AclEntry]
    dns: bool
    ntp: bool


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

    def acl_usage(self) -> List[AclEntry]:
        pass

    def usage(self) -> ResultObject:
        res = ResultObject()
        res.acl_list = self.acl_usage()
        res.dns = self.dns_usage()
        res.ntp = self.ntp_usage()
        res.obj_name = self.name
        res.origin_addr = self.origin_addr

        return res

    def hostname(self) -> str:
        pass

    def systime(self) -> str:
        pass


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
