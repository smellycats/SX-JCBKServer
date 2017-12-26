# -*- coding: utf-8 -*-
#import io
#import sys
import json
from functools import wraps

import arrow
import xmltodict
from flask import g, request, make_response, jsonify, abort
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import db, app, api, auth, cache, logger, access_logger
from .models import *
from .soap_func import JCBKClient

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


@app.route('/')
#@limiter.limit("5000/hour")
def index_get():
    result = {
        'jcbk_url': '%sjcbk' % (request.url_root)
    }
    header = {'Cache-Control': 'public, max-age=60, s-maxage=60'}
    return jsonify(result), 200, header

@cache.memoize(60*60)
def get_jcbk_dict(kkdd_id, fxbh_id, cdbh):
    try:
        dev = DeviceMap.query.filter_by(kk_kkbh=kkdd_id, kk_fxbh_id=fxbh_id).first()
        if dev is None:
            return None
        jc = JCBKClient(app.config['JCBK_URL'], dev.map_kkid, dev.map_fxbh, str(cdbh))
        init = jc.jcbk_init()
        doc = xmltodict.parse(init)
        code = dict(doc).get('result', {'code': None}).get('code', None)
        if int(code) == 1:
            app.config['JCBK_DICT'][(kkdd_id, fxbh_id, cdbh)] = jc
        #else:
        #    logger.warning('{0} {1} {2}'.format(dev.map_kkid, dev.map_fxbh, str(cdbh)))
        #    logger.warning(init.encode('utf-8'))
        return code
    except Exception as e:
        logger.error(e)
    return None


@app.route('/time', methods=['GET'])
#@limiter.limit("5000/hour")
def jcbk_get():
    try:
        jc = JCBKClient(app.config['JCBK_URL'], '', '', '')
        return jsonify({'time': jc.jcbk_time()}), 200
    except Exception as e:
        logger.exception(e)
        raise


@app.route('/jcbk_list', methods=['POST'])
#@limiter.limit('6000/minute')
def jcbk_list_post():
    if not request.json:
        return jsonify({'message': 'Problems parsing JSON'}), 415
    try:
        items = []
        for i in request.json:
            code = get_jcbk_dict(i['kkdd_id'], i['fxbh_id'], i['cdbh'])
            if code != '1':
                items.append(code)
                continue
            jc = app.config['JCBK_DICT'].get((i['kkdd_id'], i['fxbh_id'], i['cdbh']), None)
            if jc is None:
                items.append(None)
                continue
            result = jc.jcbk_write(**i)
            doc = xmltodict.parse(result)
            write_code = dict(doc).get('result', {'code': None}).get('code', None)
            items.append(write_code)
            if int(write_code) == 1 or write_code is None:
                continue
            logger.error(i)
            logger.error(result.encode('utf-8'))
        return jsonify({'items': items}), 201
    except Exception as e:
        logger.exception(e)
        raise


@app.route('/jcbk', methods=['POST'])
#@limiter.limit('6000/minute')
def jcbk_post():
    if not request.json:
        return jsonify({'message': 'Problems parsing JSON'}), 415
    try:
        i = request.json
        code = get_jcbk_dict(i['kkdd_id'], i['fxbh_id'], i['cdbh'])
        if code != '1':
            return jsonify({'item': code}), 201
        jc = app.config['JCBK_DICT'].get((i['kkdd_id'], i['fxbh_id'], i['cdbh']), None)
        if jc is None:
            return jsonify({'item': None}), 201
        result = jc.jcbk_write(**i)
        doc = xmltodict.parse(result)
        write_code = dict(doc).get('result', {'code': None}).get('code', None)
        if int(write_code) == 1 or write_code is None:
            pass
        else:
            logger.error(i)
            logger.error(result.encode('utf-8'))
        return jsonify({'item': write_code}), 201
    except Exception as e:
        logger.exception(e)
        raise


