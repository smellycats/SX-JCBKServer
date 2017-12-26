# -*- coding: utf-8 -*-
import arrow

from . import db


class DeviceMap(db.Model):
    """设备编码"""
    __tablename__ = 'device_map'

    id = db.Column(db.Integer, primary_key=True)
    kk_kkbh = db.Column(db.String(64), default='')
    kk_name = db.Column(db.String(128), default='')
    kk_cdbh = db.Column(db.Integer, default=1)
    kk_fxbh_id = db.Column(db.Integer, default=1)
    kk_fxbh = db.Column(db.String(64), default='')
    map_kkid = db.Column(db.String(128), default='')
    map_fxbh = db.Column(db.String(64), default='')
    map_cdbh = db.Column(db.String(8), default='')

    def __init__(self, kk_kkbh='', kk_name='', kk_cdbh=1, kk_fxbh_id=1,
                 kk_fxbh='', map_kkid='', map_fxbh='', map_cdbh=''):
        self.kk_kkbh = kk_kkbh
        self.kk_name = kk_name
        self.kk_cdbh = kk_cdbh
        self.kk_fxbh_id = kk_fxbh_id
        self.kk_fxbh = kk_fxbh
        self.map_kkid = map_kkid
        self.map_fxbh = map_fxbh
        self.map_cdbh = map_cdbh

    def __repr__(self):
        return '<DeviceMap %r>' % self.id


