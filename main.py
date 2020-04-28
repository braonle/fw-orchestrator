from engine.managers.search_manager import find_named_host_object, find_named_network_object
from hosts import HOSTS
from frontend.web.frontend import app

if __name__ == '__main__':
    app.run(host='0.0.0.0')

# res = find_named_network_object(HOSTS, "NOBJ-NETWORK")
# for x in res:
#     print(x.origin_addr)
#     print(x.obj_name)
#     print(x.ntp)
#     print(x.dns)
#     print(x.acl_list)
