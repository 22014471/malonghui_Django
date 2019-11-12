import logging
from rest_framework import serializers

from activity.models import Activity
from headlines.models import HeadlinesCategory, HeadlinesNews, NewsComment, UserAttention, NewsCollection
from questions.models import Question, Tag
from talks.models import Talks
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器1
    """
    class Meta:
        model = User
        fields = ("id", "username", "avatar")


class NewsSerializer(serializers.ModelSerializer):
    """
    新闻序列化器
    """
    class Meta:
        model = HeadlinesNews
        fields = ("id", "title", "create_time")


class NewsCollectionSerializer(serializers.ModelSerializer):
    """
    收藏序列化器
    """
    user = UserSerializer()

    class Meta:
        model = NewsCollection
        fields = ("user",)


class QuestionSerializer(serializers.ModelSerializer):
    """
    头条详情作者问答排行序列化器
    """
    class Meta:
        model = Question
        fields = ('id', 'title', 'update_time')


class AuthorAttentionSerializer(serializers.ModelSerializer):
    """
    作者粉丝序列化器
    """
    user = UserSerializer()

    class Meta:
        model = User
        fields = ("id", 'user')


class HeadlineUserSerializer(serializers.ModelSerializer):
    """
    用户序列化器2(用户新闻+用户粉丝)
    """
    news = NewsSerializer(many=True)
    attention = AuthorAttentionSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "avatar", 'news', 'attention')


class HeadlineAuthorSerializer(serializers.ModelSerializer):
    """
    用户序列化器3(用户粉丝)
    """
    attention = AuthorAttentionSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "avatar", 'attention')


class HeadlinesCategorySerializer(serializers.ModelSerializer):
    """
    头条分类序列化器
    """
    class Meta:
        model = HeadlinesCategory
        fields = ('id', 'name')


class HeadlinesNewsSerializer(serializers.ModelSerializer):
    """
    头条新闻列表序列化器
    """
    author = HeadlineAuthorSerializer()

    class Meta:
        model = HeadlinesNews
        fields = ('id', 'title', 'author', 'create_time', 'content', "clicks")


class HeadlinesDetailSerializer(serializers.ModelSerializer):
    """
    头条新闻详情序列化器
    """
    author = HeadlineUserSerializer()
    collected = NewsCollectionSerializer(many=True)

    class Meta:
        model = HeadlinesNews
        fields = ('id', 'title', 'author', 'collected', 'create_time', 'content', "comment_count")


class CommentsSerializer(serializers.ModelSerializer):
    """
    新闻评论序列化器
    """
    user = UserSerializer()

    class Meta:
        model = NewsComment
        fields = ('id', 'user', 'content')


class HeadlinesCommentsSerializer(serializers.ModelSerializer):
    """
    头条新闻详情页评论序列化器
    """
    user = UserSerializer()
    child = CommentsSerializer(many=True)

    class Meta:
        model = NewsComment
        fields = ('id', 'user', 'content', 'child', 'parent')


class HeadlinesCommentAddSerializer(serializers.ModelSerializer):
    """
    评论添加序列化器
    """
    class Meta:
        model = NewsComment
        fields = ('id', 'news', 'user', 'content', 'parent')

    def create(self, validated_data):
        """
        创建评论
        """
        news= validated_data['news']
        news.comment_count += 1
        news.save()
        return super().create(validated_data)


class HeadlinesQuestionSerializer(serializers.ModelSerializer):
    """
    头条首页问答排行序列化器
    """
    author = UserSerializer()

    class Meta:
        model = Question
        fields = ('id', 'author', 'title', 'update_time')


class HeadlinesActivitiesSerializer(serializers.ModelSerializer):
    """
    热门活动排行序列化器
    """

    class Meta:
        model = Activity
        fields = ('id', 'cover', 'city', 'act_name', 'start_time')


class HeadlinesTalksSerializer(serializers.ModelSerializer):
    """
    详情页吐槽排行序列化器
    """
    class Meta:
        model = Talks
        fields = ('id', 'content')


class HeadlinesHotsSerializer(serializers.ModelSerializer):
    """
    详情页热门头条排行序列化器
    """
    class Meta:
        model = HeadlinesNews
        fields = ('id', 'title')


class HeadlinesUserAttention(serializers.ModelSerializer):
    """
    用户关注作者序列化器
    """
    class Meta:
        model = UserAttention
        fields = ('user', 'author')

    def create(self, validated_data):
        """
        创建关注保存
        """
        user = validated_data['user']
        author = validated_data['author']

        # fans_list = author.attention.all() #作者的fans表
        # user_attention = user.fun.all()  #用户的attention表
        # print(fans_list)
        # print(user_attention)
        # # 判断是否关注过
        # for fan in fans_list:
        #     if user == fan.user:
        #         raise serializers.ValidationError('已关注该用户，请勿重复添加')

        #判断作者是否存在
        if not author:
            raise serializers.ValidationError('没有该作者')

        # 判断作者是否是用户自己
        if author.id == user.id:
            raise serializers.ValidationError('自己不能关注自己')

        return super().create(validated_data)


class HeadlinesUserCollectionSerializer(serializers.ModelSerializer):
    """
    用户收藏序列化器
    """
    class Meta:
        model = NewsCollection
        fields = ('user', 'news')

    def create(self, validated_data):
        """
        创建收藏保存
        """
        user = validated_data['user']
        news = validated_data['news']

        #判断作者是否存在
        if not news:
            raise serializers.ValidationError('没有该新闻')

        # 判断作者是否是用户自己
        if news.author == user:
            raise serializers.ValidationError('不能收藏自己的新闻')

        return super().create(validated_data)


class HeadlinesNewsAddSerializer(serializers.ModelSerializer):
    """
    发布新闻序列化器
    """
    class Meta:
        model = HeadlinesNews
        fields = ("title", 'category', 'author', 'content')

