from django.conf.urls import url


from .views import *

urlpatterns = [
    url(r'^question/categories/$', QuestionCategoryView.as_view()),
    url(r'^questions/$', QuestionListView.as_view()),
    url(r'^question/$', QuestionDetailView.as_view()),
    url(r'^hottags/$', HotTagsView.as_view()),
    url(r'^question/answers/$',QAnswerView.as_view()),
    url(r'^question/like/$',QuestionLikeView.as_view()),
    url(r'^answer/like/$',AnswerLikeView.as_view()),
    url(r'^question/answer/$',SubmitAnswerView.as_view()),
    url(r'^tags/$', TagListView.as_view()),
    url(r'^tag/(?P<tag_id>\d+)/$', TagDetailView.as_view()),
    url(r'^tag/like/$', TagLikeView.as_view()),
    url(r'^tag_category/$', CustomTagsView.as_view()),
    url(r'^tag/questions/$', TagQuestionListView.as_view()),
]

