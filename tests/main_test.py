import sys
from pathlib import Path

# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / ".." ).resolve()
sys.path.insert(1, str(repository_root))

from hosts import FDM
# import tests.asa_object_test as asa
import tests.ftd_object_test as ftd
import engine.objects.ftd.fdm_api_util as ftd_util


OBJECT_NAME = "NOBJ"
HOST = "8.8.8.8"
NETWORK = "192.168.12.0/24"
FQDN = "host.example.local"
LIST = ["192.168.0.1", "192.168.0.100"]

DNS = "173.38.200.100"
NTP_FQDN = "1.ntp.esl.cisco.com"
# NTP_FQDN_2 = "0.sourcefire.pool.ntp.org"

# ASA section
# asa.named_object_test(OBJECT_NAME)
# asa.addressed_object_test(HOST, NETWORK, FQDN, LIST)
# asa.unknown_addressed_object_test()
# asa.dns_object_test(OBJECT_NAME)
# asa.ntp_object_test(OBJECT_NAME)
# asa.acl_object_test(OBJECT_NAME)

# exit(0)

# FTD section
token = ftd_util.fdm_login(
    host=FDM.get("host"),
    port=FDM.get("port"),
    username=FDM.get("username"),
    password=FDM.get("password"))
ftd_util.fdm_create_network(token,
                            host=FDM.get("host"),
                            port=FDM.get("port"),
                            name = OBJECT_NAME + "-HOST",
                            description = "Test Host from Python",
                            subType = "HOST",
                            value = HOST)
ftd_util.fdm_create_network(token,
                            host=FDM.get("host"),
                            port=FDM.get("port"),
                            name = OBJECT_NAME + "-NETWORK",
                            description = "Test Network from Python",
                            subType = "NETWORK",
                            value = NETWORK)
ftd_util.fdm_create_network(token,
                            host=FDM.get("host"),
                            port=FDM.get("port"),
                            name = OBJECT_NAME + "-FQDN",
                            description = "Test FQDN from Python",
                            subType = "FQDN",
                            value = NTP_FQDN)
ftd_util.fdm_create_network(token,
                            host=FDM.get("host"),
                            port=FDM.get("port"),
                            name = OBJECT_NAME + "-RANGE",
                            description = "Test Range from Python",
                            subType = "RANGE",
                            value = LIST[0]+"-"+LIST[1])
ftd_util.fdm_create_network(token,
                            host=FDM.get("host"),
                            port=FDM.get("port"),
                            name = OBJECT_NAME + "-DNS-HOST",
                            description = "Test Host from Python",
                            subType = "HOST",
                            value = DNS)

ftd.named_object_test(OBJECT_NAME)
ftd.addressed_object_test(HOST, NETWORK, NTP_FQDN, LIST)
ftd.unknown_addressed_object_test()
ftd.dns_object_test(OBJECT_NAME)
ftd.ntp_object_test(OBJECT_NAME)
ftd.acl_object_test(OBJECT_NAME)
ftd.hostname_test(OBJECT_NAME)
