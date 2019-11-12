import json
from urllib.parse import urlencode, parse_qs

import logging
from urllib.request import urlopen



from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings

from oauth import constants
from oauth.execptions import QQAPIError, WEIBOAPIError

logger = logging.getLogger('django')

class QQOAuth(object):
    """QQ认证辅助工具"""
    def __init__(self, client_id=None, redirect_uri=None, state=None):
        self.client_id = client_id if client_id else settings.OAUTH_CLIENT_ID
        self.redirect_uri = redirect_uri if redirect_uri else settings.OAUTH_REDIRECT_URI
        self.state = state or settings.OAUTH_STATUS

    def get_login_url(self):
        url = 'https://graph.qq.com/oauth2.0/authorize?'
        params = {
            'response_type':'code',
            'client_id':self.client_id,
            'redirect_uri':self.redirect_uri,
            'state':self.state,
        }
        url += urlencode(params)
        return url

    def get_access_token(self, code):
        url = 'https://graph.qq.com/oauth2.0/token?'
        params = {
            'grant_type':'authorization_code',
            'client_id':self.client_id,
            'client_secret':settings.OAUTH_CLIENT_SECRET,
            'code':code,
            'redirect_uri':self.redirect_uri
        }
        url += urlencode(params)
        try:
            response = urlopen(url)
            response_data = response.read().decode()
        except QQAPIError as e:
            logger.error('access_token请求失败:%s'%e)
            raise QQAPIError
        response_dict = parse_qs(response_data)
        access_token = response_dict.get('access_token')
        if not access_token:
            raise QQAPIError
        return access_token[0]

    def get_openid(self, access_token):
        url = 'https://graph.qq.com/oauth2.0/me?access_token=%s'%access_token
        try:
            response = urlopen(url)
            # callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} )\n;
            response_data = response.read().decode()
        except QQAPIError as e:
            logger.error('openid请求失败:%s'%e)
            raise QQAPIError
        response_dict = json.loads(response_data[10:-4])
        openid = response_dict.get('openid')
        return openid

    @staticmethod
    def generate_save_user_token(openid):
        serializer = Serializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        token = serializer.dumps({'openid':openid})
        return token.decode()

    @staticmethod
    def check_save_user_token(access_token):
        serializer = Serializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        try:
            data = serializer.loads(access_token)
        except BadData as e:
            logger.error('无效的access_token:%s'%e)
            return None
        openid = data.get('openid')
        return openid


class WEIBOAuth(object):
    def __init__(self, app_key=None, app_secret=None, redirect_uri=None,state=None):
        self.client_id = app_key or settings.WEIBO_CLIENT_ID
        self.client_secret = app_secret or settings.WEIBO_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.WEIBO_REDIRECT_URI
        self.state = state or settings.WEIBO_STATE # 用于保存登录成功后的跳转页面路径


    def get_authorize_url(self):
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
        }
        url = 'https://api.weibo.com/oauth2/authorize?' + urlencode(params)
        return url

    def get_access_token_and_uid(self, code):
        """
        获取access_token
        :param code: qq提供的code
        :return: access_token
        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code,
            'grant_type': 'authorization_code',
        }
        url = 'https://api.weibo.com/oauth2/access_token?'
        url += urlencode(params)
        data = {}
        data = json.dumps(data).encode()
        try:
            response = urlopen(url=url,data=data)
            response_data = response.read().decode()
        except WEIBOAPIError as e:
            logger.error('access_token请求失败:%s'%e)
            raise WEIBOAPIError
        response_data = json.loads(response_data)
        access_token = response_data.get('access_token', None)
        uid = response_data.get('uid', None)
        if not access_token:
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise WEIBOAPIError
        if not uid:
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise WEIBOAPIError

        return (access_token, uid)

    @staticmethod
    def generate_save_user_token(uid):
        """
        生成保存用户数据的token
        :param access_token: 用户的新浪access_token
        :return: token
        """
        serializer = Serializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        data = {'uid': uid}
        token = serializer.dumps(data)
        return token.decode()

    @staticmethod
    def check_save_user_token(access_token):
        serializer = Serializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        try:
            data = serializer.loads(access_token)
        except BadData as e:
            logger.error('无效的access_token:%s' % e)
            return None
        uid = data.get('uid')
        return uid

    @staticmethod
    def share_to_wb(oauth_access_token,content):
        content = content + 'http://www.mlh.com'
        params = {
            'access_token':oauth_access_token,
            'status':content,
        }
        url = 'https://api.weibo.com/2/statuses/share.json?'
        url += urlencode(params)
        data = {}
        data = json.dumps(data).encode()
        try:
            response = urlopen(url=url, data=data)
            response_data = response.read().decode()
        except WEIBOAPIError as e:
            logger.error('access_token请求失败:%s' % e)
            raise WEIBOAPIError
        data = json.loads(response_data)
        return data