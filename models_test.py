# -*- coding: utf-8 -*-
import json

import arrow

from app import db
from app.models import *


def device_test():
    dev = DeviceMap.query.filter_by(kk_kkbh='441302305', kk_fxbh_id=2).first()
    print(dev.map_kkid, dev.map_fxbh)

if __name__ == '__main__':
    device_test()

