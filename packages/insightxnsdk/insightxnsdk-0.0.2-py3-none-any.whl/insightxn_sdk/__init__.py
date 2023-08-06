#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import requests
import hashlib
import envx
import json
salt = envx.read('salt.env')['salt']


def make_sk(
        ak: str
):
    """
    输入ak生成sk
    """
    local_content = 'ak=%s;salt=%s' % (ak, salt)
    d5 = hashlib.sha256()
    d5.update(local_content.encode(encoding='UTF-8'))  # update添加时会进行计算
    return d5.hexdigest()


def make_signer(
        ak: str,
        sk: str,
        data: dict
):
    """
    生成签名
    :param ak: 身份识别码
    :param sk: 身份密码
    :param data:
        ts: 必填，时间戳,使用int(time.time())方法生成
        method: 必填，请求方法：GET/POST
        url: 必填，请求的url，例如 https://...
        query: 必填，请求要发送的数据，为json格式
    如果data数据中包含sk、sign，在签名时会自动剔除

    正确签名返回：{'code': 0, 'msg': 'success', 'data': '签名内容'}
    """
    data['ak'] = ak
    data_keys = list(data.keys())
    if 'ts' not in data_keys:
        return {'code': 1, 'msg': 'ts required', 'data': ''}
    if 'method' not in data_keys:
        return {'code': 1, 'msg': 'method required', 'data': ''}
    if 'url' not in data_keys:
        return {'code': 1, 'msg': 'url required', 'data': ''}
    if 'query' not in data_keys:
        return {'code': 1, 'msg': 'query required', 'data': ''}
    data_keys.sort()  # 升序
    data_str = ''
    for each_key in data_keys:
        if each_key == 'query' and type(each_key) == 'dict':
            temp_str = '%s=%s;' % (each_key, json.dumps(data[each_key]))
        else:
            if each_key == 'sk':
                continue
            elif each_key == 'sign':
                continue
            else:
                temp_str = '%s=%s;' % (each_key, data[each_key])
        data_str += temp_str
    data_str += 'sk=%s;' % sk
    d5 = hashlib.sha256()
    d5.update(data_str.encode(encoding='UTF-8'))  # update添加时会进行计算
    return {'code': 0, 'msg': 'success', 'data': d5.hexdigest()}


def make_sign_request(
        ak: str,
        sk: str,
        data: dict
):
    """
    自动签名并发起请求
    :param ak: 身份识别码
    :param sk: 身份密码
    :param data:
        ts: 必填，时间戳,使用int(time.time())方法生成
        method: 必填，请求方法：GET/POST
        url: 必填，请求的url，例如 https://...
        query: 必填，请求要发送的数据，为json格式
    如果data数据中包含sk、sign，在签名时会自动剔除

    正确返回：{'code': 0, 'msg': 'success', 'data': '...'}
    """
    sign_res = make_signer(
        ak=ak,
        sk=sk,
        data=data
    )
    if sign_res['code'] == 0:
        data['sign'] = sign_res['data']
        response = requests.request(
            method=data['method'],
            url=data['url'],
            json=data
        )
        return response.json()
    else:
        return sign_res
