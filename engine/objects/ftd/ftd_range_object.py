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

import re
from ipaddress import ip_address, IPv4Address
from engine.objects.base_objects import AddrRangeObject, ReturnCode
from engine.objects.ftd.fdm_api_util import fdm_login, fdm_get_networks
from engine.objects.ftd.ftd_object import FtdObject
from engine.config import *


class FtdRangeObject(FtdObject, AddrRangeObject):

    range_regex = r"\b(?P<first_addr>(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.){3}" \
                  r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))\b" \
                  r".*-.*" \
                  r"\b(?P<last_addr>(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.){3}" \
                  r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))\b"

    def __init__(self, origin_address: str, port: int = 0, first: IPv4Address = None, last: IPv4Address = None,
                 obj_name: str = None, username: str = USERNAME, password: str = PASSWORD):
        FtdObject.__init__(self, origin_address, port, obj_name, username, password)
        AddrRangeObject.__init__(self, first, last)

    def fetch_config(self) -> ReturnCode:
        if (self.name is not None) and not (self.first_addr is None or self.last_addr is None):
            return ReturnCode.SUCCESS
        elif (self.name is None) and not (self.first_addr is None or self.last_addr is None):
            return self.__range_fetch()
        elif (self.name is not None) and (self.first_addr is None or self.last_addr is None):
            return self.__named_fetch()
        else:
            return ReturnCode.OBJECT_NOT_FOUND


    def __named_fetch(self) -> ReturnCode:
        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)
        networks = fdm_get_networks(token,
                                    host=self.origin_addr,
                                    port=self.port,)

        for obj in networks['items']:
            if obj['subType'] == "RANGE":
                if obj['name'] == self.name:
                    first_addr = re.search(self.range_regex, obj['value']).group("first_addr")
                    last_addr = re.search(self.range_regex, obj['value']).group("last_addr")
                    self.first_addr = ip_address(first_addr)
                    self.last_addr = ip_address(last_addr)
                    self.id = obj['id']
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND

    def __range_fetch(self) -> ReturnCode:
        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)
        networks = fdm_get_networks(token,
                                    host=self.origin_addr,
                                    port=self.port,)

        for obj in networks['items']:
            if obj['subType'] == "RANGE":
                first_addr = re.search(self.range_regex, obj['value']).group("first_addr")
                last_addr = re.search(self.range_regex, obj['value']).group("last_addr")
                if ip_address(first_addr) == self.first_addr \
                    and ip_address(last_addr) == self.last_addr:
                    self.name = obj['name']
                    self.id = obj['id']
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND
