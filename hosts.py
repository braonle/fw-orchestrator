from engine.managers.device import DeviceTypes, Device

# Add your environment variables

FDM = {
    "host": "10.62.18.27", #ip
    "port": 443,
    "username": "admin",
    "password": "cisco",
}

HOSTS = [
    Device(DeviceTypes.ASA, "10.62.18.24"),
    Device(DeviceTypes.FTD, "10.62.18.27")
]
