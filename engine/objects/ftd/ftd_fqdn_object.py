from engine.objects.base_objects import FqdnObject, ReturnCode
from engine.objects.ftd.fdm_api_util import fdm_login, fdm_get_networks
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
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND
