from django.conf.urls import url

from talks.views import TalksListView, TalksDetailView, TalksCommentListView, TalkLikeView, TalkCollectView, \
    TalkCommentLikeView, CreationTsukkomiView

urlpatterns = [
    url(r"^talks/$", TalksListView.as_view()),  # 吐槽列表页
    url(r"^talks/(?P<pk>\d+)$", TalksDetailView.as_view()),  # 吐槽详情页
    url(r"^talks/(?P<talk_id>\d+)/comments$", TalksCommentListView.as_view()),  # 吐槽详情页的评论
    url(r"^talk/likes$", TalkLikeView.as_view()),  # 首页吐槽点赞
    url(r"^talk/likes/(?P<talk_id>\d+)$", TalkLikeView.as_view()),  # 首页取消点赞
    url(r"^talk/comment/likes$", TalkCommentLikeView.as_view()),  # 评论点赞
    url(r"^talk/collect$", TalkCollectView.as_view()),  # 首页吐槽收藏
    url(r"^talk/collect/(?P<talk_id>\d+)$", TalkCollectView.as_view()),  # 首页取消收藏
    url(r'^creation/talk/$', CreationTsukkomiView.as_view()),  # 发布吐槽
]

