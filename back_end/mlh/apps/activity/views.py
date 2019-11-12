from django.shortcuts import render

# Create your views here.

from rest_framework.generics import ListAPIView, RetrieveAPIView

from activity.models import Activity
from activity.serializers import ActivitySerializer, ActivityDetailSerializer
from mlh.utils.pagination import StandardResultsSetPagination


class ActivityView(ListAPIView):
    """
    活动页
    """
    queryset = Activity.objects.all().order_by('-start_time')
    serializer_class = ActivitySerializer
    pagination_class = StandardResultsSetPagination


class ActivityDetailView(RetrieveAPIView):
    """
    活动详细页
    """
    queryset = Activity.objects.all()
    serializer_class = ActivityDetailSerializer
