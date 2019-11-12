from django.db import models

# Create your models here.
from users.models import User


class Talks(models.Model):
    """吐槽模型"""
    TALK_STATUS_ENUM = {
        (1, "审核中"),
        (0, "审核通过"),
        (-1, "审核失败")
    }
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="吐槽用户")
    content = models.TextField(verbose_name="吐槽内容")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="发布时间")
    status = models.SmallIntegerField(choices=TALK_STATUS_ENUM, default=1, verbose_name="状态")
    like_count = models.IntegerField(default=0, verbose_name="点赞总数")
    comment_count = models.IntegerField(default=0, verbose_name="评论总数")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名吐槽')
    like_user = models.ManyToManyField(to=User, through="TalkLike", related_name="like_talks", verbose_name="点赞吐槽的用户")
    collect_user = models.ManyToManyField(to=User, through="TalkCollection", related_name="collect_talks",
                                          verbose_name="收藏吐槽的用户")
    collect = models.BooleanField(default=False, verbose_name="是否收藏")
    is_like = models.BooleanField(default=False, verbose_name="是否点赞")

    class Meta:
        db_table = "tb_talks"
        verbose_name = "吐槽"
        verbose_name_plural = verbose_name

    def __str__(self):  # admin显示内容
        return self.content


class TalkComment(models.Model):
    """评论模型"""
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="评论用户")
    talk_id = models.ForeignKey(Talks, on_delete=models.PROTECT, verbose_name="吐槽")
    content = models.CharField(max_length=1024, verbose_name="吐槽评论")
    like_count = models.IntegerField(default=0, verbose_name="点赞数")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "tb_talk_comment"
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __str__(self):  # admin显示内容
        return self.content


class TalkCollection(models.Model):
    """吐槽的收藏"""
    talk = models.ForeignKey(Talks, on_delete=models.PROTECT, verbose_name="吐槽的收藏")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="收藏用户")

    class Meta:
        db_table = "tb_talk_collection"
        verbose_name = "吐槽的收藏"
        verbose_name_plural = verbose_name


class TalkLike(models.Model):
    """吐槽的点赞"""
    talk = models.ForeignKey(Talks, on_delete=models.PROTECT, verbose_name="吐槽的点赞")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="吐槽点赞用户")

    class Meta:
        db_table = "tb_talk_like"
        verbose_name = "吐槽的收藏"
        verbose_name_plural = verbose_name


class CommentLike(models.Model):
    """评论的点赞"""
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="评论点赞用户")
    comment = models.ForeignKey(TalkComment, on_delete=models.PROTECT, verbose_name="评论的点赞")
    is_like = models.BooleanField(default=False, verbose_name="是否点赞")

    class Meta:
        db_table = "tb_comment_like"
        verbose_name = "评论的点赞"
        verbose_name_plural = verbose_name
