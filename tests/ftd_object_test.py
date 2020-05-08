from ipaddress import ip_address, ip_network

from engine.objects.ftd.ftd_host_object import FtdHostObject
from engine.objects.ftd.ftd_fqdn_object import FtdFqdnObject
from engine.objects.ftd.ftd_network_object import FtdNetworkObject
from engine.objects.ftd.ftd_range_object import FtdRangeObject
from engine.objects.base_objects import ReturnCode

from hosts import FDM

def named_object_test(name: str):
    print("Test FTD host named object:")
    obj = FtdHostObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-HOST")
    if obj.fetch_config() == ReturnCode.SUCCESS:
        print(obj.name + " -> " + str(obj.ip_addr))
    else:
        print("FAILED")
    print()

    print("Test FTD network named object:")
    obj = FtdNetworkObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-NETWORK")
    if obj.fetch_config() == ReturnCode.SUCCESS:
        print(obj.name + " -> " + str(obj.prefix))
    else:
        print("FAILED")
    print()

    print("Test FTD FQDN named object:")
    obj = FtdFqdnObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-FQDN")
    if obj.fetch_config() == ReturnCode.SUCCESS:
        print(obj.name + " -> " + str(obj.fqdn))
    else:
        print("FAILED")
    print()

    print("Test FTD range named object:")
    obj = FtdRangeObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-RANGE")
    if obj.fetch_config() == ReturnCode.SUCCESS:
        print(obj.name + " -> " + str(obj.first_addr) + " - " + str(obj.last_addr))
    else:
        print("FAILED")
    print()


def addressed_object_test(host: str, network: str, fqdn: str, lst: list):
    print("Test FTD host addressed object")
    obj = FtdHostObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        ip_addr=ip_address(host))
    if obj.fetch_config() == ReturnCode.SUCCESS:
        print(str(obj.ip_addr) + " -> " + obj.name)
    else:
        print("FAILED")
    print()

    print("Test FTD network addressed object")
    obj = FtdNetworkObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        prefix=ip_network(network))
    if obj.fetch_config() == ReturnCode.SUCCESS:
        print(str(obj.prefix) + " -> " + obj.name)
    else:
        print("FAILED")
    print()

    print("Test FTD FQDN addressed object")
    obj = FtdFqdnObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        fqdn=fqdn)
    if obj.fetch_config() == ReturnCode.SUCCESS:
        print(str(obj.fqdn) + " -> " + obj.name)
    else:
        print("FAILED")
    print()


    print("Test FTD range addressed object")
    obj = FtdRangeObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        first=ip_address(lst[0]),
        last=ip_address(lst[1]))
    if obj.fetch_config() == ReturnCode.SUCCESS:
        print(str(obj.first_addr) + " - " + str(obj.last_addr) + " -> " + obj.name)
    else:
        print("FAILED")
    print()


def unknown_addressed_object_test():
    host = "127.0.0.1"
    lst = ["127.0.0.1", "127.0.0.2"]
    network = "127.0.0.0/8"
    fqdn = "test.local"

    print("Test FTD unknown host addressed object")
    obj = FtdHostObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        ip_addr=ip_address(host))
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND)
    print()

    print("Test FTD unknown network addressed object")
    obj = FtdNetworkObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        prefix=ip_network(network))
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND)
    print()

    print("Test FTD unknown FQDN addressed object")
    obj = FtdFqdnObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        fqdn=fqdn)
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND)
    print()

    print("Test FTD unknown range addressed object")
    obj = FtdRangeObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        first=ip_address(lst[0]),
        last=ip_address(lst[1]))
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND)
    print()


def dns_object_test(name: str):
    print("Test FTD host DNS object:")
    obj = FtdHostObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-DNS-HOST")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.dns_usage()))
    print()

    print("Test FTD network DNS object:")
    obj = FtdNetworkObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-NETWORK")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.dns_usage()))
    print()

    print("Test FTD FQDN DNS object:")
    obj = FtdFqdnObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-FQDN")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.dns_usage()))
    print()

    print("Test FTD range DNS object:")
    obj = FtdRangeObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-RANGE")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.dns_usage()))
    print()


def ntp_object_test(name: str):
    print("Test FTD host NTP object:")
    obj = FtdHostObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-HOST")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.ntp_usage()))
    print()

    print("Test FTD network NTP object:")
    obj = FtdNetworkObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-NETWORK")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.ntp_usage()))
    print()

    print("Test FTD FQDN NTP object:")
    obj = FtdFqdnObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-FQDN")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.ntp_usage()))
    print()

    print("Test FTD range NTP object:")
    obj = FtdRangeObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-RANGE")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.ntp_usage()))
    print()


def acl_object_test(name: str):
    print("Test FTD host ACL object:")
    obj = FtdHostObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-HOST")
    obj.fetch_config()
    print(obj.name + " -> " )
    for acl in obj.acl_usage():
        print("  " + str(acl))
    print()

    print("Test FTD network ACL object:")
    obj = FtdNetworkObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-NETWORK")
    obj.fetch_config()
    print(obj.name + " -> " )
    for acl in obj.acl_usage():
        print("  " + str(acl))
    print()

    print("Test FTD FQDN ACL object:")
    obj = FtdFqdnObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-FQDN")
    obj.fetch_config()
    print(obj.name + " -> " )
    for acl in obj.acl_usage():
        print("  " + str(acl))
    print()

    print("Test FTD range ACL object:")
    obj = FtdRangeObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-RANGE")
    obj.fetch_config()
    print(obj.name + " -> " )
    for acl in obj.acl_usage():
        print("  " + str(acl))
    print()


def hostname_test(name: str):
    print("Test FTD hostname:")
    obj = FtdHostObject(
        origin_address=FDM.get("host"),
        port=FDM.get("port"),
        username=FDM.get("username"),
        password=FDM.get("password"),
        obj_name=name + "-HOST")
    print(obj.name + " -> " + str(obj.hostname()))
    print()
