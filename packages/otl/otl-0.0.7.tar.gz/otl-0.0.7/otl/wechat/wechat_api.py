# -*- coding: utf-8 -*-

import random
from .src.CoreApi import CorpApi, CORP_API_TYPE


class WechatApp(object):
    def __init__(self, corp_id, app_id, app_secret):
        self.available_msg_type = ['text', 'markdown']
        self.corp_id = corp_id
        self.app_id = app_id
        self.app_secret = app_secret
        self.api = CorpApi(corp_id, app_secret)

        self.app_info = {}
        self.allow_parts = {}
        self.allow_users = {}

        self.get_app_info()
        self.get_departs_info()
        self.get_users_info()

    def send(self, msg_type, to_users_list=[], to_group_list=[], msg_string=''):
        """

        :param msg_type: 消息类型：text or markdown
        :param to_users_list: 接收用户列表
        :param to_group_list: 接收组列表
        :param msg_string: message
        :return:
        """
        if msg_type not in self.available_msg_type:
            return False, ('msg_type_error:{},available:{}'.format(msg_type, ",".join([str(k) for k in self.available_msg_type])))

        for user in to_users_list:
            user = str(user)
            if user not in self.allow_users:
                return False, ('to_users_list_error: {}, available: {}'.format(user, ','.join([str(k) for k in self.allow_users.keys()])))

        for part in to_group_list:
            part = str(part)
            if part not in self.allow_parts:
                return False, ('to_group_list_error: {}, available: {}'.format(part, ','.join([str(k) for k in self.allow_parts.keys()])))

        to_users_list = [str(self.allow_users[str(user)]) for user in to_users_list]
        to_group_list = [str(self.allow_parts[str(group)]) for group in to_group_list]
        if msg_type == 'text':
            return True, self.send_text(to_users_list=to_users_list, to_group_list=to_group_list, msg_string=msg_string)
        elif msg_type == 'markdown':
            return True, self.send_markdown(to_users_list=to_users_list, to_group_list=to_group_list, markdown=msg_string)

    def get_app_info(self):
        response = self.api.httpCall(
            CORP_API_TYPE['AGENT_GET'],
            {
                'agentid': self.app_id,
            }
        )
        self.app_info = response

    def get_departs_info(self):
        for pid in self.app_info.get('allow_partys', {}).get('partyid', []):
            response = self.api.httpCall(
                CORP_API_TYPE['DEPARTMENT_LIST'],
                {
                    "id": str(pid)
                }
            )
            for k in response['department']:
                self.allow_parts[str(k['name'])] = int(k['id'])

    def get_users_info(self):
        for k, pid in self.allow_parts.items():
            response = self.api.httpCall(
                CORP_API_TYPE['USER_SIMPLE_LIST'],
                {
                    "department_id": str(pid),
                    "fetch_child": "1",
                }
            )
            for user in response['userlist']:
                self.allow_users[str(user['name'])] = user['userid']
        for user in self.app_info['allow_userinfos'].get('user', []):
            response = self.api.httpCall(
                CORP_API_TYPE['USER_GET'],
                {
                    "userid": str(user['userid'])
                }
            )
            name = response.get('name')
            self.allow_users[str(name)] = user['userid']

    def send_text(self, to_users_list=[], to_group_list=[], msg_string=""):
        response = self.api.httpCall(
            CORP_API_TYPE['MESSAGE_SEND'],
            {
                "touser": "|".join(to_users_list),
                "toparty": "|".join(to_group_list),
                "agentid": str(self.app_id),
                'msgtype': 'text',
                'climsgid': 'climsgidclimsgid_%f' % (random.random()),
                'text': {
                    'content': msg_string,
                },
                'safe': 0,
            }
        )

        return response

    def send_markdown(self, to_users_list=[], to_group_list=[], markdown=""):
        response = self.api.httpCall(
            CORP_API_TYPE['MESSAGE_SEND'],
            {
                "touser": "|".join(to_users_list),
                "toparty": "|".join(to_group_list),
                "agentid": str(self.app_id),
                'msgtype': 'markdown',
                'climsgid': 'climsgidclimsgid_%f' % (random.random()),
                "markdown": {
                    "content": str(markdown)
                },
                'safe': 0,
            }
        )
        return response


class WechatApi(object):
    def __init__(self, config):
        self.config = config
        self.NAME = config['NAME']
        self.CORP_ID = config['CORP_ID']
        self.APP_LIST_CONFIG = config['APP_LIST']
        self.apps = {}
        self.trans = {}
        self.init_apps()

    def init_apps(self):
        for k, v in self.APP_LIST_CONFIG.items():
            if v.get('switch') != 'on': continue
            app = WechatApp(self.CORP_ID, v['APP_ID'], v['APP_SECRET'])
            self.apps[k] = app
