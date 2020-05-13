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

from ipaddress import ip_network, IPv4Network
from engine.objects.asa.asa_object import AsaObject
from engine.objects.base_objects import NetworkObject, ReturnCode, AclEntry
from engine.config import *


class AsaNetworkObject(AsaObject, NetworkObject):

    def __init__(self, origin_address: str, prefix: IPv4Network = None, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        AsaObject.__init__(self, origin_address, obj_name, username, password, secret)
        NetworkObject.__init__(self, prefix)

    def fetch_config(self):
        if (self.name is None) and (self.prefix is not None):
            return self.__prefix_fetch()
        elif (self.name is not None) and (self.prefix is None):
            return self.__named_fetch()
        else:
            self.raw_config = []

    def __named_fetch(self) -> ReturnCode:
        command = "sh run obj in | i " + self.name + " subnet"
        self.raw_config = self.cli_command(command)

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.prefix = ip_network(re.search("subnet (.+)", self.raw_config[0]).group(1).replace(" ", "/"))
        return ReturnCode.SUCCESS

    def __prefix_fetch(self) -> ReturnCode:
        command = "sh run obj in | i subnet " + str(self.prefix.network_address) + \
                    " " + str(self.prefix.netmask) + " "
        self.raw_config = self.cli_command(command)

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.name = re.search("object network (.+) subnet", self.raw_config[0]).group(1)
        return ReturnCode.SUCCESS

    def _acl_attr_string(self) -> str:
        return str(self.prefix.network_address) + " " + str(self.prefix.netmask)

