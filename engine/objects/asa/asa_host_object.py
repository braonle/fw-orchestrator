from ipaddress import ip_address
import re

from engine.objects.base_objects import HostObject, ReturnCode
from engine.objects.asa.asa_cli_connection import asa_cli_command


class AsaHostObject(HostObject):

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
        self.raw_config = asa_cli_command(str(self.origin_addr), self.username, self.password, self.secret,
                                          command).rstrip()

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.ip_addr = ip_address(re.search("host (.*)", self.raw_config).group(1))
        return ReturnCode.SUCCESS

    def __addr_fetch(self) -> ReturnCode:
        command = "sh run obj in | i host " + str(self.ip_addr)
        self.raw_config = asa_cli_command(str(self.origin_addr), self.username, self.password, self.secret,
                                          command).rstrip()

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.name = re.search("object network (.*) host", self.raw_config).group(1)
        return ReturnCode.SUCCESS
