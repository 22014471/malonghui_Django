from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'famale')
    )
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性別')
    birthday = models.DateField(verbose_name='出生日期', blank=True, null=True)
    personal_url = models.CharField(max_length=64, verbose_name='个人网站', blank=True, null=True)
    live_city = models.CharField(max_length=64,verbose_name='现居城市', blank=True, null=True)
    address = models.CharField(max_length=64,verbose_name='通讯地址',blank=True, null=True)
    avatar = models.CharField(max_length=256, verbose_name='头像', blank=True, null=True)
    graduation = models.CharField(max_length=64,verbose_name='毕业学校', blank=True, null=True)
    commany = models.CharField(max_length=32,verbose_name='所在公司', blank=True, null=True)

    class Meta:
        db_table = "tb_users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Technology(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    techn = models.CharField(max_length=32, verbose_name="技术名称")

    class Meta:
        db_table = "tb_technology"
        verbose_name = "擅长技术"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.techn


class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    start_time = models.DateField(verbose_name="工作起始时间")
    end_time = models.DateField(verbose_name="工作结束时间", null=True, blank=True)
    work_position = models.CharField(max_length=64, verbose_name="职位")

    class Meta:
        db_table = "tb_work_experience"
        verbose_name = "工作经历"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.work_position


class StudyExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    start_time = models.DateField(verbose_name="学习起始时间")
    end_time = models.DateField(verbose_name="学习结束时间")
    study_position = models.CharField(max_length=32, verbose_name="所学专业或任职")

    class Meta:
        db_table = "tb_study_experience"
        verbose_name = "教育经历"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.study_position


class Dynamic(models.Model):
    """个人动态模型类"""
    TYPE_CHOICES = (
        (0, 'tag'),
        (1, 'answer'),
        (2, 'talk'),
        (3, 'headline_news'),
    )
    user = models.ForeignKey(User,verbose_name="用户")
    update_time = models.DateTimeField(auto_now=True, verbose_name="关注时间")
    action = models.CharField(max_length=32,verbose_name="用户具体动作")
    type = models.SmallIntegerField(choices=TYPE_CHOICES, verbose_name='动态类型')
    type_id = models.IntegerField(verbose_name="类型id")

    class Meta:
        db_table = "tb_dynamic"
        verbose_name = "个人动态"
        verbose_name_plural = verbose_name


