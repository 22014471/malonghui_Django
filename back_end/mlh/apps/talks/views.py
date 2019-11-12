# Create your views here.
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mlh.utils.pagination import TalksPagination
from users.models import Dynamic
from .models import Talks, TalkComment, TalkLike, TalkCollection, CommentLike
from .serializers import TalksListSerializer, TalksDetailSerializer, TalkCommentSerializer, TalkLikeSerializer, \
    TalkCollectSerializer, CreationTsukkomiSerializer, CommentLikeSerializer, TalkCommentLikeSerializer


class TalksListView(ListAPIView):
    """吐槽首页视图"""
    serializer_class = TalksListSerializer
    pagination_class = TalksPagination

    def perform_authentication(self, request):
        pass

    def get_queryset(self):
        queryset = Talks.objects.all().order_by("-create_time")
        try:
            user = self.request.user  # 此处校验用户

        except Exception:
            user = None

        for i in queryset:
            i.is_like = 0
            i.is_collect = 0
            if user is not None and user.is_authenticated():  # 登陆状态／未登陆状态
                user_likes = user.like_talks.all()  # 多对多查询
                user_collects = user.collect_talks.all()  # 多对多查询
                if i in user_likes:
                    i.is_like = 1
                if i in user_collects:
                    i.is_collect = 1

        return queryset


class TalksDetailView(RetrieveAPIView):
    """吐槽详情页"""

    serializer_class = TalksDetailSerializer
    queryset = Talks.objects.all().order_by("-create_time")

    def perform_authentication(self, request):
        pass

    def get_object(self):
        obj = super(TalksDetailView, self).get_object()
        try:
            user = self.request.user
        except Exception:
            user = None
        obj.is_like = 0
        if user and user.is_authenticated():
            user_likes = user.like_talks.all()
            for i in user_likes:
                if obj == i:
                    obj.is_like = 1
                    # print(obj.id)
                    # 将 访问了吐槽 记录到 我的动态表 中
                    # Dynamic.objects.create(user=user, type=2, action="访问了吐槽", type_id=obj.id)

        return obj


class TalksCommentListView(ListAPIView, CreateAPIView):
    """评论查询/新增"""
    serializer_class = TalkCommentSerializer

    def perform_authentication(self, request):
        pass

    def get_queryset(self):
        talk_id = self.kwargs['talk_id']
        queryset = TalkComment.objects.filter(talk_id_id=talk_id).order_by("-create_time")
        try:
            user = self.request.user
        except Exception:
            user = None
        if user and user.is_authenticated():
            user_comment_like = CommentLike.objects.filter(user=user)
            for i in queryset:
                i.is_like = 0
                if i in user_comment_like:
                    i.is_like = 1


        return queryset


class TalkCommentLikeView(CreateAPIView, DestroyAPIView):
    """评论的点赞/取消点赞"""
    serializer_class = TalkCommentLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        点赞
        """
        try:
            user = request.user
            comment_id = request.data['comment']
            talkcomment = TalkComment.objects.filter(id=comment_id)[0]
            commentlike = CommentLike.objects.filter(comment=comment_id, user=user).first()
            if not commentlike:
                commentlike = CommentLike.objects.create(comment=talkcomment, user=user)
                talkcomment.like_count += 1
                talkcomment.save()
        except Exception as e:
            raise e
        else:
            return Response({'message': "ok"})


    def delete(self, request, *args, **kwargs):
        """
        取消点赞
        """
        user = self.request.user
        comment_id = self.request.data['comment']
        commentlike = CommentLike.objects.filter(comment=comment_id, user=user).first()
        # 如过记录存在
        if commentlike:
            commentlike.delete()
            # 对应相关吐槽点赞数-1
            talkcomment = TalkComment.objects.get(id=commentlike)
            talkcomment.like_count -= 1
            talkcomment.save()
            return Response({'message': "ok"}, status=200)
        return Response(status=400)

class TalkLikeView(CreateAPIView, DestroyAPIView):
    """吐槽的点赞/取消点赞"""
    serializer_class = TalkLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        点赞
        """
        try:
            response = super().post(request, *args, **kwargs)
            talk_id = request.data['talk_id']
            talk = Talks.objects.get(id=talk_id)
            talk.like_count += 1
            talk.save()
        except Exception as e:
            raise e
        else:
            return response

    def delete(self, request, *args, **kwargs):
        """
        取消点赞
        """
        user = self.request.user
        talk_id = request.query_params['talk_id']
        talk_like = TalkLike.objects.filter(talk_id=talk_id, user=user).first()
        # 如过记录存在
        if talk_like:
            talk_like.delete()
            # 对应相关吐槽点赞数-1
            talk = Talks.objects.get(id=talk_id)
            talk.like_count -= 1
            talk.save()
            return Response(status=200)
        return Response(status=400)


class TalkCollectView(CreateAPIView, DestroyAPIView):
    """吐槽的收藏/取消收藏"""
    serializer_class = TalkCollectSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        取消收藏
        """
        user = self.request.user
        talk_id = request.query_params['talk_id']
        talk_collect = TalkCollection.objects.filter(talk_id=talk_id, user=user).first()
        # 如果记录存在
        if talk_collect:
            talk_collect.delete()
            return Response(status=200)
        return Response(status=400)


























class CommentLikeView(CreateAPIView):
    """评论点赞"""
    # permission_classes = [IsAuthenticated]  # 必须经过验证
    serializer_class = CommentLikeSerializer

    def create (self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie('like_comment_' + str(serializer.data["comment"]),
                            'like_is_true_' + str(serializer.data["comment"]),)
        return response





























class CreationTsukkomiView(CreateAPIView):
    """发布吐槽"""
    permission_classes = [IsAuthenticated]  # 必须经过验证
    serializer_class = CreationTsukkomiSerializer



# class CreationTsukkomiView(APIView):
#
#     def post(self,request):
#         serializer = CreationTsukkomiSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data.get('user')
#         content = serializer.validated_data.get('content')
#         Talk =Talks.objects.create(
#             content=content,
#             user_id = user
#         )
#         return Response(status=status.HTTP_201_CREATED)