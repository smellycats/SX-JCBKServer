# -*- coding: utf-8 -*-
import time

from suds.client import Client


class JCBKClient(object):
    def __init__(self, url, gateId, directId, wayId):
        self.client = Client(url)
        self.gateId = gateId
        self.directId = directId
        self.wayId = wayId

    def jcbk_init(self):
        return self.client.service.initTrans(gateId=self.gateId, directId=self.directId, wayId=self.wayId, initKey='')

    def jcbk_write(self, **kwargs):
        if kwargs['hpys_id'] == 1:
            car_type = '1'
        else:
            car_type = '0'
        if kwargs['hphm'] == '-':
            lic_type = '41'
        elif kwargs['hpzl'] == '88':
            lic_type = '02'
        else:
            lic_type = kwargs['hpzl']
        if kwargs['hphm'] is None:
            hphm = '-'
            lic_type = '41'
        else:
            hphm = kwargs['hphm'].encode('utf-8').decode('unicode_escape')
        return self.client.service.writeVehicleInfo(gateId=self.gateId,
                                                    directionId=self.directId,
                                                    driverWayId=self.wayId,
                                                    driverWayType='00',
                                                    licenseType=lic_type,
                                                    passTime=kwargs['jgsj'],
                                                    speed=kwargs['clsd'],
                                                    licenseColor=str(kwargs['hpys_id']),
                                                    carType=car_type,
                                                    license=hphm,
                                                    backLicense='0',
                                                    backLicenseColor='0',
                                                    identical='0',
                                                    carColor=kwargs['csys'],
                                                    limitSpeed=kwargs['clxs'],
                                                    carBrand='0',
                                                    carShape='0',
                                                    travelStatus='0',
                                                    violationFlag='0',
                                                    picPath1=kwargs['imgurl'],
                                                    picPath2='0',
                                                    picPath3='0',
                                                    featurePic='0',
                                                    driverPic='0',
                                                    copilotPic='0',
                                                    sendFlag='0')

    def jcbk_time(self):
        return self.client.service.querySyncTime()

