# -*-coding:utf-8 -*-

import requests
from requests import RequestException
import json
import os
from datacenter_utils.logger import logger


def ding_talk_alert(msg, alert_to, level='P0', keyword=None, access_token=None):
    if not keyword:
        keyword = os.environ.get('DING_TALK_KEYWORD')
    if not access_token:
        access_token = os.environ.get('DING_TALK_TOKEN')
    u_str = os.environ.get('USER_PHONE_DICT')
    if u_str:
        user_dict = json.loads(u_str)
    else:
        user_dict = dict()

    at_name = user_dict.get(alert_to) if user_dict else alert_to
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "{}".format(keyword),
            "text": "{}告警：{}\n@{}".format(
                keyword, msg, at_name)
        },

        "at": {
            "atMobiles": [user_dict.get(alert_to)],
            "isAtAll": False,
        }
    }
    try:
        r = requests.request('POST', 'https://oapi.dingtalk.com/robot/send',
                             headers={'Content-Type': 'application/json'},
                             params={'access_token': access_token},
                             data=json.dumps(data)
                             )
        logger.info("send msg:{}, return:{}".format(msg, r.text))
    except RequestException as e:
        logger.error(e)
