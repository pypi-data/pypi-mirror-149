# -*- coding:utf-8 -*-

import requests
import hashlib
import time
import os

class OpenApi:
    '''
    api = WinmailApi(server, port, apikey, apisecret)

    login_result = api.login('adminUser', 'myPassword', manage_path='admin', tid=2)

    method_params = {
        "method": "user",
        "domain": "test.com"
    }
    
    method_result = api.get_api(**method_params)
    '''
    def __init__(self, server, port, apikey, apisecret):
        self.sessid = None
        self.url = None
        self.server = server
        self.port = port
        self.apikey = apikey
        self.apisecret = apisecret
        self.params = None
    
    # 字典参数排序，计算sign，返回对应的新字典参数
    def sign_para(self, params):
        sort_params = sorted(params.items(),  key=lambda t: t[0],  reverse=False,  )
        # {'b':2,'a':1,'c':3} -> [('a', 1), ('b', 2), ('c', 3)]

        urlstr = self.apisecret
        for item in sort_params:
            for x in item:
                urlstr += x
        urlstr += self.apisecret
        sign = hashlib.md5(urlstr.encode('utf-8')).hexdigest()

        params.update({"sign": sign})
        self.params = None
        self.params = params
        return params
        
    # http request get json data ,return dict
    def request(self, method_params):
        # Winmail 6.6的上传附件接口处理，sign中不计算attachfile
        if 'attachfile' in method_params:
            attch_file = method_params['attachfile']
            if isinstance(attch_file, list):
                files = []
                for f in attch_file:
                    fname = os.path.split(f)[1]
                    files.append(('attachfile[]', (fname, open(f, 'rb'))))
            else:
                files = {'attachfile': open(attch_file, 'rb')}

            method_params.pop('attachfile')

            try:
                response = requests.post(self.url, self.sign_para(method_params), files=files)
            except Exception as e:
                return {'result': 'error', 'info': 'http connect error 0 : %s'% e}
        else:

            try:
                response = requests.post(self.url, self.sign_para(method_params))
            except Exception as e:
                return {'result': 'error', 'info': 'http connect error 1 : %s'% e}
        
        if response.status_code == 200:
            # Winmail 本身newmsg.reset接口没有返回json数据，执行后就完成。单独处理下
            # (6.6 0812版本已经加入json返回结果, 注释掉)
            #if method_params['method'] == 'newmsg.reset':
            #    return {"result": 'ok'}
            try:
                data = response.json()
            except Exception as e:
                return {'result': 'error', 'info': '%s : %s'% (method_params['method'], e)}
        else:
            data = {"result": "error", 'info': "http status %s." % response.status_code }

        return data

    # login 
    def login(self, user, pwd, manage_path='', tid='2'):
        '''
        登陆成功将把sessid赋值给实例的sessid。
        返回结果为API接口返回的JSON字符串转换的dict。

        :param user: 用户名

        :param pwd: 密码

        :param manage_path: 管理端路径默认是admin，6.6版本的Winmail可以在管理工具后台修改管理端路径。
                如果值为空是邮箱用户。

        :param tid: Webmail的themes，tid=6时为手机web界面

        :return: dict {result: ok/error, info: ""}
        '''
        if manage_path:
            self.url = 'http://' + self.server + ':' + str(self.port) + '/' + manage_path + '/openapi.php'
        else:
            self.url = 'http://' + self.server + ':' + str(self.port) + '/openapi.php'
        
        # method=login
        timestamp = str(int(time.time()))
        param_dict = {'user': user, 'pass': pwd}
        param_dict.update({"apikey": self.apikey,  "method": "login",  "timestamp": timestamp})

        if not manage_path:
            param_dict.update({'tid': tid})
            
        result = self.request(param_dict)
        if result['result'] == 'ok':
            self.sessid = result['info']['sessid']
        return result

    # update session id
    def update_session(self):
        '''
        :return: True/False
        '''
        if not self.sessid:
            return False
        timestamp = str(int(time.time()))
        param_dict = {"apikey": self.apikey,  "method": "updatesession",  "sessid": self.sessid,  "timestamp": timestamp}
        result = self.request(param_dict)

        if result['result'] == 'ok':
            return True
        return False

    # method function return dict data
    def get_api(self, **kwargs):
        '''
        返回结果为API接口返回的JSON字符串转换的dict。

        :param kwargs: OpenApi方法和参数集合的字典 {'method': 'user', 'domain': 'winmail.cn' .....}

        :return: dict {result: ok/error, info: ""}
        '''

        param_dict = kwargs
            
        if not self.url or not self.sessid:
            return {"result": "error", "info": "Use login first %s.login(user, pwd, manage_path) " % self.__class__.__name__}

        timestamp = str(int(time.time()))

        if 'sessid' not in param_dict:
            param_dict.update({'sessid': self.sessid})
        if 'apikey' not in param_dict:
            param_dict.update({"apikey": self.apikey})
        if 'timestamp' not in param_dict:
            param_dict.update({"timestamp": timestamp})
        result = self.request(param_dict)

        return result
