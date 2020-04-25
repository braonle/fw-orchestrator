import re

from netmiko import ConnectHandler
from engine.objects.base_objects import FwObject
from engine.config import *


class AsaObject(FwObject):

    raw_config: str
    secret: str

    def __init__(self, origin_address: str, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD, secret: str = SECRET):
        FwObject.__init__(self, origin_address, obj_name, username, password)
        self.secret = secret

    def cli_command(self, command: str) -> str:
        device_params = {
            'device_type': 'cisco_asa',
            'ip': str(self.origin_addr),
            'username': self.username,
            'password': self.password,
            'secret': self.secret
        }

        result = ""

        with ConnectHandler(**device_params) as ssh:
            ssh.enable()
            result = ssh.send_command(command).rstrip()

        return result

    def dns_usage(self) -> bool:
        return False

    def ntp_usage(self) -> bool:
        return False

    def acl_usage(self) -> list:
        if self.name is None:
            return []

        command = "sho run access-list | i " + self.name
        ace = self.cli_command(command).splitlines()
        lst = []

        for x in ace:
            lst.append(re.search("access-list (\w+)", x).group(1))

        return lst
