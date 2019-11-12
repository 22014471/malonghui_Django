from django.conf.urls import url

# Django REST framework JWT提供了登录签发JWT的视图，可直接使用,但是默认的返回值仅有token，还需创建jwt_response_payload_handler,在返回值中增加username和user_id,并在配置中设置jwt返回值
from rest_framework_jwt.views import obtain_jwt_token

from users import views

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileView.as_view()),
    url(r'^users/$', views.UserCreateView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^myanswers/$', views.AnswerView.as_view()),
    url(r'^user/detail/$', views.UserDetailView.as_view()),
    url(r'^myquestions/$', views.QuestionView.as_view()),
    url(r'^account/$', views.AccountView.as_view()),
    url(r'^dynamics/$', views.DynamicView.as_view()),
    url(r'^collections/news/$', views.CollectionNewsView.as_view()),
    url(r'^collections/talks/$', views.CollectionTalksView.as_view()),
    url(r'^myfocus/$', views.MyFocusView.as_view()),
    url(r'^myfile/$', views.MyFileView.as_view()),
]