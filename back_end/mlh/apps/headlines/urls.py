from django.conf.urls import url

from headlines.views import HeadlinesCategoryView, HeadlinesNewsListView, HeadlinesNewsDetailView,  \
    HeadlinesQuestionListView, HeadlinesActivitiesListView, HeadlinesHotsListView, HeadlinesTalksListView, \
    HeadlinesCommentsView, HeadlinesUserAttentionView, HeadlinesCommentAddView, HeadlinesUserCollectionView, \
    HeadlinesNewsAddView

urlpatterns = [
    url(r'^headlines_news/(?P<category_id>\d+)$', HeadlinesNewsListView.as_view()),
    url(r'^headlines_category$', HeadlinesCategoryView.as_view()),
    url(r'^headlines_detail/(?P<pk>\d+)$', HeadlinesNewsDetailView.as_view()),
    url(r'^headlines_comments/(?P<news_id>\d+)$', HeadlinesCommentsView.as_view()),
    url(r'^headlines_questions$', HeadlinesQuestionListView.as_view()),
    url(r'^headlines_activities$', HeadlinesActivitiesListView.as_view()),
    url(r'^headlines_hots$', HeadlinesHotsListView.as_view()),
    url(r'^headlines_talks$', HeadlinesTalksListView.as_view()),
    url(r'^headlines_attention$', HeadlinesUserAttentionView.as_view({'post': 'create', 'delete': 'destroy'})),
    url(r'^headlines_comment$', HeadlinesCommentAddView.as_view()),
    url(r'^headlines_collection$', HeadlinesUserCollectionView.as_view({'post': 'create', 'delete': 'destroy'})),
    url(r'^headlines_add$', HeadlinesNewsAddView.as_view()),

]