
from django.db import models
from users.models import User


class QuestionCategory(models.Model):
    """
    问题分类模型类
    """
    name = models.CharField(max_length=64, verbose_name="问题分类名")
    sequence = models.IntegerField(verbose_name="问题分类顺序")
    is_deleted = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "tb_question_categories"
        verbose_name = "问题分类表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TagCategory(models.Model):
    """问题标签分类表"""
    name = models.CharField(max_length=20, verbose_name="问题标签名称")
    is_deleted = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "tb_tag_categories"
        verbose_name = "问题表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """问题标签模型类"""
    name = models.CharField(max_length=20, unique=True, verbose_name="标签名称")
    concerns = models.IntegerField(default=0, verbose_name="标签关注人数")
    describe = models.CharField(max_length=140, verbose_name="标签描述")
    image_url = models.CharField(max_length=256, verbose_name="标签图标url")
    category = models.ForeignKey(TagCategory, related_name="category_tags", on_delete=models.PROTECT, verbose_name="标签分类")
    is_deleted = models.BooleanField(default=False, verbose_name="逻辑删除")
    concern_user = models.ManyToManyField(to=User, blank=True, through='TagConcern', related_name="concern_tags", verbose_name="关注该标签的用户")

    class Meta:
        db_table = "tb_tags"
        verbose_name = "标签表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Question(models.Model):
    """问题模型类"""
    title = models.CharField(max_length=64, unique=True, verbose_name="问题标题")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question', verbose_name="问题作者")
    content = models.CharField(max_length=120, verbose_name="问题内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="问题创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="问题更新时间")
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, verbose_name="问题分类")
    visits = models.IntegerField(default=0, verbose_name="浏览量")
    like_count = models.IntegerField(default=0, verbose_name="问题点赞数")
    answer_count = models.IntegerField(default=0, verbose_name="问题解答数")
    status = models.IntegerField(default=1, verbose_name="问题状态")
    is_deleted = models.BooleanField(default=False, verbose_name="逻辑删除")
    latest_answer = models.OneToOneField(to="Answer", null=True, blank=True, on_delete=models.CASCADE, related_name='answer_question', verbose_name="问题最新回答")
    question_tags = models.ManyToManyField(to='Tag', blank=True, through='QuestionTag', verbose_name="该问题的标签")
    like_users = models.ManyToManyField(to=User, blank=True, through="QuestionLike", related_name="like_questions", verbose_name="点赞该问题的用户")

    class Meta:
        db_table = "tb_questions"
        verbose_name = "问题表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Answer(models.Model):
    """解答模型类"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer', verbose_name="解答用户")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answer', verbose_name="问题")
    parent = models.ForeignKey('Answer', blank=True, null=True, on_delete=models.CASCADE, related_name='parent_answer', verbose_name="父评论")
    content = models.CharField(max_length=200,verbose_name="解答内容")
    create_time = models.DateTimeField(auto_now_add=True ,verbose_name="解答时间")
    is_deleted = models.BooleanField(default=False, verbose_name="逻辑删除")
    like_count = models.IntegerField(default=0, verbose_name="解答点赞数")
    like_users = models.ManyToManyField(to=User, blank=True, through="AnswerLike", related_name="like_answers", verbose_name="点赞该解答的用户")

    class Meta:
        db_table = "tb_answers"
        verbose_name = "解答表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "解答"


class AnswerLike(models.Model):
    """解答模点赞表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="点赞解答的用户")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="点赞的解答")

    class Meta:
        db_table = "tb_answer_likes"
        verbose_name = "解答点赞表"
        verbose_name_plural = verbose_name


class QuestionTag(models.Model):
    """问题的标签表"""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_questions', verbose_name="问题的标签")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='qtags', verbose_name="标签所属的问题")

    class Meta:
        db_table = "tb_question_tags"
        verbose_name = "问题表"
        verbose_name_plural = verbose_name


class TagConcern(models.Model):
    """标签关注表"""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="关注的标签")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="关注标签的人")

    class Meta:
        db_table = "tb_tag_concerns"
        verbose_name = "标签关注表"
        verbose_name_plural = verbose_name


class QuestionLike(models.Model):
    """点赞模型类"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="用户")
    question = models.ForeignKey(Question, on_delete=models.CASCADE,verbose_name="问题")

    class Meta:
        db_table = "tb_question_likes"
        verbose_name = "点赞表"
        verbose_name_plural = verbose_name
