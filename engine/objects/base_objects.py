from ipaddress import IPv4Address, IPv4Network, ip_network, ip_address
import socket


class FwObject:
    name: str
    origin_addr: IPv4Address
    raw_config: str

    def __init__(self, origin_address, obj_name):
        self.origin_addr = ip_address(origin_address)
        self.name = obj_name

    def fetch_config(self):
        pass

    def push_config(self):
        pass


class HostObject(FwObject):
    ip_addr: IPv4Address

    def __init__(self, origin_address, obj_name, ip):
        super().__init__(origin_address, obj_name)
        self.ip_addr = ip_address(ip)


class NetworkObject(FwObject):
    prefix: IPv4Network

    def __init__(self, origin_address, obj_name, prefix):
        super().__init__(origin_address, obj_name)
        self.prefix = ip_network(prefix, strict=False)


class FqdnObject(FwObject):
    fqdn: str
    ip_addr = None

    def __init__(self, origin_address, obj_name, fqdn):
        super().__init__(origin_address, obj_name)
        self.fqdn = fqdn
        # TODO Check that the resolution is correct
        ip = socket.gethostbyname(fqdn)
        self.ip_addr = ip_address(ip)


class AddrRangeObject(FwObject):
    ip_addr: list

    def __init__(self, origin_address, obj_name, first_ip, last_ip):
        super().__init__(origin_address, obj_name)
        self.ip_addr = [ip_address(first_ip)]
        # TODO iterate through the range + add check first_ip < last_ip
        self.ip_addr.append(ip_address(last_ip))
