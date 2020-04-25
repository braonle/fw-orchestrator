from engine.objects.base_objects import FwObject

from engine.config import *


class FtdObject(FwObject):

    port: int

    def __init__(self, origin_address: str, port: int = 443, obj_name: str = None,
                 username: str = USERNAME, password: str = PASSWORD):
        FwObject.__init__(self, origin_address, obj_name, username, password)
        self.port = port
