from rest_framework import serializers

from talks.models import Talks, TalkComment, TalkLike, TalkCollection, CommentLike
from users.models import User


class TalksListSerializer(serializers.ModelSerializer):
    """吐槽首页序列化器"""
    is_like = serializers.BooleanField(read_only=True)
    is_collect = serializers.BooleanField(read_only=True)

    class Meta:
        model = Talks
        fields = ("id", "content", "create_time", "user", "like_count", 'is_like', 'is_collect')


class TalksUserMessageSerializer(serializers.ModelSerializer):
    """吐槽用户序列化器"""

    class Meta:
        model = User
        fields = ('username', 'avatar')


class TalksDetailSerializer(serializers.ModelSerializer):
    """吐槽详情序列化器"""
    user = TalksUserMessageSerializer(read_only=True)
    is_like = serializers.CharField(read_only=True)

    class Meta:
        model = Talks
        fields = ("id", "content", "like_count", "comment_count", "user", "is_like")


class CommentUserSerializer(serializers.ModelSerializer):
    """评论用户序列化器"""

    class Meta:
        model = User
        fields = ('username', 'avatar')


class TalkCommentSerializer(serializers.ModelSerializer):
    """评论列表"""
    is_like = serializers.BooleanField(read_only=True)

    # user = TalksUserMessageSerializer(read_only=True)
    class Meta:
        model = TalkComment
        fields = ("id", "content", "like_count", "user", 'create_time', 'talk_id', 'is_like')
        # fields = '__all__'

    def create(self, validated_data):
        talk = validated_data['talk_id']
        talk.comment_count += 1
        talk.save()
        talkcomment = TalkComment.objects.create(**validated_data)
        talkcomment.save()
        return talkcomment


class TalkCommentLikeSerializer(serializers.ModelSerializer):
    """评论点赞序列化器"""

    class Meta:
        model = CommentLike
        fields = '__all__'

    # 获取用户登录的相关信息
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_talks(self, value):
        """校验所属吐槽"""
        if not TalkComment.objects.get(id=value.id):
            raise serializers.ValidationError('吐槽评论内容不存在')
        return value


class TalkLikeSerializer(serializers.ModelSerializer):
    """吐槽点赞序列化器"""
    talk_id = serializers.CharField(required=True)

    class Meta:
        model = TalkLike
        fields = ("talk_id",)

    # 获取用户登录的相关信息
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_talks(self, value):
        """校验所属吐槽"""
        if not Talks.objects.get(id=value.id):
            raise serializers.ValidationError('吐槽内容不存在')
        return value


class TalkCollectSerializer(serializers.ModelSerializer):
    """吐槽收藏序列化器"""
    talk_id = serializers.CharField(required=True)

    class Meta:
        model = TalkCollection
        fields = ("talk_id",)

        # 获取用户登录的相关信息

    def validate(self, attrs):
        talk_id = attrs['talk_id']
        user = self.context['request'].user
        talk_collection = TalkCollection.objects.filter(talk_id=talk_id, user=user).first()
        if talk_collection:
            raise serializers.ValidationError('请求错误')
        attrs['user'] = user
        return attrs

    def validate_talks(self, value):
        """校验所属吐槽"""
        if not Talks.objects.get(id=value.id):
            raise serializers.ValidationError('吐槽内容不存在')
        return value


class CreationTsukkomiSerializer(serializers.ModelSerializer):
    """创建吐槽信息"""
    like_count = serializers.IntegerField(default=0, label="点赞数量", read_only=True)
    comment_count = serializers.IntegerField(default=0, label="评论数量", read_only=True)
    user = serializers.StringRelatedField(read_only=True, label="用户名")  # 显示用户名而不是用户id

    class Meta:
        model = Talks
        fields = ("id", "content", "create_time", "like_count", "comment_count", "user")
        extra_kwargs = {
            'create_time': {
                "read_only": True,

            },

        }

    def validate_content(self, data):
        if data is None:
            raise serializers.ValidationError("吐槽内容为空")
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        talks = Talks.objects.create(content=validated_data["content"], user_id=user.id)

        talks.save()
        return talks


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('id', 'comment', 'user',)
        extra_kwargs = {
            'uers': {
                'read_only': True,
            }
        }

        def validate(self, attrs):
            if not CommentLike.object.get(id=attrs['comment'].id):
                raise serializers.ValidationError('sss')
            return attrs

        def create(self, validated_data):
            user_id = self.context['request'].user.id
            request = self.context['request']
            if not request.COOKIES.get('like_comment_' + str(validated_data['comment'].id)):
                comment = CommentLike.objects.create(comment=validated_data['comment'], user_id=user_id)
                return comment
            else:
                raise serializers.ValidationError({'message': 'sajksjkd'})
