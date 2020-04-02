import tests.asa_object_test as asa

OBJECT_NAME = "NOBJ"
HOST = "8.8.8.8"
NETWORK = "192.168.12.0/24"
LIST = ["192.168.0.1", "192.168.0.100"]
FQDN = "host.example.local"

# ASA section
asa.named_object_test(OBJECT_NAME)
asa.addressed_object_test(HOST, NETWORK, FQDN, LIST)
asa.unknown_addressed_object_test()
