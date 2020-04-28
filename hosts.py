from engine.managers.device import DeviceTypes, Device

# Add your environment variables

FDM = {
    "host": "192.168.1.100", #ip
    "port": 443,
    "username": "admin",
    "password": "cisco",
}

HOSTS = [
    Device(DeviceTypes.ASA, "192.168.2.100"),
    Device(DeviceTypes.FTD, "192.168.1.100")
]
