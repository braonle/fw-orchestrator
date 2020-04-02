from ipaddress import ip_address, ip_network

from engine.objects.asa.asa_host_object import AsaHostObject
from engine.objects.asa.asa_fqdn_object import AsaFqdnObject
from engine.objects.asa.asa_network_object import AsaNetworkObject
from engine.objects.asa.asa_range_object import AsaRangeObject
from engine.objects.base_objects import ReturnCode

''' ASA configuration prerequisites

object network NOBJ-HOST
 host 8.8.8.8
object network NOBJ-NETWORK
 subnet 192.168.12.0 255.255.255.0
object network NOBJ-FQDN
 fqdn host.example.local
object network NOBJ-RANGE
 range 192.168.0.1 192.168.0.100
    
'''

ASA_ADDRESS = "192.168.2.100"


def named_object_test(name: str):
    print("Test ASA host named object:")
    obj = AsaHostObject(origin_address=ASA_ADDRESS, obj_name=name + "-HOST")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.ip_addr))
    print()

    print("Test ASA network named object:")
    obj = AsaNetworkObject(origin_address=ASA_ADDRESS, obj_name=name + "-NETWORK")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.prefix))
    print()

    print("Test ASA FQDN named object:")
    obj = AsaFqdnObject(origin_address=ASA_ADDRESS, obj_name=name + "-FQDN")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.fqdn))
    print()

    print("Test ASA range named object:")
    obj = AsaRangeObject(origin_address=ASA_ADDRESS, obj_name=name + "-RANGE")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.first_addr) + " - " + str(obj.last_addr))
    print()


def addressed_object_test(host: str, network: str, fqdn: str, lst: list):
    print("Test ASA host addressed object")
    obj = AsaHostObject(origin_address=ASA_ADDRESS, ip_addr=ip_address(host))
    obj.fetch_config()
    print(str(obj.ip_addr) + " -> " + obj.name)
    print()

    print("Test ASA network addressed object")
    obj = AsaNetworkObject(origin_address=ASA_ADDRESS, prefix=ip_network(network))
    obj.fetch_config()
    print(str(obj.prefix) + " -> " + obj.name)
    print()

    print("Test ASA FQDN addressed object")
    obj = AsaFqdnObject(origin_address=ASA_ADDRESS, fqdn=fqdn)
    obj.fetch_config()
    print(str(obj.fqdn) + " -> " + obj.name)
    print()

    print("Test ASA range addressed object")
    obj = AsaRangeObject(origin_address=ASA_ADDRESS, first=ip_address(lst[0]), last=ip_address(lst[1]))
    obj.fetch_config()
    print(str(obj.first_addr) + " - " + str(obj.last_addr) + " -> " + obj.name)
    print()


def unknown_addressed_object_test():
    host = "127.0.0.1"
    lst = ["127.0.0.1", "127.0.0.2"]
    network = "127.0.0.0/8"
    fqdn = "test.local"

    print("Test ASA unknown host addressed object")
    obj = AsaHostObject(origin_address=ASA_ADDRESS, ip_addr=ip_address(host))
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND)
    print()

    print("Test ASA network addressed object")
    obj = AsaNetworkObject(origin_address=ASA_ADDRESS, prefix=ip_network(network))
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND)
    print()

    print("Test ASA FQDN addressed object")
    obj = AsaFqdnObject(origin_address=ASA_ADDRESS, fqdn=fqdn)
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND)
    print()

    print("Test ASA range addressed object")
    obj = AsaRangeObject(origin_address=ASA_ADDRESS, first=ip_address(lst[0]), last=ip_address(lst[1]))
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND)
    print()



