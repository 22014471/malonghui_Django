import logging

from .utils.yuntongxun.sms import CCP
from celery_tasks.main import celery_app

logger = logging.getLogger('django')


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code, sms_expiry, sms_temp_id):
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile, [sms_code, sms_expiry], sms_temp_id)
    except Exception as e:
        logger.error("短信验证码发送失败[%s]:%s" % (mobile, e))
    else:
        if result == 0:
            logger.error("短信验证码发送成功[%s]" % mobile)
        else:
            logger.error("短信验证码发送失败[%s]" % mobile)
