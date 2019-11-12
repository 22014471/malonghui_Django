from django.conf.urls import url

from activity import views

urlpatterns = [
    url(r'^activities/$', views.ActivityView.as_view()),
    url(r'^activities/(?P<pk>\d+)/$', views.ActivityDetailView.as_view()),
]