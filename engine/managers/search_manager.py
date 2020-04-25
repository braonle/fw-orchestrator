from ipaddress import ip_address

from engine.objects.asa.asa_host_object import AsaHostObject
from engine.managers.device import DeviceTypes


def find_named_host_object(devices: list, name: str = "", addr: str = ""):

    objs = []
    result = []

    if len(name) != 0:
        for x in devices:
            if x.type == DeviceTypes.ASA:
                objs.append(AsaHostObject(x.ip_addr, obj_name=name))

    elif len(addr) != 0:
        for x in devices:
            if x.type == DeviceTypes.ASA:
                objs.append(AsaHostObject(x.ip_addr, ip_addr=ip_address(addr)))
    else:
        return None

    for x in objs:
        x.fetch_config()
        result.append(x.usage())

    return result
