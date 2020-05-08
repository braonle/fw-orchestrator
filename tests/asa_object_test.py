#
#	Copyright (c) 2020 Cisco and/or its affiliates.
#
#	This software is licensed to you under the terms of the Cisco Sample
#	Code License, Version 1.1 (the "License"). You may obtain a copy of the
#	License at
#
#		       https://developer.cisco.com/docs/licenses
#
#	All use of the material herein must be in accordance with the terms of
#	the License. All rights not expressly granted by the License are
#	reserved. Unless required by applicable law or agreed to separately in
#	writing, software distributed under the License is distributed on an "AS
#	IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#	or implied.
#

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
 
dns domain-lookup Outside
dns name-server 8.8.8.8

ntp server 8.8.8.8
    
access-list ACL extended permit ip object NOBJ-HOST any 
access-list ACL1 extended permit ip object NOBJ-HOST any 
access-list ACL1 extended permit ip object NOBJ-FQDN any
access-list ACL2 extended permit ip any 8.8.8.8 255.255.255.255 
access-list ACL3 extended permit ip 192.168.12.0 255.255.255.0 any 

'''

ASA_ADDRESS = "127.0.0.1"

def named_object_test(name: str):
    print("Test ASA host named object:")
    obj = AsaHostObject(origin_address=ASA_ADDRESS, obj_name=name + "-HOST")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.ip_addr)), print()

    print("Test ASA network named object:")
    obj = AsaNetworkObject(origin_address=ASA_ADDRESS, obj_name=name + "-NETWORK")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.prefix)), print()

    print("Test ASA FQDN named object:")
    obj = AsaFqdnObject(origin_address=ASA_ADDRESS, obj_name=name + "-FQDN")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.fqdn)), print()

    print("Test ASA range named object:")
    obj = AsaRangeObject(origin_address=ASA_ADDRESS, obj_name=name + "-RANGE")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.first_addr) + " - " + str(obj.last_addr)), print()


def addressed_object_test(host: str, network: str, fqdn: str, lst: list):
    print("Test ASA host addressed object")
    obj = AsaHostObject(origin_address=ASA_ADDRESS, ip_addr=ip_address(host))
    obj.fetch_config()
    print(str(obj.ip_addr) + " -> " + obj.name), print()

    print("Test ASA network addressed object")
    obj = AsaNetworkObject(origin_address=ASA_ADDRESS, prefix=ip_network(network))
    obj.fetch_config()
    print(str(obj.prefix) + " -> " + obj.name), print()

    print("Test ASA FQDN addressed object")
    obj = AsaFqdnObject(origin_address=ASA_ADDRESS, fqdn=fqdn)
    obj.fetch_config()
    print(str(obj.fqdn) + " -> " + obj.name), print()

    print("Test ASA range addressed object")
    obj = AsaRangeObject(origin_address=ASA_ADDRESS, first=ip_address(lst[0]), last=ip_address(lst[1]))
    obj.fetch_config()
    print(str(obj.first_addr) + " - " + str(obj.last_addr) + " -> " + obj.name), print()


def unknown_addressed_object_test():
    host = "127.0.0.1"
    lst = ["127.0.0.1", "127.0.0.2"]
    network = "127.0.0.0/8"
    fqdn = "test.local"

    print("Test ASA unknown host addressed object")
    obj = AsaHostObject(origin_address=ASA_ADDRESS, ip_addr=ip_address(host))
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND), print()

    print("Test ASA network addressed object")
    obj = AsaNetworkObject(origin_address=ASA_ADDRESS, prefix=ip_network(network))
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND), print()

    print("Test ASA FQDN addressed object")
    obj = AsaFqdnObject(origin_address=ASA_ADDRESS, fqdn=fqdn)
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND), print()

    print("Test ASA range addressed object")
    obj = AsaRangeObject(origin_address=ASA_ADDRESS, first=ip_address(lst[0]), last=ip_address(lst[1]))
    print(obj.fetch_config() == ReturnCode.OBJECT_NOT_FOUND), print()


def dns_object_test(name: str):
    print("Test ASA host DNS object:")
    obj = AsaHostObject(origin_address=ASA_ADDRESS, obj_name=name + "-HOST")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.dns_usage())), print()

    print("Test ASA network DNS object:")
    obj = AsaNetworkObject(origin_address=ASA_ADDRESS, obj_name=name + "-NETWORK")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.dns_usage())), print()

    print("Test ASA FQDN DNS object:")
    obj = AsaFqdnObject(origin_address=ASA_ADDRESS, obj_name=name + "-FQDN")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.dns_usage())), print()

    print("Test ASA range DNS object:")
    obj = AsaRangeObject(origin_address=ASA_ADDRESS, obj_name=name + "-RANGE")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.dns_usage())), print()


def ntp_object_test(name: str):
    print("Test ASA host NTP object:")
    obj = AsaHostObject(origin_address=ASA_ADDRESS, obj_name=name + "-HOST")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.ntp_usage())), print()

    print("Test ASA network NTP object:")
    obj = AsaNetworkObject(origin_address=ASA_ADDRESS, obj_name=name + "-NETWORK")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.ntp_usage())), print()

    print("Test ASA FQDN NTP object:")
    obj = AsaFqdnObject(origin_address=ASA_ADDRESS, obj_name=name + "-FQDN")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.ntp_usage())), print()

    print("Test ASA range NTP object:")
    obj = AsaRangeObject(origin_address=ASA_ADDRESS, obj_name=name + "-RANGE")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.ntp_usage())), print()


def acl_object_test(name: str):
    print("Test ASA host ACL object:")
    obj = AsaHostObject(origin_address=ASA_ADDRESS, obj_name=name + "-HOST")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.acl_usage())), print()

    print("Test ASA network ACL object:")
    obj = AsaNetworkObject(origin_address=ASA_ADDRESS, obj_name=name + "-NETWORK")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.acl_usage())), print()

    print("Test ASA FQDN ACL object:")
    obj = AsaFqdnObject(origin_address=ASA_ADDRESS, obj_name=name + "-FQDN")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.acl_usage())), print()

    print("Test ASA range ACL object:")
    obj = AsaRangeObject(origin_address=ASA_ADDRESS, obj_name=name + "-RANGE")
    obj.fetch_config()
    print(obj.name + " -> " + str(obj.acl_usage())), print()


