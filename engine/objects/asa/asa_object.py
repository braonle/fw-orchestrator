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
from typing import List, Set
from netmiko import ConnectHandler
from engine.objects.base_objects import FwObject, AclEntry
from engine.config import *


class AsaObject(FwObject):

    raw_config: str
    secret: str

    def __init__(self, origin_address: str, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        FwObject.__init__(self, origin_address, obj_name, username, password)
        self.secret = secret

    def cli_command(self, command: str) -> str:
        device_params = {
            'device_type': 'cisco_asa',
            'ip': str(self.origin_addr),
            'username': self.username,
            'password': self.password,
            'secret': self.secret
        }

        result = ""

        with ConnectHandler(**device_params) as ssh:
            ssh.enable()
            result = ssh.send_command(command).rstrip()

        return result

    def dns_usage(self) -> bool:
        return False

    def ntp_usage(self) -> bool:
        return False

    def acl_usage(self) -> List[AclEntry]:
        lst = self._acl_usage_names(self.name)
        lst = lst.union(self._acl_usage_names(self._acl_attr_string()))
        res = []

        for x in lst:
            entries = self.cli_command("sho access-l " + x + " | i " + self._acl_attr_string()).splitlines()
            hitcnt = 0
            for s in entries:
                expr = re.search("\(hitcnt=([0-9]+)\)", s)
                if expr is not None:
                    hitcnt += int(expr.group(1))

            acl = AclEntry()
            acl.acl_name = x
            acl.hit_count = hitcnt
            res.append(acl)

        return res

    def _acl_attr_string(self) -> str:
        pass

    def _acl_usage_names(self, command_key) -> Set[str]:
        command = "sho run access-list | i " + command_key
        ace = self.cli_command(command).splitlines()
        lst = []

        for x in ace:
            lst.append(re.search("access-list (\w+)", x).group(1))

        return set(lst)

    def hostname(self) -> str:
        return self.cli_command("sho hostname")

    def systime(self) -> str:
        return self.cli_command("sho clock")
