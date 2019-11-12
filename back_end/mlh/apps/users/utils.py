import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    设置jwt返回值
    :param token:
    :param user:
    :param request:
    :return:
    """
    request.user = user
    return {
        "token": token,
        "user_id": user.id,
        "avatar": user.avatar,
        "username": user.username
    }


def get_user_by_account(account):
    """
    根据帐号获取user对象
    :param account: 账号，可以是手机号，也可以是邮箱
    :return: User对象 或者 None
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 帐号为手机号
            user = User.objects.get(mobile=account)
        elif re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",account):
            # 帐号为邮箱
            user = User.objects.get(email=account)
        else:
            return None
    except User.DoesNotExist:
        return None
    else:
        return user



class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user