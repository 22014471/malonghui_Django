from django.db import models

# Create your models here.


class Activity(models.Model):
    """
    活动模型类
    """
    GENDER_CHOICES = (
        (0, '立即报名'),
        (1, '报名进行中'),
        (2, '报名结束'),

    )
    act_name = models.CharField(max_length=64, verbose_name='活动名称')
    cover = models.URLField(verbose_name='封面图片')
    start_time = models.DateTimeField(verbose_name='活动开始时间')
    start_end = models.DateTimeField(verbose_name='活动结束时间')
    city = models.CharField(max_length=16, verbose_name='举办城市')
    act_address = models.CharField(max_length=128, verbose_name='举办地点')
    sponsor = models.CharField(max_length=64, verbose_name='举办方')
    deadline = models.DateTimeField(verbose_name='报名截止时间')
    detail = models.TextField(verbose_name='详情')
    introduce = models.TextField(verbose_name='大会介绍')
    status = models.SmallIntegerField(choices=GENDER_CHOICES, verbose_name='活动状态')
    web_sit = models.URLField(verbose_name='链接网址')

    class Meta:
        db_table = 'tb_activity'
        verbose_name = '活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.act_name
