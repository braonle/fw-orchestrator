from ipaddress import ip_address, IPv4Address
import re

from engine.objects.base_objects import HostObject, ReturnCode
from engine.objects.asa.asa_object import AsaObject
from engine.config import *


class AsaHostObject(AsaObject, HostObject):

    def __init__(self, origin_address: str, ip_addr: IPv4Address = None, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        AsaObject.__init__(self, origin_address, obj_name, username, password, secret)
        HostObject.__init__(self, ip_addr)

    def fetch_config(self):
        if (self.name is None) and (self.ip_addr is not None):
            return self.__addr_fetch()
        elif (self.name is not None) and (self.ip_addr is None):
            self.__named_fetch()
            return ReturnCode.SUCCESS
        else:
            self.raw_config = ""
            return ReturnCode.INVALID_FIELDS

    def __named_fetch(self) -> ReturnCode:
        command = "sh run obj in | i " + self.name + " host"
        self.raw_config = self.cli_command(command)

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.ip_addr = ip_address(re.search("host (.+)", self.raw_config).group(1))
        return ReturnCode.SUCCESS

    def __addr_fetch(self) -> ReturnCode:
        command = "sh run obj in | i host " + str(self.ip_addr)
        self.raw_config = self.cli_command(command)

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.name = re.search("object network (.+) host", self.raw_config).group(1)
        return ReturnCode.SUCCESS

    def dns_usage(self) -> bool:
        if self.ip_addr is None:
            return False

        command = "sho run dns server | i " + str(self.ip_addr)
        return len(self.cli_command(command)) != 0

    def ntp_usage(self) -> bool:
        if self.ip_addr is None:
            return False

        command = "sho run ntp | i " + str(self.ip_addr)
        return len(self.cli_command(command)) != 0

    def acl_usage(self) -> list:
        lst = super().acl_usage()
        lst = lst + super()._acl_usage_string(str(self.ip_addr))

        return list(set(lst))
