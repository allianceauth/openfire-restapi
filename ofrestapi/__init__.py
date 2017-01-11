# -*- coding: utf-8 -*-

from ofrestapi.users import Users
from ofrestapi.muc import Muc
from ofrestapi.system import System
from ofrestapi.groups import Groups
from ofrestapi.sessions import Sessions
from ofrestapi.messages import Messages

import pkg_resources
__version__ = pkg_resources.require("openfire-restapi")[0].version
