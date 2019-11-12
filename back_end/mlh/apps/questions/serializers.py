from rest_framework import serializers

from questions.models import Question, Tag, Answer, QuestionCategory, QuestionLike, AnswerLike, TagConcern, TagCategory, \
    QuestionTag
from users.models import User, Dynamic


class QuestionCategorySerializer(serializers.ModelSerializer):
    """问题分类序列化器"""
    class Meta:
        model = QuestionCategory
        fields = ('id', 'name')


class LatestQASerializer(serializers.ModelSerializer):
    """问题最新回答"""
    user = serializers.SlugRelatedField(label="问题作者", read_only=True, slug_field='username')

    class Meta:
        model = Answer
        fields = ('id', 'create_time', 'user')


class QuestionTagsSerializer(serializers.ModelSerializer):
    """该问题所含标签序列化器"""

    class Meta:
        model = Tag
        fields = ('id', 'name')


class QuestionListSerializer(serializers.ModelSerializer):
    """问题列表序列化器"""
    author = serializers.SlugRelatedField(label="问题作者", read_only=True, slug_field='username')
    latest_answer = LatestQASerializer(read_only=True)
    question_tags = QuestionTagsSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        exclude = ('content', 'is_deleted', 'like_users')


class QAAuthorSerializer(serializers.ModelSerializer):
    """该解答的作者序列化器"""
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class ParentAnswerSerializer(serializers.ModelSerializer):
    """父解答序列化器"""
    user = QAAuthorSerializer(read_only=True)

    class Meta:
        model = Answer
        exclude = ('like_users',)


class QAnswerSerializer(serializers.ModelSerializer):
    """该问题的解答序列化器"""
    user = QAAuthorSerializer(read_only=True)
    is_like = serializers.IntegerField(label="用户是否点赞")
    is_author = serializers.IntegerField(label="用户是否是作者")
    parent = ParentAnswerSerializer()

    class Meta:
        model = Answer
        exclude = ('like_users',)


class QuestionDetailSerializer(serializers.ModelSerializer):
    """问题详情序列化器"""
    author = serializers.SlugRelatedField(label="问题作者", read_only=True, slug_field='username')
    is_like = serializers.IntegerField(label="用户是否点赞")
    question_tags = QuestionTagsSerializer(read_only=True, many=True)
    is_author = serializers.IntegerField(label="用户是否作者")

    class Meta:
        model = Question
        exclude = ('visits', 'is_deleted', 'like_users')


class PublishAnswerSerializer(serializers.ModelSerializer):
    """发表解答序列化器"""
    question = serializers.CharField(write_only=True, required=True)
    parent = serializers.CharField(required=False)

    class Meta:
        model = Answer
        exclude = ('like_users', 'is_deleted')
        read_only_fields = ['id', 'user']
        extra_kwargs = {
            'content':{
                'required': True,
            },
        }

    def validate(self, attrs):
        question_id = attrs['question']
        question = Question.objects.filter(id=question_id).first()
        if not question:
            raise serializers.ValidationError("问题不存在")
        attrs['question'] = question
        return attrs

    def create(self, validated_data):
        content = validated_data['content']
        request = self.context['request']
        user = request.user
        question = validated_data['question']
        parent_id = validated_data.get('parent', None)
        answer = Answer.objects.create(
            content=content,
            user=user,
            question=question,
            parent_id=parent_id,
        )
        question.answer_count += 1
        question.latest_answer = answer
        question.save()

        # 将 回答问题 记录到 我的动态表 中
        if request.user and request.user.is_authenticated():
            Dynamic.objects.create(user=request.user, type=1, action="回答了问题", type_id=answer.id)

        return answer


class QuestionLikeSerializer(serializers.Serializer):
    """问题点赞序列化器"""
    action = serializers.CharField(write_only=True, required=True)
    question_id = serializers.CharField(required=False)
    user_id = serializers.CharField(read_only=True)

    def validate(self, attrs):
        question_id = attrs['question_id']
        question = Question.objects.filter(id=question_id).first()
        if not question:
            raise serializers.ValidationError('错误的请求')
        action = attrs['action']
        if action not in ['like', 'dislike']:
            raise serializers.ValidationError('错误的请求')
        request = self.context['request']
        user = request.user
        question_like = QuestionLike.objects.filter(user=user, question=question).first()
        if question_like:
            raise serializers.ValidationError('一个问题只能点赞或踩一次')
        return attrs

    def create(self, validated_data):
        action = validated_data.get("action")
        request = self.context['request']
        user = request.user
        question_id = validated_data.get('question_id')
        question = Question.objects.filter(id=question_id).first()
        if not question:
            raise serializers.ValidationError('错误的请求')
        instance = QuestionLike.objects.create(
            user=user,
            question=question
        )
        if action == 'like':
            question.like_count += 1
        else:
            question.like_count -= 1
        question.save()
        return instance


class AnswerLikeSerializer(serializers.Serializer):
    """解答点赞序列化器"""
    action = serializers.CharField(write_only=True, required=True)
    answer_id = serializers.CharField(required=False)
    user_id = serializers.CharField(read_only=True)

    def validate(self, attrs):
        answer_id = attrs['answer_id']
        answer = Answer.objects.filter(id=answer_id).first()
        if not answer:
            raise serializers.ValidationError('错误的请求')
        action = attrs['action']
        if action not in ['like', 'dislike']:
            raise serializers.ValidationError('错误的请求')
        request = self.context['request']
        user = request.user
        answer_like = AnswerLike.objects.filter(user=user,answer=answer).first()
        if answer_like:
            raise serializers.ValidationError('一个解答只能点赞或踩一次')
        return attrs

    def create(self, validated_data):
        action = validated_data.get("action")
        request = self.context['request']
        user = request.user
        answer_id = validated_data.get('answer_id', None)
        if answer_id:
            answer =Answer.objects.filter(id=answer_id).first()
            if not answer:
                raise serializers.ValidationError('错误的请求')
            instance = AnswerLike.objects.create(
                user=user,
                answer=answer
            )
            if action == 'like':
                answer.like_count += 1
            else:
                answer.like_count -= 1
            answer.save()
            return instance


class TagListSerializer(serializers.ModelSerializer):
    """所有标签序列化器"""
    is_like = serializers.IntegerField(label="用户是否关注该标签")

    class Meta:
        model = Tag
        fields = ("id", "name", "concerns", "is_like")


class TagDetailSerializer(serializers.ModelSerializer):
    """标签详情序列化器"""
    is_like = serializers.IntegerField(label="用户是否关注该标签")

    class Meta:
        model = Tag
        fields = ('id', 'name', 'describe', 'image_url', 'is_like')


class TagLikeSerializer(serializers.Serializer):
    """标签关注序列化器"""
    tag_id = serializers.CharField(required=False)
    user_id = serializers.CharField(read_only=True)

    def validate(self, attrs):
        tag_id = attrs.get("tag_id", None)
        if not tag_id:
            raise serializers.ValidationError("错误的请求")
        tag = Tag.objects.filter(id=tag_id).first()
        if not tag:
            raise serializers.ValidationError("错误的请求")
        request = self.context["request"]
        user = request.user
        tag_concern = TagConcern.objects.filter(user=user, tag=tag).first()
        if tag_concern:
            raise serializers.ValidationError("错误的请求")
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        tag_id = validated_data.get("tag_id")
        tag = Tag.objects.filter(id=tag_id).first()
        instance = TagConcern.objects.create(
            tag=tag,
            user=user,
        )
        tag.concerns += 1
        tag.save()

        # 将 关注标签 记录到 我的动态表 中
        if user and user.is_authenticated():
            Dynamic.objects.create(user=request.user, type=0, action="关注了标签", type_id=tag_id)

        return instance

class CustomTagsSerializer(serializers.ModelSerializer):
    """常用标签序列化器"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'describe']


class TagCategorySerializer(serializers.ModelSerializer):
    """标签分类序列化器"""
    category_tags = CustomTagsSerializer(many=True)

    class Meta:
        model = TagCategory
        fields = "__all__"


class SubmitQuestionSerializer(serializers.Serializer):
    """提交问题序列化器"""

    id = serializers.IntegerField(read_only=True)
    tags = serializers.ListField(required=True, write_only=True)
    content = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    category = serializers.IntegerField(required=True)
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

    def create(self, validated_data):
        tags = validated_data.get('tags')
        content = validated_data.get('content')
        title = validated_data.get("title")
        user = self.context['request'].user
        instance = Question.objects.create(
            content=content,
            title=title,
            category_id=1,
            author=user,
        )
        for tag_name in tags:
            tag = Tag.objects.filter(name=tag_name).first()
            if not tag:
                raise serializers.ValidationError("错误的请求")
            questiontag = QuestionTag.objects.create(
                tag=tag,
                question=instance
            )
            questiontag.save()
        instance.save()
        del validated_data['tags']
        return instance


class EditAnswerSerializer(serializers.Serializer):
    """编辑解答序列化器"""
    id = serializers.IntegerField(required=True)
    question_id = serializers.IntegerField(required=True, write_only=True)
    content = serializers.CharField(max_length=120, required=True)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        question_id = validated_data.get('question_id')
        question = Question.objects.filter(id=question_id).first()
        if not question:
            raise serializers.ValidationError("错误的请求")
        if user.id != instance.user_id:
            raise serializers.ValidationError("错误的请求")
        if question.id != instance.question_id:
            raise serializers.ValidationError("错误的请求")
        content = validated_data.get('content')
        instance.content = content
        instance.save()
        return instance


class EditQuestionSerializer(serializers.Serializer):
    """编辑问题序列化器"""
    tags = serializers.ListField(required=True, write_only=True)
    content = serializers.CharField(required=True)
    title = serializers.CharField(required=True)

    def validate(self, attrs):
        tags = attrs["tags"]
        for tag_name in tags:
            tag = Tag.objects.filter(name=tag_name).first()
            if not tag:
                raise serializers.ValidationError("错误的请求")
        return attrs

    def update(self, instance, validated_data):
        user = self.context['request'].user
        question_id = validated_data.get('question_id')
        question = Question.objects.filter(id=question_id).first()
        if not question:
            raise serializers.ValidationError("错误的请求")
        if user.id != instance.author_id:
            raise serializers.ValidationError("错误的请求")
        content = validated_data.get('content')
        instance.content = content
        instance.save()
        return instance