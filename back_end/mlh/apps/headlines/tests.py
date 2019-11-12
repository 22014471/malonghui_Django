from django.test import TestCase

# Create your tests here.
from headlines.models import NewsComment
from headlines.serializers import HeadlinesCommentsSerializer, HeadlinesCommentChildrenSerializer

queryset = NewsComment.objects.filter(news=1)
for query in queryset:
    child_list = []
    child = query.parent
    if child:
        child_list.append(child)
    data = HeadlinesCommentChildrenSerializer(child_list, many=True)
    query.children = data.data

data = HeadlinesCommentsSerializer(queryset,many=True)
print(data.data)


