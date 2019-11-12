from django.db import models

# Create your models here.
from questions.models import Question
from users.models import User


class BaseModel(models.Model):
    """为模型类补充字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表

class OAuthUser(BaseModel):
    """QQ登录用户类"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    uid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Mete:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name


class QuestionShareToOAuth(BaseModel):
    """第三方分享"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="用户")



