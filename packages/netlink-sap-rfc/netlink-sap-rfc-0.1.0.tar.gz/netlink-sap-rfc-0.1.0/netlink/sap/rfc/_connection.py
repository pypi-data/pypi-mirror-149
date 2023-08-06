import getpass
import pyrfc

from ._landscape import Landscape
from netlink.logging import logger

landscape = Landscape()


class Connection:
    def __init__(self, sysid, client, user_id=None, language='EN', raw=False):
        sysid = sysid.upper()
        if user_id is None:
            user_id = getpass.getuser()
        user_id = user_id.upper()
