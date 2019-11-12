from celery import Celery
import os

# 为celery设置django默认配置
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mlh.settings.dev'



# 创建对象，命名为meiduo,并指明broker
celery_app = Celery('mlh',broker='redis://127.0.0.1:6379/15')

# 自动注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms',])