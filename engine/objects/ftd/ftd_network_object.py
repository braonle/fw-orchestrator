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

from ipaddress import ip_network, IPv4Network
from engine.objects.base_objects import NetworkObject, ReturnCode
from engine.objects.ftd.fdm_api_util import fdm_login, fdm_get_networks
from engine.objects.ftd.ftd_object import FtdObject
from engine.config import *


class FtdNetworkObject(FtdObject, NetworkObject):

    def __init__(self, origin_address: str, port: int = 0, prefix: IPv4Network = None, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD):
        FtdObject.__init__(self, origin_address, port, obj_name, username, password)
        NetworkObject.__init__(self, prefix)

    def fetch_config(self) -> ReturnCode:
        if (self.name is not None) and (self.prefix is not None):
            return ReturnCode.SUCCESS
        elif (self.name is None) and (self.prefix is not None):
            return self.__prefix_fetch()
        elif (self.name is not None) and (self.prefix is None):
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
            if obj['subType'] == "NETWORK":
                if obj['name'] == self.name:
                    self.prefix = ip_network(obj['value'])
                    self.id = obj['id']
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND

    def __prefix_fetch(self) -> ReturnCode:
        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)
        networks = fdm_get_networks(token,
                                    host=self.origin_addr,
                                    port=self.port,)

        for obj in networks['items']:
            if obj['subType'] == "NETWORK":
                if obj['value'] == str(self.prefix):
                    self.name = obj['name']
                    self.id = obj['id']
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND
