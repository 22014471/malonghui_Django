import json

from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from headlines.models import HeadlinesNews, NewsCollection, UserAttention
from mlh.utils.pagination import StandardResultsSetPagination
from questions.models import Answer, Question, Tag
from questions.serializers import TagListSerializer
from talks.models import Talks, TalkCollection
from users.models import User, Dynamic
from users.serializers import UserCreateCheckSerializer, AnswerSerializer, QuestionSerializer, AccountSerializer, \
    DynamicSerializer, DynamicTagSerialzer, DynamicAnswerSerialzer, DynamicTalksSerialzer, \
    DynamicNewsSerialzer, CollectNewsSerializer, UserBaseSerializer, CollectTalksSerializer, \
    CollectTalksAuthorSerializer


class UsernameView(APIView):
    """校验用户名"""
    # GET http://127.0.0.1:8000/users/(?P<username>\w{5,20})/count/
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        data = {
            "username": username,
            "count": count
        }
        return Response(data)


class MobileView(APIView):
    """校验手机号"""
    # GET http://127.0.0.1:8000/mobiles/(?P<mobile>1[3-9]\d{9})/count/
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            "mobile": mobile,
            "count": count
        }
        return Response(data)


class UserCreateView(CreateAPIView):
    """用户注册"""
    # POST http://127.0.0.1:8000/users/
    serializer_class = UserCreateCheckSerializer


class UserDetailView(RetrieveAPIView):
    """个人中心顶部页首的信息"""
    serializer_class = UserBaseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# http://127.0.0.1:8080/answers?page=2&page_size=4
class AnswerView(ListAPIView):
    """
    我的回答列表获取
    """
    # 序列化器用于序列化输出
    serializer_class = AnswerSerializer

    # 分页：构建一个类，其继承于PageNumberPagination，用于标准化分页
    pagination_class = StandardResultsSetPagination

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Answer.objects.filter(user=self.request.user).order_by("-create_time")
        return queryset


# http://127.0.0.1:8080/questions?page_size=2
class QuestionView(ListAPIView):
    """
    我的提问
    """
    serializer_class = QuestionSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        queryset = Question.objects.filter(author=self.request.user).order_by("-create_time")
        return queryset


# http://127.0.0.1:8000/accounts/
class AccountView(RetrieveUpdateAPIView):
    """个人账户设置"""

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# http://127.0.0.1:8000/dynamics/
class DynamicView(APIView):
    """个人动态"""
    permission_classes = [IsAuthenticated]

    def get(self,request):
        # 获取所有数据
        dynamics = Dynamic.objects.filter(user=request.user).order_by("-update_time")
        # 创建分页对象
        pg = StandardResultsSetPagination()
        # 在数据库中获取分页数据
        pg_dynamics = pg.paginate_queryset(queryset=dynamics, request=request, view=self)
        # 对分页数据进行序列化
        serializer = DynamicSerializer(instance=pg_dynamics,many=True)

        for item in serializer.data:
            type = item.get("type")
            type_id = item.pop("type_id")
            content = None
            # type   (0, 'tag'),---标签  (1, 'answer'),---回答    (2, 'talks'),---吐槽   (3, 'headline_news')---新闻
            if type == 0:
                tag = Tag.objects.get(id=type_id)
                tag_serializer = DynamicTagSerialzer(tag)
                content = tag_serializer.data
            elif type == 1:
                answer = Answer.objects.get(id=type_id)
                answer_serializer = DynamicAnswerSerialzer(answer)
                # type(answer_serializer.data)
                # >> <class 'rest_framework.utils.serializer_helpers.ReturnDict'>
                # JSONRenderer().render(answer_serializer.data)是json的bytes形式，需要decode成str
                # 使用json.loads转化成python中字典，然后才能添加额外数据不然是不可以添加的
                answer_dict = json.loads(JSONRenderer().render(answer_serializer.data).decode())
                print(answer_dict)

                answer_dict['answer_count'] = answer.question.answer_count
                content = answer_dict
            elif type == 2:
                talks = Talks.objects.get(id=type_id)
                talks_serializer = DynamicTalksSerialzer(talks)
                content = talks_serializer.data
            elif type == 3:
                headline_news = HeadlinesNews.objects.get(id=type_id)
                headline_news_serializer = DynamicNewsSerialzer(headline_news)
                content = headline_news_serializer.data
            item["content"] = content
        return pg.get_paginated_response(serializer.data) # 返回上一页或者下一页


# http://127.0.0.1:8000/collections/news?page=2&page_size=2
class CollectionNewsView(APIView):
    """新闻头条收藏"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        news_obj_list = []
        # 获取所有数据
        news_collections = NewsCollection.objects.filter(user=user).order_by("-create_time")

        for item in news_collections:
            news_obj = HeadlinesNews.objects.get(id=item.news_id)
            news_obj_list.append(news_obj)

        # 创建分页对象
        pg = StandardResultsSetPagination()
        # 在数据库中获取分页数据
        pg_news = pg.paginate_queryset(queryset=news_obj_list, request=request, view=self)
        # 对分页数据进行序列化
        serializer = CollectNewsSerializer(instance=pg_news, many=True)

        #给每个收藏的新闻加上收藏时间（collection_time），判断是否已经关注过作者（attention）,当前用户信息
        for s_news in serializer.data:
            news_collections_obj = NewsCollection.objects.get(news_id=s_news["id"])
            s_news["collection_time"] = news_collections_obj.create_time
            try:
                news_obj = HeadlinesNews.objects.get(id=s_news["id"])
                user_attention = UserAttention.objects.filter(author_id=news_obj.author_id, user_id=user.id)
                if user_attention:
                    s_news["attention"] = "已关注"
            except UserAttention.DoesNotExist:
                s_news["attention"] = "关注"
        return pg.get_paginated_response(serializer.data)  # 返回上一页或者下一页


# http://127.0.0.1:8000/collections/talks?page=2&page_size=2
class CollectionTalksView(APIView):
    """吐槽收藏"""
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        talks_obj_list = []
        talks_collections = TalkCollection.objects.filter(user=user)
        for item in talks_collections:
            talk_obj = Talks.objects.get(id=item.talk_id)
            talks_obj_list.append(talk_obj)

        pg = StandardResultsSetPagination()
        pg_news = pg.paginate_queryset(queryset=talks_obj_list, request=request, view=self)
        serializer = CollectTalksSerializer(instance=pg_news, many=True)

        # 给每个收藏的吐槽加上吐槽的作者信息（author）；因为是当前用户收藏的，所以所有的吐槽的collect=1；当前用户信息
        for s_talk in serializer.data:
            talk_obj = Talks.objects.get(id=s_talk["id"])
            author = User.objects.get(id=talk_obj.user_id)
            author_serializer = CollectTalksAuthorSerializer(author)
            s_talk["collect"] = 1
            s_talk["author"] = author_serializer.data
        return pg.get_paginated_response(serializer.data)


class MyFocusView(ListAPIView):
    """用户关注的所有标签"""
    serializer_class = TagListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.request.user.concern_tags.all()
        for tag in queryset:
            tag.is_like = 1
        return queryset


class MyFileView(RetrieveUpdateAPIView):
    """档案列表，修改档案视图"""
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
