from ipaddress import ip_address, IPv4Address

from engine.objects.base_objects import HostObject, ReturnCode
from engine.objects.ftd.fdm_api_util import (fdm_login, fdm_get_networks,
    fdm_get_ntp, fdm_get_dns_server_groups)
from engine.objects.ftd.ftd_object import FtdObject

from engine.config import *


class FtdHostObject(FtdObject, HostObject):

    def __init__(self, origin_address: str, port: int = 0, ip_addr: IPv4Address = None, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD):
        FtdObject.__init__(self, origin_address, port, obj_name, username, password)
        HostObject.__init__(self, ip_addr)

    def fetch_config(self) -> ReturnCode:
        if (self.name is not None) and (self.ip_addr is not None):
            return ReturnCode.SUCCESS
        elif (self.name is None) and (self.ip_addr is not None):
            return self.__addr_fetch()
        elif (self.name is not None) and (self.ip_addr is None):
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
            if obj['subType'] == "HOST":
                if obj['name'] == self.name:
                    self.ip_addr = ip_address(obj['value'])
                    self.id = obj['id']
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND

    def __addr_fetch(self) -> ReturnCode:
        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)
        networks = fdm_get_networks(token,
                                    host=self.origin_addr,
                                    port=self.port,)

        for obj in networks['items']:
            if obj['subType'] == "HOST":
                if obj['value'] == str(self.ip_addr):
                    self.name = obj['name']
                    self.id = obj['id']
                    return ReturnCode.SUCCESS

        return ReturnCode.OBJECT_NOT_FOUND

    def dns_usage(self) -> bool:
        if self.ip_addr is None:
            return False

        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)
        dns = fdm_get_dns_server_groups(token,
                          host=self.origin_addr,
                          port=self.port)

        for i in dns['items']:
            for dns_server in i['dnsServers']:
                if dns_server['ipAddress'] == str(self.ip_addr):
                    return True

        return False

    def ntp_usage(self) -> bool:
        if self.ip_addr is None:
            return False

        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)
        ntp = fdm_get_ntp(token,
                          host=self.origin_addr,
                          port=self.port)

        for i in ntp['items']:
            for ntp_server in i['ntpServers']:
                if ntp_server == str(self.ip_addr):
                    # if i['enabled']:
                    return True

        return False
