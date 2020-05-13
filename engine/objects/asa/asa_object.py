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
import paramiko
from typing import List, Set
from time import sleep
from engine.objects.base_objects import FwObject, AclEntry
from engine.config import *


class AsaObject(FwObject):

    BUFFER = 65535
    DELAY = 0.25

    raw_config: List[str]
    secret: str

    def __init__(self, origin_address: str, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        FwObject.__init__(self, origin_address, obj_name, username, password)
        self.secret = secret

    def cli_command(self, command: str) -> List[str]:

        pre_conn = paramiko.SSHClient()
        pre_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pre_conn.connect(str(self.origin_addr),
                    username=self.username,
                    password=self.password,
                            look_for_keys=False,
                    allow_agent=False)
        conn = pre_conn.invoke_shell()
        conn.recv(self.BUFFER)
        conn.send('enable\n')
        conn.send(self.secret + '\n')
        sleep(self.DELAY)
        conn.recv(self.BUFFER)

        conn.send(command + '\n')
        sleep(self.DELAY)
        output = conn.recv(self.BUFFER)

        lines = str(output).split("\\r\\n")
        # Popping command and prompt
        lines.pop(0)
        lines.pop(len(lines) - 1)

        pre_conn.close()

        return lines

    def dns_usage(self) -> bool:
        return False

    def ntp_usage(self) -> bool:
        return False

    def acl_usage(self) -> List[AclEntry]:
        lst = self._acl_usage_names(self.name)
        lst = lst.union(self._acl_usage_names(self._acl_attr_string()))
        res = []

        for x in lst:
            entries = self.cli_command("sho access-l " + x + " | i " + self._acl_attr_string())
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
        ace = self.cli_command(command)
        lst = []

        for x in ace:
            lst.append(re.search("access-list (\w+)", x).group(1))

        return set(lst)

    def hostname(self) -> str:
        return self.cli_command("sho hostname")[0]

    def systime(self) -> str:
        return self.cli_command("sho clock")[0]
