from ipaddress import ip_network
import re

from engine.objects.base_objects import NetworkObject, ReturnCode
from engine.objects.asa.asa_cli_connection import asa_cli_command


class AsaNetworkObject(NetworkObject):

    def fetch_config(self):
        if (self.name is None) and (self.prefix is not None):
            return self.__prefix_fetch()
        elif (self.name is not None) and (self.prefix is None):
            return self.__named_fetch()
        else:
            self.raw_config = ""

    def __named_fetch(self) -> ReturnCode:
        command = "sh run obj in | i " + self.name + " subnet"
        self.raw_config = asa_cli_command(str(self.origin_addr), self.username, self.password, self.secret,
                                          command).rstrip()

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.prefix = ip_network(re.search("subnet (.*)", self.raw_config).group(1).replace(" ", "/"))
        return ReturnCode.SUCCESS

    def __prefix_fetch(self) -> ReturnCode:
        command = "sh run obj in | i subnet " + str(self.prefix.network_address) + \
                    " " + str(self.prefix.netmask) + " "
        self.raw_config = asa_cli_command(str(self.origin_addr), self.username, self.password, self.secret,
                                          command).rstrip()

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.name = re.search("object network (.*) subnet", self.raw_config).group(1)
        return ReturnCode.SUCCESS

