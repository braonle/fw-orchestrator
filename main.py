from engine.managers.search_manager import find_named_host_object
from hosts import HOSTS

res = find_named_host_object(HOSTS, "NOBJ-HOST")
for x in res:
    print(x.origin_addr)
    print(x.obj_name)
    print(x.ntp)
    print(x.dns)
    print(x.acl_list)
