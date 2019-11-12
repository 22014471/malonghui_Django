import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from oauth.models import OAuthUser, QuestionShareToOAuth
from oauth.utils import QQOAuth, WEIBOAuth
from questions.models import Question
from users.models import User


class QQUserSerializer(serializers.ModelSerializer):
    """QQ绑定用户序列化器"""
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6, write_only=True)
    mobile = serializers.CharField(max_length=11, label='手机号')
    token = serializers.CharField(label='JWT Token', read_only=True)
    access_token = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['mobile','token','sms_code','password','username','access_token']
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的用户名',
                    'max_length': '仅允许8-20个字符的用户名',
                }
            }
        }

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机格式错误')
        return value

    def validate(self, attrs):
        # 检测token是否合法
        access_token = attrs['access_token']
        openid = QQOAuth.check_save_user_token(access_token)
        if not openid:
            raise serializers.ValidationError('无效的access_token')
        attrs['openid'] = openid
        # 验证短信验证码是否正确
        mobile = attrs['mobile']
        sms_code = attrs['sms_code']
        redis_conn = get_redis_connection('verify_codes')
        real_sms_code = redis_conn.get("sms_%s" % mobile)
        real_sms_code = real_sms_code.decode()
        if not real_sms_code:
            raise serializers.ValidationError('无效的短信验证码')
        if real_sms_code != sms_code:
            raise serializers.ValidationError('短信验证码错误')

        user = User.objects.filter(mobile=mobile).first()
        password = attrs['password']
        if user:
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')
            attrs['user'] = user
        return attrs

    def create(self, validated_data):

        mobile = validated_data['mobile']
        password = validated_data['password']
        openid = validated_data['openid']
        user = validated_data.get('user', None)
        if user is None:
            user = User.objects.create(username=mobile, mobile=mobile, password=password)
        OAuthUser.objects.create(uid=openid, user=user)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token
        self.context['request'].user = user
        return user

class WBUserSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6, write_only=True)
    mobile = serializers.CharField(max_length=11, label='手机号')
    token = serializers.CharField(label='JWT Token', read_only=True)
    access_token = serializers.CharField(write_only=True)
    oauth_access_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['mobile','token','sms_code','password','username','access_token','oauth_access_token']
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的用户名',
                    'max_length': '仅允许8-20个字符的用户名',
                }
            }
        }

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机格式错误')
        return value

    def validate(self, attrs):
        # 检测token是否合法
        access_token = attrs['access_token']
        uid = WEIBOAuth.check_save_user_token(access_token)
        if not uid:
            raise serializers.ValidationError('无效的access_token')
        attrs['uid'] = uid
        # 验证短信验证码是否正确
        mobile = attrs['mobile']
        sms_code = attrs['sms_code']
        redis_conn = get_redis_connection('verify_codes')
        real_sms_code = redis_conn.get("sms_%s" % mobile)
        real_sms_code = real_sms_code.decode()
        if not real_sms_code:
            raise serializers.ValidationError('无效的短信验证码')
        if real_sms_code != sms_code:
            raise serializers.ValidationError('短信验证码错误')

        user = User.objects.filter(mobile=mobile).first()
        password = attrs['password']
        if user:
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')
            attrs['user'] = user
        return attrs

    def create(self, validated_data):

        mobile = validated_data['mobile']
        password = validated_data['password']
        uid = validated_data['uid']
        user = validated_data.get('user', None)
        if user is None:
            user = User.objects.create(username=mobile, mobile=mobile, password=password)
        OAuthUser.objects.create(uid=uid, user=user)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token
        self.context['request'].user = user
        return user


class QuestionOAuthShareSerializer(serializers.Serializer):
    """问题第三方分享序列化器"""
    question_id = serializers.CharField(label="问题id")

    def create(self, attrs):
        question_id = attrs['question_id']
        question = Question.objects.filter(id=question_id).first()
        if not question:
            raise serializers.ValidationError('请求错误')
        user = self.context['request'].user
        question_share = QuestionShareToOAuth.objects.filter(user=user,question=question).first()
        if question_share:
            raise serializers.ValidationError('请求错误')
        instance = QuestionShareToOAuth.objects.create(
            user=user,
            question=question
        )
        return instance
