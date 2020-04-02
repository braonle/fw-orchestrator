import re

from engine.objects.base_objects import FqdnObject, ReturnCode
from engine.objects.asa.asa_cli_connection import asa_cli_command


class AsaFqdnObject(FqdnObject):

    def fetch_config(self):
        if (self.name is None) and (self.fqdn is not None):
            return self.__fqdn_fetch()
        elif (self.name is not None) and (self.fqdn is None):
            return self.__named_fetch()
        else:
            self.raw_config = ""
            return ReturnCode.INVALID_FIELDS

    def __named_fetch(self) -> ReturnCode:
        command = "sh run obj in | i " + self.name + " fqdn"
        self.raw_config = asa_cli_command(str(self.origin_addr), self.username, self.password, self.secret,
                                          command).rstrip()

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.fqdn = re.search("fqdn (.*)", self.raw_config).group(1)
        return ReturnCode.SUCCESS

    def __fqdn_fetch(self) -> ReturnCode:
        command = "sh run obj in | i fqdn " + str(self.fqdn)
        self.raw_config = asa_cli_command(str(self.origin_addr), self.username, self.password, self.secret,
                                          command).rstrip()

        if len(self.raw_config) == 0:
            return ReturnCode.OBJECT_NOT_FOUND

        self.name = re.search("object network (.*) fqdn", self.raw_config).group(1)
        return ReturnCode.SUCCESS
