import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from headlines.models import HeadlinesNews
from questions.models import Answer, Question, Tag
from talks.models import Talks
from users.models import User


class UserCreateCheckSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(write_only=True)
    allow = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'sms_code', 'mobile', 'allow', "token")
        extra_kwargs = {
            "username": {
                "min_length": 5,
                "max_length": 32,
                "error_messages": {
                    "min_length": "用户名5-32个字符",
                    "max_length": "用户名5-32个字符"
                    }
            },
            "password": {
                "min_length": 8,
                "max_length": 20,
                "error_messages": {
                    "min_length": "密码8-20个字符",
                    "max_length": "密码8-20个字符"
                }
            }
        }

    def validate_mobile(self, value):
        if not re.match(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError("手机号格式不正确")
        return value

    def validate_allow(self, value):
        if value != "true":
            raise serializers.ValidationError("请同意用户协议")
        return value

    def validate(self, attrs):
        sms_code = attrs["sms_code"]
        mobile = attrs["mobile"]
        redis_conn = get_redis_connection('verify_codes')
        real_sms_code = redis_conn.get("sms_%s" % mobile)
        # 当用户使用其他手机号，和注册手机的验证码注册时，上面的代码则会报错'NoneType' object has no attribute 'decode'，所以分开来写
        if not real_sms_code:
            raise serializers.ValidationError("无效的验证码")
        real_sms_code = real_sms_code.decode()
        if sms_code != real_sms_code:
            raise serializers.ValidationError("短信验证码不正确")
        return attrs

    def create(self, validated_data):
        """创建用户"""
        del validated_data["sms_code"]
        del validated_data["allow"]
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        # jwt token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        self.context['request'].user = user
        return user


class UserBaseSerializer(serializers.ModelSerializer):
    """个人中心表头页数据序列化器"""
    class Meta:
        model = User
        fields = ("username", "live_city", "graduation", "commany", "personal_url", "avatar")


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """回答"""
    title = serializers.CharField(read_only=True,min_length=1)


class AnswerSerializer(serializers.ModelSerializer):
    """回答序列化器"""
    question = serializers.SlugRelatedField(label="问题标题", read_only=True, slug_field="title")
    class Meta:
        model = Answer
        fields = ("id", "like_count", "question", "question_id", "create_time")


class QuestionSerializer(serializers.ModelSerializer):
    """ 问题序列化器"""
    class Meta:
        model = Question
        fields = ("id", "like_count", "title", "create_time")


class AccountSerializer(serializers.ModelSerializer):
    """个人账户设置序列化器"""
    class Meta:
        model = User
        fields = ("username", "personal_url", "email", "mobile", "live_city", "graduation", "commany", "address","gender", "birthday")


class DynamicTagSerialzer(serializers.ModelSerializer):
    """个人动态标签序列化器"""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'concerns', 'describe')

class DynamicAnswerSerialzer(serializers.ModelSerializer):
    """个人动态回答序列化器"""
    question = serializers.SlugRelatedField(label="问题标题", read_only=True, slug_field="title")

    class Meta:
        model = Answer
        fields = ('id', 'question', 'content','question_id')

class DynamicTalksSerialzer(serializers.ModelSerializer):
    """个人动态吐槽序列化器"""
    class Meta:
        model = Talks
        fields = ('id','content')

class DynamicNewsSerialzer(serializers.ModelSerializer):
    """个人动态新闻序列化器"""
    class Meta:
        model = HeadlinesNews
        fields = ('id','title')


class DynamicSerializer(serializers.Serializer):
    """个人动态序列化器"""
    """
    :type
    (0, 'tag'),---标签
    (1, 'answer'),---回答
    (2, 'talks'),---吐槽
    (3, 'headline_news')---新闻
    """
    id = serializers.IntegerField(label="个人动态id",read_only=True)
    create_time = serializers.DateTimeField(label="关注时间",read_only=True)
    action = serializers.CharField(min_length=1,label="用户动作")
    type = serializers.IntegerField(label="动态类型", min_value=0)
    type_id = serializers.IntegerField(label="类型id",min_value=0)


class CollectNewsSerializer(serializers.ModelSerializer):
    """新闻收藏序列化器"""
    author = serializers.SlugRelatedField(label="新闻作者", read_only=True, slug_field="username")
    class Meta:
        model = HeadlinesNews
        fields = ("id", "title", "author", "content")


class CollectTalksAuthorSerializer(serializers.ModelSerializer):
    """吐槽收藏的作者的序列化器"""
    class Meta:
        model = User
        fields = ("id", "username", "avatar", "email")


class CollectTalksSerializer(serializers.Serializer):
    """吐槽收藏序列化器"""
    id = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(max_value=0)
    content = serializers.CharField(max_length=0)
