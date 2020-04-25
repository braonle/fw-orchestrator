import re

from ipaddress import ip_address, IPv4Address
from engine.objects.asa.asa_object import AsaObject
from engine.objects.base_objects import AddrRangeObject, ReturnCode
from engine.config import *


class AsaRangeObject(AsaObject, AddrRangeObject):

    def __init__(self, origin_address: str, first: IPv4Address = None, last: IPv4Address = None,
                 obj_name: str = None, username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        AsaObject.__init__(self, origin_address, obj_name, username, password, secret)
        AddrRangeObject.__init__(self, first, last)

    def fetch_config(self):
        if (self.name is None) and not (self.first_addr is None or self.last_addr is None):
            return self.__range_fetch()
        elif (self.name is not None) and (self.first_addr is None and self.last_addr is None):
            return self.__named_fetch()
        else:
            self.raw_config = ""
            return ReturnCode.INVALID_FIELDS

    def __named_fetch(self) -> ReturnCode:
        command = "sh run obj in | i " + self.name + " range"
        self.raw_config = self.cli_command(command)

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        (first, last) = re.search("range (.+)", self.raw_config).group(1).split()
        self.first_addr = ip_address(first)
        self.last_addr = ip_address(last)
        return ReturnCode.SUCCESS

    def __range_fetch(self) -> ReturnCode:
        command = "sh run obj in | i range " + str(self.first_addr) + " " + str(self.last_addr) + " "
        self.raw_config = self.cli_command(command)

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.name = re.search("object network (.+) range", self.raw_config).group(1)
        return ReturnCode.SUCCESS
