from ipaddress import ip_network

from engine.objects.base_objects import NetworkObject, ReturnCode
from engine.objects.ftd.fdm_api_util import fdm_login, fdm_get_networks

class FtdNetworkObject(NetworkObject):

    def fetch_config(self) -> ReturnCode:
        if (self.name is not None) and (self.prefix is not None):
            return ReturnCode.SUCCESS
        elif (self.name is None) and (self.prefix is not None):
            return self.__prefix_fetch()
        elif (self.name is not None) and (self.prefix is None):
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
            if obj['subType'] == "NETWORK":
                if obj['name'] == self.name:
                    self.prefix = ip_network(obj['value'])
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND

    def __prefix_fetch(self) -> ReturnCode:
        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)
        networks = fdm_get_networks(token,
                                    host=self.origin_addr,
                                    port=self.port,)

        for obj in networks['items']:
            if obj['subType'] == "NETWORK":
                if obj['value'] == str(self.prefix):
                    self.name = obj['name']
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND
