from typing import List

from engine.objects.base_objects import FwObject, AclEntry
from engine.objects.ftd.fdm_api_util import (fdm_login, fdm_get_access_policies,
    fdm_get_access_rules)

from engine.config import *


class FtdObject(FwObject):

    port: int
    id: str

    def __init__(self, origin_address: str, port: int = 443, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD,  id = None):
        FwObject.__init__(self, origin_address, obj_name, username, password)
        self.port = port

    def dns_usage(self) -> bool:
        return False

    def ntp_usage(self) -> bool:
        return False

    def acl_usage(self) -> List[AclEntry]:
        if self.id is None:
            return []

        lst = []

        token = fdm_login(host=self.origin_addr,
                          port=self.port,
                          username=self.username,
                          password=self.password)
        accesspolicies = fdm_get_access_policies(token,
                                                 host=self.origin_addr,
                                                 port=self.port)
        for accesspolicy in accesspolicies['items']:
            accessrules = fdm_get_access_rules(token,
                                               host=self.origin_addr,
                                               port=self.port,
                                               access_policy_id=accesspolicy['id'])
            for accessrule in accessrules['items']:
                for src in accessrule['sourceNetworks']:
                    if src['id'] == self.id:
                        lst.append(f"{accesspolicy['name']}: {accessrule['name']}")
                for dest in accessrule['destinationNetworks']:
                    if dest['id'] == self.id:
                        lst.append(f"{accesspolicy['name']}: {accessrule['name']}")

        res = []

        for x in lst:
            obj = AclEntry()
            obj.acl_name = x
            obj.hit_count = 0
            res.append(obj)

        return res
