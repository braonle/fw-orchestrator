from engine.objects.base_objects import ResultObject, ReturnCode, FwObject


def list_to_str(l : list) -> str:
    res = ''
    for x in l:
        res = res + " " + str(x)
    return res

def mp_get_object_usage(x: FwObject):
    if x.fetch_config() == ReturnCode.SUCCESS:
        obj = x.usage()

        output = 'Name: ' + str(obj.obj_name) + '<br/>' + \
                 'Origin Address: ' + str(obj.origin_addr) + '<br/>' + \
                 'Origin Name: ' + str(x.hostname()) + '<br/>' + \
                 'ACL: ' + list_to_str(obj.acl_list) + '<br/>' + \
                 'DNS: ' + str(obj.dns) + '<br/>' + \
                 'NTP: ' + str(obj.ntp) + '<br/><br/>'
        return output

    return ""