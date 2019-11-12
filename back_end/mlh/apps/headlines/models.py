from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
from questions.models import Tag
from users.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class HeadlinesCategory(models.Model):
    """
    头条分类
    """
    name = models.CharField(max_length=10, unique=True, null=False, verbose_name='分类名称')
    weight = models.SmallIntegerField(default=1, verbose_name='显示顺序')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_headlines_category'
        verbose_name = '头条分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class HeadlinesNews(models.Model):
    """
    头条新闻
    """
    title = models.CharField(max_length=30, unique=True, null=False, verbose_name='头条标题')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news', verbose_name='发布作者')
    category = models.ForeignKey(HeadlinesCategory, on_delete=models.CASCADE, verbose_name='分类')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    content = RichTextField(verbose_name='内容')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    clicks = models.IntegerField(default=0, verbose_name='点击量')
    tags = models.ManyToManyField(to=Tag, blank=True, through='NewsTag', related_name='new', verbose_name='文章所属标签')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_headlines_news'
        verbose_name = '头条新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class NewsComment(models.Model):
    """
    头条新闻评论
    """
    news = models.ForeignKey(HeadlinesNews, on_delete=models.CASCADE, verbose_name='新闻')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", verbose_name='评论用户')
    content = models.CharField(max_length=300, verbose_name='评论内容')
    parent = models.ForeignKey('self', null=True, blank=True, related_name="child", verbose_name='父评论')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_news_comment'
        verbose_name = '新闻评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class NewsCollection(models.Model):
    """
     用户收藏新闻
    """
    news = models.ForeignKey(HeadlinesNews, on_delete=models.CASCADE, related_name='collected', verbose_name='收藏的新闻')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections', verbose_name='用户')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        db_table = 'tb_news_collection'
        verbose_name = '新闻收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.news.title


class UserAttention(models.Model):
    """
     用户关注作者
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fun', verbose_name='用户')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attention', verbose_name='关注作者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        db_table = 'tb_user_attention'
        verbose_name = '用户关注作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class NewsTag(models.Model):
    """
    新闻标签
    """
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="标签")
    news = models.ForeignKey(HeadlinesNews, on_delete=models.CASCADE, verbose_name="新闻")

    class Meta:
        db_table = "tb_news_tags"
        verbose_name = "新闻标签"
        verbose_name_plural = verbose_name