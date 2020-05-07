import re

from ipaddress import ip_network, IPv4Network
from typing import List

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
            self.raw_config = ""

    def __named_fetch(self) -> ReturnCode:
        command = "sh run obj in | i " + self.name + " subnet"
        self.raw_config = self.cli_command(command)

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.prefix = ip_network(re.search("subnet (.+)", self.raw_config).group(1).replace(" ", "/"))
        return ReturnCode.SUCCESS

    def __prefix_fetch(self) -> ReturnCode:
        command = "sh run obj in | i subnet " + str(self.prefix.network_address) + \
                    " " + str(self.prefix.netmask) + " "
        self.raw_config = self.cli_command(command)

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.name = re.search("object network (.+) subnet", self.raw_config).group(1)
        return ReturnCode.SUCCESS

    def acl_usage(self) -> List[AclEntry]:
        lst = super()._acl_usage_string(self.name)
        lst = lst.union(super()._acl_usage_string(str(self.prefix.network_address)))
        res = []

        for x in lst:
            entries = self.cli_command("sho access-l " + x + " " + str(self.prefix.network_address) + " | i " + str(self.prefix.network_address)).splitlines()
            hitcnt = 0
            for s in entries:
                hitcnt += int(re.search("\(hitcnt=([0-9]+)\)", s).group(1))

            acl = AclEntry()
            acl.acl_name = x
            acl.hit_count = hitcnt
            res.append(acl)

        return res

