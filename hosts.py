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

from engine.objects.device import DeviceTypes, Device

# Environment variables

FDM = {
    "host": "127.0.0.1", #ip
    "port": 443,
    "username": "",
    "password": "",
}

# Inventory
HOSTS = [
    Device(DeviceTypes.ASA, "127.0.0.2"),
    Device(DeviceTypes.FTD, "127.0.0.3")
]
