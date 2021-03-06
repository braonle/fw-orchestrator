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

from typing import List
from engine.objects.base_objects import FwObject, AclEntry
from engine.objects.ftd.fdm_api_util import (fdm_login, fdm_get_access_policies,
    fdm_get_access_rules, fdm_get_hostnames, fdm_get_hitcount)
from engine.config import *


class FtdObject(FwObject):

    port: int
    id: str

    def __init__(self, origin_address: str, port: int = 443, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD,  id = None):
        FwObject.__init__(self, origin_address, obj_name, username, password)
        self.port = port
        self.id = id

    def dns_usage(self) -> bool:
        return False

    def ntp_usage(self) -> bool:
        return False

    def acl_usage(self) -> List[AclEntry]:
        if self.id is None:
            return []

        lst = []

        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)
        accesspolicies = fdm_get_access_policies(token,
                                                 host=self.origin_addr,
                                                 port=self.port)
        for accesspolicy in accesspolicies['items']:
            accessrules = fdm_get_access_rules(token,
                                               host=self.origin_addr,
                                               port=self.port,
                                               access_policy_id=accesspolicy['id'])
            for accessrule in accessrules['items']:
                for src in accessrule['sourceNetworks']:
                    if src['id'] == self.id:
                        obj = AclEntry()
                        obj.acl_name = f"{accesspolicy['name']}: {accessrule['name']}"
                        hitcount = fdm_get_hitcount(token,
                                                    host=self.origin_addr,
                                                    port=self.port,
                                                    access_policy_id=accesspolicy['id'],
                                                    access_rule_id=accessrule['id'])
                        obj.hit_count = hitcount['items'][0]['hitCount']
                        lst.append(obj)
                for dest in accessrule['destinationNetworks']:
                    if dest['id'] == self.id:
                        obj = AclEntry()
                        obj.acl_name = f"{accesspolicy['name']}: {accessrule['name']}"
                        hitcount = fdm_get_hitcount(token,
                                                    host=self.origin_addr,
                                                    port=self.port,
                                                    access_policy_id=accesspolicy['id'],
                                                    access_rule_id=accessrule['id'])
                        obj.hit_count = hitcount['items'][0]['hitCount']
                        lst.append(obj)

        return lst


    def hostname(self) -> str:
        hostname = ""

        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)

        hostnames = fdm_get_hostnames(token,
                                      host=self.origin_addr,
                                      port=self.port)

        if hostnames['paging']['count'] > 0:
            hostname = hostnames['items'][0]['hostname']

        return hostname
