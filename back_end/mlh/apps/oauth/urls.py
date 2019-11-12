from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^oauth/qq/authorization/$', QQOAuthURLView.as_view()),
    url(r'^oauth/qq/user/$', QQOAuthUser.as_view()),
    url(r'^oauth/wb/authorization/$', WBOAuthURLView.as_view()),
    url(r'^oauth/wb/user/$', WBOAuthUser.as_view()),
    url(r'^oauth/share_to_weibo/$', QuestionOAuthShareView.as_view()),
]