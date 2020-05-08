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

from engine.objects.base_objects import FqdnObject, ReturnCode
from engine.objects.ftd.fdm_api_util import fdm_login, fdm_get_networks, fdm_get_ntp
from engine.objects.ftd.ftd_object import FtdObject
from engine.config import *


class FtdFqdnObject(FtdObject, FqdnObject):

    def __init__(self, origin_address: str, port: int = 0, fqdn: str = None, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD):
        FtdObject.__init__(self, origin_address, port, obj_name, username, password)
        FqdnObject.__init__(self, fqdn)

    def fetch_config(self) -> ReturnCode:
        if (self.name is not None) and (self.fqdn is not None):
            return ReturnCode.SUCCESS
        elif (self.name is None) and (self.fqdn is not None):
            return self.__fqdn_fetch()
        elif (self.name is not None) and (self.fqdn is None):
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
            if obj['subType'] == "FQDN":
                if obj['name'] == self.name:
                    self.fqdn = obj['value']
                    self.id = obj['id']
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND

    def __fqdn_fetch(self) -> ReturnCode:
        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)
        networks = fdm_get_networks(token,
                                    host=self.origin_addr,
                                    port=self.port,)

        for obj in networks['items']:
            if obj['subType'] == "FQDN":
                if obj['value'] == str(self.fqdn):
                    self.name = obj['name']
                    self.id = obj['id']
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND

    def ntp_usage(self) -> bool:
            if self.fqdn is None:
                return False

            token = fdm_login(host=self.origin_addr,
                              port=self.port,
                              username=self.username,
                              password=self.password)
            ntp = fdm_get_ntp(token,
                              host=self.origin_addr,
                              port=self.port)

            for i in ntp['items']:
                for ntp_server in i['ntpServers']:
                    if ntp_server == self.fqdn:
                        if i['enabled']:
                            return True

            return False
