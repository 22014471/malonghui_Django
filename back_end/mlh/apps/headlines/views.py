import logging
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Prefetch
from rest_framework.viewsets import GenericViewSet

from activity.models import Activity
from headlines.models import HeadlinesCategory, HeadlinesNews, NewsComment, UserAttention, NewsCollection, NewsTag
from headlines.serializers import HeadlinesCategorySerializer, HeadlinesNewsSerializer, HeadlinesCommentsSerializer, \
     HeadlinesQuestionSerializer, HeadlinesActivitiesSerializer, \
    HeadlinesHotsSerializer, HeadlinesTalksSerializer, HeadlinesDetailSerializer, HeadlinesUserAttention, \
    HeadlinesCommentAddSerializer, HeadlinesUserCollectionSerializer, HeadlinesNewsAddSerializer
from mlh.utils.pagination import StandardResultsSetPagination
from questions.models import Question, Tag
from talks.models import Talks
from users.models import User, Dynamic


class HeadlinesCategoryView(ListAPIView):
    """
    头条分类
    """
    queryset = HeadlinesCategory.objects.filter(is_delete=0).order_by('-weight')
    serializer_class = HeadlinesCategorySerializer


class HeadlinesNewsListView(ListAPIView):
    """
    头条新闻列表
    """
    serializer_class = HeadlinesNewsSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category_id = 1
        try:
            category_id = self.kwargs['category_id']
        except Exception as e:
            logging.error(e)
        if category_id == '1':
            return HeadlinesNews.objects.filter(is_delete=0).order_by('-create_time').select_related('author')

        return HeadlinesNews.objects.filter(is_delete=0, category=category_id).order_by('-create_time').select_related('author')


class HeadlinesNewsDetailView(RetrieveAPIView):
    """
    头条新闻详情
    """
    serializer_class = HeadlinesDetailSerializer
    queryset = HeadlinesNews.objects.all().select_related('author')

    def perform_authentication(self, request):
        pass

    def get(self, request, *args, **kwargs):
        # 将 访问了吐槽 记录到 我的动态表 中
        if request.user and request.user.is_authenticated():
            news_id = self.kwargs['pk']
            Dynamic.objects.create(user=request.user, type=3, action="访问了新闻头条", type_id=news_id)
        return super().get(request, *args, **kwargs)

class HeadlinesCommentsView(ListAPIView):
    """
    头条新闻详情评论显示
    """
    serializer_class = HeadlinesCommentsSerializer

    def get_queryset(self):
        news_id = ''
        try:
            news_id = self.kwargs['news_id']
        except Exception as e:
            logging.error(e)
        queryset = NewsComment.objects.filter(news=news_id, parent=None).select_related('user')\
            .prefetch_related(Prefetch('child', NewsComment.objects.all().select_related('user')))

        return queryset


class HeadlinesCommentAddView(CreateAPIView):
    """
    新闻评论添加
    """
    serializer_class = HeadlinesCommentAddSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        创建用户评论
        """
        user = request.user
        request.data['user'] = user.id


        return super().create(request, *args, **kwargs)


class HeadlinesQuestionListView(ListAPIView):
    """
    头条问答排行
    """
    serializer_class = HeadlinesQuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all().order_by('-update_time').select_related('author')
        if len(queryset) >= 5:
            queryset = queryset[0:5]
        return queryset


class HeadlinesActivitiesListView(ListAPIView):
    """
    热门活动排行
    """
    serializer_class = HeadlinesActivitiesSerializer

    def get_queryset(self):
        queryset = Activity.objects.all().order_by('start_time')
        if len(queryset) >= 4:
            queryset = queryset[0:4]
        return queryset


class HeadlinesHotsListView(ListAPIView):
    """
    热门头条排行
    """
    serializer_class = HeadlinesHotsSerializer

    def get_queryset(self):
        queryset = HeadlinesNews.objects.all().order_by('-create_time')
        if len(queryset) >= 4:
            queryset = queryset[0:4]
        return queryset


class HeadlinesTalksListView(ListAPIView):
    """
    热门吐槽排行
    """
    serializer_class = HeadlinesTalksSerializer

    def get_queryset(self):
        queryset = Talks.objects.filter(status=0).order_by('-create_time')
        if len(queryset) >= 4:
            queryset = queryset[0:4]
        return queryset


class HeadlinesUserAttentionView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    首页及详情页添加作者关注
    """
    serializer_class = HeadlinesUserAttention
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        创建用户关注作者
        """
        user = request.user
        request.data['user'] = user.id
        author_id = request.data.get('author')
        user_attention = user.fun.all() #用户的关注作者
        for author in user_attention:
            if author_id == author.author.id:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        author_id = request.data.get('author')
        user_id = request.user.id
        instance = UserAttention.objects.filter(user=user_id, author=author_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HeadlinesUserCollectionView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    详情页添加新闻收藏
    """
    serializer_class = HeadlinesUserCollectionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        创建用户收藏
        """
        user = request.user
        request.data['user'] = user.id

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        news_id = request.data.get('news')
        user_id = request.user.id
        instance = NewsCollection.objects.filter(user=user_id, news_id=news_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HeadlinesNewsAddView(GenericAPIView):
    """
    头条新闻添加
    """
    serializer_class = HeadlinesNewsAddSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request, *args, **kwargs):

        user = request.user
        request.data['author'] = user
        category = HeadlinesCategory.objects.filter(name=request.data['category']).first()

        request.data['category'] = category

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        news = HeadlinesNews(**serializer.data)
        news.save()
        label = request.data.get('label')

        tags_list = label.split(',')
        for i in tags_list:
            tags = Tag.objects.filter(name=i).first()
            NewsTag.objects.create(news=news, tag=tags)
        return Response(status=status.HTTP_201_CREATED)


