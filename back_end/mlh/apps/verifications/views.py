import random

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from . import constants
from celery_tasks.sms.tasks import send_sms_code

# /sms_codes/(?P<mobile>1[3-9]\d{9})/
class SMSCodeView(APIView):
    """获取短信验证码"""
    def get(self, request, mobile):
        # 手机号、text
        redis_conn = get_redis_connection('verify_codes')
        sms_code = "%06d" % random.randint(0, 999999)
        print("sms_code: ", sms_code) # 测试用

        # 在发送短信验证码前保存数据，以免多次访问和注册时验证
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_TIME, sms_code)
        pl.setex("send_sms_%s" % mobile, constants.SEND_SMS_CODE_TIME, 1)
        pl.execute()

        # send_sms_code.delay(mobile, sms_code, constants.SEND_SMS_CODE_TIME//60, constants.SMS_CODE_TEMP_ID)
        return Response({"message": "ok"})