from django.http import Http404
from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from questions.models import Question, QuestionTag, Tag, TagCategory
from questions.serializers import *
from questions.utils import StandardResultsSetPagination

class IsLikeMixin(object):
    """判断点赞逻辑拓展类"""
    def is_like(self, obj, user_list):
        if obj in user_list:
            obj.is_like = 1
        return obj




class QuestionCategoryView(ListAPIView):
    """问题分类视图类"""
    serializer_class = QuestionCategorySerializer
    queryset = QuestionCategory.objects.filter(is_deleted=False).order_by('sequence')


class QuestionListView(ListAPIView):
    """问题列表视图类"""
    serializer_class = QuestionListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            queryset = Question.objects.filter(category_id=category_id, is_deleted=False).order_by('-create_time')
        else:
            queryset = Question.objects.all().order_by('-create_time')
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            if ordering == "hot":
                queryset = Question.objects.all().order_by('-visits')
            elif ordering == "wait":
                queryset = Question.objects.filter(answer_count=0)
        return queryset


class HotTagsView(ListAPIView):
    """热门标签视图类"""
    serializer_class = QuestionTagsSerializer

    def get_queryset(self):
        queryset = Tag.objects.filter(is_deleted=False).order_by('-concerns')
        return queryset


class QuestionDetailView(IsLikeMixin, APIView):
    """问答详情视图类"""
    def perform_authentication(self, request):
        try:
            request.user
        except Exception:
            request.user = None

    def get(self, request):
        question_id = request.query_params.get('question_id', None)
        if not question_id:
            return Response({'message':"错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        question = Question.objects.filter(is_deleted=False, id=question_id).first()
        user = request.user
        question.is_like = 0
        question.is_author = 0
        if user and user.is_authenticated:
            question = self.is_like(question, user.like_questions.all())
            if question.author == user:
                question.is_author = 1
        serializer = QuestionDetailSerializer(instance=question)
        question.visits += 1
        question.save()
        return Response(serializer.data)

    def post(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"message":"用户未登录"}, status=status.HTTP_401_UNAUTHORIZED)
        tags = request.data.get('tags',None)
        if not tags:
            return Response({'message': "错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        tag_name_list = tags.split('; ')
        request.data['tags'] = tag_name_list
        serializer = SubmitQuestionSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)

    def put(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"message":"用户未登录"}, status=status.HTTP_401_UNAUTHORIZED)
        question_id = request.data.get('question_id', None)
        if not question_id:
            return Response({'message': "错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        question = Question.objects.filter(id=question_id).first()
        if not question:
            return Response({'message': "错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        tags = request.data.get('tags', None)
        if not tags:
            return Response({'message': "错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        tag_name_list = tags.split('; ')
        request.data['tags'] = tag_name_list
        request.data.pop('question_id')
        serializer = EditQuestionSerializer(question, data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class QAnswerView(IsLikeMixin, ListAPIView):
    """该问题的解答列表视图类"""
    serializer_class = QAnswerSerializer

    def perform_authentication(self, request):
        try:
            request.user
        except Exception:
            request.user = None

    def get_queryset(self):
        request = self.request
        question_id = request.query_params['question_id']
        queryset = Answer.objects.filter(is_deleted=False, question_id=question_id).order_by('-like_count')
        for answer in queryset:
            user = request.user
            answer.is_like = 0
            answer.is_author = 0
            if user and user.is_authenticated:
                answer = self.is_like(answer, user.like_answers.all())
                if answer.user == user:
                    answer.is_author = 1
        return queryset



class QuestionLikeView(CreateAPIView):
    """问题点赞"""
    serializer_class = QuestionLikeSerializer
    permission_classes = [IsAuthenticated]


class AnswerLikeView(CreateAPIView):
    """答案点赞"""
    serializer_class = AnswerLikeSerializer
    permission_classes = [IsAuthenticated]



class SubmitAnswerView(CreateAPIView):
    """提交解答视图类"""
    serializer_class = PublishAnswerSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        answer_id = request.data.get('id', None)
        if not answer_id:
            return Response({'message':"错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        answer = Answer.objects.filter(id=answer_id).first()
        if not answer:
            return Response({'message': "错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EditAnswerSerializer(answer, data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class TagListView(IsLikeMixin, ListAPIView):
    """所有标签"""
    serializer_class = TagListSerializer
    pagination_class = StandardResultsSetPagination

    def perform_authentication(self, request):
        try:
            request.user
        except Exception:
            request.user = None

    def get_queryset(self):
        queryset = Tag.objects.all()
        for tag in queryset:
            user = self.request.user
            tag.is_like = 0
            if user and user.is_authenticated:
                tag = self.is_like(tag, user.concern_tags.all())
        return queryset


class TagDetailView(RetrieveAPIView):
    """标签详情"""
    serializer_class = TagDetailSerializer

    def perform_authentication(self, request):
        try:
            request.user
        except Exception:
            request.user = None

    def get_object(self):
        tag_id = self.kwargs['tag_id']
        tag = Tag.objects.filter(id=tag_id).first()
        if not tag:
            raise Http404
        tag.is_like = 0
        user = self.request.user
        if user and user.is_authenticated:
            if tag in user.concern_tags.all():
                tag.is_like = 1
        return tag


class TagLikeView(CreateAPIView):
    """标签点赞"""
    serializer_class = TagLikeSerializer
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        tag_id = request.query_params.get('tag_id', None)
        if not tag_id:
            return Response({"message":"错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        tag = Tag.objects.filter(id=tag_id).first()
        if not tag:
            return Response({"message": "错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        obj = TagConcern.objects.filter(user=user, tag_id=tag_id).first()
        if not obj:
            return Response({"message": "错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        tag.concerns -= 1

        # 将 取关标签 记录到 我的动态表 中
        if request.user and request.user.is_authenticated():
            Dynamic.objects.create(user=request.user, type=0, action="取关了标签", type_id=tag_id)

        return Response({'message':"取消关注成功"})

class CustomTagsView(APIView):
    """常用标签列表"""

    def get(self, request):
        tag_categories = TagCategory.objects.all()
        for tag_category in tag_categories:
            tag_list = []
            for tag in tag_category.category_tags.all():
                tag_list.append(tag.id)
            tag_category.category_tags = Tag.objects.filter(id__in=tag_list).order_by('-concerns')
        serializer = TagCategorySerializer(tag_categories, many=True)
        return Response(serializer.data)


class TagQuestionListView(ListAPIView):
    """标签页新闻列表"""
    serializer_class = QuestionListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering','-create_time')
        queryset = Question.objects.filter().order_by(ordering)
        return queryset

